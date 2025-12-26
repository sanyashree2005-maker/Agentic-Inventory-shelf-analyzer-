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
    Step-by-step shelf analysis system that:
    1. Confirms shelf count  
    2. Analyzes each shelf individually  
    3. Generates restocking alerts based on findings
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
# STEP 1: User confirms shelf count
# --------------------------------------------------
if uploaded_image is not None:
    shelves = st.slider(
        "🧮 STEP 1: Select the number of product shelves visible",
        min_value=1,
        max_value=12,
        value=7
    )

    confirm = st.checkbox("✅ I confirm this shelf count")

    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded Shelf Image", use_column_width=True)

    # --------------------------------------------------
    # STEP 2: Shelf-wise analysis (ONLY after confirmation)
    # --------------------------------------------------
    if confirm:

        st.divider()
        st.subheader("🔍 STEP 2: Shelf-wise Analysis")

        img_array = np.array(image)
        height = img_array.shape[0]
        shelf_height = height // shelves

        empty_shelves = []

        for i in range(shelves):
            y1 = i * shelf_height
            y2 = min((i + 1) * shelf_height, height)
            region = img_array[y1:y2, :, :]

            brightness = region.mean()

            # Simple & consistent emptiness proxy
            if brightness < 130:
                empty_shelves.append(i + 1)

        # Show intermediate result (IMPORTANT)
        st.write(f"**Shelves analyzed:** {shelves}")
        st.write(f"**Empty shelves detected:** {len(empty_shelves)}")

        if empty_shelves:
            st.write("📌 Empty shelf numbers:")
            for shelf in empty_shelves:
                st.markdown(f"- Shelf {shelf}")
        else:
            st.success("✅ No empty shelves detected.")

        # --------------------------------------------------
        # STEP 3: Decision & Alert Generation
        # --------------------------------------------------
        st.divider()
        st.subheader("🚨 STEP 3: Restocking Decision")

        empty_ratio = len(empty_shelves) / shelves if shelves > 0 else 0

        if empty_ratio == 0:
            decision = "NO RESTOCK REQUIRED"
            priority = "LOW"
        elif empty_ratio <= 0.4:
            decision = "RESTOCK CAN BE PLANNED"
            priority = "MEDIUM"
        else:
            decision = "IMMEDIATE RESTOCK REQUIRED"
            priority = "HIGH"

        st.write(f"**Decision:** {decision}")
        st.write(f"**Priority Level:** {priority}")

        if priority == "HIGH":
            st.error("🚨 Immediate restocking required.")
        elif priority == "MEDIUM":
            st.warning("⚠️ Restocking recommended soon.")
        else:
            st.success("✅ Stock levels acceptable.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Stepwise, Human-in-the-loop Analysis | Streamlit Deployment"
)
