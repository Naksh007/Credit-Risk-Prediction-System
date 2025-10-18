# src/prepare_db.py
import os, duckdb, yaml
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH, "r") as f: cfg = yaml.safe_load(f)
csv_path, db_path, table_name = cfg["data_csv_path"], cfg["db_path"], cfg["table_name"]
os.makedirs(os.path.dirname(db_path), exist_ok=True)
con = duckdb.connect(db_path)
con.execute(f"""CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path}', sample_size=-1);""")
for sql_file in ["../sql/build_features.sql","../sql/kpis_duckdb.sql"]:
    with open(os.path.join(os.path.dirname(__file__), sql_file), "r", encoding="utf-8") as f:
        con.execute(f.read())
print(con.execute("SHOW TABLES").fetchdf()); print(con.execute("SHOW VIEWS").fetchdf())
con.close(); print(f"DuckDB ready at {db_path}")
