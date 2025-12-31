import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Fixed Loop ACL Calculator",
    page_icon="🦵",
    layout="centered"
)

st.title("🦵 Fixed Loop ACL Calculator")
st.markdown("Implant-aware calculator for **fixed-loop cortical button ACL reconstruction**")

st.divider()

# ================= AVAILABLE IMPLANTS =================
AVAILABLE_BUTTON_SIZES = [12, 14]  # mm
AVAILABLE_LOOP_LENGTHS = [15, 20, 25, 30, 35]  # mm

# ================= INPUTS =================
st.header("🔢 Surgical Measurements (mm)")

col1, col2 = st.columns(2)

with col1:
    femoral_tunnel = st.number_input("Femoral Tunnel Length (T)", 20, 60, 35)
    tibial_tunnel = st.number_input("Tibial Tunnel Length", 25, 70, 40)
    intra_articular = st.number_input("Intra-articular Graft Length", 15, 40, 25)

with col2:
    femoral_graft_required = st.number_input(
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
ideal_loop = femoral_tunnel - femoral_graft_required - safety_margin

# Select nearest available loop ≥ ideal
valid_loops = [l for l in AVAILABLE_LOOP_LENGTHS if l >= ideal_loop]
selected_loop = min(valid_loops) if valid_loops else None

# Socket depth calculation
if selected_loop:
    socket_depth = (femoral_tunnel - selected_loop) + (0.75 * button_length)
else:
    socket_depth = None

# Graft calculations
total_graft_required = femoral_graft_required + intra_articular + tibial_graft
graft_excess = total_graft_length - total_graft_required

# ================= RESULTS =================
st.divider()
st.header("📊 Results")

st.metric("Calculated Ideal Loop Length", f"{ideal_loop:.1f} mm")

if selected_loop:
    st.metric("Selected Available Loop Length", f"{selected_loop} mm")
    st.metric("Femoral Socket Depth (S)", f"{socket_depth:.1f} mm")
else:
    st.error("❌ No suitable fixed loop length available.")

st.metric("Total Graft Required", f"{total_graft_required:.1f} mm")
st.metric("Graft Excess / Deficit", f"{graft_excess:.1f} mm")

# ================= CLINICAL INTERPRETATION =================
st.divider()
st.header("⚠️ Clinical Interpretation")

# Socket depth check
if socket_depth is not None:
    if socket_depth < femoral_graft_required:
        st.error(
            "❌ Femoral socket depth is INADEQUATE for required graft seating."
        )
    elif socket_depth > femoral_tunnel:
        st.warning(
            "⚠️ Socket depth exceeds tunnel length. Verify measurements."
        )
    else:
        st.success(
            "✅ Femoral socket depth is adequate for graft fixation."
        )

# Graft length check
if graft_excess < 0:
    st.error("❌ Graft too short – risk of graft–tunnel mismatch.")
elif graft_excess > 15:
    st.warning("⚠️ Excess graft length – assess tibial overhang.")
else:
    st.success("✅ Graft length appropriate.")

# ================= OPERATIVE NOTE =================
st.divider()
st.subheader("📝 Auto-generated Operative Note")

note = f"""
• Femoral tunnel length (T): {femoral_tunnel} mm
• Button length (B): {button_length} mm
• Loop length selected (L): {selected_loop if selected_loop else 'N/A'} mm
• Femoral socket depth (S): {socket_depth:.1f} mm
• Graft adequacy: {'Adequate' if graft_excess >= 0 else 'Inadequate'}
"""

st.text_area("Copy into operative notes:", note, height=180)

st.caption("⚕️ Decision-support tool only. Final surgical judgment remains with the surgeon.")
