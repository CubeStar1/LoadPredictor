from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import altair as alt

st.set_page_config(layout='wide')


@st.cache_data
def load_data(selected_year):
    files = {
        2023: 'utilities/datasets/2023_load_data_clean.csv',
        2024: 'utilities/datasets/load_data_2024_cleaned.csv'
    }
    data = pd.read_csv(files[selected_year])
    data['datetime'] = pd.to_datetime((data['datetime']), format='%Y-%m-%d %H:%M:%S')
    # data = data.set_index('datetime')
    return data
    # data = pd.read_csv('2023_load_data_clean.csv')
    # data['datetime'] = pd.to_datetime((data['datetime']) ,format='%Y-%m-%d %H:%M:%S')
    # # data = data.set_index('datetime')
    # return data


def load_data_2024():
    data = pd.read_csv('utilities/datasets/load_data_2024_cleaned.csv')
    data['datetime'] = pd.to_datetime((data['datetime']), format='%Y-%m-%d %H:%M:%S')
    # data = data.set_index('datetime')
    return data


def custom_resampler(arraylike):
    return np.sum(arraylike) / (12 * 1000)


def description():
    description, image = st.columns([1, 1], gap='large')

    with description:
        st.markdown('''
        ### Introduction

        - This project focuses on developing an intelligent load forecasting system for enhanced energy management within smart grids.
        - Employing an LSTM (Long Short-Term Memory) model, the project aims to predict daily power load patterns, contributing to efficient energy management.

        #### Objectives

        1. **Implement Predictive Analytics:** Develop and implement an LSTM model to forecast daily power load patterns based on historical data from the Delhi State Load Dispatch Centre.

        2. **Enhance Energy Management:** Enable energy management within smart grids by providing real-time insights into power load patterns and energy consumption.

        3. **Design User-Friendly Interface:** Design a user-friendly dashboard providing real-time insights into past energy consumption and future load predictions, 
        fostering accessibility and practical application.

        #### Features

        - Analyze historical power load data from the Delhi State Load Dispatch Centre (SLDC) for the years 2023 and 2024.
        - Visualize daily, monthly, and yearly power load curves to identify trends and patterns.
        - Access data collected at 5-minute intervals to predict future load patterns and energy consumption.
        - The Machine Learning LSTM model predicts daily power load patterns based on historical data collected from the SLDC at 5-minute intervals.

            ''')
        with st.expander('Delhi SLDC Operational Map'):
            map_data = pd.DataFrame({
                'latitude': [28.6139],
                'longitude': [77.2090]
            })  # Latitude and Longitude for Delhi
            st.map(map_data, use_container_width=True)

    with image:
        # st.image('power-line-rounded-modified.png', use_column_width=True)
        st.image('images/smart_grid.png', use_column_width=True)


def year_load(data, selected_year):
    average_daily_load_full_year = int(data['load'].mean())
    cumulative_energy_full_year = int(data['load'].sum())
    cumulative_energy_full_year_GWh = round(cumulative_energy_full_year / (12 * 1000), 2)
    with st.container(border=True):
        average_daily_load_full_year_card, cumulative_energy_full_year_card = st.columns(2, gap='medium')

        with average_daily_load_full_year_card:
            with st.container(border=True):
                st.info('Average Load per Day')
                st.metric(label='Average Load per Day',
                          value=str(average_daily_load_full_year) + ' MW',
                          label_visibility='collapsed')
            with st.container(border=True):
                year_data_per_day = data.resample('D', on='datetime').median()
                year_data_per_day.rename(columns={'load': 'Load in MW'}, inplace=True)
                st.line_chart(data=year_data_per_day, y='Load in MW', use_container_width=True, color='#BED754')
        with cumulative_energy_full_year_card:
            with st.container(border=True):
                st.info('Total Energy Generated')
                st.metric(label='Total Energy Generated',
                          value=str(cumulative_energy_full_year_GWh) + ' GWh',
                          label_visibility='collapsed')

            with st.container(border=True):
                year_data_per_month = data.resample('M', on='datetime').apply(custom_resampler)
                year_data_per_month.rename(columns={'load': 'Energy in GWh'}, inplace=True)
                st.bar_chart(data=year_data_per_month, y='Energy in GWh', use_container_width=True, color='#BED754')


def month_load(data, selected_month):
    month_data = data[data['datetime'].dt.month == selected_month]
    average_daily_load = int(month_data['load'].mean())
    average_daily_load_delta = int(average_daily_load - data['load'].mean())
    average_daily_load_delta_percentage = round(average_daily_load_delta / average_daily_load * 100, 2)

    cumulative_energy_per_month = data.resample('M', on='datetime').sum()
    cumulative_month_energy = int(month_data['load'].sum())
    cumulative_month_energy_GWh = round(cumulative_month_energy / (12 * 1000), 2)
    cumulative_month_energy_delta = int(cumulative_month_energy - cumulative_energy_per_month['load'].mean())
    cumulative_month_energy_delta_percentage = round(cumulative_month_energy_delta / cumulative_month_energy * 100, 2)

    with st.container(border=True):
        average_month_load_card, cumulative_month_energy_card = st.columns(2, gap='medium')
        with average_month_load_card:
            with st.container(border=True):
                st.info('Average Load per Day')
                st.metric(label='Average Load per Day',
                          value=str(average_daily_load) + ' MW',
                          delta=str(average_daily_load_delta_percentage) + ' %',
                          label_visibility='collapsed')

            with st.container(border=True):
                month_data_resampled_H = month_data.resample('H', on='datetime').median()
                month_data_resampled_H.rename(columns={'load': 'Load in MW'}, inplace=True)
                # st.line_chart(data=monthly_data, x='datetime', y='load', width=300, color='#f8007a')
                # st.line_chart(data=monthly_data, x='datetime', y='Load in MW', width=300)
                st.line_chart(data=month_data_resampled_H, y='Load in MW')

        with cumulative_month_energy_card:
            with st.container(border=True):
                st.info('Total Energy Generated')
                st.metric(label='Total Energy Generated',
                          value=str(cumulative_month_energy_GWh) + ' GWh',
                          delta=str(cumulative_month_energy_delta_percentage) + ' %',
                          label_visibility='collapsed')
            with st.container(border=True):
                month_data_resampled_D = month_data.resample('D', on='datetime').apply(custom_resampler)
                month_data_resampled_D.rename(columns={'load': 'Energy in GWh'}, inplace=True)
                # st.bar_chart(monthly_data, color='#f95959')
                st.bar_chart(data=month_data_resampled_D, y='Energy in GWh')


