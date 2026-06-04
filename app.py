import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# ------------------------
# PAGE CONFIG
# ------------------------

st.set_page_config(
    page_title="Hepatitis Analytics Dashboard",
    page_icon="🩺",
    layout="wide"
)

# ------------------------
# DARK THEME
# ------------------------

st.markdown("""
<style>

.stApp{
    background-color:#0F1117;
    color:white;
}
            section[data-testid="stSidebar"]{
    background-color:#161b28;
}
         table {
    width:100%;
    border-collapse:collapse !important;
}

table, th, td {
    border:1px solid #2d3446 !important;
}

th {
    background:#24304d !important;
    color:white !important;
    padding:10px;
}

td {
    background:#1a1f2e !important;
    color:white !important;
    padding:8px;
}
            tr:hover td{
    background:#222b42;
}

.metric-card{
    background:#1E1E2E;
    padding:20px;
    border-radius:15px;
}
            

h1,h2,h3{
    color:white;
}
            section[data-testid="stSidebar"] *{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)


# ------------------------
# LOAD DATA
# ------------------------

df = pd.read_excel("hepatitis_patient_records_corrected.xlsx")

df = df.replace("?", pd.NA)

# ------------------------
# SIDEBAR
# ------------------------
st.sidebar.markdown("""
# 🩺 Dashboard Controls
---
""")

age_range = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (
        int(df["Age"].min()),
        int(df["Age"].max())
    )
)

filtered_df = df[
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1])
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="
background:#1a2747;
padding:18px;
border-radius:12px;
color:white;
font-size:20px;
font-weight:600;
line-height:2;
">

📊 Records: {len(df)}<br>

🧑 Ages: {df['Age'].min()} - {df['Age'].max()}<br>

📈 Features: {len(df.columns)}<br>

🎯 Version: 1.0

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# ------------------------
# KPI VALUES
# ------------------------

total_patients = len(filtered_df)

live_patients = len(
    filtered_df[filtered_df["Class"] == 2]
)

dead_patients = len(
    filtered_df[filtered_df["Class"] == 1]
)

survival_rate = (
    live_patients / total_patients
) * 100
st.sidebar.markdown(f"""
<div style="
background:#26301f;
padding:18px;
border-radius:12px;
color:white;
font-size:20px;
font-weight:600;
line-height:2;
">

🟢 Live Patients: {live_patients}<br>

🔴 Dead Patients: {dead_patients}<br>

📉 Survival Rate: {survival_rate:.1f}%

</div>
""", unsafe_allow_html=True)
# ------------------------
# TITLE
# ------------------------

st.title("🩺 Hepatitis Analytics Dashboard")
st.caption(
    "Interactive Exploratory Data Analysis Dashboard for Hepatitis Patient Dataset"
)
# ------------------------
# KPI CARDS
# ------------------------
st.markdown("""
<style>

[data-testid="stMetric"]{
    background-color:#1a1f2e;
    border:1px solid #2d3446;
    padding:20px;
    border-radius:15px;
    text-align:center;
}

[data-testid="stMetricValue"]{
    color:#ffffff !important;
    font-size:52px !important;
    font-weight:700 !important;
    line-height:1.2 !important;
}

[data-testid="stMetricLabel"]{
    color:#9aa4c7 !important;
    font-size:18px !important;
    font-weight:600 !important;
}

</style>
""", unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Patients",
    total_patients
)

c2.metric(
    "Live Patients",
    live_patients
)

c3.metric(
    "Dead Patients",
    dead_patients
)

c4.metric(
    "Survival Rate",
    f"{survival_rate:.1f}%"
)

st.markdown("---")

# ------------------------
# CHARTS
# ------------------------

left,right = st.columns(2)

with left:

    fig = px.histogram(
        filtered_df,
        x="Age",
        title="Age Distribution",
        nbins=15
    )
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font_color="white"
)
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font=dict(color="white"),
    title_font=dict(color="white", size=20),
    xaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    )
)
    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    outcome = filtered_df["Class"].value_counts()

    fig = px.pie(
        values=outcome.values,
        names=["Live","Dead"],
        hole=0.6,
        title="Patient Outcome"
    )
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font_color="white"
)
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font=dict(color="white"),
    title_font=dict(color="white", size=20),
    xaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    )
)
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font=dict(color="white"),
    title_font=dict(color="white", size=20),
    xaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    )
)
    

    st.plotly_chart(
        fig,
        width="stretch"
    )
    
st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    temp_df = filtered_df.copy()

    temp_df["Bilirubin"] = pd.to_numeric(
        temp_df["Bilirubin"],
        errors="coerce"
    )

    fig = px.scatter(
        temp_df,
        x="Age",
        y="Bilirubin",
        color="Class",
        title="Age vs Bilirubin"
    )
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font_color="white"
)
    fig.update_layout(
    height=500
)
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font=dict(color="white"),
    title_font=dict(color="white", size=20),
    xaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    )
)
    st.plotly_chart(
        fig,
        width="stretch"
    )

with col2:

    temp_df = filtered_df.copy()

    temp_df["Albumin"] = pd.to_numeric(
        temp_df["Albumin"],
        errors="coerce"
    )

    fig = px.box(
        temp_df,
        y="Albumin",
        color="Class",
        title="Albumin Distribution"
    )
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font_color="white",
    height=650
)
    fig.update_layout(
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font=dict(color="white"),
    title_font=dict(color="white", size=20),
    xaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    )
)
    fig.update_layout(
    height=500
)

    st.plotly_chart(
        fig,
        width="stretch"
    )
    st.markdown("---")

summary1, summary2, summary3, summary4 = st.columns(4)

ascites_cases = len(filtered_df[filtered_df["Ascites"].astype(str) == "2"])
varices_cases = len(filtered_df[filtered_df["Varices"].astype(str) == "2"])
histology_positive = len(filtered_df[filtered_df["Histology"] == 1])

albumin_avg = pd.to_numeric(
    filtered_df["Albumin"],
    errors="coerce"
).mean()

summary1.metric(
    "Ascites Cases",
    ascites_cases
)

summary2.metric(
    "Varices Cases",
    varices_cases
)

summary3.metric(
    "Histology Positive",
    histology_positive
)

summary4.metric(
    "Avg Albumin",
    f"{albumin_avg:.2f}"
)
st.markdown("---")

st.subheader("Correlation Heatmap")

numeric_df = filtered_df.copy()

for col in numeric_df.columns:
    numeric_df[col] = pd.to_numeric(
        numeric_df[col],
        errors="coerce"
    )

corr_matrix = numeric_df.corr(numeric_only=True)

fig = px.imshow(
    corr_matrix,
    text_auto=".3f",
    aspect="auto",
    color_continuous_scale="Blues"
)
fig.update_traces(
    textfont=dict(size=6, color="white")
)
fig.update_layout(
    title={
        "text":"Feature Correlation Matrix",
        "x":0.4,
        "font":{"size":24,"color":"white"}
    },
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font=dict(color="white"),
    height=650,
    coloraxis_colorbar=dict(
        tickfont=dict(color="White")
    )
)


fig.update_layout(
    height=650
)
st.plotly_chart(
    fig,
    width="stretch"
)
st.markdown("""
<div style="
background:#1a1f2e;
padding:25px;
border-radius:15px;
border-left:5px solid #22c55e;
color:white;
">

<h3>🔍 Key Findings</h3>

<ul>
<li>Survival Rate = 79.4%</li>
<li>Average Albumin = 3.82</li>
<li>Majority patients belong to age 30–50</li>
<li>Ascites and Varices are highly prevalent</li>
<li>Correlation analysis reveals feature relationships</li>
</ul>

</div>
""", unsafe_allow_html=True)
# ------------------------
# DATA PREVIEW
# ------------------------

# st.markdown("---")

# with st.expander("View Dataset"):

#     st.dataframe(
#         filtered_df.head(20),
#         width="stretch"
#     )
with st.expander("📋 View Dataset Preview", expanded=False):

    st.markdown("### Dataset Preview")

    html_table = (
    filtered_df.head(10)
    .fillna("No")
    .to_html(index=False)
)

    st.markdown(f"""
    <div style="
        background:#1a1f2e;
        padding:20px;
        border-radius:15px;
        border:1px solid #2d3446;
        overflow-x:auto;
    ">
    {html_table}
    </div>
    """, unsafe_allow_html=True)

st.markdown(
"""
<div style='text-align:center;color:gray'>
Developed by AMAN RIZWAN | Hepatitis Aanlytics Dashboard | 2026
</div>
""",
unsafe_allow_html=True
)