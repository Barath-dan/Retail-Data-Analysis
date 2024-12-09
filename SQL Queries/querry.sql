# 6. Find the total profit per category
select products.category,sum(orders.profit) as total_profit
from products inner join orders
on products.product_id=orders.product_id
group by products.category
order by total_profit desc;

# 7. Identify the top 3 segments with the highest quantity of orders
select segment,sum(quantity) as quantity
from orders
group by segment
order by quantity desc;

# 8. Determine the average discount percentage given per region
select region,concat(round(avg(discount_percent),2),'%') as avg_discount
from orders
group by region;

# 9. Find the product category with the highest total profit
select products.category,sum(orders.profit) as total_profit
from products inner join orders 
on orders.product_id=products.product_id
group by products.category
order by total_profit desc
limit 1;

# 10. Calculate the total revenue generated per year
select year(order_date) as year,sum(profit) as revenue
from orders
group by year
order by revenue;
