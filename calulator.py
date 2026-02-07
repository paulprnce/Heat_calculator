import math
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Heat Exchanger Calculator",
    page_icon="🔥",
    layout="wide",
)
st.markdown("A clean and interactive tool to calculate **Heat Duty**, **Qmax**, and **Effectiveness** of a heat exchanger.")

st.sidebar.header("🔧 Input Parameters")

st.title("Heat Exchanger Effectiveness Calculator".upper())
st.sidebar.subheader("Hot Fluid")

m_hot = st.sidebar.number_input("Mass flow rate of hot fluid (kg/s)")
cp_hot = st.sidebar.number_input("Specific heat of hot fluid (kJ/kg·K)")
t1_hot = st.sidebar.number_input("Hot fluid inlet temperature (°C)")
t2_hot = st.sidebar.number_input("Hot fluid outlet temperature (°C)")

st.sidebar.subheader("Cold Fluid")
m_cold = st.sidebar.number_input("Mass flow rate of cold fluid (kg/s)", )
cp_cold = st.sidebar.number_input("Specific heat of cold fluid (kJ/kg·K)")
t1_cold = st.sidebar.number_input("Cold fluid inlet temperature (°C)")
t2_cold = st.sidebar.number_input("Cold fluid outlet temperature (°C)")

# FIX 1 → dropdown instead of number input
flow_type = st.sidebar.selectbox("Flow Type", ["parallel flow", "counter flow"])

if st.sidebar.button("Calculate"):

    # Heat duty
    q_hot = m_hot * cp_hot * (t1_hot - t2_hot)
    q_cold = m_cold * cp_cold * (t2_cold - t1_cold)

    # FIX 2 → use smaller heat duty
    q = min(abs(q_hot), abs(q_cold))

    # Temperature differences for LMTD
    if flow_type == "parallel flow":
        dt1 = t1_hot - t1_cold
        dt2 = t2_hot - t2_cold
    else:
        dt1 = t1_hot - t2_cold
        dt2 = t2_hot - t1_cold

    # LMTD (with protection)
    if dt1 == dt2:
        lmtd = dt1
    else:
        if dt1 * dt2 > 0:  # prevents log of negative number
            lmtd = (dt1 - dt2) / math.log(dt1 / dt2)
        else:
            lmtd = 0

    # FIX 5 → convert Q to W for UA
    ua = (q * 1000) / lmtd if lmtd != 0 else 0

    # Effectiveness
    ch = cp_hot * m_hot
    cc = cp_cold * m_cold
    cmin = min(ch, cc)
    qmax = cmin * (t1_hot - t1_cold)
    effectiveness = q / qmax if qmax != 0 else 0

    # ----- Output -----
    st.subheader("📊 Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background:#1a759f;padding:20px;border-radius:12px;color:white;">
            <h3 style="text-align:center;">Actual Heat Duty (Q)</h3>
            <h2 style="text-align:center;">{q:.2f} kW</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:#34a0a4;padding:20px;border-radius:12px;color:white;">
            <h3 style="text-align:center;">Maximum Heat Duty (Qmax)</h3>
            <h2 style="text-align:center;">{qmax:.2f} kW</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background:#168aad;padding:20px;border-radius:12px;color:white;">
            <h3 style="text-align:center;">Effectiveness</h3>
            <h2 style="text-align:center;">{effectiveness:.3f}</h2>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("Enter values in the sidebar and click **Calculate** to see results.")
