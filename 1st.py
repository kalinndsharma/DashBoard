import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(page_title="Attendance Dashboard", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: white;
}
h1 {
    color: black !important;
    text-align: center;
}
.message {
    font-size: 16px;
    font-weight: 700;
    color: black;
    text-align: center;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Student Attendance Dashboard")

# ---------------- DATA ----------------
data = {
    "Subject": ["CSET301", "CSET302", "CSET303"],
    "Attended": [15, 20, 25],
    "Total": [35, 30, 25]
}

df = pd.DataFrame(data)
df["Attendance %"] = (df["Attended"] / df["Total"]) * 100

# ---------------- RINGS ----------------
cols = st.columns(3)

for i in range(len(df)):
    percentage = df["Attendance %"][i]
    subject = df["Subject"][i]

    # ---- COLOR & MESSAGE LOGIC ----
    if percentage < 50:
        color = "red"
        message = "LOW ATTENDANCE - RISK ZONE"

    elif percentage <= 75:
        color = "blue"
        message = "REQUIREMENT NOT MET - NEED MORE ATTENDANCE"

    else:
        color = "green"
        message = "REQUIREMENT COMPLETED"

    # ---- DISPLAY INSIDE COLUMN ----
    with cols[i]:

        fig, ax = plt.subplots(figsize=(3,3))
        values = [percentage, 100 - percentage]

        ax.pie(
            values,
            startangle=90,
            colors=[color, "#E0E0E0"],
            wedgeprops={"width": 0.25}
        )

        # Center percentage text
        ax.text(0, 0, f"{percentage:.1f}%",
                ha='center', va='center',
                fontsize=16, fontweight='bold', color='black')

        ax.set_title(f"{subject}", fontsize=12)
        ax.axis("equal")

        st.pyplot(fig)

        # ---- BLACK MESSAGE ----
        st.markdown(f"<div class='message'>{message}</div>", unsafe_allow_html=True)

# ---------------- OVERALL ATTENDANCE ----------------
overall = (df["Attended"].sum() / df["Total"].sum()) * 100

st.markdown(f"""
<div style="
    text-align:center;
    font-size:34px;
    font-weight:900;
    color:black;
    margin-top:40px;">
    OVERALL ATTENDANCE
</div>

<div style="
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:black;">
    {overall:.2f}%
</div>
""", unsafe_allow_html=True)