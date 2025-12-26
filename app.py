import streamlit as st
from PIL import Image, ImageDraw
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
    Upload a retail shelf image, select the number of shelf rows,
    and visually identify **empty regions** that require restocking.
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
# Manual Shelf Control (Stable & Realistic)
# --------------------------------------------------
shelves = st.slider(
    "🧮 Select number of shelf rows visible in image",
    min_value=3,
    max_value=12,
    value=7
)

# --------------------------------------------------
# Agentic Analysis Logic
# --------------------------------------------------
def agentic_inventory_analysis(image: Image.Image, shelves: int):
    img_array = np.array(image)
    height, width, _ = img_array.shape
    shelf_height = height // shelves

    empty_shelves = []

    for i in range(shelves):
        y1 = i * shelf_height
        y2 = min((i + 1) * shelf_height, height)

        region = img_array[y1:y2, :, :]
        brightness = region.mean()

        # Simple, explainable proxy for shelf emptiness
        if brightness < 130:
            empty_shelves.append(i)

    empty_ratio = len(empty_shelves) / shelves

    if empty_ratio == 0:
        decision = "NO RESTOCK REQUIRED"
        priority = "LOW"
    elif empty_ratio <= 0.3:
        decision = "RESTOCK CAN BE PLANNED"
        priority = "LOW"
    elif empty_ratio <= 0.6:
        decision = "RESTOCK ADVISED"
        priority = "MEDIUM"
    else:
        decision = "IMMEDIATE RESTOCK REQUIRED"
        priority = "HIGH"

    return empty_shelves, decision, priority

# --------------------------------------------------
# Draw Precise Bounding Boxes (Empty Regions Only)
# --------------------------------------------------
def draw_bounding_boxes(image, empty_shelves, shelves):
    draw = ImageDraw.Draw(image)
    img_array = np.array(image)

    width, height = image.size
    shelf_height = height // shelves

    for shelf in empty_shelves:
        y1 = shelf * shelf_height
        y2 = min((shelf + 1) * shelf_height, height)

        shelf_region = img_array[y1:y2, :, :]
        gray = np.mean(shelf_region, axis=2)

        # Split shelf into vertical strips
        num_strips = 6
        strip_width = width // num_strips

        for i in range(num_strips):
            x1 = i * strip_width
            x2 = min((i + 1) * strip_width, width)

            strip = gray[:, x1:x2]

            brightness = strip.mean()
            texture = np.abs(np.diff(strip, axis=1)).mean()

            # Empty region heuristic
            if brightness > 160 and texture < 10:
                draw.rectangle(
                    [(x1, y1 + 5), (x2, y2 - 5)],
                    outline="red",
                    width=3
                )

                draw.text(
                    (x1 + 5, y1 + 8),
                    "Empty",
                    fill="red"
                )

    return image

# --------------------------------------------------
# Run Analysis
# --------------------------------------------------
if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")

    st.image(image, caption="Uploaded Shelf Image", use_column_width=True)

    st.subheader("🔍 Agent Analysis")

    empty_shelves, decision, priority = agentic_inventory_analysis(image, shelves)

    st.write(f"**Total Shelves Analysed:** {shelves}")
    st.write(f"**Shelves with Empty Regions:** {len(empty_shelves)}")
    st.write(f"**Decision:** {decision}")
    st.write(f"**Priority Level:** {priority}")

    if priority == "HIGH":
        st.error("🚨 High urgency: Immediate restocking required.")
    elif priority == "MEDIUM":
        st.warning("⚠️ Medium urgency: Plan restocking soon.")
    else:
        st.success("✅ Low urgency: Stock levels acceptable.")

    st.divider()

    boxed_image = draw_bounding_boxes(image.copy(), empty_shelves, shelves)

    st.subheader("🟥 Visual Restock Indicators")
    st.image(
        boxed_image,
        caption="Red boxes indicate actual empty regions within shelves",
        use_column_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Human-Guided Shelf Analysis | Streamlit Deployment"
)
