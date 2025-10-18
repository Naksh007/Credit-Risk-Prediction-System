# app/streamlit_app.py
import os, pandas as pd, streamlit as st
st.set_page_config(page_title="Credit Risk KPIs & Model (Nubank-style)", layout="wide")
st.title("Credit Risk Prediction – Nubank-style (SQL + ML)")

kpi_dir = os.path.join(os.path.dirname(__file__), "..", "artifacts", "kpis")

def show_csv(name, parse_dates=None):
    path = os.path.join(kpi_dir, f"{name}.csv")
    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=parse_dates or [])
        st.subheader(name)
        st.dataframe(df)
        return df
    else:
        st.info(f"Run `python src/kpi_runner.py` to generate {name}.csv")
        return None

st.header("KPIs")
monthly = show_csv("monthly_kpis", parse_dates=["month"])
if monthly is not None:
    st.line_chart(monthly.set_index("month")[["loan_applications","total_funded_amount","amount_received"]])
show_csv("good_bad")
show_csv("mom_received")

st.header("Model")
art_dir = os.path.join(os.path.dirname(__file__), "..", "artifacts")
if os.path.exists(os.path.join(art_dir, "model_cv_results.csv")):
    st.subheader("Cross-Validation Summary")
    st.dataframe(pd.read_csv(os.path.join(art_dir, "model_cv_results.csv")))
if os.path.exists(os.path.join(art_dir, "shap_summary.png")):
    st.subheader("SHAP Summary (Top 20)")
    st.image(os.path.join(art_dir, "shap_summary.png"))
else:
    st.info("Run `python src/train.py` to train and generate SHAP plots.")
