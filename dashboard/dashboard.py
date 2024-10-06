#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Project Information
st.sidebar.write("### Nama: Muhammad Nur Iskandar Dzulqarnain")
st.sidebar.write("### Email: m200b4ky2978@bangkit.academy")
st.sidebar.write("### ID Dicoding: m200b4ky2978")

# Function to load and clean data
def load_data():
    # Load the datasets
    pd_day = pd.read_csv('./data/day.csv')
    pd_hour = pd.read_csv('./data/hour.csv')

    # Remove duplicates
    pd_day = pd_day.drop_duplicates()
    pd_hour = pd_hour.drop_duplicates()

    # Ensure the 'dteday' columns are in datetime format
    pd_day['dteday'] = pd.to_datetime(pd_day['dteday'])
    pd_hour['dteday'] = pd.to_datetime(pd_hour['dteday'])

    # Create a main data by merging the day and hour datasets
    main_data = pd.merge(pd_hour, pd_day, on=['instant', 'dteday', 'season', 'yr', 
                                               'mnth', 'holiday', 'weekday', 
                                               'workingday', 'weathersit', 
                                               'temp', 'atemp', 'hum', 'windspeed'], 
                         how='left')
    
    return main_data

# Function to inspect data columns and check for 'cnt'
def inspect_data(data):
    st.write("### Kolom-kolom Data:")
    st.write(data.columns)  # Display all column names
    if 'cnt_x' in data.columns:
        st.write("Menggunakan kolom 'cnt_x' untuk jumlah sewa sepeda.")
        return 'cnt_x'
    elif 'cnt_y' in data.columns:
        st.write("Menggunakan kolom 'cnt_y' untuk jumlah sewa sepeda.")
        return 'cnt_y'
    else:
        st.error("Kolom 'cnt' tidak ditemukan di data!")
        return None

# Main function
def main():
    st.title("Analisis Data Penyewaan Sepeda")
    st.write("## Menentukan Pertanyaan Bisnis")
    st.write("1. Bagaimana sewa sepeda bervariasi berdasarkan jam dalam sehari dan hari dalam seminggu?")
    st.write("2. Apa dampak kondisi cuaca terhadap sewa sepeda?")

    # Load data
    main_data = load_data()
    
    # Display the first few rows of the dataset
    st.write("### Data Utama:")
    st.dataframe(main_data.head())

if __name__ == "__main__":
    main()

## EDA

# Set the aesthetic style of the plots
sns.set(style='whitegrid')

# Load main_data
main_data = pd.read_csv('./dashboard/main_data.csv')

# Strip any leading or trailing spaces from column names
main_data.columns = main_data.columns.str.strip()

# Check the columns in main_data
st.write("Column Names in main_data:")
st.write(main_data.columns)

# Display data overview
st.title('Exploratory Data Analysis (EDA) of Bike Rentals')
st.write(main_data.head())
st.write(main_data.describe())
st.write("Missing Values Count:")
st.write(main_data.isnull().sum())

# Ensure 'cnt_x' column exists
if 'cnt_x' not in main_data.columns:
    st.error("Column 'cnt_x' not found in the data!")
