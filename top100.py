import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ---------------------- Page Configuration ----------------------
st.set_page_config(page_title="📊 Largest Companies Dashboard", layout="wide")

# ---------------------- Custom Styling ----------------------
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
        }
        h1, h2, h3 {
            font-family: 'Segoe UI Semibold', sans-serif;
            color: #30475E;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 20px;
            padding: 1.5rem 2.5rem;
            margin-right: 15px;
            background-color: #e8f0fe;
            border-radius: 10px 10px 0 0;
            color: #1a237e !important;
            font-weight: 600;
        }
        .main {
            background-color: #f5f7fa;
        }
        .chart-box {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Title ----------------------
st.title("📈 Analysis of the Largest Companies by Revenue")
st.markdown("Explore insights into the top companies globally based on revenue, industry, growth, and location.")

# ---------------------- Data Loader ----------------------
@st.cache_data
def load_data(path_or_buffer):
    df = pd.read_csv(path_or_buffer)
    df['Revenue (USD millions)'] = df['Revenue (USD millions)'].str.replace(',', '', regex=True).astype(int)
    df['Revenue growth'] = df['Revenue growth'].str.replace('%', '', regex=True).astype(float)
    return df

uploaded_file = st.file_uploader("📤 Upload 'Largest_Companies.csv'", type=["csv"])
default_path = "Largest_Companies.csv"

if uploaded_file is not None:
    data = load_data(uploaded_file)
elif os.path.exists(default_path):
    st.info("📂 Using default `Largest_Companies.csv` from local directory.")
    data = load_data(default_path)
else:
    st.warning("⚠️ Please upload the `Largest_Companies.csv` file to begin.")
    st.stop()

# ✅ Auto-detect company name column
company_col = None
for col in data.columns:
    if "name" in col.lower() or "company" in col.lower():
        company_col = col
        break
if not company_col:
    st.error("❌ Company name column not found. Please make sure your file contains a column like 'Name' or 'Company Name'.")
    st.stop()

# ---------------------- Tabs ----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📉 Revenue vs Growth",
    "🏭 Industry Insight",
    "🌍 Headquarters"
])

# ---------------------- Tab 1: Overview ----------------------
with tab1:
    st.header("📊 Dataset Overview")
    st.markdown("The table below presents the first few records from the dataset, including company name, revenue, growth, industry, and headquarters.")
    st.dataframe(data.head(10), use_container_width=True)

    st.header("📋 Dataset Summary")
    st.markdown("This section provides basic statistical summaries of numerical columns in the dataset.")
    st.write(data.describe())

    industries = st.multiselect("🔎 Filter by Industry", options=data["Industry"].unique(), default=data["Industry"].unique())
    filtered_data = data[data["Industry"].isin(industries)]

    st.markdown("Filtered companies from the selected industries:")
    st.dataframe(filtered_data.head(10), use_container_width=True)

# ---------------------- Tab 2: Revenue vs Growth ----------------------
with tab2:
    st.header("📉 Revenue vs Revenue Growth (Top 10 Companies)")
    top_10 = data.head(10)

    with st.container():
        st.subheader("📐 Adjust Chart Dimensions")
        width = st.slider("Chart Width", 4, 12, 8, key="growth_width")
        height = st.slider("Chart Height", 3, 8, 5, key="growth_height")
        st.write(f"🧭 Chart size: **{width} x {height}** (inches)")

    with st.container():
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(width, height))
        sns.scatterplot(
            x='Revenue growth',
            y='Revenue (USD millions)',
            data=top_10,
            hue=company_col,
            palette='Set1',
            s=150,
            ax=ax1
        )
        ax1.set_title("Top 10 Companies: Revenue vs Growth", fontsize=14)
        ax1.set_xlabel("Revenue Growth (%)")
        ax1.set_ylabel("Revenue (USD millions)")
        st.pyplot(fig1)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    **Summary:**  
    This scatter plot compares company revenue with their growth rate.  
    It helps identify companies with high revenue but low growth (e.g. market leaders), and those with fast growth but modest revenue (e.g. rising disruptors).
    """)

# ---------------------- Tab 3: Industry Bar Chart ----------------------
with tab3:
    st.header("🏭 Revenue by Industry (Top 10 Companies)")

    with st.container():
        st.subheader("📐 Adjust Chart Dimensions")
        width2 = st.slider("Chart Width", 4, 12, 8, key="industry_width")
        height2 = st.slider("Chart Height", 3, 8, 5, key="industry_height")
        st.write(f"🧭 Chart size: **{width2} x {height2}** (inches)")

    with st.container():
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(width2, height2))
        sns.barplot(
            data=top_10,
            x='Industry',
            y='Revenue (USD millions)',
            palette='coolwarm',
            ax=ax2
        )
        ax2.set_title("Top 10 Companies - Revenue by Industry", fontsize=14)
        ax2.set_xlabel("Industry")
        ax2.set_ylabel("Revenue (USD millions)")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    **Summary:**  
    This bar chart highlights the industries that dominate in terms of revenue among the top 10 companies.  
    It emphasizes sectors like **Technology**, **Energy**, and **Retail** as the major revenue drivers globally.
    """)

# ---------------------- Tab 4: Headquarters Pie Chart ----------------------
with tab4:
    st.header("🌍 Headquarters Distribution (Top 5 Locations)")

    with st.container():
        st.subheader("📐 Adjust Chart Dimensions")
        width3 = st.slider("Chart Width", 4, 12, 6, key="hq_width")
        height3 = st.slider("Chart Height", 3, 8, 5, key="hq_height")
        st.write(f"🧭 Chart size: **{width3} x {height3}** (inches)")

    top_locations = data['Headquarters'].value_counts().head(5)

    with st.container():
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(width3, height3))
        ax3.pie(
            top_locations.values,
            labels=top_locations.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=sns.color_palette('pastel')
        )
        ax3.set_title("Top 5 Headquarters Locations", fontsize=14)
        st.pyplot(fig3)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    **Summary:**  
    This pie chart shows where the largest companies are headquartered.  
    It illustrates the dominance of major economic regions like **North America**, **East Asia**, and **Western Europe**.  
    Corporate clustering in financial hubs reflects access to infrastructure, innovation, and capital.
    """)

# ---------------------- Footer ----------------------
st.markdown("---")
st.markdown("📘 *Interactive dashboard built with Streamlit & Seaborn for corporate financial insights.*")
