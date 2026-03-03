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
    font-size: 14px;
    font-weight: 700;
    color: black;
    text-align: center;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

st.title("Student Attendance Dashboard")

# ---------------- DATA ----------------
data = {
    "Subject": ["CSET301", "CSET302", "CSET303", "CSET304", "CSET305"],
    "Attended": [15, 20, 25, 30, 42],
    "Total": [35, 30, 25, 30, 50]
}

df = pd.DataFrame(data)

# Calculate attendance %
df["Attendance %"] = (df["Attended"] / df["Total"]) * 100

# Prevent negative / >100 values
df["Attendance %"] = df["Attendance %"].clip(0, 100)

# ---------------- SUBJECT WISE RINGS ----------------
st.markdown("<h2 style='color:black;'>Subject-wise Attendance</h2>", unsafe_allow_html=True)

cols = st.columns(len(df))

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

    with cols[i]:

        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        values = [percentage, 100 - percentage]

        # Make blue ring thinner
        if color == "blue":
            ring_width = 0.18
        else:
            ring_width = 0.30

        ax.pie(
            values,
            startangle=90,
            colors=[color, "#E0E0E0"],
            wedgeprops={"width": ring_width}
        )

        ax.text(0, 0, f"{percentage:.1f}%",
                ha='center', va='center',
                fontsize=14, fontweight='bold', color='black')

        ax.set_title(subject, fontsize=11)
        ax.axis("equal")

        st.pyplot(fig)

        st.markdown(f"<div class='message'>{message}</div>", unsafe_allow_html=True)

# ---------------- TOTAL ATTENDANCE ----------------
st.markdown(
    "<h2 style='color:black; text-align:center;'>Total Attendance</h2>",
    unsafe_allow_html=True
)

overall = (df["Attended"].sum() / df["Total"].sum()) * 100
overall = min(max(overall, 0), 100)

fig2, ax2 = plt.subplots(figsize=(3, 3))
values2 = [overall, 100 - overall]

# Overall color logic
if overall < 50:
    overall_color = "red"
elif overall <= 75:
    overall_color = "blue"
else:
    overall_color = "green"

ax2.pie(
    values2,
    startangle=90,
    colors=[overall_color, "#E0E0E0"],
    wedgeprops={"width": 0.35}
)

ax2.text(0, 0, f"{overall:.1f}%",
         ha='center', va='center',
         fontsize=18, fontweight='bold', color='black')

ax2.axis("equal")

st.pyplot(fig2)

# Progress bar
st.progress(overall / 100)

if overall < 75:
    st.warning("You need more attendance to reach safe zone (75%).")
else:
    st.success("Good job! You are in safe attendance zone.")