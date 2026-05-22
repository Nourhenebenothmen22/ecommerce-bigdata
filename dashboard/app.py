from flask import Flask, render_template
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
    # === Chart 1 : Revenu par catégorie (Bar) ===
    df_cat = load_revenue_by_category()
    fig1 = px.bar(
        df_cat, x="category", y="revenue",
        title="💰 Revenu par Catégorie",
        color="revenue",
        color_continuous_scale="Blues",
        labels={"revenue": "Revenu (€)", "category": "Catégorie"}
    )
    fig1.update_layout(template="plotly_dark", height=400)

    # === Chart 2 : Revenu par catégorie (Pie) ===
    fig2 = px.pie(
        df_cat, values="revenue", names="category",
        title="📊 Répartition du Revenu par Catégorie",
        hole=0.4
    )
    fig2.update_layout(template="plotly_dark", height=400)

    # === Chart 3 : Ventes mensuelles (Line) ===
    df_month = load_monthly_sales()
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
        title="📈 Évolution Mensuelle des Ventes",
        template="plotly_dark", height=450,
        yaxis=dict(title="Revenu (€)"),
        yaxis2=dict(title="Nb Commandes", overlaying="y", side="right"),
        legend=dict(x=0, y=1.1, orientation="h")
    )

    # === Chart 4 : Ventes par pays (Bar horizontal) ===
    df_country = load_sales_by_country()
    fig4 = px.bar(
        df_country, x="revenue", y="country",
        orientation="h",
        title="🌍 Revenu par Pays",
        color="revenue",
        color_continuous_scale="Viridis",
        labels={"revenue": "Revenu (€)", "country": "Pays"}
    )
    fig4.update_layout(template="plotly_dark", height=450, yaxis=dict(autorange="reversed"))

    # === Chart 5 : Nombre de commandes par pays (Treemap) ===
    fig5 = px.treemap(
        df_country, path=["country"], values="orders",
        title="🗺️ Volume de Commandes par Pays",
        color="revenue",
        color_continuous_scale="RdYlGn"
    )
    fig5.update_layout(template="plotly_dark", height=450)

    # === KPIs ===
    total_revenue = df_cat["revenue"].sum()
    total_orders = df_month["orders"].sum()
    total_countries = len(df_country)
    avg_order = total_revenue / total_orders if total_orders > 0 else 0

    kpis = {
        "total_revenue": f"{total_revenue:,.2f} €",
        "total_orders": f"{total_orders:,}",
        "total_countries": total_countries,
        "avg_order": f"{avg_order:,.2f} €"
    }

    # Convertir les figures en JSON
    charts = {
        "chart1": json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
        "chart2": json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
        "chart3": json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
        "chart4": json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder),
        "chart5": json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder),
    }

    return render_template("dashboard.html", charts=charts, kpis=kpis)


if __name__ == "__main__":
    app.run(debug=True, port=5000)