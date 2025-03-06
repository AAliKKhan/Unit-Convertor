import streamlit as st
import math
import pandas as pd


st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered")

# Custom CSS for button styling and futuristic look
st.markdown(
    '''
    <style>
    .stButton>button {
      background-color: #4CAF50;
      color: white;
      border: none;
      padding: 10px 20px;
      text-align: center;
      font-size: 16px;
      margin: 4px 2px;
      border-radius: 12px;
      transition-duration: 0.4s;
      cursor: pointer;
    }
    .stButton>button:hover {
      background-color: white; 
      color: black;
      border: 2px solid #4CAF50;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Define unit categories and conversion factors
unit_categories = {
    "Length": {
        "Meter": 1,
        "Kilometer": 0.001,
        "Centimeter": 100,
        "Millimeter": 1000,
        "Mile": 0.000621371,
        "Yard": 1.09361,
        "Foot": 3.28084,
        "Inch": 39.3701
    },
    "Weight": {
        "Kilogram": 1,
        "Gram": 1000,
        "Milligram": 1000000,
        "Pound": 2.20462,
        "Ounce": 35.274
    },
    "Temperature": "Special",
    "Time": {
        "Second": 1,
        "Minute": 1/60,
        "Hour": 1/3600,
        "Day": 1/86400
    },
    "Speed": {
        "Meter per second": 1,
        "Kilometer per hour": 3.6,
        "Mile per hour": 2.23694,
        "Foot per second": 3.28084
    }
}

def convert_units(category, from_unit, to_unit, value):
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            formula = "(°C × 9/5) + 32"
            result = (value * 9/5) + 32
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            formula = "(°F - 32) × 5/9"
            result = (value - 32) * 5/9
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            formula = "°C + 273.15"
            result = value + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            formula = "K - 273.15"
            result = value - 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            formula = "(°F - 32) × 5/9 + 273.15"
            result = (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            formula = "(K - 273.15) × 9/5 + 32"
            result = (value - 273.15) * 9/5 + 32
        else:
            formula = "N/A"
            result = value
    else:
        factor_from = unit_categories[category][from_unit]
        factor_to = unit_categories[category][to_unit]
        formula = f"(value / {factor_from}) × {factor_to}"
        base_value = value / factor_from
        result = base_value * factor_to
    
    return result, formula

# Initialize session state for conversion history
if "history" not in st.session_state:
    st.session_state.history = []

# Streamlit UI
st.title("Unit Converter")
st.write("Convert units effortlessly with a sleek, modern interface!")

# Sidebar for additional controls and conversion history
st.sidebar.header("Options")
show_history = st.sidebar.checkbox("Show Conversion History", value=True)

# Select unit category with tooltip
category = st.selectbox("Select Category", list(unit_categories.keys()),
                        help="Choose the category of units you want to convert.")

# Select units based on category
if category == "Temperature":
    units = ["Celsius", "Fahrenheit", "Kelvin"]
else:
    units = list(unit_categories[category].keys())

col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From Unit", units, help="Select the unit you are converting from.")
with col2:
    to_unit = st.selectbox("To Unit", units, help="Select the unit you want to convert to.")

# Input value with validation: allow negatives only for Temperature
if category == "Temperature":
    value = st.number_input("Enter Value", format="%.4f", step=0.1,
                            help="Enter the value you wish to convert (temperatures can be negative).")
else:
    value = st.number_input("Enter Value", format="%.4f", step=0.1, min_value=0.0,
                            help="Enter a non-negative value for conversion.")

# Convert button with futuristic animation
if st.button("Convert ⚡"):
    if from_unit == to_unit:
        st.warning("⚠️ Please select different units for conversion!")
    else:
        with st.spinner("Processing... 🚀"):
            result, formula = convert_units(category, from_unit, to_unit, value)
            st.success(f"✅ {value} {from_unit} = {result:.4f} {to_unit}")
            st.info(f"📌 Conversion Formula: {formula}")
            # Append conversion record to history
            st.session_state.history.append({
                "Category": category,
                "From Unit": from_unit,
                "To Unit": to_unit,
                "Input Value": value,
                "Result": result,
                "Formula": formula
            })
            # Display a temporary notification
            st.info("Conversion Successful!")
            
            # Copy-to-clipboard functionality using HTML & JavaScript
            copy_text = f"{value} {from_unit} = {result:.4f} {to_unit}\\nFormula: {formula}"
            copy_button = f'''<button onclick="navigator.clipboard.writeText('{copy_text}')">Copy Result to Clipboard</button>'''
            st.markdown(copy_button, unsafe_allow_html=True)

# Conversion History Section in Sidebar
if show_history:
    st.sidebar.header("Conversion History")
    if st.session_state.history:
        for idx, record in enumerate(st.session_state.history[::-1], 1):
            st.sidebar.write(f"**{idx}. {record['Input Value']} {record['From Unit']}** in {record['Category']} = **{record['Result']:.4f} {record['To Unit']}**")
            st.sidebar.caption(f"Formula: {record['Formula']}")
    else:
        st.sidebar.write("No conversion history yet.")

    # Download history as CSV
    if st.session_state.history:
        df_history = pd.DataFrame(st.session_state.history)
        st.sidebar.download_button("Download History as CSV", df_history.to_csv(index=False), "conversion_history.csv", "text/csv")
    
    if st.sidebar.button("Clear History"):
        st.session_state.history = []
        st.sidebar.success("History cleared!")

# Footer with additional info and conversion formulas reference
st.markdown("---")
st.markdown("🔹 *Precision, speed, and a sleek experience at your fingertips!* 🌟")
st.markdown("""\
**Conversion Formulas:**  
- Temperature conversions follow standard formulas (e.g., (°C × 9/5) + 32).  
- For other categories, the conversion is based on defined factors: (input value / factor of from_unit) × factor of to_unit.  
""")
