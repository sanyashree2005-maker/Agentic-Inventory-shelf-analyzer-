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
    **Step-wise shelf analysis system**

    1️⃣ Confirm number of shelves  
    2️⃣ Analyse shelves comparatively  
    3️⃣ Detect empty shelves  
    4️⃣ Generate restocking alert
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
# STEP 1 — Shelf count confirmation
# --------------------------------------------------
if uploaded_image is not None:

    shelves = st.slider(
        "🧮 STEP 1: Select number of product shelves visible",
        min_value=1,
        max_value=12,
        value=7
    )

    confirm = st.checkbox("✅ I confirm this shelf count")

    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded Shelf Image", use_column_width=True)

    # --------------------------------------------------
    # STEP 2 — Shelf-wise comparative analysis
    # --------------------------------------------------
    if confirm:

        st.divider()
        st.subheader("🔍 STEP 2: Shelf-wise Analysis")

        img = np.array(image)
        height = img.shape[0]
        shelf_height = height // shelves

        emptiness_scores = []

        # Compute emptiness score for each shelf
        for i in range(shelves):
            y1 = i * shelf_height
            y2 = min((i + 1) * shelf_height, height)
            region = img[y1:y2, :, :]

            # Emptiness score (higher = more empty)
            score = 255 - region.mean()
            emptiness_scores.append(score)

        mean_score = np.mean(emptiness_scores)
        std_score = np.std(emptiness_scores)

        empty_shelves = []
        empty_levels = {}

        for i, score in enumerate(emptiness_scores):
            if score > mean_score + std_score:
                empty_shelves.append(i + 1)
                empty_levels[i + 1] = score

        # Transparent output
        st.write(f"**Shelves analysed:** {shelves}")
        st.write(f"**Empty shelves detected:** {len(empty_shelves)}")

        if empty_shelves:
            st.write("📌 Empty shelves & empty level score:")
            for shelf, level in empty_levels.items():
                st.markdown(
                    f"- **Shelf {shelf}** → Empty Level Score: `{level:.2f}`"
                )
        else:
            st.success("✅ No empty shelves detected.")

        # --------------------------------------------------
        # STEP 3 — Restocking decision
        # --------------------------------------------------
        st.divider()
        st.subheader("🚨 STEP 3: Restocking Decision")

        empty_ratio = len(empty_shelves) / shelves

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
    "Agentic Inventory Alert Bot | Comparative Shelf Analysis | Streamlit Deployment"
)
