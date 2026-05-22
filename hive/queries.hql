-- Créer la base de données
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- Créer la table externe pointant vers HDFS
CREATE EXTERNAL TABLE IF NOT EXISTS sales (
    order_id STRING,
    sale_date STRING,
    category STRING,
    product STRING,
    quantity INT,
    unit_price DOUBLE,
    total DOUBLE,
    country STRING,
    payment_method STRING,
    customer_id STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'hdfs://localhost:8020/ecommerce/input'
TBLPROPERTIES ("skip.header.line.count"="1");

-- Vérifier
SELECT COUNT(*) AS total_orders FROM sales;

-- Top 10 produits par revenu
SELECT product, category,
       SUM(total) AS revenue,
       SUM(quantity) AS qty_sold
FROM sales
GROUP BY product, category
ORDER BY revenue DESC
LIMIT 10;

-- Revenu mensuel
SELECT SUBSTR(sale_date, 1, 7) AS month,
       SUM(total) AS revenue,
       COUNT(*) AS nb_orders
FROM sales
GROUP BY SUBSTR(sale_date, 1, 7)
ORDER BY month;

-- Revenu par pays
SELECT country,
       SUM(total) AS revenue,
       COUNT(*) AS nb_orders,
       ROUND(AVG(total), 2) AS avg_order
FROM sales
GROUP BY country
ORDER BY revenue DESC;

-- Revenu par mode de paiement
SELECT payment_method,
       SUM(total) AS revenue,
       COUNT(*) AS nb_orders
FROM sales
GROUP BY payment_method
ORDER BY revenue DESC;

-- Top 10 clients
SELECT customer_id,
       SUM(total) AS total_spent,
       COUNT(*) AS nb_orders
FROM sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- Export : Revenu par catégorie et mois
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/hive_cat_month'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
SELECT category, SUBSTR(sale_date, 1, 7) AS month, SUM(total) AS revenue
FROM sales
GROUP BY category, SUBSTR(sale_date, 1, 7)
ORDER BY category, month;