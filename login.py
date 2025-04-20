import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import random

# === Fake user database === #
USER_CREDENTIALS = {
    "tharun": "bala123",
    "admin": "admin123",
    "user1": "password1"
}

# === Tamil Nadu-specific vehicle info === #
def generate_vehicle_info():
    models = ["Hyundai i20", "Tata Nexon", "Maruti Baleno", "Mahindra XUV300", "Honda City"]
    colors = ["Red", "Blue", "Black", "White", "Grey"]
    rc_numbers = ["TN01AB1234", "TN05CD5678", "TN10EF9101", "TN15GH3456", "TN23JK7890"]
    license_numbers = ["TN10X123456", "TN01A987654", "TN12V987654", "TN07M123456", "TN08B678912"]
    insurances = ["Valid till 2026", "Expired", "Valid till 2025", "Valid till 2024", "Valid till 2027"]

    tamil_names_male = ["Arun Kumar", "Karthik Raja", "Saravanan", "Dinesh Kumar", "Vignesh", "Prakash", "Ravi Shankar"]
    tamil_names_female = ["Divya", "Meena Kumari", "Anitha", "Kavya", "Revathi", "Subha", "Nandhini"]
    all_names = tamil_names_male + tamil_names_female

    addresses = [
        "12 Gandhi Street, Chennai", 
        "45 Anna Nagar, Coimbatore", 
        "78 MG Road, Madurai", 
        "90 Trichy Main Road, Trichy", 
        "23 Mambalam West, Salem"
    ]
    accidents = ["None", "2 accidents", "1 accident", "No major accidents", "Had a minor accident"]
    fines = ["No fines", "₹200 for speeding", "₹500 for illegal parking", "₹100 for expired insurance", "₹300 for violation"]

    return {
        "model": random.choice(models),
        "color": random.choice(colors),
        "rc_number": random.choice(rc_numbers),
        "license": random.choice(license_numbers),
        "insurance": random.choice(insurances),
        "owner": random.choice(all_names),
        "address": random.choice(addresses),
        "accidents": random.choice(accidents),
        "fine": random.choice(fines)
    }

# === OCR Setup === #
reader = easyocr.Reader(['en'])

# === Login Section === #
def login():
    st.title("🔐 Login to use the NPR App")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

# === Main App after login === #
def npr_app():
    st.title("📸 Live NPR App with EasyOCR")
    st.write("Capture an image using the cam and extract the Info with NPR")

    img_file_buffer = st.camera_input("Capture Image")

    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        image_np = np.array(image)

        st.image(image, caption="Captured Image", use_column_width=True)

        st.write("🔍 Extracting text from image...")
        results = reader.readtext(image_np)

        st.subheader("Extracted Text:")
        extracted_text = "\n".join([res[1] for res in results])
        st.text_area("OCR Result:", extracted_text, height=200)

        st.download_button("📥 Download Text", extracted_text, file_name="extracted_text.txt")

        st.subheader("Tamil Nadu Vehicle Information:")
        vehicle_info = generate_vehicle_info()

        st.write(f"🚗 **Vehicle Model:** {vehicle_info['model']}")
        st.write(f"🎨 **Color:** {vehicle_info['color']}")
        st.write(f"📄 **RC Number:** {vehicle_info['rc_number']}")
        st.write(f"🛡️ **License Insurance:** {vehicle_info['insurance']}")
        st.write(f"👤 **Owner Name:** {vehicle_info['owner']}")
        st.write(f"🏠 **Owner Address:** {vehicle_info['address']}")
        st.write(f"🚑 **Accidents History:** {vehicle_info['accidents']}")
        st.write(f"💸 **Case Fine:** {vehicle_info['fine']}")

# === App Controller === #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    npr_app()
else:
    login()
