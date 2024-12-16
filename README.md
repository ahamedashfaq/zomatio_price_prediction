**Building a Zomato-like Restaurant Recommendation and Price Prediction System**

This App is a web-based application similar to Zomato, which allows users to select restaurants based on location and cuisine and provides average price predictions for two people dining based on various features. The project should include data structuring, model building, and interactive visualizations, and the web app should be hosted on AWS EC2.

Zomato is an Indian multinational company that operates in the online food delivery, restaurant discovery, and food-tech industry. Founded in 2008 by Deepinder Goyal and Pankaj Chaddah, Zomato originally started as a restaurant review and discovery platform, allowing users to search for restaurants, read reviews, view menus, and make reservations. Over time, it expanded its services to include online food ordering and delivery, and has become one of the largest food delivery services in India.


1.AWS S3 and RDS usage for data storage and retrieval
2.Data structuring and preprocessing
3.Machine learning model development for price prediction
4.Web application development using Streamlit
5.Deployment of applications on AWS EC2
6.Interactive data visualization
7.Building recommendation systems

Approach:
Data Management:
  Upload the provided Zomato dataset (in JSON format) into an AWS S3 bucket.
  Pull the dataset from S3 and preprocess it for structuring.
  Store the structured data into AWS RDS in SQL format.
Model Development:
  Extract relevant features from the dataset (e.g., location, cuisine, average cost, ratings).
  Build a machine learning model to predict the average cost for two people based on these features.
  Train, evaluate, and save the model for deployment.
Web Application:
  Build an interactive Streamlit web application.
  The app should display restaurant options based on user input (location, cuisine) and predict the average price for two people.
  Add interactive visualizations for restaurant ratings, cuisines, and price range distribution.
Deployment:
  Host the Streamlit web application on an AWS EC2 instance for public access.

It is also deployed in streamlit cloud : 
**https://zomatopriceprediction-tcfk4waydigdwdef7vougd.streamlit.app/**


A snap of the app, can be found below :
![image](https://github.com/user-attachments/assets/3417cdbe-bf40-4346-9a25-7ff26b7f8772)


![image](https://github.com/user-attachments/assets/16c1e987-057f-4f8e-a1d0-d049499f1e12)


![image](https://github.com/user-attachments/assets/19c2a3f2-38d9-4dd7-a03e-f980f2c26bda)

