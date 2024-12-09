#11. What is the total number of orders for each month
SELECT YEAR(order_date),MONTH(order_date) AS month, COUNT(order_id) AS total_orders
FROM orders
GROUP BY YEAR(order_date),MONTH(order_date)
ORDER BY YEAR(order_date),MONTH(order_date);

#12. Which are the top 5 products in terms of revenue within each category?
SELECT category, product_id, revenue, rnk
FROM 
(SELECT products.category,products.product_id,SUM(orders.profit) AS revenue,
DENSE_RANK() OVER (PARTITION BY products.category ORDER BY SUM(orders.profit) DESC) AS rnk
FROM products INNER JOIN orders ON orders.product_id = products.product_id
GROUP BY products.category, products.product_id) AS ranked_products
WHERE rnk <= 5
ORDER BY category, rnk;

#13. Find the products whose total profit exceeds the average profit across all products.
SELECT products.product_id,SUM(orders.profit) AS revenue
FROM orders INNER JOIN products
ON orders.product_id = products.product_id
GROUP BY products.product_id
HAVING SUM(orders.profit)>(SELECT AVG(profit) FROM orders)
ORDER BY revenue desc;

#14. What are the top 3 most profitable subcategories within each product category?
SELECT category,sub_category,profit,position FROM
(SELECT products.category,products.sub_category,SUM(orders.profit) AS profit,
DENSE_RANK () OVER(PARTITION BY products.category ORDER BY SUM(orders.profit) DESC) AS position
FROM orders INNER JOIN products ON
products.product_id=orders.product_id
GROUP BY products.category,products.sub_category) AS ranked_sub
WHERE position<=3
ORDER BY category,position,profit;

#15. Rank top 5 products within each subcategory by total quantity sold.
SELECT sub_category,product_id,quantity_sold,rnk FROM
(SELECT products.sub_category,orders.product_id,SUM(orders.quantity) AS quantity_sold,
DENSE_RANK() OVER(PARTITION BY products.sub_category ORDER BY SUM(orders.quantity) DESC) AS rnk
FROM orders INNER JOIN products ON
orders.product_id=products.product_id
GROUP BY products.sub_category,orders.product_id) AS ranked
WHERE rnk<=5
ORDER BY sub_category,rnk,quantity_sold;




