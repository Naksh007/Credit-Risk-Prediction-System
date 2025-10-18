
# Credit Risk Prediction (SQL + ML)

## Project Overview

This project demonstrates an **end-to-end credit risk prediction system** built using **machine learning (ML)** models and **SQL**. The system predicts whether a loan will default, based on various borrower and loan features.

## Folder Structure

```
credit-risk-project/
├── data/ -> bank loan data
├── sql/
│   ├── build_features.sql              # SQL to preprocess and transform data
│   └── kpis_duckdb.sql                # SQL to compute KPIs
├── src/
│   ├── config.yaml                    # Configuration file for paths and parameters
│   ├── prepare_db.py                  # Loads data into DuckDB and creates views
│   ├── kpi_runner.py                  # Runs SQL queries and exports KPIs as CSVs
│   └── train.py                       # Machine learning model training and evaluation
├── notebooks/
│   └── Credit_Risk_Prediction.ipynb  # Jupyter notebook for analysis and modeling
├── app/
│   └── streamlit_app.py               # Streamlit app for KPI and model result visualization
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
└── .gitignore                         # Git ignore file for unnecessary files
```

## Getting Started

### Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.8+**
- **Pip** for installing dependencies
- **Streamlit** for running the interactive dashboard

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repo-url>
   cd credit-risk-nubank-style-project
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the Database**:
   ```bash
   python src/prepare_db.py
   ```

4. **Run the KPI Export**:
   ```bash
   python src/kpi_runner.py
   ```

5. **Train the Model**:
   ```bash
   python src/train.py
   ```

6. **Launch the Streamlit Dashboard**:
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Project Walkthrough

- **Data Preprocessing with SQL**: We use SQL to clean and transform the data, creating necessary features like `loan_to_income` and temporal features (`issue_year`, `issue_month`). SQL views are created to handle preprocessing and KPIs efficiently.

- **Model Training**: Multiple models, including **Logistic Regression**, **Random Forest**, **LightGBM**, and **CatBoost**, are trained using **Stratified K-Fold Cross-Validation**. We use **RandomizedSearchCV** for hyperparameter tuning.

- **Model Evaluation**: The models are evaluated using **Average Precision (PR-AUC)** to account for the imbalanced nature of the dataset.

- **SHAP for Model Interpretability**: We use **SHAP** to explain the model’s predictions, identifying which features were most influential in determining loan defaults.

- **Streamlit Dashboard**: An interactive **Streamlit app** visualizes the **KPIs**, **model performance**, and **SHAP explanations**.

## Future Work and Extensions

- **Real-Time Model Deployment**: Adapt the pipeline for real-time credit risk prediction services.
- **Enhanced Feature Engineering**: Add advanced features like **text-based features** or **time-series models**.
- **Additional Models**: Integrate other models like **XGBoost** or **Neural Networks** for improved performance.

## Conclusion

This **Credit Risk Prediction System** offers a comprehensive, **scalable**, and **reproducible** approach for predicting loan defaults, using **SQL for preprocessing** and **machine learning models** for prediction.
