import streamlit as st
import hashlib
import json
import secrets
import string

PASSWORD_FILE = "passwords.json"

def load_passwords():
    try:
        with open(PASSWORD_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

def check_password_strength(password):
    length = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    score = sum([length, has_upper, has_lower, has_digit, has_special])
    
    if score == 5:
        return "Strong"
    elif score >= 3:
        return "Medium"
    else:
        return "Weak"

def store_password(site, username, password):
    passwords = load_passwords()
    passwords[site] = {"username": username, "password": hash_password(password)}
    save_passwords(passwords)
    return f"Password for {site} saved successfully!"

def retrieve_password(site):
    passwords = load_passwords()
    if site in passwords:
        return passwords[site]
    else:
        return "No password found for this site."

st.set_page_config(page_title="Password Manager", page_icon="🔐", layout="wide")

st.markdown(
    """
    <style>
        body {background-color: #f9f9f9;}
        .stApp {background-color: #f9f9f9;}
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .stSidebar {
            background-color: #e3f2fd;
            color: #333;
            padding: 10px;
        }
        .stSidebar .stRadio > label {
            color: #333;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔐 Password Manager & Strength Checker")

menu = ["Generate Password", "Check Password Strength", "Store Password", "Retrieve Password"]
choice = st.sidebar.radio("Select an option", menu)

st.markdown("---")

if choice == "Generate Password":
    st.subheader("🔑 Generate a Secure Password")
    length = st.slider("Select password length", min_value=4, max_value=50, value=12)
    if st.button("Generate", help="Click to generate a random secure password"):
        st.success(f"Generated Password: {generate_password(length)}")

elif choice == "Check Password Strength":
    st.subheader("🛡️ Check Password Strength")
    password = st.text_input("Enter password", type="password")
    if st.button("Check", help="Click to analyze the strength of the password"):
        st.info(f"Password Strength: {check_password_strength(password)}")

elif choice == "Store Password":
    st.subheader("💾 Store a Password")
    site = st.text_input("Enter site name")
    username = st.text_input("Enter username")
    password = st.text_input("Enter password", type="password")
    if st.button("Save", help="Click to securely store this password"):
        st.success(store_password(site, username, password))

elif choice == "Retrieve Password":
    st.subheader("🔍 Retrieve Stored Password")
    site = st.text_input("Enter site name")
    if st.button("Retrieve", help="Click to fetch stored credentials"):
        data = retrieve_password(site)
        if isinstance(data, dict):
            st.info(f"**Username:** {data['username']}\n\n**Password Hash:** {data['password']}")
        else:
            st.warning(data)
