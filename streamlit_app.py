import pandas as pd
from scikit-learn.model_selection import train_test_split
from scikit-learn.linear_model import LinearRegression
from scikit-learn.metrics import mean_squared_error
import joblib
import streamlit as st
import numpy as np

# Load the dataset
file_path = './data/house_price_prediction.csv'
df = pd.read_csv(file_path)

# Display the first few rows of the dataset (for debugging purposes)
st.write("Dataset Preview:", df.head())

# Check for missing values (for debugging purposes)
st.write("Missing Values:", df.isnull().sum())

# Features and target variable
X = df[['num_bedrooms', 'num_bathrooms', 'square_footage', 'age_of_house']]
y = df[['price']]  # Assuming the target column is named 'price'

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model (for debugging purposes)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
st.write(f'Mean Squared Error: {mse}')

# Save the model
joblib.dump(model, 'house_price_model.pkl')
st.write("Model saved!")

# Load the trained model (for prediction)
model = joblib.load('house_price_model.pkl')

# Function to predict house price using the model
def predict_price(bedrooms, bathrooms, square_footage, age):
    features = np.array([[bedrooms, bathrooms, square_footage, age]])
    price = model.predict(features)[0]
    return price

# Streamlit app
st.title('House Price Prediction')

# Input fields
bedrooms = st.number_input('Enter the number of bedrooms:', min_value=1, max_value=10, value=3)
bathrooms = st.number_input('Enter the number of bathrooms:', min_value=1, max_value=10, value=2)
square_footage = st.number_input('Enter the square footage:', min_value=300, max_value=10000, value=1500)
age = st.number_input('Enter the age of the house:', min_value=0, max_value=100, value=20)

# Predict button
if st.button('Predict House Price'):
    price = predict_price(bedrooms, bathrooms, square_footage, age)
    st.write(f'Predicted House Price: ${price:,.2f}')
