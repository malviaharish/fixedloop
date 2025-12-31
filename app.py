import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Fixed Loop ACL Calculator",
    page_icon="🦵",
    layout="centered"
)

st.title("🦵 Fixed Loop Length Calculator – ACL Reconstruction")
st.markdown(
    """
    This app assists surgeons in calculating **fixed loop length**
    and identifying **graft–tunnel mismatch risks** during ACL reconstruction.
    """
)

st.divider()

# ================= INPUTS =================
st.header("🔢 Surgical Measurements (mm)")

col1, col2 = st.columns(2)

with col1:
    femoral_tunnel = st.number_input(
        "Femoral Tunnel Length (mm)", min_value=20, max_value=60, value=35
    )
    tibial_tunnel = st.number_input(
        "Tibial Tunnel Length (mm)", min_value=25, max_value=70, value=40
    )
    intra_articular = st.number_input(
        "Intra-articular Graft Length (mm)", min_value=15, max_value=40, value=25
    )

with col2:
    femoral_graft = st.number_input(
        "Desired Graft in Femoral Tunnel (mm)", min_value=15, max_value=30, value=20
    )
    tibial_graft = st.number_input(
        "Desired Graft in Tibial Tunnel (mm)", min_value=20, max_value=35, value=30
    )
    safety_margin = st.number_input(
        "Safety Margin (mm)", min_value=2, max_value=10, value=5
    )

st.divider()

st.header("🧬 Graft Information")
total_graft_length = st.number_input(
    "Total Graft Length Available (mm)", min_value=150, max_value=300, value=240
)

# ================= CALCULATIONS =================

recommended_loop = femoral_tunnel - femoral_graft - safety_margin
total_graft_required = femoral_graft + intra_articular + tibial_graft
graft_excess = total_graft_length - total_graft_required

# ================= RESULTS =================
st.divider()
st.header("📊 Calculation Results")

st.metric(
    label="Recommended Fixed Loop Length (mm)",
    value=f"{recommended_loop:.1f}"
)

st.metric(
    label="Total Graft Required (mm)",
    value=f"{total_graft_required:.1f}"
)

st.metric(
    label="Graft Excess / Deficit (mm)",
    value=f"{graft_excess:.1f}"
)

# ================= CLINICAL INTERPRETATION =================
st.divider()
st.header("⚠️ Clinical Interpretation")

# Loop Length Evaluation
if recommended_loop < 5:
    st.error(
        "❌ Fixed loop is TOO SHORT. Risk of inadequate femoral fixation."
    )
elif recommended_loop > 25:
    st.warning(
        "⚠️ Fixed loop is LONG. Risk of graft bottoming out."
    )
else:
    st.success(
        "✅ Fixed loop length is within the safe clinical range."
    )

# Graft Length Evaluation
if graft_excess < 0:
    st.error(
        "❌ Graft is SHORT. High risk of graft–tunnel mismatch."
    )
elif graft_excess > 15:
    st.warning(
        "⚠️ Excess graft length present. Check tibial overhang."
    )
else:
    st.success(
        "✅ Graft length is appropriate for tunnel configuration."
    )

# ================= CLINICAL NOTE =================
st.divider()
st.subheader("📝 Operative Note (Auto-Generated)")

operative_note = f"""
• Femoral tunnel length: {femoral_tunnel} mm  
• Tibial tunnel length: {tibial_tunnel} mm  
• Recommended fixed loop length: {recommended_loop:.1f} mm  
• Graft adequacy: {'Adequate' if graft_excess >= 0 else 'Inadequate'}  
"""

st.text_area("Copy into operative notes:", operative_note, height=150)

st.caption(
    "⚕️ Educational tool only. Final surgical decisions remain with the operating surgeon."
)
