#!/bin/bash
echo "=== Upload data to HDFS ==="

docker exec namenode hdfs dfs -mkdir -p /ecommerce/input
docker exec namenode hdfs dfs -put -f /data/sales.csv /ecommerce/input/
docker exec namenode hdfs dfs -ls /ecommerce/input/

echo "=== Upload done ==="