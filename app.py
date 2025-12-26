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
    Upload a retail shelf image, select the number of shelves,
    and identify **which shelves require restocking** using
    clear visual indicators.
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
# Manual Shelf Control (Human-in-the-loop)
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

        # Simple & explainable emptiness proxy
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
# Draw SIMPLE DOT INDICATORS (CLEAR & VISIBLE)
# --------------------------------------------------
def draw_shelf_markers(image, empty_shelves, shelves):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    shelf_height = height // shelves

    radius = 10  # dot size

    for shelf in empty_shelves:
        # Center of the shelf
        cx = width // 2
        cy = int((shelf + 0.5) * shelf_height)

        draw.ellipse(
            [
                (cx - radius, cy - radius),
                (cx + radius, cy + radius)
            ],
            fill="red",
            outline="red"
        )

        draw.text(
            (cx + radius + 5, cy - radius),
            f"Shelf {shelf + 1}",
            fill="red"
        )

    return image

# --------------------------------------------------
# Run Analysis
# --------------------------------------------------
if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")

    st.image(
        image,
        caption="Uploaded Shelf Image",
        use_column_width=True
    )

    st.subheader("🔍 Agent Analysis")

    empty_shelves, decision, priority = agentic_inventory_analysis(image, shelves)

    st.write(f"**Total Shelves Analysed:** {shelves}")
    st.write(f"**Shelves Needing Restock:** {len(empty_shelves)}")
    st.write(f"**Decision:** {decision}")
    st.write(f"**Priority Level:** {priority}")

    if priority == "HIGH":
        st.error("🚨 High urgency: Immediate restocking required.")
    elif priority == "MEDIUM":
        st.warning("⚠️ Medium urgency: Plan restocking soon.")
    else:
        st.success("✅ Low urgency: Stock levels acceptable.")

    st.divider()

    marked_image = draw_shelf_markers(image.copy(), empty_shelves, shelves)

    st.subheader("🔴 Visual Restock Indicators")
    st.image(
        marked_image,
        caption="Red dots mark shelves that require restocking",
        use_column_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Clear Shelf-Level Indicators | Streamlit Deployment"
)
