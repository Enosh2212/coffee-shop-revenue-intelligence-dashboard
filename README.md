# Coffee Shop Revenue Intelligence Dashboard

A professional MNC-style data analytics dashboard built for the Coffee Shop Sales & Customer Behavior Analysis project.

## Why this version is portfolio-ready

This is not a basic demo dashboard. It is structured like a consulting/client dashboard:

- Boardroom-style executive overview
- KPI cards with business framing
- Product intelligence and SKU performance
- Customer demand behavior analysis
- Day-hour demand heatmap
- Store workload matrix
- Operational planning recommendations
- Data QA and export center
- Dynamic filters and updated data upload
- Robust CSV/XLSX handling

## How to run

### Option 1: Windows double-click
Double-click:

`run_dashboard.bat`

### Option 2: Terminal

```bash
cd coffee_shop_mnc_dashboard_pack
pip install -r requirements.txt
streamlit run app.py
```

Then open:

`http://localhost:8501`

If port 8501 is busy, Streamlit may open 8502 automatically. Check terminal output.

## Dataset schema

Default data is included in:

`data/coffee_shop_sales_raw.csv`

The upload feature expects these columns:

- transaction_id
- transaction_date
- transaction_time
- transaction_qty
- store_location
- product_id
- unit_price
- product_category
- product_type
- product_detail

The dashboard automatically creates:

- total_revenue
- hour
- month_name
- month_number
- year_month
- day_name
- day_number
- time_slot

## Portfolio / LinkedIn line

Built a professional revenue intelligence dashboard using Streamlit, Pandas and Plotly to analyze coffee shop sales, product performance, customer demand patterns, staffing windows, category contribution and client-ready business recommendations.
