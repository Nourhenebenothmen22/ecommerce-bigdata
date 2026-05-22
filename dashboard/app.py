from flask import Flask, Response
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
import json
import os

app = Flask(__name__)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


def load_revenue_by_category():
    path = os.path.join(RESULTS_DIR, "revenue_by_category.tsv")
    df = pd.read_csv(path, sep="\t", header=None, names=["category", "revenue"])
    df["revenue"] = df["revenue"].astype(float)
    return df.sort_values("revenue", ascending=False)


def load_monthly_sales():
    path = os.path.join(RESULTS_DIR, "monthly_sales.tsv")
    df = pd.read_csv(path, sep="\t", header=None, names=["month", "revenue", "orders"])
    df["revenue"] = df["revenue"].astype(float)
    df["orders"] = df["orders"].astype(int)
    return df.sort_values("month")


def load_sales_by_country():
    path = os.path.join(RESULTS_DIR, "sales_by_country.tsv")
    df = pd.read_csv(path, sep="\t", header=None, names=["country", "revenue", "orders"])
    df["revenue"] = df["revenue"].astype(float)
    df["orders"] = df["orders"].astype(int)
    return df.sort_values("revenue", ascending=False)


@app.route("/")
def dashboard():
    # === Charger les donnees ===
    df_cat = load_revenue_by_category()
    df_month = load_monthly_sales()
    df_country = load_sales_by_country()

    # === KPIs ===
    total_revenue = df_cat["revenue"].sum()
    total_orders = df_month["orders"].sum()
    total_countries = len(df_country)
    avg_order = total_revenue / total_orders if total_orders > 0 else 0

    # === Chart 1 : Revenu par categorie (Bar) ===
    fig1 = px.bar(
        df_cat, x="category", y="revenue",
        title="Revenu par Categorie",
        color="revenue",
        color_continuous_scale="Blues",
        labels={"revenue": "Revenu", "category": "Categorie"}
    )
    fig1.update_layout(template="plotly_dark", height=400)

    # === Chart 2 : Repartition (Pie) ===
    fig2 = px.pie(
        df_cat, values="revenue", names="category",
        title="Repartition du Revenu par Categorie",
        hole=0.4
    )
    fig2.update_layout(template="plotly_dark", height=400)

    # === Chart 3 : Ventes mensuelles (Line + Bar) ===
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_month["month"], y=df_month["revenue"],
        mode="lines+markers", name="Revenu",
        line=dict(color="#00d4ff", width=3)
    ))
    fig3.add_trace(go.Bar(
        x=df_month["month"], y=df_month["orders"],
        name="Commandes", yaxis="y2",
        marker_color="rgba(255,165,0,0.4)"
    ))
    fig3.update_layout(
        title="Evolution Mensuelle des Ventes",
        template="plotly_dark", height=450,
        yaxis=dict(title="Revenu"),
        yaxis2=dict(title="Nb Commandes", overlaying="y", side="right"),
        legend=dict(x=0, y=1.1, orientation="h")
    )

    # === Chart 4 : Ventes par pays (Bar horizontal) ===
    fig4 = px.bar(
        df_country, x="revenue", y="country",
        orientation="h",
        title="Revenu par Pays",
        color="revenue",
        color_continuous_scale="Viridis",
        labels={"revenue": "Revenu", "country": "Pays"}
    )
    fig4.update_layout(template="plotly_dark", height=450, yaxis=dict(autorange="reversed"))

    # === Chart 5 : Treemap commandes par pays ===
    fig5 = px.treemap(
        df_country, path=["country"], values="orders",
        title="Volume de Commandes par Pays",
        color="revenue",
        color_continuous_scale="RdYlGn"
    )
    fig5.update_layout(template="plotly_dark", height=450)

    # === Convertir en JSON ===
    c1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    c2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    c3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    c4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    c5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

    # === HTML complet ===
    html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>E-Commerce Big Data Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0f0f23;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            padding: 20px;
        }
        h1 {
            text-align: center;
            font-size: 2.2em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .kpi-card {
            background: linear-gradient(135deg, #1a1a3e, #2d2d5e);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .kpi-card .icon { font-size: 2em; margin-bottom: 10px; }
        .kpi-card .value {
            font-size: 1.8em;
            font-weight: bold;
            color: #00d4ff;
        }
        .kpi-card .label {
            color: #aaa;
            margin-top: 5px;
            font-size: 0.95em;
        }
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .chart-card {
            background: #1a1a3e;
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .chart-full {
            grid-column: span 2;
        }
        .footer {
            text-align: center;
            color: #555;
            margin-top: 30px;
            padding: 15px;
            font-size: 0.9em;
        }
        @media (max-width: 900px) {
            .kpi-container { grid-template-columns: repeat(2, 1fr); }
            .charts-grid { grid-template-columns: 1fr; }
            .chart-full { grid-column: span 1; }
        }
    </style>
</head>
<body>

    <h1>E-Commerce Big Data Dashboard</h1>
    <p class="subtitle">Analyse des ventes - HDFS + MapReduce + Hive</p>

    <div class="kpi-container">
        <div class="kpi-card">
            <div class="icon">💰</div>
            <div class="value">""" + "{:,.2f}".format(total_revenue) + """</div>
            <div class="label">Revenu Total</div>
        </div>
        <div class="kpi-card">
            <div class="icon">📦</div>
            <div class="value">""" + "{:,}".format(total_orders) + """</div>
            <div class="label">Commandes</div>
        </div>
        <div class="kpi-card">
            <div class="icon">🌍</div>
            <div class="value">""" + str(total_countries) + """</div>
            <div class="label">Pays</div>
        </div>
        <div class="kpi-card">
            <div class="icon">🧾</div>
            <div class="value">""" + "{:,.2f}".format(avg_order) + """</div>
            <div class="label">Panier Moyen</div>
        </div>
    </div>

    <div class="charts-grid">
        <div class="chart-card">
            <div id="chart1"></div>
        </div>
        <div class="chart-card">
            <div id="chart2"></div>
        </div>
        <div class="chart-card chart-full">
            <div id="chart3"></div>
        </div>
        <div class="chart-card">
            <div id="chart4"></div>
        </div>
        <div class="chart-card">
            <div id="chart5"></div>
        </div>
    </div>

    <div class="footer">
        Projet Big Data - HDFS - MapReduce - Hive - Flask - Plotly
    </div>

    <script>
        var c1 = """ + c1 + """;
        var c2 = """ + c2 + """;
        var c3 = """ + c3 + """;
        var c4 = """ + c4 + """;
        var c5 = """ + c5 + """;
        Plotly.newPlot("chart1", c1.data, c1.layout);
        Plotly.newPlot("chart2", c2.data, c2.layout);
        Plotly.newPlot("chart3", c3.data, c3.layout);
        Plotly.newPlot("chart4", c4.data, c4.layout);
        Plotly.newPlot("chart5", c5.data, c5.layout);
    </script>

</body>
</html>
"""
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)