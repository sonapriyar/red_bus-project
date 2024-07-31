import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu

# Function to get data from the database
def get_data_from_db(query, params):
    mydb = None
    my_cursor = None
    try:
        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="127.0.0.1",  # Use 127.0.0.1 or localhost
            port=3306,  # Specify the port if needed
            user="root",  # Replace with your actual username
            password="Vinayak@12",  # Replace with your actual password
            database="red_bus"
        )
        my_cursor = mydb.cursor(dictionary=True)
        my_cursor.execute(query, params)
        result = my_cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None
    finally:
        if my_cursor:
            my_cursor.close()
        if mydb:
            mydb.close()

# Function to get unique values from the merged_bus_details table
def get_unique_values(column_name):
    query = f"SELECT DISTINCT {column_name} FROM mergedbus_f_details"
    data = get_data_from_db(query, ())
    if data:
        return [row[column_name] for row in data]
    else:
        return []

# Function to filter data based on bus type, fare, and route name
def type_and_fare(bus_type, max_fare, route_name):
    query = """
    SELECT * 
    FROM mergedbus_f_details 
    WHERE bus_type = %s 
    AND price <= %s 
    AND route_name = %s
    """
    params = (bus_type, max_fare, route_name)
    data = get_data_from_db(query, params)
    if data is not None:
        df = pd.DataFrame(data)
        return df
    else:
        return pd.DataFrame()

# Streamlit app
st.title("Welcome to RedBus")
st.write("Vaccy made easy, coz we are always on time ⏱")

# Navigation menu
web = option_menu(menu_title="OnlineBooking",
                  options=["Home", "📌states and Routes"],
                  icons=["house", "info-circle"],
                  orientation="horizontal")

# Homepage
if web == "Home":
    st.subheader("About Us")
    st.markdown("""
        We are committed to delivering high-quality service and support. 
        Our team is here to assist you with any inquiries or issues you are facing.
    """)
    st.subheader("Our Services")
    st.markdown("""
        - **Customer Support**: We offer 24/7 customer support to assist with any questions regarding offers and booking.
        - **Feedback**: We value your feedback and use it to improve our services and offers.
    """)
    st.header("Customer Service")
    st.write("""
        If you need assistance, please reach out to our customer service team:
        - **Email**: myredbus@google.com
        - **Phone**: 7010745761
    """)
    st.header("Feedback")
    st.write("We appreciate your feedback. Please fill out the form below to share your thoughts and suggestions.")
    feedback = st.text_area("Your Feedback:")
    if st.button("Submit Feedback"):
        if feedback:
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter your feedback before submitting.")

# States and Routes page
if web == "📌states and Routes":
    st.title("RedBus Bus Details")

    # Get unique values for dropdowns
    bus_types = get_unique_values("bus_type")
    fare_options = get_unique_values("price")  # No default value for dropdowns
    route_names = get_unique_values("route_name")

    # Get user inputs
    select_type = st.selectbox("Select Bus Type", bus_types)
    select_fare = st.selectbox("Select Maximum Fare", fare_options)
    route_name = st.selectbox("Select Route Name", route_names)

    if st.button("Search"):
        if route_name:
            df_result = type_and_fare(select_type, select_fare, route_name)
            if not df_result.empty:
                st.dataframe(df_result)
            else:
                st.write("No results found.")
        else:
            st.write("Please select a route name.")
