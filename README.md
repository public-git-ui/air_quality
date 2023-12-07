# DATA: Data Analytics Tool for Africa

## Overview

This repository introduces our data analytics tool designed for Sensors Africa. The tool is specifically developed to handle sensor data uploads, accommodating instances of missing values. Leveraging Gaussian kernel density smoothing, our tool predicts missing values on an hourly basis for each location in the dataset. The results are then presented, showcasing both the recorded and imputed values, enabling users to observe the variations throughout the day.

## Features

- **Missing Value Prediction:** Utilizes Gaussian kernel density smoothing for accurate hourly predictions.
- **Data Visualization:** Displays both recorded and imputed values for comprehensive data analysis.
- **Data Download:** Allows users to download processed data with missing values filled for further in-depth analysis.
- **Geospatial Representation:** Includes a map displaying sensor locations to inform future sensor placement decisions.

## Usage

Install dependencies

```
pip install -r requirement.txt

```

Run server

```
streamlit run app.py

```