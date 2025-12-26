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
    Analyze retail shelf images to identify **empty shelves** and
    generate **adaptive restocking alerts** using agent-based logic.
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
# Manual Shelf Control (KEY STABILITY FIX)
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

        # Simple, explainable proxy for emptiness
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
# Draw Bounding Boxes (ONLY EMPTY SHELVES)
# --------------------------------------------------
def draw_bounding_boxes(image, empty_shelves, shelves):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    shelf_height = height // shelves

    x_start = int(0.2 * width)
    x_end = int(0.8 * width)

    for shelf in empty_shelves:
        y1 = shelf * shelf_height + 5
        y2 = min((shelf + 1) * shelf_height - 5, height)

        draw.rectangle(
            [(x_start, y1), (x_end, y2)],
            outline="red",
            width=4
        )

        draw.text(
            (x_start + 10, y1 + 10),
            f"Shelf {shelf + 1} – Empty",
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
    st.write(f"**Empty Shelves Detected:** {len(empty_shelves)}")
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
        caption="Only empty shelves are highlighted",
        use_column_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Stable Shelf-Level Decision System | Streamlit Deployment"
)
