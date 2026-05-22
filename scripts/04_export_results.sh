#!/bin/bash
echo "=== Exporting results from HDFS ==="

mkdir -p dashboard/results

docker exec namenode hdfs dfs -cat /ecommerce/output_revenue/part-00000 > dashboard/results/revenue_by_category.tsv
docker exec namenode hdfs dfs -cat /ecommerce/output_monthly/part-00000 > dashboard/results/monthly_sales.tsv
docker exec namenode hdfs dfs -cat /ecommerce/output_country/part-00000 > dashboard/results/sales_by_country.tsv

echo "=== Export done ==="