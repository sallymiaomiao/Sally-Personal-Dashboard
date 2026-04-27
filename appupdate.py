import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sally Personal Dashboard", layout="wide")

# =========================
# CSS
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

h1 {
    text-align: center;
    font-size: 42px !important;
    font-weight: 700 !important;
    margin-bottom: 18px !important;
}

h3 {
    font-size: 22px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {
    font-size: 34px;
    font-weight: 700;
}

.stDataFrame {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Sally Personal Dashboard</h1>", unsafe_allow_html=True)

# =========================
# DATA
# =========================
def load_inventory():
    inventory_data = {
        "Part Number": [
            "110113080", "5700455", "110115010", "110159900", "110097770",
            "100181480", "100213561", "170164106", "100145630", "110094090",
            "1174680", "110132760", "110214250", "110139750", "110130670",
            "110215141", "300000666", "120210211","170167631", "100158620",
            "100185370"
        ],
        "On Hand": [
            1, 1, 1, 2, 2, 1, 1, 2, 1, 1,
            1, 2, 1, 1, 1, 1, 1, 1, 1, 1,
            1
        ],
        "Description": [
            "AFT", "STK", "STK", "0A1500K", "STK",
            "0A9388", "0A1502", "0A9255", "0A9412", "STK",
            "080747", "0A1499 & NEXT TOOL", "STK", "STK", "0A9254K",
            "0A1502", "STK", "0A1500K", "0A9412", "0A9412",
            "0A9412"
        ]
    }

    df = pd.DataFrame(inventory_data)

    df["Status"] = df["Description"].apply(
        lambda x: "In Stock" if x == "STK" else ("Aftermarket" if x == "AFT" else "Allocated")
    )

    return df


# =========================
# STYLE
# =========================
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
    return "background-color: #fee2e2; color: black; font-weight: bold;"


# =========================
# SECTIONS
# =========================
def display_daily_metrics():
    st.subheader("Daily Metrics")

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.metric("Tasks Today", 9)

    with c2:
        with st.container(border=True):
            st.metric("Completed", 8)

    with c3:
        with st.container(border=True):
            st.metric("Open Items", 1)


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


def display_weekly_kpi():
    st.subheader("Weekly KPI Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        with st.container(border=True):
            st.metric("Weekly Tasks Done", 28)

    with c2:
        with st.container(border=True):
            st.metric("Open Items", 6)

    with c3:
        with st.container(border=True):
            st.metric("Shortages", 4)

    with c4:
        with st.container(border=True):
            st.metric("Overdue Items", 2)

    kpi_df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Tasks Completed": [8, 6, 8, 4, 3],
        "Shortages Closed": [1, 2, 1, 0, 1]
    })

    st.bar_chart(kpi_df.set_index("Day"), height=260)


def display_weekly_progress():
    st.subheader("Weekly Progress")

    df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Tasks Completed": [8, 6, 7, 5, 8],
    })

    st.bar_chart(df.set_index("Day"), height=240)

    progress_value = 25
    st.progress(progress_value)
    st.caption(f"Current focus: Streamlit basics    {progress_value}%")


def create_inventory_pie_chart(status_counts):
    fig, ax = plt.subplots(figsize=(2.2,2.2), dpi=120)

    colors = ["#66bd63", "#ffd54f", "#1565c0", "#ef5350"]

    ax.pie(
        status_counts.values,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[:len(status_counts)],
        wedgeprops={"width": 0.45, "edgecolor": "white"},
        textprops={"fontsize": 8}
    )

    ax.text(
        0,
        0,
        f"Total Items\n{status_counts.sum()}",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold"
    )

    ax.axis("equal")
    plt.tight_layout()
    return fig


def display_inventory():
    inventory_df = load_inventory()

    left, right = st.columns([1.6, 0.6])

    with left:
        with st.container(border=True):
            st.subheader("Inventory - On Hand Balance")

            f1, f2, f3 = st.columns([1.3, 1, 1])

            with f1:
                search_part = st.text_input("Search Part Number", placeholder="Enter part number...")

            with f2:
                search_tool = st.text_input("Search Tool Number", placeholder="Enter tool number...")

            with f3:
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "In Stock", "Allocated", "Aftermarket"]
                )

            filtered_df = inventory_df.copy()

            if search_part:
                filtered_df = filtered_df[
                    filtered_df["Part Number"].astype(str).str.contains(search_part, case=False, na=False)
                ]

            if search_tool:
                filtered_df = filtered_df[
                    filtered_df["Description"].astype(str).str.contains(search_tool, case=False, na=False)
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
                height=260,
                hide_index=True
            )

            st.caption(f"Showing {len(filtered_df)} of {len(inventory_df)} items")

    with right:
        with st.container(border=True):
            st.subheader("Inventory Status Distribution")

            status_counts = inventory_df["Status"].value_counts()

            fig = create_inventory_pie_chart(status_counts)

            center_col = st.columns([1, 2, 1])[1]

            with center_col:
                st.pyplot(fig)

            percent_df = pd.DataFrame({
                "Status": status_counts.index,
                "Count": status_counts.values,
                "Percentage": (status_counts / status_counts.sum() * 100).round(1).astype(str) + "%"
            })

            st.dataframe(percent_df, use_container_width=True, hide_index=True)


# =========================
# PAGE LAYOUT
# =========================

top_left, top_right = st.columns([1, 1.1])

with top_left:
    with st.container(border=True):
        display_daily_metrics()

    with st.container(border=True):
        display_tasks()

with top_right:
    with st.container(border=True):
        display_weekly_kpi()

    with st.container(border=True):
        display_weekly_progress()

display_inventory()