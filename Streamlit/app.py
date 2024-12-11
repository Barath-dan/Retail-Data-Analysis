#IMPORTING REQUIRED PACKAGES AND LIBRARIES
import streamlit as st
import mysql.connector as connector
import pandas as pd
import vanna
from vanna.remote import VannaDefault
from typing import List
import plotly.express as px
#DICTIONARIES TO HOLD QUERY TITLE AND RESPECTIVE QUERIES AS KEY-VALUE PAIR. THE VALUES WILL BE PASSED ON TO THE QUERY EXECUTION FUNCTION LATER
Provided_Queries={
    "Top 10 highest revenue generating products":"""select products.category,products.sub_category,orders.product_id,sum(orders.profit) as revenue
from orders left join products
on orders.product_id=products.product_id
group by orders.product_id,products.category,products.sub_category
order by revenue desc
limit 10;""",
    "Top 5 cities with the highest profit margins":"""select city,sum(profit) as profit,sum(total) as total_sales,
round((sum(profit) / sum(total)) * 100,2) as profit_margin,
dense_rank() over(order by round((sum(profit) / sum(total)) * 100,2) desc) as position
from orders
group by city
order by position,profit_margin desc
limit 6;""",
    "Total discount given for each category":"""select products.category,sum(orders.discount_price) as total_discount_offered
from products inner join orders
on products.product_id=orders.product_id
group by products.category
order by total_discount_offered desc;""",
    "Average sale price per product category":"""select products.category,round(avg(orders.total),2) as average_sale_price
from products inner join orders
on products.product_id=orders.product_id
group by products.category
order by  average_sale_price desc;""",
    "Region with the highest average sale price":"""select region,round(avg(total),2) as average_sale_price
from orders
group by region
order by average_sale_price desc
limit 1;""",
    "Total profit per category":"""select products.category,sum(orders.profit) as total_profit
from products inner join orders
on products.product_id=orders.product_id
group by products.category
order by total_profit desc;""",
    "Top 3 segments with the highest quantity of orders":"""select segment,sum(quantity) as quantity
from orders
group by segment
order by quantity desc;""",
    "Average discount percentage given per region":"""select region,concat(round(avg(discount_percent),2),'%') as avg_discount
from orders
group by region;""",
    "Product category with the highest total profit":"""select products.category,sum(orders.profit) as total_profit
from products inner join orders
on orders.product_id=products.product_id
group by products.category
order by total_profit desc
limit 1;""",
    "Total revenue generated per year":"""select year(order_date) as year,sum(profit) as revenue
from orders
group by year
order by revenue;"""
}
Own_Queries={"Total number of orders for each month":"""SELECT YEAR(order_date),MONTH(order_date) AS month, COUNT(order_id) AS total_orders
FROM orders
GROUP BY YEAR(order_date),MONTH(order_date)
ORDER BY YEAR(order_date),MONTH(order_date);""",
"Top 5 products in terms of revenue within each category":"""SELECT category, product_id, revenue, rnk
FROM 
(SELECT products.category,products.product_id,SUM(orders.profit) AS revenue,
DENSE_RANK() OVER (PARTITION BY products.category ORDER BY SUM(orders.profit) DESC) AS rnk
FROM products INNER JOIN orders ON orders.product_id = products.product_id
GROUP BY products.category, products.product_id) AS ranked_products
WHERE rnk <= 5
ORDER BY category, rnk;""",
"Products whose total profit exceeds the average profit across all products":"""SELECT products.product_id,SUM(orders.profit) AS revenue
FROM orders INNER JOIN products
ON orders.product_id = products.product_id
GROUP BY products.product_id
HAVING SUM(orders.profit)>(SELECT AVG(profit) FROM orders)
ORDER BY revenue desc;""",
"Top 3 most profitable subcategories within each product category":"""SELECT category,sub_category,profit,position FROM
(SELECT products.category,products.sub_category,SUM(orders.profit) AS profit,
DENSE_RANK () OVER(PARTITION BY products.category ORDER BY SUM(orders.profit) DESC) AS position
FROM orders INNER JOIN products ON
products.product_id=orders.product_id
GROUP BY products.category,products.sub_category) AS ranked_sub
WHERE position<=3
ORDER BY category,position,profit;""",
"Top 5 products within each subcategory by total quantity sold":"""SELECT sub_category,product_id,quantity_sold,rnk FROM
(SELECT products.sub_category,orders.product_id,SUM(orders.quantity) AS quantity_sold,
DENSE_RANK() OVER(PARTITION BY products.sub_category ORDER BY SUM(orders.quantity) DESC) AS rnk
FROM orders INNER JOIN products ON
orders.product_id=products.product_id
GROUP BY products.sub_category,orders.product_id) AS ranked
WHERE rnk<=5
ORDER BY sub_category,rnk,quantity_sold;""",
"Top 3 customer segments with the highest total profit per region":"""SELECT region,segment,profit,rnk FROM
(SELECT region,segment,SUM(profit) AS profit,
DENSE_RANK() OVER(PARTITION BY region ORDER BY SUM(profit) DESC) AS rnk
FROM orders
GROUP BY region,segment) AS ranked
WHERE rnk<=3
ORDER BY region,rnk,profit;""",
"Top 3 products with the highest revenue in each customer segment":"""SELECT product_id,segment,profit,rnk FROM
(SELECT product_id,segment,SUM(profit) AS profit,
DENSE_RANK() OVER(PARTITION BY segment ORDER BY SUM(profit) DESC) AS rnk
FROM orders
GROUP BY product_id,segment) AS ranked
WHERE rnk<=3
ORDER BY segment,rnk,profit;""",
"For each category, label products by their profit into High(GREATER THAT 10000),MEDIUM(BETWEEN 10000 AND 3000),LOW(BELOW 3000)":
"""SELECT products.category,products.product_id,SUM(orders.quantity) AS total_quantity,SUM(orders.profit) AS total_profit,
CASE 
WHEN SUM(orders.profit) > 10000 THEN 'High Profit' 
WHEN SUM(orders.profit) <= 10000 AND SUM(orders.profit) > 3000 THEN 'Medium Profit'  
ELSE 'Low Profit' END AS profit_category
FROM orders
INNER JOIN products ON orders.product_id = products.product_id
GROUP BY products.category, products.product_id
ORDER BY total_profit DESC;""",
"Rank the top 5 selling products by region based on total quantity sold using ROW_NUMBER()":"""SELECT region,product_id,total_quantity,rnk FROM
(SELECT orders.region,products.product_id,SUM(orders.quantity) AS total_quantity,
ROW_NUMBER () OVER(PARTITION BY orders.region ORDER BY SUM(orders.quantity) DESC) AS rnk
FROM orders INNER JOIN products ON orders.product_id=products.product_id
GROUP BY orders.region,products.product_id) AS ranked
WHERE rnk<=5
ORDER BY region,rnk,total_quantity;""",
"Identify products with a total profit greater than $10,000 but less than 50 units sold for each category":
"""SELECT products.category,products.product_id,SUM(orders.quantity) AS total_quantity,
SUM(orders.profit) AS total_profit FROM orders
INNER JOIN products ON orders.product_id = products.product_id
GROUP BY products.category, products.product_id
HAVING SUM(orders.profit) > 10000 AND SUM(orders.quantity) < 50
ORDER BY total_profit DESC;""",
"Compare the monthly profit trends between 2023 and 2022.For each month, show whether the profit increased, decreased, or remained the same compared to the previous year.":
"""SELECT MONTH(order_date) AS Month,
SUM(CASE WHEN YEAR(order_date)=2022 THEN profit ELSE 0 END) AS Profit_for_Previous_year,
SUM(CASE WHEN YEAR(order_date)=2023 THEN profit ELSE 0 END) AS Profit_for_Current_year,
CASE
WHEN SUM(CASE WHEN YEAR(order_date) = 2023 THEN profit ELSE 0 END) > SUM(CASE WHEN YEAR(order_date) = 2022 THEN profit ELSE 0 END)
THEN 'Increased'
WHEN SUM(CASE WHEN YEAR(order_date) = 2023 THEN profit ELSE 0 END) < SUM(CASE WHEN YEAR(order_date) = 2022 THEN profit ELSE 0 END) 
THEN 'Decreased'
ELSE 'No Change'
END AS profit_trend
FROM orders
GROUP BY MONTH(order_date)
ORDER BY MONTH(order_date);"""
}
#CONNECTING TO OUR MODEL IN VANNA AI
vn=VannaDefault(model='retail_sales_datan',api_key='95df20a8eff1425db53ca1558012256e')
#FUNCTION FOR DATABASE CREATION. IT RETURNS DATABASE CONNECTION
def database_connection():
    try:
        connection = connector.connect(
            host="localhost",
            user="root",
            password="Barath@01",
            database="retail_store_db"
        )
        return connection
    except connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None
