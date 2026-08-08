import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Hotel Business Dashboard",
    page_icon="🏨",
    layout="wide"
)

# Professional color theme — matches the notebook
HOTEL_COLORS = {"City Hotel": "#1f3a5f", "Resort Hotel": "#c98a2c"}

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("hotel_bookings_clean.csv")
    df["total_stay"] = df["stays_in_weekend_nights"] + df["stays_in_weekdays_nights"]

    bins = [0, 7, 30, 90, 180, 365, df["lead_time"].max() + 1]
    labels = ["0-7", "8-30", "31-90", "91-180", "181-365", "365+"]
    df["lead_time_bucket"] = pd.cut(df["lead_time"], bins=bins, labels=labels, include_lowest=True)

    month_order = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
    df["arrival_date_month"] = pd.Categorical(df["arrival_date_month"], categories=month_order, ordered=True)
    return df

df = load_data()

# ============================================================
# TITLE
# ============================================================
st.title("🏨 Hotel Business Dashboard")
st.markdown("### Understanding Booking & Cancellation Behaviour (2017–2019)")
st.markdown("---")

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.header("Filters")

hotel_filter = st.sidebar.multiselect(
    "Hotel Type",
    options=df["hotel"].unique(),
    default=list(df["hotel"].unique())
)

year_filter = st.sidebar.multiselect(
    "Arrival Year",
    options=sorted(df["arrival_date_year"].unique()),
    default=sorted(df["arrival_date_year"].unique())
)

df_filtered = df[(df["hotel"].isin(hotel_filter)) & (df["arrival_date_year"].isin(year_filter))]

if df_filtered.empty:
    st.warning("કૃપા કરી ઓછામાં ઓછું એક Hotel Type અને એક Year select કરો.")
    st.stop()

# ============================================================
# KPI CARDS
# ============================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings", f"{len(df_filtered):,}")
col2.metric("Cancellation Rate", f"{df_filtered['is_canceled'].mean()*100:.1f}%")
col3.metric("Avg Lead Time", f"{df_filtered['lead_time'].mean():.0f} days")
col4.metric("Avg Daily Rate", f"₹{df_filtered['adr'].mean():.0f}")

st.markdown("---")

# ============================================================
# QUESTION 1: HOTEL TYPE POPULARITY
# ============================================================
st.header("1️⃣ Which hotel type do customers book most often?")

c1, c2 = st.columns([1, 2])

with c1:
    hotel_counts = df_filtered["hotel"].value_counts().reset_index()
    hotel_counts.columns = ["hotel", "bookings"]
    fig_pie = px.pie(
        hotel_counts, names="hotel", values="bookings",
        color="hotel", color_discrete_map=HOTEL_COLORS,
        title="Share of Bookings by Hotel Type", hole=0.35
    )
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    monthly = df_filtered.groupby(["arrival_date_month", "hotel"], observed=False).size().reset_index(name="bookings")
    fig_month = px.line(
        monthly, x="arrival_date_month", y="bookings", color="hotel",
        color_discrete_map=HOTEL_COLORS, markers=True,
        title="Monthly Bookings by Hotel Type"
    )
    fig_month.update_layout(xaxis_title="Month", yaxis_title="Number of Bookings")
    st.plotly_chart(fig_month, use_container_width=True)

st.info("💡 **Insight:** City Hotel is booked more often overall, and both hotel types peak during summer months.")
st.markdown("---")

# ============================================================
# QUESTION 2: STAY DURATION VS CANCELLATION
# ============================================================
st.header("2️⃣ Does length of stay affect cancellation rate?")

c3, c4 = st.columns([1, 2])

with c3:
    cancel_rate = (df_filtered.groupby("hotel")["is_canceled"].mean() * 100).reset_index()
    cancel_rate.columns = ["hotel", "cancellation_rate"]
    fig_bar = px.bar(
        cancel_rate, x="hotel", y="cancellation_rate", color="hotel",
        color_discrete_map=HOTEL_COLORS, text_auto=".1f",
        title="Cancellation Rate by Hotel Type"
    )
    fig_bar.update_layout(yaxis_title="Cancellation Rate (%)", showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with c4:
    stay_cancel = (
        df_filtered[df_filtered["total_stay"] <= 14]
        .groupby(["total_stay", "hotel"])["is_canceled"]
        .mean().reset_index()
    )
    stay_cancel["is_canceled"] *= 100
    fig_stay = px.line(
        stay_cancel, x="total_stay", y="is_canceled", color="hotel",
        color_discrete_map=HOTEL_COLORS, markers=True,
        title="Cancellation Rate vs. Length of Stay"
    )
    fig_stay.update_layout(xaxis_title="Total Nights Stayed", yaxis_title="Cancellation Rate (%)")
    st.plotly_chart(fig_stay, use_container_width=True)

st.info("💡 **Insight:** Longer stays tend to have higher cancellation rates, and City Hotel is consistently higher than Resort Hotel.")
st.markdown("---")

# ============================================================
# QUESTION 3: LEAD TIME VS CANCELLATION
# ============================================================
st.header("3️⃣ Does lead time affect cancellation rate?")

lead_cancel = df_filtered.groupby(["lead_time_bucket", "hotel"], observed=False)["is_canceled"].mean().reset_index()
lead_cancel["is_canceled"] *= 100

fig_lead = px.line(
    lead_cancel, x="lead_time_bucket", y="is_canceled", color="hotel",
    color_discrete_map=HOTEL_COLORS, markers=True,
    title="Cancellation Rate vs. Lead Time"
)
fig_lead.update_layout(xaxis_title="Lead Time (days, bucketed)", yaxis_title="Cancellation Rate (%)")
st.plotly_chart(fig_lead, use_container_width=True)

st.info("💡 **Insight:** Cancellation rate rises sharply as lead time increases — far-ahead bookings (365+ days) cancel most often, especially for City Hotel.")
st.markdown("---")

# ============================================================
# RAW DATA (OPTIONAL)
# ============================================================
with st.expander("📄 View Filtered Raw Data"):
    st.dataframe(df_filtered.head(500))

st.caption("Data source: Hotel Bookings Dataset (2017–2019) · Dashboard built with Streamlit")
