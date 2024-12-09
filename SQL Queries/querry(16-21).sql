#16. Identify the top 3 customer segments with the highest total profit per region.
SELECT region,segment,profit,rnk FROM
(SELECT region,segment,SUM(profit) AS profit,
DENSE_RANK() OVER(PARTITION BY region ORDER BY SUM(profit) DESC) AS rnk
FROM orders
GROUP BY region,segment) AS ranked
WHERE rnk<=3
ORDER BY region,rnk,profit;

#17. Identify the top 3 products with the highest revenue in each customer segment.
SELECT product_id,segment,profit,rnk FROM
(SELECT product_id,segment,SUM(profit) AS profit,
DENSE_RANK() OVER(PARTITION BY segment ORDER BY SUM(profit) DESC) AS rnk
FROM orders
GROUP BY product_id,segment) AS ranked
WHERE rnk<=3
ORDER BY segment,rnk,profit;

#18. For each category, label products by their profit into High(GREATER THAT 10000),MEDIUM(BETWEEN 10000 AND 3000),LOW(BELOW 3000) 
SELECT products.category,products.product_id,SUM(orders.quantity) AS total_quantity,SUM(orders.profit) AS total_profit,
CASE 
WHEN SUM(orders.profit) > 10000 THEN 'High Profit' 
WHEN SUM(orders.profit) <= 10000 AND SUM(orders.profit) > 3000 THEN 'Medium Profit'  
ELSE 'Low Profit' END AS profit_category
FROM orders
INNER JOIN products ON orders.product_id = products.product_id
GROUP BY products.category, products.product_id
ORDER BY total_profit DESC;

#19. Rank the top 5 selling products by region based on total quantity sold using ROW_NUMBER().
SELECT region,product_id,total_quantity,rnk FROM
(SELECT orders.region,products.product_id,SUM(orders.quantity) AS total_quantity,
ROW_NUMBER () OVER(PARTITION BY orders.region ORDER BY SUM(orders.quantity) DESC) AS rnk
FROM orders INNER JOIN products ON orders.product_id=products.product_id
GROUP BY orders.region,products.product_id) AS ranked
WHERE rnk<=5
ORDER BY region,rnk,total_quantity;

#20. Identify products with a total profit greater than $10,000 but less than 50 units sold for each category
SELECT products.category,products.product_id,SUM(orders.quantity) AS total_quantity,
SUM(orders.profit) AS total_profit FROM orders
INNER JOIN products ON orders.product_id = products.product_id
GROUP BY products.category, products.product_id
HAVING SUM(orders.profit) > 10000 AND SUM(orders.quantity) < 50
ORDER BY total_profit DESC;

#21. Compare the monthly profit trends between 2023 and 2022.
	#For each month, show whether the profit increased, decreased, or remained the same compared to the previous year.
SELECT MONTH(order_date) AS Month,
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
ORDER BY MONTH(order_date);