def day_load(data, selected_date):
    # Filter data for the selected date
    selected_data = data[data['datetime'].dt.date == selected_date]
    selected_data.rename(columns={'load': 'Load in MW'}, inplace=True)
    # st.dataframe(selected_data)
    # selected_data.to_excel('selected_data.xlsx')
    # print(selected_data.head())
    st.line_chart(data=selected_data, x='datetime', y='Load in MW', use_container_width=True, color='#ff8011')


def load_prediction():
    predicted_data = pd.read_excel('utilities/datasets/selected_data.xlsx')
    predicted_data.drop(columns=['Unnamed: 0'], inplace=True)
    predicted_data.rename(columns={'load': 'Predicted Load in MW'}, inplace=True)
    # predicted_data = predicted_data.set_index('datetime')
    print(predicted_data.head())
    # st.dataframe(predicted_data)

    with st.container(border=True):
        actual_graph, predicted_graph = st.columns(2, gap='medium')

        with actual_graph:
            with st.container(border=True):
                st.markdown('#### Actual Load')
                st.line_chart(data=predicted_data, x='datetime',
                              y="Load in MW",
                              color=['#ff8011'], use_container_width=True)
        with predicted_graph:
            with st.container(border=True):
                st.markdown('#### Predicted Load')
                st.line_chart(data=predicted_data, x='datetime',
                              y="Predicted Load in MW",
                              color=["#83c9ff"],
                              use_container_width=True)

        actual_vs_predicted_graph, prediction_metrics = st.columns(2, gap='medium')
        with actual_vs_predicted_graph:
            with st.container(border=True):
                st.markdown('#### Actual vs Predicted Load')
                st.line_chart(data=predicted_data, x='datetime',
                              y=["Load in MW", "Predicted Load in MW"],
                              color=['#ff8011', '#83c9ff'], use_container_width=True)

        with prediction_metrics:
            RMSE = round(np.sqrt(np.mean((predicted_data['Load in MW'] - predicted_data['Predicted Load in MW']) ** 2)),
                         3)
            MAE = round(np.mean(np.abs(predicted_data['Load in MW'] - predicted_data['Predicted Load in MW'])), 3)
            MAPE = round(np.mean(np.abs(
                (predicted_data['Load in MW'] - predicted_data['Predicted Load in MW']) / predicted_data[
                    'Load in MW'])), 3) * 100
            accuracy = round(100 - MAPE, 3)
            with st.container(border=True):
                st.markdown('#### Prediction Metrics')
                col1, col2 = st.columns(2, gap='small')
                with col1:
                    with st.container(border=True):
                        st.info('RMSE')
                        st.metric(label='RMSE',
                                  value=str(RMSE) + ' MW',
                                  label_visibility='collapsed')
                    with st.container(border=True):
                        st.info('MAE')
                        st.metric(label='MAE',
                                  value=str(MAE) + ' MW',
                                  label_visibility='collapsed')

                with col2:
                    with st.container(border=True):
                        st.info('MAPE')
                        st.metric(label='MAPE',
                                  value=str(MAPE) + ' %',
                                  label_visibility='collapsed')
                    with st.container(border=True):
                        st.info('Accuracy')
                        st.metric(label='Accuracy',
                                  value=str(accuracy) + ' %',
                                  label_visibility='collapsed')


@st.cache_data
def get_min_max_date(data):
    min_date = data['datetime'].min().date()
    max_date = data['datetime'].max().date()
    return min_date, max_date


# data_2024 = load_data_2024()

st.title('Intelligent Load Forecasting for Enhanced Energy Management in Smart Grids')
st.markdown('---')
description()

st.sidebar.header('Select Data')
st.markdown('---')

# Year-wise load
st.header('Yearly Load Curve')
with st.sidebar:
    selected_year = st.selectbox('Select a year', [2023, 2024])

data = load_data(selected_year)
year_load(data, selected_year)
st.markdown('---')

# Month-wise load
st.header('Monthly Load Curve ')

with st.sidebar:
    selected_month = st.selectbox('Select a month', data['datetime'].dt.month.unique())
month_load(data, selected_month)
st.markdown('---')

# Day-wise load
st.header('Daily Load Curve ')
with st.sidebar:
    min_date, max_date = get_min_max_date(data)
    default_date = min_date + (max_date - min_date) // 2
    selected_date = st.date_input('Select a date', default_date, min_value=min_date, max_value=max_date)
day_load(data, selected_date)

st.markdown('---')

# Load Prediction
st.header('Load Prediction')
load_prediction()



