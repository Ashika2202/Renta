import streamlit as st
import time

# -------------- Init Session State -------------- #
if 'page' not in st.session_state:
    st.session_state.page = 'Intro'
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'cart' not in st.session_state:
    st.session_state.cart = []

# -------------- Shared UI -------------- #
def show_app_logo():
    st.markdown("""
        <h3 style='position: fixed; top: 10px; left: 10px; color: #ff3366; font-family: Pacifico, cursive;'>Renta</h3>
    """, unsafe_allow_html=True)

# -------------- Page 1: Intro (Auto goes to Login) -------------- #
def intro_page():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
        <style>
        @keyframes appear {
            from {opacity: 0; transform: translateX(-50px);}
            to {opacity: 1; transform: translateX(0);}
        }
        .title {
            animation: appear 2s ease-out forwards;
            font-family: 'Pacifico', cursive;
            text-align: center;
            padding-top: 200px;
            font-size: 80px;
            color: #ff3366;
            text-shadow: 3px 3px 6px #00000066;
        }
        .tagline {
            text-align: center;
            font-size: 24px;
            color: #777;
            font-style: italic;
            margin-top: -20px;
        }
        </style>
        <div class='title'>Renta</div>
        <div class='tagline'>renting yours.</div>
    """, unsafe_allow_html=True)
    time.sleep(4)
    st.session_state.page = "Login"
    st.rerun()

# -------------- Page 2: Login -------------- #
def login_page():
    show_app_logo()
    st.title("Login Page")
    name = st.text_input("Name")
    email = st.text_input("Email")
    location = st.text_input("Location")
    phone = st.text_input("Phone Number")
    occupation = st.text_input("Occupation")
    
    if st.button("Login", type="primary"):
        if name and email and location and phone and occupation:
            st.session_state.user_info = {
                "name": name,
                "email": email,
                "location": location,
                "phone": phone,
                "occupation": occupation
            }
            st.session_state.page = "Home"
            st.rerun()
        else:
            st.warning("Please fill all fields.")
    
    if st.button("Don't have an account? Sign up"):
        st.session_state.page = "Signup"
        st.rerun()

# -------------- Page 3: Signup -------------- #
def signup_page():
    show_app_logo()
    st.title("Signup Page")
    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Sign Up", type="primary"):
        if name and email:
            st.session_state.user_info = {
                "name": name,
                "email": email
            }
            st.session_state.page = "Home"
            st.rerun()
        else:
            st.warning("Please fill all fields.")

# -------------- Page 4: Home -------------- #
def home_page():
    show_app_logo()
    st.title("Home Page")
    st.button("Profile", on_click=lambda: st.session_state.update(page="Profile"))

    st.subheader("Available Appliances")
    appliances = [
        {"name": "Mini Fridge", "price": "₹500/mo", "img": "https://m.media-amazon.com/images/I/71jl4b5WaTL._AC_SL1500_.jpg"},
        {"name": "Washing Machine", "price": "₹700/mo", "img": "https://m.media-amazon.com/images/I/81AHzJfFzAL._AC_SL1500_.jpg"},
        {"name": "Mixer Grinder", "price": "₹300/mo", "img": "https://m.media-amazon.com/images/I/61FJtVQh8gL._SL1500_.jpg"},
        {"name": "Air Cooler", "price": "₹600/mo", "img": "https://m.media-amazon.com/images/I/71WZ0+8+VCL._SL1500_.jpg"},
    ]

    for item in appliances:
        st.image(item["img"], width=150)
        st.write(f"**{item['name']}** - {item['price']}")
        cols = st.columns(2)
        if cols[0].button(f"Buy {item['name']}"):
            st.session_state.selected_item = item
            st.session_state.page = "Checkout"
            st.rerun()
        if cols[1].button(f"Add to Cart {item['name']}"):
            st.session_state.cart.append(item)
            st.success("Added to cart")

# -------------- Page 5: Profile -------------- #
def profile_page():
    show_app_logo()
    st.title("Profile")
    user = st.session_state.user_info
    name = st.text_input("Name", user.get("name", ""))
    email = st.text_input("Email", user.get("email", ""))
    location = st.text_input("Location", user.get("location", ""))
    phone = st.text_input("Phone", user.get("phone", ""))
    occupation = st.text_input("Occupation", user.get("occupation", ""))

    if st.button("Save & Continue", type="primary"):
        st.session_state.user_info.update({"name": name, "email": email, "location": location, "phone": phone, "occupation": occupation})
        st.success("Profile updated!")
        time.sleep(1)
        st.session_state.page = "Home"
        st.rerun()

# -------------- Page 6: Checkout -------------- #
def checkout_page():
    show_app_logo()
    st.title("Checkout")
    user = st.session_state.user_info
    item = st.session_state.get("selected_item", {})

    st.write(f"Ordering: **{item.get('name', '')}** - {item.get('price', '')}")
    address = st.text_area("Edit Delivery Address", user.get("location", ""))

    payment = st.radio("Choose Payment Method", ["Cash on Delivery", "Online Payment"])
    if payment == "Online Payment":
        method = st.radio("Select", ["GPay", "PhonePe", "UPI", "Wallet"])

    if st.button("Place Order", type="primary"):
        st.success("\u2705 Order placed successfully!")
        time.sleep(2)
        st.session_state.page = "Home"
        st.rerun()

# -------------- Controller -------------- #
page = st.session_state.page
if page == "Intro":
    intro_page()
elif page == "Login":
    login_page()
elif page == "Signup":
    signup_page()
elif page == "Home":
    home_page()
elif page == "Profile":
    profile_page()
elif page == "Checkout":
    checkout_page()
