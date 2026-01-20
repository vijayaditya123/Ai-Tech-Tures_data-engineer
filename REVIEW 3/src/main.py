from fastapi import FastAPI
from sqlalchemy import text
from src.database import engine
import pandas as pd
import matplotlib.pyplot as plt
import os

app = FastAPI(title="Product Category Trend Analytics API")

@app.get("/category/revenue-trends")
def category_revenue_trends():
   
    query = """
    SELECT 
        p.category,
        DATE_TRUNC('month', s.sale_date) AS month,
        SUM(s.revenue) AS monthly_revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.category, month
    ORDER BY p.category, month;
    """

    df = pd.read_sql(text(query), engine)

   
    df["month"] = pd.to_datetime(df["month"])
    df["monthly_revenue"] = df["monthly_revenue"].astype(float)

  
    valid_categories = (
        df.groupby("category")["month"]
        .nunique()
        .loc[lambda x: x >= 6]
        .index
    )

    df = df[df["category"].isin(valid_categories)]

   
    df["mom_growth_pct"] = (
        df.groupby("category")["monthly_revenue"]
        .pct_change() * 100
    )

    unstable_categories = (
        df.groupby("category")["mom_growth_pct"]
        .apply(lambda x: (x.abs() > 20).any())
    )

    df = df[df["category"].isin(unstable_categories[unstable_categories].index)]

 
    df["rolling_3_month_avg"] = (
        df.groupby("category")["monthly_revenue"]
        .rolling(window=3)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df["below_rolling_avg"] = (
        df["monthly_revenue"] < df["rolling_3_month_avg"]
    )

  
    os.makedirs("charts", exist_ok=True)
    chart_path = "charts/category_revenue_trends.png"

    plt.figure(figsize=(12, 6))

    for category in df["category"].unique():
        cat_df = df[df["category"] == category]

        plt.plot(
            cat_df["month"],
            cat_df["monthly_revenue"],
            marker="o",
            label=f"{category} Revenue"
        )

        plt.plot(
            cat_df["month"],
            cat_df["rolling_3_month_avg"],
            linestyle="--",
            label=f"{category} Rolling Avg"
        )

        drop_df = cat_df[cat_df["below_rolling_avg"]]
        plt.scatter(
            drop_df["month"],
            drop_df["monthly_revenue"],
            s=80,
            marker="x"
        )

    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.title("Category-wise Monthly Revenue Trends")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

  
    response = {
        "categories": [],
        "chart_path": chart_path
    }

    for category, group in df.groupby("category"):
        response["categories"].append({
            "category": category,
            "data": [
                {
                    "month": row.month.strftime("%Y-%m"),
                    "monthly_revenue": row.monthly_revenue,
                    "mom_growth_pct": row.mom_growth_pct,
                    "rolling_3_month_avg": row.rolling_3_month_avg,
                    "below_rolling_avg": row.below_rolling_avg
                }
                for row in group.itertuples()
            ]
        })

    return response
