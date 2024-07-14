# Import necessary libraries
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

tab1,tab2,tab3=st.tabs(['Home','Prediction','Conclusion of Prediction'])
with tab1:

    col1,col2=st.columns(2,gap='large')

    with col1:
        st.write('## :violet[Problem Statement]')
        st.write('* The resale flat market in Singapore is highly competitive, and it can be challenging to accurately estimate the resale value of a flat. There are many factors that can affect resale prices, such as location, flat type, floor area, and lease duration.')
        st.write('* This predictive model will be based on historical data of resale flat transactions, and it aims to assist both potential buyers and sellers in estimating the resale value of a flat.')
        st.write('## :red[Objective]')
        st.write('* The objective of this project is to develop a machine learning model and deploy it as a user-friendly web application that predicts the resale prices of flats in Singapore. ')

    with col2:
        st.write('## Tools and Technologies used')
        st.write(' Python, Pandas, numpy, matplotlib, seaborn, Plotly, Streamlit, sklearn')
        st.write('## :red[ML Model]')
        st.write('* The ML model used in this project is :blue[Random Forest Regressor].')
        st.write('* Comparing other regressors, Random Forest Regressor had a high :red[R-squared score], which means it has performed best. ')


with tab2:
    @st.cache_data  # Caches the dataset for faster loading
    def load_data():
        return pd.read_csv(r'C:\Users\admin\Downloads\DataScience\Singapure_resale_flat_prices_updated.csv')


    # Sidebar - Input parameters for the model
    st.sidebar.header('Input Parameters')
    def user_input_features():
        floor_area_sqm = st.sidebar.slider('Floor Area (sqm)', 30, 300, 100)
        remaining_lease_years = st.sidebar.slider('Remaining Lease (years)', 30, 99, 70)
        storey_range = st.sidebar.selectbox('Storey Range', ['01 to 03', '04 to 06', '07 to 09', '10 to 12', '13 to 15'])
        flat_model = st.sidebar.selectbox('flat_model', {'IMPROVED': 1, 'NEW GENERATION': 2, 'MODEL A': 3, 'STANDARD': 4, 'SIMPLIFIED': 5,
                                'MODEL A-MAISONETTE': 6, 'APARTMENT': 7, 'MAISONETTE': 8, 'TERRACE': 9, '2-ROOM': 10,
                                'IMPROVED-MAISONETTE': 11,
                                'MULTI GENERATION': 12, 'PREMIUM APARTMENT': 13, 'Improved': 14, 'New Generation': 15,
                                'Model A':
                                    16, 'Standard': 17, 'Apartment': 18, 'Simplified': 19, 'Model A-Maisonette': 20,
                                'Maisonette':
                                    21, 'Multi Generation': 22, 'Adjoined flat': 23, 'Premium Apartment': 24, 'Terrace': 25,
                                'Improved-Maisonette': 26, 'Premium Maisonette': 27, '2-room': 28, 'Model A2': 29, 'DBSS': 30,
                                'Type S1': 31, 'Type S2': 32, 'Premium Apartment Loft': 33, '3Gen': 34})

        data = {'floor_area_sqm': floor_area_sqm,
                'remaining_lease': remaining_lease_years,
                'storey_range': storey_range,
                'flat_model': flat_model}
        features = pd.DataFrame(data, index=[0])
        return features

    # Main section
    st.title('Singapore Flat Price Prediction')
    st.markdown('### Predicting flat prices based on user inputs')

    # Load data
    df = load_data()

    # Display some data
    st.subheader('Dataset')
    st.write(df.head())

    # Split data into features and target variable
    X = df[['floor_area_sqm', 'remaining_lease', 'storey_range', 'flat_model']]
    y = df['resale_price']

    # Convert categorical variables into dummy/indicator variables
    X = pd.get_dummies(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Sidebar - Input parameters for predictionhgdZ
    input_df = user_input_features()
    input_df_encoded = pd.get_dummies(input_df)

    # Ensure input_df_encoded has the same columns as X after one-hot encoding
    missing_cols = set(X.columns) - set(input_df_encoded.columns)
    for col in missing_cols:
        input_df_encoded[col] = 0

    # Ensure the order of columns in input_df_encoded is the same as in X
    input_df_encoded = input_df_encoded[X.columns]

    # Prediction
    prediction = model.predict(input_df_encoded)

with tab3:

    # Display prediction
    st.subheader('Prediction')
    st.write('Predicted Price (SGD):', prediction[0])
