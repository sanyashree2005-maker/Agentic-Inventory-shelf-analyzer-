import streamlit as st
from PIL import Image
import numpy as np

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Agentic Inventory Alert Bot",
    layout="centered"
)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🛒 Agentic Inventory Alert Bot")

st.markdown(
    """
    Human-guided shelf analysis system that identifies  
    **which shelf rows require restocking**.
    """
)

st.divider()

# --------------------------------------------------
# Image Upload
# --------------------------------------------------
uploaded_image = st.file_uploader(
    "📤 Upload Shelf Image",
    type=["jpg", "jpeg", "png"]
)

# --------------------------------------------------
# Manual Shelf Control
# --------------------------------------------------
shelves = st.slider(
    "🧮 Select number of shelf rows (product shelves only)",
    min_value=3,
    max_value=12,
    value=7
)

# --------------------------------------------------
# Agentic Shelf-Level Analysis
# --------------------------------------------------
def analyze_shelves(image, shelves):
    img = np.array(image)
    height = img.shape[0]
    shelf_height = height // shelves

    shelves_needing_attention = []

    for i in range(shelves):
        y1 = i * shelf_height
        y2 = min((i + 1) * shelf_height, height)
        region = img[y1:y2, :, :]

        brightness = region.mean()

        # Simple, explainable rule
        if brightness < 130:
            shelves_needing_attention.append(i + 1)

    ratio = len(shelves_needing_attention) / shelves

    if ratio == 0:
        decision = "NO RESTOCK REQUIRED"
        priority = "LOW"
    elif ratio <= 0.4:
        decision = "RESTOCK CAN BE PLANNED"
        priority = "MEDIUM"
    else:
        decision = "IMMEDIATE RESTOCK REQUIRED"
        priority = "HIGH"

    return shelves_needing_attention, decision, priority

# --------------------------------------------------
# Run Analysis
# --------------------------------------------------
if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")

    st.image(image, caption="Uploaded Shelf Image", use_column_width=True)

    shelves_to_restock, decision, priority = analyze_shelves(image, shelves)

    st.subheader("🔍 Agent Analysis")

    st.write(f"**Decision:** {decision}")
    st.write(f"**Priority:** {priority}")

    st.divider()

    st.subheader("📌 Shelves Requiring Attention")

    if shelves_to_restock:
        for shelf in shelves_to_restock:
            st.markdown(f"🔴 **Shelf {shelf} – Needs Restocking**")
    else:
        st.success("✅ All shelves appear sufficiently stocked.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Shelf-Level Decision System | Streamlit Deployment"
)
