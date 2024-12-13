# Retail-Data-Analysis

## Project Overview
This project aims to analyze and optimize sales performance by identifying key trends, top-performing products, and growth opportunities using a dataset of sales transactions. We focus on extracting insights, calculating key performance indicators (KPIs), and building a data pipeline that integrates SQL, Python, and Streamlit with AI integration.

![](https://github.com/Barath-dan/Retail-Data-Analysis/blob/main/asset/thmb2.png)

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
### Data Analysis
- Streamlit
### Vanna AI Integration
- Vanna AI: Integrates with the application to generate SQL queries from natural language user input. This allows users to ask business-related questions in plain language, and Vanna AI converts these queries into SQL syntax, which can then be executed against the database.
### Hosting
- AWS RDS: The project is hosted on AWS RDS (Relational Database Service) for scalable and secure database management. AWS RDS allows for easy deployment, backup, and scaling of the SQL Server database, ensuring high availability and reliability of the application.
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
Streamlit is used to create an interactive dashboard for displaying data and insights.
### 6. Vanna AI for Custom Query Generation
Vanna AI integrated in Streamlit App. It enables users to generate SQL queries by simply inputting business-related questions. The AI converts these questions into SQL queries, which are then executed on the database. This feature allows non-technical users to interact with the data in a more intuitive way.
## Conclusion
By integrating these technologies, businesses can optimize their sales strategies by identifying key trends, top-performing products, and growth opportunities. The addition of AI further empowers users to generate custom SQL queries with ease, making the application more user-friendly and accessible.
