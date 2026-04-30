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
            "0A9412", "STK", "STK", "0A1500K", "STK",
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

def display_task_metrics():

    st.subheader("Task Metrics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Tasks Today", 9)

    with c2:
        st.metric("Completed", 8)

    with c3:
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

    st.bar_chart(kpi_df.set_index("Day"), height=290)

def display_weekly_progress():
    st.subheader("Weekly Progress")

    df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Tasks Completed": [8, 7, 6, 5, 9],
    })

    st.bar_chart(df.set_index("Day"), height=290)

    progress_value = 25
    st.progress(progress_value)
    st.caption(f"Current focus: Streamlit basics    {progress_value}%")

#monthly performance
def display_monthly_metrics():

    st.subheader("Monthly KPIs")

    c1, c2, c3 = st.columns(3)

    with c1:
        system_otd = 98.7
        color = "🔴" if system_otd < 99 else "🟢"

        with st.container(border=True):
            st.metric("System OTD", f"{system_otd}% {color}")
            st.caption("Target: >99%")

    with c2:
        so_otd = 96.1
        color = "🔴" if so_otd < 95 else "🟢"

        with st.container(border=True):
            st.metric("SO OTD", f"{so_otd}% {color}")
            st.caption("Target: ≥95%")

    with c3:
        variance_explained = 92
        color = "🔴" if variance_explained < 100 else "🟢"

        with st.container(border=True):
            st.metric("WO Variance Explained", f"{variance_explained}% {color}")
            st.caption("Target: All variances explained")

    c4, c5 = st.columns(2)

    with c4:
        mrb_cycle_time = 5.6
        color = "🔴" if mrb_cycle_time >= 7 else "🟢"

        with st.container(border=True):
            st.metric("MRB Cycle Time", f"{mrb_cycle_time} Days {color}")
            st.caption("Target: <7 days")

    with c5:
        wo_45 = 182
        color = "🔴" if wo_45 >= 200 else "🟢"

        with st.container(border=True):
            st.metric("WO >45 Days", f"{wo_45} {color}")
            st.caption("Target: <200")

def display_yearly_metrics():

    st.subheader("Yearly Metrics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Physical Inventory Accuracy", "99.6% 🟢")

    with c2:
        st.metric("Training Progress", "2 Courses")

    with c3:
        st.metric("Annual Goal Progress", "65%")

def display_inventory():
    inventory_df = load_inventory()

    # =========================
    # Inventory Table
    # =========================
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

        # =========================
        # Inventory Pie Chart
        # =========================
        with st.container(border=True):
            st.subheader("Inventory Status Distribution")

            status_counts = inventory_df["Status"].value_counts()

            fig = create_inventory_pie_chart(status_counts)

            percent_df = pd.DataFrame({
                "Status": status_counts.index,
                "Count": status_counts.values,
                "Percentage": (
                                      status_counts / status_counts.sum() * 100
                              ).round(1).astype(str) + "%"
            })

            pie_col, table_col = st.columns([0.8, 1.0])

            with pie_col:
                st.pyplot(fig, use_container_width=True)

            with table_col:
                st.dataframe(
                    percent_df,
                    use_container_width=True,
                    hide_index=True,
                    height=120
                )

def create_inventory_pie_chart(status_counts):

    fig, ax = plt.subplots(figsize=(1.3, 1.3), dpi=220)

    colors = ["#66bd63", "#ffd54f", "#1565c0", "#ef5350"]

    ax.pie(
        status_counts.values,
        labels=None,
        autopct="%1.1f%%",
        startangle=80,
        colors=colors[:len(status_counts)],

        wedgeprops={
            "width": 0.6,   # 中间白色减少
            "edgecolor": "white"
        },

        textprops={
            "fontsize": 5,
            "weight": "bold"
        }
    )

    ax.text(
        0,
        0,
        f"Total Items\n{status_counts.sum()}",
        ha="center",
        va="center",
        fontsize=5,
        fontweight="bold"
    )

    ax.axis("equal")

    # ⭐ 最关键：去掉外围空白
    plt.tight_layout(pad=0)

    return fig

# =========================
# PAGE LAYOUT
# =========================

left_col, right_col = st.columns([1, 1.15])

# 左边：Daily + Weekly
with left_col:

    st.subheader("Daily Operations")

    with st.container(border=True):
        display_daily_metrics()

    with st.container(border=True):
        display_tasks()

    # 不要divider

    st.subheader("Weekly Execution")

    with st.container(border=True):
        display_weekly_kpi()

    with st.container(border=True):
        display_weekly_progress()


# 右边：Monthly + Yearly + Inventory
with right_col:

    st.subheader("Monthly Performance")

    with st.container(border=True):
        display_monthly_metrics()

#不要divider

    st.subheader("Yearly Goals")

    with st.container(border=True):
        display_yearly_metrics()

        # 只加一点点高度（最推荐）
        st.markdown(
            "<div style='height:0px;'></div>",
            unsafe_allow_html=True
        )

    # 不要divider

    # Inventory

    st.subheader("Inventory Management")

    with st.container(border=True):
        display_inventory()