#!/bin/bash
echo "=== Running MapReduce Jobs ==="

STREAMING_JAR=$(docker exec namenode find /opt/hadoop -name "hadoop-streaming*.jar" | head -1)

# Job 1 : Revenu par catégorie
echo "--- Job 1: Revenue by Category ---"
docker exec namenode hdfs dfs -rm -r -f /ecommerce/output_revenue
docker exec namenode hadoop jar $STREAMING_JAR \
  -files /mapreduce/mapper_revenue.py,/mapreduce/reducer_revenue.py \
  -mapper "python3 mapper_revenue.py" \
  -reducer "python3 reducer_revenue.py" \
  -input /ecommerce/input/sales.csv \
  -output /ecommerce/output_revenue

# Job 2 : Ventes mensuelles
echo "--- Job 2: Monthly Sales ---"
docker exec namenode hdfs dfs -rm -r -f /ecommerce/output_monthly
docker exec namenode hadoop jar $STREAMING_JAR \
  -files /mapreduce/mapper_monthly.py,/mapreduce/reducer_monthly.py \
  -mapper "python3 mapper_monthly.py" \
  -reducer "python3 reducer_monthly.py" \
  -input /ecommerce/input/sales.csv \
  -output /ecommerce/output_monthly

# Job 3 : Ventes par pays
echo "--- Job 3: Sales by Country ---"
docker exec namenode hdfs dfs -rm -r -f /ecommerce/output_country
docker exec namenode hadoop jar $STREAMING_JAR \
  -files /mapreduce/mapper_country.py,/mapreduce/reducer_country.py \
  -mapper "python3 mapper_country.py" \
  -reducer "python3 reducer_country.py" \
  -input /ecommerce/input/sales.csv \
  -output /ecommerce/output_country

echo "=== All MapReduce Jobs Done ==="