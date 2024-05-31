# Intelligent Load Forecasting for Enhanced Energy Management in Smart Grids

## Table of Contents
1. [Overview](#overview)
2. [Objectives](#objectives)
3. [Key Features](#key-features)
4. [How it Works](#how-it-works)
5. [Installation and Setup](#installation-and-setup)
6. [How to Use](#how-to-use)
7. [Dependencies](#dependencies)
8. [File Structure](#file-structure)
9. [Hosted Version](#hosted-version)


## Overview
- This project is centered around load forecasting for electricity demand in a power grid. 
- The data used for this project was sourced from the Delhi State Load Dispatch Centre.

## Objective
- The main objective was to implement an LSTM model to generate short-term load forecasts, predicting demand 24 hours into the future.

## Key Features
- Short-term load forecasting using LSTM model
- Data visualization using Streamlit
- High accuracy with an RSME (Root Mean Square Error) less than 1%

## How it Works
- The LSTM model is trained using the dataset scraped from the Delhi State Load Dispatch Centre (https://www.delhisldc.org/Loaddata.aspx?mode=28/05/2024)
- The model learns to predict the electricity demand for the next 24 hours based on the previous 10 days. 
- The predictions are then visualized using the Streamlit app.

![Streamlit App](https://github.com/CubeStar1/LoadPredictor/blob/master/images/load_predictor.jpg?raw=true)

## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CubeStar1/LoadPredictor.git
   cd LoadPredictor
2. **Create a virtual environment:**

   ```bash
   python -m venv venv
3. **Activate the virtual environment:**

   - On Windows:   
      ```bash
     .\venv\Scripts\activate
   - On Unix or MacOS:
      ```bash
     source venv/bin/activate
4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

5. **Run the Streamlit app:**

   ```bash
    streamlit run app.py
6. Use the Jupyter Notebook to train the model and perform data analysis.
## How to Use
- After setting up the project, you can use the Streamlit app to visualize the electricity demand and the model's predictions. 
- You can also use the Jupyter Notebook to train the model and perform data analysis.

## Dependencies
- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- TensorFlow
- Keras
- Streamlit
- BeautifulSoup
- Jupyter Notebook


## File Structure
- `app.py`: The Streamlit app for data visualization
- `utilities/datasets/`: The dataset used for training the LSTM model
- `scripts/data-scraping.py`: Used to scrape data from the Delhi State Load Dispatch Centre
- `utilities/jupyter-notebook/`: Jupyter Notebook used for data analysis and model training

## Hosted Version
- The Streamlit app is hosted on and can be accessed here: https://loadpredictor.streamlit.app/
