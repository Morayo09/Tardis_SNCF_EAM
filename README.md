# 🚆 TARDIS – Predicting the Unpredictable

A data science project to **analyze** and **predict** SNCF train delays using machine learning, and to present insights through an interactive Streamlit dashboard.

## 📂 Repository Structure

```
G-AIA-210-COT-2-2-tardis-exauce.agbodjalou/
├── dataset.csv              # Initial dataset
├── cleaned_dataset.csv      # Cleaned dataset (output from tardis_eda.ipynb)
├── tardis_eda.ipynb         # Data aanalysing & cleaning notebook
├── tardis_model.ipynb       # Model training notebook
├── tardis_dashboard.py      # Streamlit dashboard
├── requirements.txt         # Project dependencies
└── utils/                   # Helper files (e.g., city.txt, yyyy_mm.txt)
```

## ✨ Features

- **Data Cleaning & Preparation**
  - Load and inspect the dataset.
  - Handle missing values and remove duplicate entries.
  - Convert columns to appropriate data types.
  - Perform feature engineering to create new useful variables.

- **Exploratory Data Analysis (EDA)**
  - Generate summary statistics to understand the dataset better.
  - Plot delay distributions and identify common delay durations.
  - Compare delays across different stations and times of day.
  - Use heatmaps to explore correlations between different variables.

- **Predictive Modeling**
  - Select relevant features for training.
  - Train a simple machine learning model using scikit-learn (Linear Regression).
  - Evaluate performance using metrics like RMSE, R², or accuracy.
  - Compare different models and justify the selection of the best one (Linear Regression and Random Forest).

- **Interactive Streamlit Dashboard**
  - Delay distribution charts (histograms, boxplots).
  - Station-level analysis (delays per station, cancellation rates).
  - Heatmaps to show correlations between delay factors (external causes, infrastructure, traffic
management).
  - Interactive elements allowing users to select routes, stations, or dates.
  - Summary statistics like average delays, cancellation counts, and punctuality rates.
  - Integrate the trained model for real-time predictions.
  - Deploy the Streamlit application and provide usage documentation.

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:EpitechPGEPromo2029/G-AIA-210-COT-2-2-tardis-exauce.agbodjalou.git
   cd G-AIA-210-COT-2-2-tardis-exauce.agbodjalou.git
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Linux system
   sudo apt install python3-venv
   cd /path/to/your/project
   python3 -m venv myvenv
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Code formatting**
   The project uses [ruff](https://docs.astral.sh/ruff/formatter/) for formatting:
   ```bash
   ruff format .
   ```

## ▶️ Usage

### 1️⃣ Data Exploration & Cleaning
Run the EDA notebook to clean the dataset:
```bash
jupyter notebook tardis_eda.ipynb
```
This produces `cleaned_dataset.csv`.

### 2️⃣ Model Training
Train and evaluate the predictive model:
```bash
jupyter notebook tardis_model.ipynb
```

### 3️⃣ Launch the Dashboard
Start the Streamlit application:
```bash
streamlit run tardis_dashboard.py
```
Then open the provided local URL (usually http://localhost:8501) in your browser.

## 📊 Data

- **dataset.csv** – Raw SNCF delay records (departure times, stations, delay durations, etc.)
- **cleaned_dataset.csv** – Processed dataset ready for modeling
- **utils/** – Auxiliary files such as city and date references

## 🚀 Possible Enhancements

- Implement a feature selection technique to optimize the model.
- Add real-time data updates from SNCF open data.
- Use advanced visualization techniques like animated charts or geospatial maps.
- Experiment with deep learning models for improved accuracy.
- Include an explanatory model component to provide reasons for predictions.

## 👥 Authors

- **Alvira, Exauce, Morayo**
- Epitech academic project **G-AIA-210**
