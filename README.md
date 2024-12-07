# Retail-Data-Analysis

## Project Overview
This project aims to analyze and optimize sales performance by identifying key trends, top-performing products, and growth opportunities using a dataset of sales transactions. We focus on extracting insights, calculating key performance indicators (KPIs), and building a data pipeline that integrates SQL, Python, and Streamlit.
## Objectives
- Identify Key Revenue and Profit Drivers: Analyze products and categories contributing the most to revenue and profit.
- Identify Key performing regions.
- Analyze Sales Trends: Assess year-over-year (YoY) and month-over-month (MoM) trends.
- Highlight Subcategories with High Profit Margins: Guide decision-making by focusing on high-margin subcategories.
- Optimize Sales Strategies: Leverage SQL, Python, and Streamlit to display insights and inform business decisions.
## Goals
- Identify Products & Categories contributing the most to revenue and profit.
- Identify profitable regions for optimizing marketing efforts.
- Analyze YoY & MoM Sales Trends to understand growth and seasonal variations.
- Highlight Subcategories with the highest profit margins for better decision-making.
- SQL Integration for querying large datasets effectively.
- Streamlit Integration for real-time data display and interactive analysis.
## Technologies & Tools
### Data Extraction & Cleaning
- Python Libraries: pandas, kaggle, mysql-connector.
- Data Source: Kaggle API for downloading retail orders data.
### Database Integration
- SQL Server: For storing and querying large datasets.
- Primary/Foreign Keys: Used for relational queries.
### Data Analysis & Visualization
- Streamlit: For displaying real-time data, charts, and insights.
- Matplotlib/Plotly: For data visualization.
## Project Workflow
### 1. Data Extraction
The raw dataset is downloaded from Kaggle using the Kaggle API.
!kaggle datasets download ankitbansal06/retail-orders -f orders.csv
### 2. Data Cleaning
Handling missing values by replacing them with None or 0.
Renaming columns for better clarity and compatibility with SQL.
Calculating new columns such as discount, sale price, and profit.
### 3. SQL Server Integration
After cleaning the data, it is loaded into an SQL Server database for querying.
### 4. SQL Queries for Insights
SQL queries will involve JOIN, GROUP BY, HAVING, ROW_NUMBER(), and CASE WHEN for advanced data operations.
### 5. Streamlit App for Real-Time Insights
Streamlit is used to create an interactive dashboard for displaying data and insights. The following steps are followed:
## Conclusion
This project showcases how to extract meaningful insights from sales data using Python, SQL, and Streamlit. By identifying key trends, top-performing products, and potential areas for growth, businesses can make informed decisions to optimize their sales strategies.