#FUNCTION FOR EXECUTING QUERY.
#IT RECEIVES QUERY SELECTED BY THE USER AS THE INPUT AND CREATES DATABASE CONNECTION USING database_connection() FUNCTION AND RETURNS THE OUTPUT AS PANDAS DATAFRAME
def execute_query(query):
    try:
        conn=database_connection()
        cursor=conn.cursor()
        cursor.execute(query)
        result=cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return pd.DataFrame(result, columns=column_names)
    except Exception as e:
        st.error(f"Error executing the query: {e}")
        return pd.DataFrame()
#FUNCTION FOR DISPLAYING RESULTS AS DATAFRAME IT GETS TWO ARGUMENTS 1. USER'S SELECTION 2.RESPECTIVE QUERY FROM THE DICTIONARY
def display_results(selection,query):
    st.subheader(selection)
    selected_query=st.selectbox("Choose a query",list(query.keys()))
    st.write("**Query:**")
    st.code(f"{query[selected_query]}")
    if st.button("Run",key=f"run_button_{selected_query}"):
        result=execute_query(query[selected_query])
        if not result.empty:
            st.write("**Result:**")
            return st.dataframe(result)
        else:
            st.warning("No data returned for the query.")
#FUNCTION USING VANNA AI GENERATE SQL METHOD TO DISPLAY QUERY FOR USER'S QUESTION   
def get_sql_vanna(user_query):
    try:
        sql_query = vn.generate_sql(user_query)
        return sql_query
    except Exception as e:
        st.error(f"Error generating SQL query with Vanna AI: {e}")
        return ""   
#STREAMLIT USER INTERFACE
st.title("SQL Querry App")
st.sidebar.title("Menu")
option=st.sidebar.radio("Choose an option",["Provided Queries", "Own Queries", "Create AI-Powered Custom Query"])

if option == "Provided Queries":
    display_results("Provided Queries", Provided_Queries)

elif option == "Own Queries":
    display_results("Own Queries", Own_Queries)

elif option == "Create AI-Powered Custom Query":
    st.subheader("Custom Query Generation-Powered by AI")
    user_input = st.text_area("Enter your query:")
    
    if user_input:
            # Get the SQL query from Vanna AI
            generated_query = get_sql_vanna(user_input)
            st.write("**Generated SQL Query:**")
            st.code(generated_query)
            
            if st.button("Execute SQL Query",key="run_button"):
                    # Execute the SQL query
                result_df = execute_query(generated_query)
                if not result_df.empty:
                    st.write("**Query Results:**")
                    st.dataframe(result_df)
                else:
                    st.warning("No results found for the generated query.")
                #ONLY FOR DEBUGGING IN TERMINAL
                print(result_df)       
else:
    st.write("Please select a valid option")





