# HOTD Tweets Analysis  

This project was made with the intention to learn and get a hand on a real-world data challenge and at the same time try to develop engineering best practices about the most used Data Eng stack.  

Such as Apache Airflow and AWS S3, and for that, we decided to create a pipeline to consume data from Twitter API and analyze them.  

The project's first step was to develop a python module to communicate via API and extract tweets data, gaining scalability and maintaining control of the parameters.         After that, we made the first DAG in Aiflow, which took the tweets with the hashtag #HouseOfTheDragon and saved them to S3 where we structured the lake, dividing between"Raw" and "Trusted", and the second DAG passed the data to a warehouse created in postgres.  

The next step in this flow was to model the data in a way to facilitate data consumption. For that we chose DBT, a powerful tool for data wrangling and AnalyticsEngineering, to make the transformations, to struct data, and to create data lineage.  

Our last step was this repo itselfm, create a nice data visualization. For that a dashboard using Streamlit was the choice, consuming data directly from wor Postgres “Data Warehouse”.

## Guide 

For running this reposity check the step by step guide [here](https://github.com/NicholasBaraldi/twitter-api-data-stack)  

After that just run the dashboard by typing
```
streamlit run hotd_analysis.py
```