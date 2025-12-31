import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Fixed Loop ACL Calculator",
    page_icon="🦵",
    layout="centered"
)

st.title("🦵 Fixed Loop ACL Calculator")
st.markdown("Technique-specific calculator for **Fixed Loop ACL Reconstruction**")

st.divider()

# ================= AVAILABLE IMPLANTS =================
AVAILABLE_BUTTON_SIZES = [12, 14]        # mm
AVAILABLE_LOOP_LENGTHS = [15, 20, 25, 30, 35]  # mm

# ================= TECHNIQUE SELECTION =================
st.header("🧠 Surgical Technique")

technique = st.radio(
    "Select fixation technique:",
    ["Fixed Loop All-Inside (FLAI)", "Standard Fixed Loop"]
)

st.divider()

# ================= INPUTS =================
st.header("🔢 Surgical Measurements (mm)")

col1, col2 = st.columns(2)

with col1:
    femoral_tunnel = st.number_input("Femoral Tunnel Length (T)", 20, 60, 35)
    tibial_tunnel = st.number_input("Tibial Tunnel Length", 25, 70, 40)
    intra_articular = st.number_input("Intra-articular Graft Length", 15, 40, 25)

with col2:
    required_femoral_graft = st.number_input(
        "Minimum Required Femoral Graft Seating (mm)", 15, 30, 20
    )
    tibial_graft = st.number_input("Desired Graft in Tibial Tunnel", 20, 35, 30)
    safety_margin = st.number_input("Safety Margin", 2, 10, 5)

st.divider()

st.header("🧬 Graft & Implant Details")

total_graft_length = st.number_input("Total Graft Length Available", 150, 300, 240)

button_length = st.selectbox(
    "Cortical Button Length (B)",
    AVAILABLE_BUTTON_SIZES
)

# ================= CALCULATIONS =================

# Ideal loop length
ideal_loop = femoral_tunnel - required_femoral_graft - safety_margin

# Select nearest AVAILABLE loop ≥ ideal
valid_loops = [l for l in AVAILABLE_LOOP_LENGTHS if l >= ideal_loop]
selected_loop = min(valid_loops) if valid_loops else None

# Socket depth calculation (ONLY for FLAI)
socket_depth = None
if selected_loop and technique == "Fixed Loop All-Inside (FLAI)":
    socket_depth = femoral_tunnel - selected_loop + (0.75 * button_length)

# Graft calculations
total_graft_required = required_femoral_graft + intra_articular + tibial_graft
graft_excess = total_graft_length - total_graft_required

# ================= RESULTS =================
st.divider()
st.header("📊 Results")

st.metric("Calculated Ideal Loop Length", f"{ideal_loop:.1f} mm")

if selected_loop:
    st.metric("Selected Available Loop Length", f"{selected_loop} mm")
else:
    st.error("❌ No suitable fixed loop length available.")

if technique == "Fixed Loop All-Inside (FLAI)" and socket_depth is not None:
    st.metric("Femoral Socket Depth (FLAI)", f"{socket_depth:.1f} mm")

st.metric("Total Graft Required", f"{total_graft_required:.1f} mm")
st.metric("Graft Excess / Deficit", f"{graft_excess:.1f} mm")

# ================= CLINICAL INTERPRETATION =================
st.divider()
st.header("⚠️ Clinical Interpretation")

# FLAI socket depth assessment
if technique == "Fixed Loop All-Inside (FLAI)" and socket_depth is not None:
    if socket_depth < required_femoral_graft:
        st.error("❌ Socket depth inadequate for femoral graft seating.")
    else:
        st.success("✅ Socket depth adequate for FLAI fixation.")

# Graft length check
if graft_excess < 0:
    st.error("❌ Graft too short – risk of graft–tunnel mismatch.")
elif graft_excess > 15:
    st.warning("⚠️ Excess graft length – assess tibial tunnel exit.")
else:
    st.success("✅ Graft length appropriate.")

# ================= OPERATIVE NOTE =================
st.divider()
st.subheader("📝 Auto-generated Operative Note")

note = f"""
Technique: {technique}
Femoral tunnel length (T): {femoral_tunnel} mm
Button length (B): {button_length} mm
Loop length (L): {selected_loop if selected_loop else 'N/A'} mm
Femoral socket depth (S): {socket_depth:.1f} mm
Graft adequacy: {'Adequate' if graft_excess >= 0 else 'Inadequate'}
"""

st.text_area("Copy into operative notes:", note, height=190)

st.caption(
    "⚕️ Educational decision-support tool. Final surgical judgment remains with the operating surgeon."
)
