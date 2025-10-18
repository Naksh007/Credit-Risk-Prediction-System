# src/train.py
import os, warnings, joblib, yaml, duckdb, numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import shap, matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "r") as f: cfg = yaml.safe_load(f)
db_path, feature_view, target_col, id_col = cfg["db_path"], cfg["feature_view"], cfg["target_col"], cfg["id_col"]
seed, n_splits = int(cfg.get("seed",42)), int(cfg.get("n_splits",5))

con = duckdb.connect(db_path)
df = con.execute(f"SELECT * FROM {feature_view}").fetchdf()
con.close()
if id_col in df.columns: df = df.drop(columns=[id_col])

num_cols = df.select_dtypes(include=[np.number]).columns.tolist(); num_cols.remove(target_col)
cat_cols = [c for c in df.columns if c not in num_cols + [target_col]]

for c in num_cols:
    lo, hi = df[c].quantile([0.01,0.99]).values; df[c] = df[c].clip(lo, hi)

X, y = df.drop(columns=[target_col]), df[target_col].astype(int)
num_pipe = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
cat_pipe = Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
pre = ColumnTransformer([("num", num_pipe, num_cols), ("cat", cat_pipe, cat_cols)])

models = {
    "log_reg": (LogisticRegression(max_iter=400), {"clf__C": np.logspace(-2,2,10)}),
    "rf": (RandomForestClassifier(n_estimators=500, random_state=seed, n_jobs=-1),
           {"clf__max_depth":[None,6,10], "clf__min_samples_leaf":[1,2,5], "clf__min_samples_split":[2,5,10]}),
    "lgbm": (LGBMClassifier(random_state=seed, n_estimators=700, learning_rate=0.05),
             {"clf__num_leaves":[31,63], "clf__max_depth":[-1,6,10], "clf__min_child_samples":[10,20,50],
              "clf__subsample":[0.7,0.9,1.0], "clf__colsample_bytree":[0.7,0.9,1.0]}),
    "catboost": (CatBoostClassifier(random_state=seed, verbose=False, iterations=700, learning_rate=0.05),
                 {"clf__depth":[4,6,8], "clf__l2_leaf_reg":[1,3,5,7]})
}
cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)

best_model, best_score, results = None, -np.inf, []
for name, (clf0, grid) in models.items():
    print(f"\n=== Tuning {name} ===")
    pipe = ImbPipeline([("pre", pre), ("rus", RandomUnderSampler(random_state=seed)), ("clf", clf0)])
    search = RandomizedSearchCV(pipe, grid, n_iter=min(18, sum(len(v) if hasattr(v,'__len__') else 10 for v in grid.values())),
                                scoring="average_precision", n_jobs=-1, cv=cv, random_state=seed, verbose=1)
    search.fit(X, y); ap = search.best_score_; results.append({"model":name,"avg_precision":ap,"params":search.best_params_})
    if ap > best_score: best_model, best_score = search.best_estimator_, ap

out_dir = os.path.join(os.path.dirname(__file__), "..", "artifacts")
os.makedirs(out_dir, exist_ok=True)
pd.DataFrame(results).to_csv(os.path.join(out_dir, "model_cv_results.csv"), index=False)
joblib.dump(best_model, os.path.join(out_dir, "model_best.joblib"))
print("Best AP:", best_score)

try:
    X_small = best_model.named_steps["pre"].transform(X.head(1500))
    clf = best_model.named_steps["clf"]
    num_features = best_model.named_steps["pre"].transformers_[0][2]
    ohe = best_model.named_steps["pre"].transformers_[1][1].named_steps["ohe"]
    cat_features = ohe.get_feature_names_out(best_model.named_steps["pre"].transformers_[1][2])
    feature_names = list(num_features) + list(cat_features)
    explainer = shap.Explainer(clf, X_small, feature_names=feature_names)
    shap_values = explainer(X_small)
    shap.plots.beeswarm(shap_values, show=False, max_display=20)
    out_path = os.path.join(out_dir, "shap_summary.png")
    import matplotlib.pyplot as plt
    plt.tight_layout(); plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print("Saved SHAP summary:", out_path)
except Exception as e:
    print("SHAP skipped:", e)
