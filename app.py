import streamlit as st
import pandas as pd
from PIL.ImageTransform import AffineTransform

st.set_page_config(page_title="Sally Personal Dashboard", layout="wide")

st.title("📊 Sally Personal Dashboard")

# top metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tasks Today", 8)

with col2:
    st.metric("Completed", 5)

with col3:
    st.metric("Open Items", 3)

st.divider()

# Daily Tasks
st.subheader("Daily Tasks")

tasks = [
    "Check Cycle Counts",
    "Expedite tools and AFT shortages",
    "Backlog Report",
    "Cut Tools",
    "Check open PEs for tools in FT",
    "Deliver Spares",
    "Check Large Cost Variance",
    "Return to Stock",
    "ON HAND BALANCE"
]

for t in tasks:
    st.checkbox(t)

st.divider()

# Weekly chart
st.subheader("Weekly Progress")

df = pd.DataFrame({
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Tasks Completed": [3, 4, 2, 5, 4]
})

st.bar_chart(df.set_index("Day"))

st.divider()

# Learning progress
st.subheader("Python Learning")

st.progress(25)

st.write("Current focus: Streamlit basics")

st.divider()

st.subheader("Inventory - On Hand Balance")

# Create sample inventory table
inventory_data = {
    "Part Number": [
        "110113080",
        "5700455",
        "110115010",
        "110159900",
        "110097770",
        "100181480",
        "110018390",
        "100213561",
        "170164106",
        "100145630",
        "110094090",
        "1174680",
        "110132760",
        "110143350",
        "110214250",
        "110139750",
        "110130670",
        "110215141",
        "300000666",
        "120210211"
    ],
    "On Hand": [
        1,
        1,
        1,
        2,
        2,
        1,
        2,
        1,
        2,
        1,
        1,
        1,
        2,
        1,
        1,
        1,
        1,
        1,
        1,
        1
    ],
    "TOOL NUMBER":[
        "AFT",
        "STK",
        "0A1499",
        "0A1500K",
        "STK",
        "0A9388",
        "0A9255",
        "0A1499",
        "0A9255",
        "0A1499",
        "STK",
        "080747",
        "0A1499 & NEXT TOOL",
        "0A9255",
        "STK",
        "STK",
        "0A9254K",
        "0A1499",
        "STK",
        "0A1500K",
    ]
}

inventory_df = pd.DataFrame(inventory_data)

st.data_editor(inventory_df)