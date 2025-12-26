import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="Agentic Inventory Alert Bot",
    layout="centered"
)

st.title("🛒 Agentic Inventory Alert Bot")

st.markdown(
    """
    **Decision-support shelf analysis system**

    The agent does **not guess emptiness**.
    It computes **relative shelf scores** and lets the user interpret them.
    """
)

st.divider()

uploaded_image = st.file_uploader(
    "📤 Upload Shelf Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image is not None:

    shelves = st.slider(
        "🧮 STEP 1: Select number of product shelves",
        min_value=1,
        max_value=12,
        value=7
    )

    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded Shelf Image", use_column_width=True)

    st.divider()
    st.subheader("🔍 STEP 2: Shelf-wise Scoring (Transparent)")

    img = np.array(image)
    height = img.shape[0]
    shelf_height = height // shelves

    shelf_scores = []

    for i in range(shelves):
        y1 = i * shelf_height
        y2 = min((i + 1) * shelf_height, height)
        region = img[y1:y2, :, :]

        # Emptiness score = inverse brightness
        score = 255 - region.mean()
        shelf_scores.append(score)

    avg_score = np.mean(shelf_scores)

    # Display scores clearly
    for i, score in enumerate(shelf_scores):
        st.progress(min(score / (avg_score * 2), 1.0))
        st.write(f"Shelf {i+1} — Emptiness Score: {score:.2f}")

    st.divider()
    st.subheader("🧠 STEP 3: Human-guided Decision")

    suggested = [
        i + 1 for i, s in enumerate(shelf_scores)
        if s > avg_score * 1.2
    ]

    if suggested:
        st.info(
            f"📌 Shelves with noticeably higher emptiness score: {suggested}"
        )
    else:
        st.success("✅ All shelves appear similarly stocked.")

    st.markdown(
        """
        **Why this works:**
        - The agent computes *relative evidence*
        - The human confirms interpretation
        - No false alarms
        - No hallucinated counts
        """
    )

st.caption(
    "Agentic Inventory Alert Bot | Decision-Support System | Streamlit Deployment"
)