else:
    # Visualization & Exploratory Analysis

    # Question 1: Total Rentals by Hour
    plt.figure(figsize=(12, 6))
    hourly_rentals = main_data.groupby('hr')['cnt_x'].sum().reset_index()
    sns.lineplot(x='hr', y='cnt_x', data=hourly_rentals, marker='o')
    plt.title('Total Sewa Sepeda Berdasarkan Jam dalam Sehari')
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Total Sewa')
    plt.xticks(range(24))
    plt.grid()
    st.pyplot(plt)  # Display the plot in Streamlit

    plt.figure(figsize=(12, 6))
    daily_rentals = main_data.groupby('weekday')['cnt_x'].sum().reset_index()
    sns.barplot(x='weekday', y='cnt_x', data=daily_rentals, palette='viridis')
    plt.title('Total Sewa Sepeda Berdasarkan Hari dalam Seminggu')
    plt.xlabel('Hari dalam Seminggu (0=Min, 6=Sab)')
    plt.ylabel('Total Sewa')
    plt.xticks(ticks=range(7), labels=['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'])
    plt.grid()
    st.pyplot(plt)  # Display the plot in Streamlit

    # Question 2: Total Rentals by Weather Situation
    plt.figure(figsize=(12, 6))
    weather_rentals = main_data.groupby('weathersit')['cnt_x'].sum().reset_index()
    sns.barplot(x='weathersit', y='cnt_x', data=weather_rentals, palette='coolwarm')
    plt.title('Total Sewa Sepeda Berdasarkan Situasi Cuaca')
    plt.xlabel('Situasi Cuaca')
    plt.ylabel('Total Sewa')
    plt.xticks(ticks=[0, 1, 2, 3], labels=['Cerah', 'Kabut', 'Salju Ringan', 'Hujan Berat'])
    plt.grid()
    st.pyplot(plt)  # Display the plot in Streamlit

    plt.figure(figsize=(12, 6))
    sns.boxplot(x='weathersit', y='cnt_x', hue='season', data=main_data, palette='Set2')
    plt.title('Sewa Sepeda Berdasarkan Situasi Cuaca di Berbagai Musim')
    plt.xlabel('Situasi Cuaca')
    plt.ylabel('Jumlah Sewa')
    plt.xticks(ticks=[0, 1, 2, 3], labels=['Cerah', 'Kabut', 'Salju Ringan', 'Hujan Berat'])
    plt.legend(title='Musim', loc='upper right')
    plt.grid()
    st.pyplot(plt)  # Display the plot in Streamlit

    # Insight (Optional Analysis)

    # Total Rentals by Hour Numerical Analysis
    hourly_total = hourly_rentals['cnt_x'].sum()
    hourly_mean = hourly_rentals['cnt_x'].mean()
    hourly_median = hourly_rentals['cnt_x'].median()
    hourly_std = hourly_rentals['cnt_x'].std()

    st.subheader("Analisis Sewa Sepeda Berdasarkan Jam:")
    st.write(f"Total Sewa Sepeda: {hourly_total}")
    st.write(f"Rata-rata Sewa Sepeda per Jam: {hourly_mean:.2f}")
    st.write(f"Median Sewa Sepeda per Jam: {hourly_median:.2f}")
    st.write(f"Standar Deviasi Sewa Sepeda per Jam: {hourly_std:.2f}\n")

    # Total Rentals by Day Numerical Analysis
    daily_total = daily_rentals['cnt_x'].sum()
    daily_mean = daily_rentals['cnt_x'].mean()
    daily_median = daily_rentals['cnt_x'].median()
    daily_std = daily_rentals['cnt_x'].std()

    st.subheader("Analisis Sewa Sepeda Berdasarkan Hari:")
    st.write(f"Total Sewa Sepeda: {daily_total}")
    st.write(f"Rata-rata Sewa Sepeda per Hari: {daily_mean:.2f}")
    st.write(f"Median Sewa Sepeda per Hari: {daily_median:.2f}")
    st.write(f"Standar Deviasi Sewa Sepeda per Hari: {daily_std:.2f}")

    # Total Rentals by Weather Situation
    weather_rentals = main_data.groupby('weathersit')['cnt_x'].sum().reset_index()
    st.subheader("Total Sewa Sepeda Berdasarkan Situasi Cuaca:")
    st.write(weather_rentals)

    # Calculate and display percentage of rentals by weather situation
    total_rentals = weather_rentals['cnt_x'].sum()
    weather_rentals['persentase'] = (weather_rentals['cnt_x'] / total_rentals) * 100
    st.write("Total Sewa dan Persentase:")
    st.write(weather_rentals)

    # Descriptive statistics for rentals by weather situation and season
    weather_season_stats = main_data.groupby(['weathersit', 'season'])['cnt_x'].describe()
    st.subheader("Statistik Deskriptif Sewa Sepeda Berdasarkan Situasi Cuaca dan Musim:")
    st.write(weather_season_stats)

# Add conclusion or insights at the end
st.subheader("Kesimpulan")
st.write("""
## Kesimpulan Pertanyaan 1
Analisis sewa sepeda berdasarkan jam dalam sehari menunjukkan adanya fluktuasi yang signifikan, dengan rata-rata sewa sepeda per jam mencapai 137.194,96 unit. Hal ini mengindikasikan bahwa waktu-waktu tertentu, seperti pagi dan sore, cenderung lebih ramai dibandingkan waktu siang. Medan penggunaan ini dapat dimanfaatkan oleh pengelola untuk meningkatkan layanan, seperti menambah unit sepeda pada jam sibuk untuk menghindari antrian panjang dan meningkatkan kepuasan pelanggan. Selain itu, total sewa sepeda selama seminggu mencerminkan pola penggunaan yang berbeda di setiap hari, dengan rata-rata sewa per hari mencapai 470.382,71 unit. Data ini menunjukkan bahwa hari-hari tertentu, seperti akhir pekan, lebih diminati oleh pengguna, yang bisa dimanfaatkan untuk mengembangkan promosi khusus pada hari-hari tersebut untuk meningkatkan sewa sepeda.

## Kesimpulan Pertanyaan 2
Dari analisis yang dilakukan, terlihat bahwa kondisi cuaca memiliki pengaruh yang signifikan terhadap sewa sepeda, di mana 71,01% dari total sewa terjadi dalam situasi cuaca cerah. Hasil ini menegaskan bahwa pengguna lebih cenderung menyewa sepeda ketika cuaca mendukung, sehingga penting bagi pengelola untuk memperhatikan ramalan cuaca dalam merencanakan aktivitas promosi. Selain itu, analisis statistik deskriptif menunjukkan bahwa sewa sepeda bervariasi menurut musim dan kondisi cuaca, dengan data menunjukkan variasi signifikan dalam rata-rata sewa sepeda di setiap musim. Dengan mempertimbangkan faktor cuaca, pengelola dapat merancang strategi yang lebih efektif, seperti menawarkan diskon atau promosi pada hari dengan cuaca yang lebih mendukung, guna menarik lebih banyak pengguna dan meningkatkan total sewa sepeda.
""")

