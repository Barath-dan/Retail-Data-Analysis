# 1. Find top 10 highest revenue generating products
select products.category,products.sub_category,orders.product_id,sum(orders.profit) as revenue
from orders left join products on orders.product_id=products.product_id
group by orders.product_id,products.category,products.sub_category
order by revenue desc
limit 10;

# 2. Find the top 5 cities with the highest profit margins
select city,sum(profit) as profit,sum(total) as total_sales,
round((sum(profit) / sum(total)) * 100,2) as profit_margin,
dense_rank() over(order by round((sum(profit) / sum(total)) * 100,2) desc) as position
from orders
group by city
order by position,profit_margin desc
limit 6;


# 3. Calculate the total discount given for each category
select products.category,sum(orders.discount_price) as total_discount_offered
from products inner join orders 
on products.product_id=orders.product_id
group by products.category
order by total_discount_offered desc;

# 4. Find the average sale price per product category
select products.category,round(avg(orders.total),2) as average_sale_price
from products inner join orders
on products.product_id=orders.product_id
group by products.category
order by  average_sale_price desc;

# 5. Find the region with the highest average sale price
select region,round(avg(total),2) as average_sale_price
from orders
group by region
order by average_sale_price desc
limit 1;

