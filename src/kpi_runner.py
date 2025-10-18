# src/kpi_runner.py
import os, duckdb, yaml, pandas as pd
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH, "r") as f: cfg = yaml.safe_load(f)
db_path = cfg["db_path"]
out_dir = os.path.join(os.path.dirname(__file__), "..", "artifacts", "kpis")
os.makedirs(out_dir, exist_ok=True)
con = duckdb.connect(db_path)
for name, q in {"monthly_kpis":"SELECT * FROM v_monthly_kpis","good_bad":"SELECT * FROM v_good_bad","mom_received":"SELECT * FROM v_mom_received"}.items():
    df = con.execute(q).fetchdf(); df.to_csv(os.path.join(out_dir, f"{name}.csv"), index=False); print(f"Wrote {name}.csv ({len(df)} rows)")
con.close(); print("KPI exports done.")
