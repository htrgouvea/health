# Health

This project provides a modular, extensible Python-based CLI to process health data exported from Apple Health and generate predictions using machine learning.

#### Features

- Extract historical **weight data** from `export.xml` (Apple Health)
- Predict future weight trends using **polynomial regression**
- Save forecasts as both **CSV and visual plots**

### Download

```
git clone https://github.com/htrgouvea/health
cd health
pip3 install -r requirements.txt
```

### Module: Weight Forecast

Step 1: Export Apple Health data

Export your health data from your iPhone:

    1. Apple Health → Profile → Export All Data

    2. Unzip the exported file and place the export.xml file in the root of the project directory.
    
Step 2: Extract weight data from export.xml

```
python3 health.py --extract weight
```
    
This will parse all historical body mass records and create a clean CSV:

```
data/weight.csv
```

Step 3: Predict future weight using AI

```
python3 health.py --predict weight --value 5
````

You can change --value to any number of future days you want to predict (default is 7).

This command will:

1. Train a polynomial regression model using your full weight history;
2. Predict weight trends for the next N days;
3. Save results to:

```
output/weight_forecast.csv     # Tabular data: date, predicted_weight, min, max
plots/weight_forecast.png      # Graph with historical trend and prediction curve
```