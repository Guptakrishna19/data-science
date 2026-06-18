CREATE DATABASE day18_sql;

USE day18_sql;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    order_date DATE,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

INSERT INTO customers VALUES
(1,'Krish','Mumbai'),
(2,'Rahul','Pune'),
(3,'Aman','Delhi'),
(4,'Priya','Mumbai'),
(5,'Neha','Bangalore'),
(6,'Rohan','Hyderabad'),
(7,'Anjali','Chennai'),
(8,'Vikas','Pune'),
(9,'Sneha','Mumbai'),
(10,'Arjun','Delhi');

INSERT INTO products VALUES
(1,'Laptop','Electronics',60000),
(2,'Phone','Electronics',30000),
(3,'Mouse','Accessories',1000),
(4,'Keyboard','Accessories',2000),
(5,'Monitor','Electronics',15000),
(6,'Printer','Electronics',12000),
(7,'Webcam','Accessories',2500),
(8,'Headphones','Accessories',5000),
(9,'Tablet','Electronics',25000),
(10,'Smartwatch','Electronics',10000);

INSERT INTO orders VALUES
(101,1,1,1,'2025-01-01'),
(102,2,2,2,'2025-01-02'),
(103,1,3,5,'2025-01-03'),
(104,3,1,1,'2025-01-04'),
(105,4,5,2,'2025-01-05'),
(106,5,2,1,'2025-01-06'),
(107,6,8,3,'2025-01-07'),
(108,7,4,4,'2025-01-08'),
(109,8,9,1,'2025-01-09'),
(110,9,10,2,'2025-01-10'),
(111,10,6,1,'2025-01-11'),
(112,2,7,2,'2025-01-12');

SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM orders;


SELECT COUNT(*) AS total_customers
FROM customers;

SELECT COUNT(*) AS total_products
FROM products;

SELECT *
FROM products
WHERE price > 50000;

SELECT *
FROM customers
WHERE city='Mumbai';

SELECT *
FROM orders
ORDER BY order_date DESC
LIMIT 10;

SELECT AVG(price)
FROM products;

SELECT MAX(price)
FROM products;

SELECT MIN(price)
FROM products;

SELECT SUM(price*quantity)
FROM orders o
JOIN products p
ON o.product_id=p.product_id;

SELECT COUNT(*)
FROM orders;

SELECT
c.city,
SUM(p.price*o.quantity) revenue
FROM orders o
JOIN customers c
ON o.customer_id=c.customer_id
JOIN products p
ON o.product_id=p.product_id
GROUP BY c.city;

SELECT
category,
SUM(price*quantity)
FROM orders o
JOIN products p
ON o.product_id=p.product_id
GROUP BY category;

SELECT
customer_id,
SUM(quantity)
FROM orders
GROUP BY customer_id
ORDER BY SUM(quantity) DESC
LIMIT 1;

SELECT
product_id,
SUM(quantity)
FROM orders
GROUP BY product_id
ORDER BY SUM(quantity) DESC
LIMIT 1;

SELECT
c.city,
SUM(p.price*o.quantity) revenue
FROM orders o
JOIN customers c
ON o.customer_id=c.customer_id
JOIN products p
ON o.product_id=p.product_id
GROUP BY c.city
HAVING revenue > 50000;

SELECT
c.customer_name,
o.order_id
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id;

SELECT
p.product_name,
o.quantity
FROM products p
JOIN orders o
ON p.product_id=o.product_id;

SELECT *
FROM products
WHERE price >
(
SELECT AVG(price)
FROM products
);

SELECT
product_id,
SUM(quantity) qty_sold,
RANK() OVER(
ORDER BY SUM(quantity) DESC
) rank_num
FROM orders
GROUP BY product_id;

SELECT
order_date,
SUM(quantity)
OVER(
ORDER BY order_date
) running_total
FROM orders;

EDGE CASE 1
SELECT COUNT(*)
FROM orders;

EDGE CASE 2
SELECT *
FROM customers c
LEFT JOIN orders o
ON c.customer_id=o.customer_id;