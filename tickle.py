import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Load datasets
interactions = pd.read_csv(r"customer_interactions_synthetic.csv")
purchase_history = pd.read_csv(r"purchase_history_synthetic.csv")
product_details = pd.read_csv(r"product_details_synthetic.csv")

# Get unique Customer IDs
unique_customer_ids = purchase_history['Customer ID'].unique()

# Create a dictionary mapping new sequential numbers to Customer IDs
customer_id_mapping = {i+1: customer_id for i, customer_id in enumerate(unique_customer_ids)}

# Function to load preds_df and recommend top products for a given user
def recommend_products(user_id, num_recommendations=5):
    # Load preds_df
    preds_df = pd.read_pickle(r"preds_df.pkl")

    # Get the row corresponding to the user
    user_row_number = user_id - 1
    sorted_user_predictions = preds_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's purchase history
    user_history = purchase_history[purchase_history['Customer ID'] == user_id]['Product ID']

    # Filter out products the user has already purchased
    recommendations = sorted_user_predictions.drop(user_history, errors='ignore')

    # Get top recommendations
    top_recommendations = recommendations.head(num_recommendations)
    top_product_details = product_details[product_details['Product ID'].isin(top_recommendations.index)]

    return top_product_details[['Product ID', 'Category', 'Price', 'Ratings', 'Product Icon']], user_history

# Function to look up the user id in customer_id_mapping
def find_customer_id(user_id):
    for key, value in customer_id_mapping.items():
        if key == user_id:
            return value
    return None  # Return None if user_id not found in the dictionary

# Function to show the purchased products
def get_purchased_products(user_id, product_details, purchase_history):
    customer_id = find_customer_id(user_id)
    if customer_id is not None:
        # Get products purchased by the user
        user_purchased_products = purchase_history[purchase_history['Customer ID'] == customer_id]['Product ID']
        # Filter product_details based on the purchased products
        purchased_products = product_details[product_details['Product ID'].isin(user_purchased_products)]
        return purchased_products[['Product ID', 'Category', 'Price', 'Ratings']]
    else:
        print("User ID not found in the dictionary.")
        return None

# Streamlit UI
st.title('Product Recommendations')

# Count total rows in preds_df
try:
    preds_df = pd.read_pickle(r"preds_df.pkl")
    total_rows_preds_df = preds_df.shape[0]
except FileNotFoundError:
    st.write("preds_df file not found.")

user_id = st.number_input('Enter User ID:', min_value=1, max_value=total_rows_preds_df)

if user_id > total_rows_preds_df:
    st.error(f"User ID exceeds the total number of user IDs ({total_rows_preds_df}). Please enter a valid User ID.")
else:
    if st.button('Get Recommendations'):
        recommendations, user_history = recommend_products(user_id)
        st.write(f"Top 5 recommendations for user {user_id}:")
        
        # Display images of recommended products in a grid with tooltips
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        
        for index, row in recommendations.iterrows():
            image_url = row['Product Icon']
            try:
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                with cols.pop(0):
                    st.image(image, caption=row['Product ID'], use_column_width=True, output_format='JPEG')
                    st.info(f"Price: {row['Price']}, Ratings: {row['Ratings']}")
            except Exception as e:
                st.error(f"Error loading image for Product ID {row['Product ID']} from URL: {image_url}\nError: {e}")

        # Display purchased products in an expander
        with st.expander("Purchased Products"):
            purchased_products = get_purchased_products(user_id, product_details, purchase_history)
            st.write(purchased_products)
