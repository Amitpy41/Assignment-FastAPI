import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"
# BASE_URL = "https://assignment-fastapi.onrender.com"

def signup():
    st.title("Signup")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        response = requests.post(f"{BASE_URL}/register", json={"username": username, "email": email, "password": password})
        st.success(response.json().get("message", "Registered"))

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Logged in successfully!")
            st.session_state["token"] = response.json().get("access_token")
        else:
            st.error(response.json().get("detail", "Login failed"))

def password_recovery():
    st.title("Password Recovery")
    username_or_email = st.text_input("Username or Email")
    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    
    if st.button("Recover Password"):
        response = requests.post(
            f"{BASE_URL}/recover-password",
            json={
                "username_or_email": username_or_email,
                "old_password": old_password,
                "new_password": new_password
            }
        )
        
        if response.status_code == 200:
            st.success(response.json().get("message", "Password updated successfully!"))
        else:
            st.error(response.json().get("detail", "Password recovery failed."))

if "token" not in st.session_state:
    page = st.sidebar.radio("Navigate", ["Login", "Signup", "Password Recovery"])
    if page == "Signup":
        signup()
    elif page == "Login":
        login()
    elif page == "Password Recovery":
        password_recovery()
else:
    st.write("Welcome! You're logged in.")
    if st.button("Logout"):
        del st.session_state["token"]
