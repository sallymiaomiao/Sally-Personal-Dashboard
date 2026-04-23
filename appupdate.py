import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sally Personal Dashboard", layout="wide")

st.title("📊 Sally Personal Dashboard")

# =========================
# FUNCTIONS
# =========================

def display_top_metrics():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Tasks Today", 8)

    with col2:
        st.metric("Completed", 5)

    with col3:
        st.metric("Open Items", 3)


def display_tasks():
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


def display_weekly_progress():
    st.subheader("Weekly Progress")

    df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Tasks Completed": [7, 6, 7, 0, 0],
    })

    st.bar_chart(df.set_index("Day"))
    st.progress(25)
    st.write("Current focus: Streamlit basics")


def load_inventory():
    inventory_data = {
        "Part Number": [
            "110113080", "5700455", "110115010", "110159900", "110097770",
            "100181480", "100213561", "170164106", "100145630", "110094090",
            "1174680", "110132760", "110214250", "110139750", "110130670",
            "110215141", "300000666", "120210211"
        ],
        "On Hand": [
            1, 1, 1, 2, 2,
            1, 1, 2, 1, 1,
            1, 2, 1, 1, 1,
            1, 1, 1
        ],
        "NEXT TOOL NUMBER": [
            "AFT", "STK", "STK", "0A1500K", "STK",
            "0A9388", "0A1502", "0A9255", "0A9256", "STK",
            "080747", "0A1499 & NEXT TOOL", "STK", "STK", "0A9254K",
            "0A1502", "STK", "0A1500K"
        ]
    }

    inventory_df = pd.DataFrame(inventory_data)

    inventory_df = inventory_df.rename(columns={
        "NEXT TOOL NUMBER": "Next Tool / Location"
    })

    inventory_df["Status"] = inventory_df["Next Tool / Location"].apply(
        lambda x: "In Stock" if x == "STK" else ("Aftermarket" if x == "AFT" else "Allocated")
    )

    return inventory_df


def highlight_status(val):
    if val == "In Stock":
        return "background-color: #d1fae5; color: black;"
    elif val == "Allocated":
        return "background-color: #fde68a; color: black;"
    elif val == "Aftermarket":
        return "background-color: #bfdbfe; color: black;"
    return ""


def highlight_on_hand(val):
    if val >= 2:
        return "background-color: #dcfce7; color: black; font-weight: bold;"
    else:
        return "background-color: #fee2e2; color: black; font-weight: bold;"


def display_inventory():
    st.subheader("Inventory - On Hand Balance")

    inventory_df = load_inventory()

    col1, col2 = st.columns([2, 1])

    with col1:
        search_part = st.text_input("Search Part Number")

    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "In Stock", "Allocated", "Aftermarket"]
        )

    filtered_df = inventory_df.copy()

    if search_part:
        filtered_df = filtered_df[
            filtered_df["Part Number"].astype(str).str.contains(search_part, case=False, na=False)
        ]

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    styled_df = (
        filtered_df.style
        .map(highlight_status, subset=["Status"])
        .map(highlight_on_hand, subset=["On Hand"])
        .set_properties(**{
            "text-align": "left",
            "font-size": "14px"
        })
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        height=500
    )


# =========================
# PAGE
# =========================

display_top_metrics()

st.divider()

display_tasks()

st.divider()

display_weekly_progress()

st.divider()

display_inventory()