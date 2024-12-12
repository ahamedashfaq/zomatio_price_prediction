import streamlit as st
from streamlit_card import card
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import os 
from pathlib import Path
import pickle
from streamlit_star_rating import st_star_rating
from streamlit_navigation_bar import st_navbar
from streamlit_option_menu import option_menu
import plotly.express as px



#st.set_page_config(initial_sidebar_state="collapsed",page_title="Zomato Restaurant Search", layout = "wide")
st.set_page_config(page_title="Zomato Restaurant Search", layout = "wide")
pages = ["Home", "Search Restaurants", "Explore", "About the developer"]

styles = {
    "nav": {
        "background-color": "rgb(139, 0, 0)",
    },
    "div": {
        "max-width": "40rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(255, 255, 255)",
        "margin": "0.9 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

page = st_navbar(pages,  options={"use_padding": False}, styles=styles)



#------------------------------------Import cuisine dictionary for value summation
cuisine_dict_path = Path(__file__).parent / 'cuisine_dict.pkl'
with open(cuisine_dict_path, 'rb') as f:
    cuisine_dict_file = pickle.load(f)

def searchkey(value):
    for key, val in cuisine_dict_file.items():
        if value == val:
            return key

def cuisine_name2num(i):
    #for i in df['cuisines']:
    n1 = 0
    kval = 0
    for ij in i:
        kval = searchkey(ij)
        if kval is not None:
            n1 += kval
    return n1

def row2list(c):
    ilist=[]
    for i in c:
        ilist.append(*i)
    return ilist

#-------------------------------------import model pkf files


#----------------------------------bg image--------------------
def add_bg_from_local():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4PZ9Xjyybt5Pdr_OQSi1nsi7W9n_ZnPJ1Lg&s");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )





#----------------------------------------------------------------------

connection = mysql.connector.connect(
  host="zomato-db.c78oq0qc6csc.ap-south-1.rds.amazonaws.com",
  user="admin",
  password="adminpassword"
)


mycursor = connection.cursor()
mycursor.execute( """USE zomatodb""")

#--------------------------------




#select box
def selectoptions():
    #City names
    mycursor.execute("""SELECT DISTINCT city FROM  zom_table""")
    citynames = row2list(mycursor.fetchall())

    colum1,colum2,colum3,colum4= st.columns([8,8,8,8],gap="small")
    with colum1:
        city_option = st.selectbox(
                    "Choose City🏛️",
                    (citynames),
                    index=None
                )


    #Locality names
    if city_option != None:
        mycursor.execute(f"SELECT DISTINCT locality FROM  zom_table  WHERE city = '{city_option}'")
        localitynames = row2list(mycursor.fetchall())
    else:
        mycursor.execute(f"SELECT DISTINCT locality FROM  zom_table")
        localitynames = row2list(mycursor.fetchall())

    with colum2:
        locality_option = st.selectbox(
                    "Choose Locality📍",
                    (localitynames),
                    index=None,
                    disabled= (page=="Explore")
                )

    #Cuisine names

    def cuisinename2list(cuisinenames):
        clist=[]
        for i in cuisinenames:
            cname = i.split(', ')
            clist.extend(cname)
        clist = list(dict.fromkeys(clist))
        return clist


    if locality_option != None:
        mycursor.execute(f"SELECT DISTINCT cuisines FROM  zom_table  WHERE locality = '{locality_option}'")
        cuisinenames = cuisinename2list(row2list(mycursor.fetchall()))

    elif city_option != None:
        mycursor.execute(f"SELECT DISTINCT cuisines FROM  zom_table  WHERE city = '{city_option}'")
        cuisinenames = cuisinename2list(row2list(mycursor.fetchall()))
    else:
        mycursor.execute(f"SELECT DISTINCT cuisines FROM  zom_table")
        cuisinenames = cuisinename2list(row2list(mycursor.fetchall()))


    with colum3:
        cuisine_option = st.selectbox(
                    "Choose Cuisine🍽️",
                    (cuisinenames),
                    index=None,
                    disabled= (page=="Explore")
                )

    #star rating

    with colum4:
        #stars = st_star_rating("Select Rating", maxValue=5, defaultValue=3, key="rating",customCSS = "div {background-color: rgb(220,53,69);}" )
        stars = st_star_rating('Select rating',maxValue=5, defaultValue=3, key="rating", customCSS = "div h3{font-size: 15px}" )
        #st.write(stars)

    return city_option, locality_option, cuisine_option, cuisinenames,stars


if page == "Home":
    add_bg_from_local()
    left_co, cent_co,last_co = st.columns(3)
    #with cent_co:
        #st.image("data:image/png;base64,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",width = 250)
    st.markdown("""
        <style>
        .big-font {
            font-size:25px !important;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">This App is developed to predict price of average cost of two based on Zomato Dataset. Zomato is an Indian multinational company that operates in the online food delivery, restaurant discovery, and food-tech industry. Founded in 2008 by Deepinder Goyal and Pankaj Chaddah, Zomato originally started as a restaurant review and discovery platform, allowing users to search for restaurants, read reviews, view menus, and make reservations. Over time, it expanded its services to include online food ordering and delivery, and has become one of the largest food delivery services in India.</p>', unsafe_allow_html=True)
    #st.write("This App is developed to predict price of average cost of two based on Zomato Dataset. Zomato is an Indian multinational company that operates in the online food delivery, restaurant discovery, and food-tech industry. Founded in 2008 by Deepinder Goyal and Pankaj Chaddah, Zomato originally started as a restaurant review and discovery platform, allowing users to search for restaurants, read reviews, view menus, and make reservations. Over time, it expanded its services to include online food ordering and delivery, and has become one of the largest food delivery services in India.")




if page == "Search Restaurants":
    city_option, locality_option, cuisine_option, cuisinenames,stars = selectoptions()
    #---------------------------streamlit card--------------------------------
    def showcard(df,i):
        #for i in range(0,df.index.size):
            card(
                    title=(df['name'][i]),
                    text=(f"{df['cuisines'][i]}", f"{df['rating'][i]} ⭐", f" Rs. {df['predicted_val'][i]} "),
                    image=df['thumb'][i],
                    url=df['url'][i],
                    key=(f"card_{str(i)}"), 
                    styles={
                        "card": {
                            "width": "300px",
                            "height": "300px",
                            "border-radius": "30px",
                            "box-shadow": "0 0 10px rgba(0,0,0,0.5)"
                        },
                        "text": {
                            "font-family": "serif",
                        },
                        "div": {
                                "text-align": "left",
                                "padding": "1px 1px"
                                }
                    

                        
                    }
                )


    def runquery(df):
        if df.index.size != 0:
                cols = st.columns(3)
                x={}
                for i in range(df.index.size):
                    y = (i%3)
                    x[i] = y
                for i,j in x.items():
                    with cols[j]:
                        showcard(df,i)
        else:
            html='''
            <p style="color:white">Sorry! No Restaurants found ! Search with a different locality or cuisine!</p>
            '''

            st.markdown(html, unsafe_allow_html=True)

    #------------------------Import models

    scaler_path = Path(__file__).parent / 'scaler.pkl'
    with open(scaler_path, 'rb') as f:
        loaded_scaler = pickle.load(f)

    lm_path = Path(__file__).parent / 'lm.pkl'
    with open(lm_path, 'rb') as f:
        loaded_lm = pickle.load(f)

    dt_path = Path(__file__).parent / 'dt.pkl'
    with open(dt_path, 'rb') as f:      
        loaded_dt = pickle.load(f)   

    rf_path = Path(__file__).parent / 'rf.pkl'
    with open(rf_path, 'rb') as f:      
        loaded_rf = pickle.load(f) 


    def cuisine_count(c):
        l = []
        l = c.split(', ')
        return len(l)

    #-------------------Search restaurants
    df = pd.DataFrame()
    if st.button("Search"):
        if city_option != None and cuisine_option != None and locality_option != None:
            #mycursor.execute(f"SELECT thumb, name, rating, currency FROM  zom_table  WHERE locality = '{locality_option}'' && cuisines like '%{cuisine_option}%'")
            query = (f"SELECT url, thumb, price_range, name, cuisines, city, locality, CAST(rating AS FLOAT) as rating, rating_votes, currency FROM  zom_table  WHERE locality = '{locality_option}' && cuisines like '%{cuisine_option}%' && rating >= {stars} " )
            df = pd.read_sql(query, con = connection)
            #runquery(df)
        elif city_option != None and cuisine_option != None:
            query = (f"SELECT url, thumb, price_range, name, cuisines, city, locality, CAST(rating AS FLOAT) as rating, rating_votes, currency FROM  zom_table  WHERE city = '{city_option}' && cuisines like '%{cuisine_option}%' && rating >= {stars} ")
            df = pd.read_sql(query,  con = connection)

            #runquery(df)
        elif city_option != None and locality_option != None:
            query = (f"SELECT url, thumb, price_range, name, cuisines, city, locality, CAST(rating AS FLOAT) as rating, rating_votes, currency FROM  zom_table  WHERE city = '{city_option}' && locality like '%{locality_option}%' && rating >= {stars} ")
            df = pd.read_sql(query,  con = connection)
        else:
            html='''<p style="color:red">Sorry! Please feed values</p>'''
            st.markdown(html, unsafe_allow_html=True)


        if df.index.size != 0:
            x=1
            df_for_pred = df.drop(['url' , 'thumb', 'name', 'city', 'locality', 'currency'],axis='columns')
            df_for_pred = df_for_pred.rename(columns={'cuisines': 'cuisine_count'})
            df_for_pred['cuisine_count'] = df_for_pred['cuisine_count'].apply(cuisine_count)
            input_data = df_for_pred
            input_data[input_data.columns] = loaded_scaler.transform(input_data[input_data.columns])
            predicted_val = loaded_lm.predict(input_data)
            val = predicted_val[0]
            df['predicted_val'] = predicted_val
            df['predicted_val'] = df['predicted_val'].apply(lambda x: round(x))
            st.spinner(text="In progress...")

            with st.status(f'Found {df.index.size} Result(s)'):
                st.write(f'Found {df.index.size} Result(s)')
            #st.success("Done!")

            if df.index.size >= 100: 
                runquery(df.head(100))
            else:
                runquery(df)
            x=0
            
            
        else:
            html='''<p style="color:red">Sorry, No Results! Choose different locality or cuisines</p>'''
            st.markdown(html, unsafe_allow_html=True)

    


#--------------------------------------------------Explore------------------------------------------------
if page == "Explore":
    
    city_option, locality_option, cuisine_option, cuisinenames,stars = selectoptions()
    query = (f"SELECT name, cuisines, city, locality, CAST(rating AS FLOAT) AS rating, CAST(rating_votes AS FLOAT) AS rating_votes, currency, average_cost_for_two FROM zom_table where currency like 'Rs.'")
    df2 = pd.read_sql(query, con = connection)
    price = st.slider('Select price', df2.average_cost_for_two.min(), df2.average_cost_for_two.max(), (df2.average_cost_for_two.min(), df2.average_cost_for_two.max()))
    df2['average_cost_for_two'] = df2['average_cost_for_two'].apply(lambda x : int(x))

    


    col1, col2 = st.columns(2, gap='medium')
    with col1:
            query =  f"average_cost_for_two >= {price[0]} & average_cost_for_two <= {price[1]}"
            df4 = df2.query(query).groupby('city', as_index=False)['average_cost_for_two'].agg('sum').sort_values(by = ['average_cost_for_two'],ascending=False)[:10]
            
            fig = px.bar(df4,
                         title='Top 10 cities with high price',
                         x='city',
                         y='average_cost_for_two',
                         orientation='v',
                         color='city',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)



            query =  f"city in '{city_option}'  & average_cost_for_two >= {price[0]} & average_cost_for_two <= {price[1]}"
            df3 = df2.query(query).groupby('locality', as_index=False)['average_cost_for_two'].agg('sum').sort_values(by = ['average_cost_for_two'],ascending=False)[:10]
            
            fig = px.bar(df3,
                         title='Top 10 locality with high price',
                         x='locality',
                         y='average_cost_for_two',
                         orientation='v',
                         color='locality',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)



    with col2:
            query =  f"city in '{city_option}'  & average_cost_for_two >= {price[0]} & average_cost_for_two <= {price[1]}"
            df4 = df2.query(query).groupby('name', as_index=False)['average_cost_for_two'].agg('sum').sort_values(by = ['average_cost_for_two'],ascending=False)[:10]
            
            fig = px.bar(df4,
                         title='Top 10 establishment with high price',
                         x='name',
                         y='average_cost_for_two',
                         orientation='v',
                         color='name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)


            # top 10 cuisines
            dfx = pd.DataFrame()
    
            for c in cuisinenames:
                query =  f"city in '{city_option}' & cuisines.str.contains('{c}') & average_cost_for_two >= {price[0]} & average_cost_for_two <= {price[1]}"
                df3 = df2.query(query).groupby('cuisines', as_index=False).agg('sum')

                df3['cname'] = c
                dfx = pd.concat([dfx,df3])

            
            unique_dfx = dfx.drop_duplicates()
            unique_cname_dfx = unique_dfx.groupby('cname', as_index=False)['average_cost_for_two'].agg('sum').sort_values(by = ['average_cost_for_two'],ascending=False)[:10]


            fig = px.bar(unique_cname_dfx,
                         title='Top 10 cuisines with high price',
                         x='cname',
                         y='average_cost_for_two',
                         orientation='v',
                         color='cname',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)
