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
# Title & Description
# --------------------------------------------------
st.title("🛒 Agentic Inventory Alert Bot")

st.markdown(
    """
    Upload a retail shelf image to analyze shelf-wise empty spaces and
    generate adaptive inventory alerts using an agent-based decision system.
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
# Shelf Count Estimation (DEFINE FIRST)
# --------------------------------------------------
def estimate_shelf_count(image, min_shelf_height=90):
    height = image.size[1]
    return max(1, height // min_shelf_height)

# --------------------------------------------------
# Agentic Analysis Logic
# --------------------------------------------------
def agentic_inventory_analysis(image: Image.Image):
    img_array = np.array(image)
    height, width, _ = img_array.shape

    shelves = estimate_shelf_count(image)
    shelf_height = height // shelves

    empty_shelves = []
    shelf_status = []

    for i in range(shelves):
        y1 = i * shelf_height
        y2 = min((i + 1) * shelf_height, height)

        shelf_region = img_array[y1:y2, :, :]
        brightness = shelf_region.mean()

        if brightness < 130:
            empty_shelves.append(i)
            shelf_status.append("EMPTY")
        else:
            shelf_status.append("STOCKED")

    empty_ratio = len(empty_shelves) / shelves

    if empty_ratio == 0:
        decision = "NO RESTOCK REQUIRED"
        priority = "LOW"
    elif empty_ratio <= 0.30:
        decision = "RESTOCK CAN BE PLANNED"
        priority = "LOW"
    elif empty_ratio <= 0.60:
        decision = "RESTOCK ADVISED"
        priority = "MEDIUM"
    else:
        decision = "IMMEDIATE RESTOCK REQUIRED"
        priority = "HIGH"

    return shelves, empty_shelves, shelf_status, decision, priority

# --------------------------------------------------
# Draw Bounding Boxes (Only Empty Shelves)
# --------------------------------------------------
def draw_bounding_boxes(image, empty_shelves, shelves):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    shelf_height = height // shelves

    x_start = int(0.2 * width)
    x_end = int(0.8 * width)

    for shelf in empty_shelves:
        y1 = shelf * shelf_height + 6
        y2 = min((shelf + 1) * shelf_height - 6, height)

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

    st.image(
        image,
        caption="Uploaded Shelf Image",
        use_column_width=True
    )

    st.subheader("🔍 Agent Analysis")

    shelves, empty_shelves, shelf_status, decision, priority = agentic_inventory_analysis(image)

    st.write(f"**Total Shelves Analysed:** {shelves}")
    st.write(f"**Empty Shelves Detected:** {len(empty_shelves)}")
    st.write(f"**Decision:** {decision}")
    st.write(f"**Priority Level:** {priority}")

    if priority == "HIGH":
        st.error("🚨 High urgency: Multiple shelves are empty. Immediate restocking required.")
    elif priority == "MEDIUM":
        st.warning("⚠️ Medium urgency: Some shelves need attention. Plan restocking soon.")
    else:
        st.success("✅ Low urgency: Shelf levels are acceptable. Continue monitoring.")

    st.divider()

    st.subheader("📦 Shelf-wise Status")
    for idx, status in enumerate(shelf_status):
        st.write(f"Shelf {idx + 1}: {status}")

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
    "Agentic Inventory Alert Bot | Flexible Shelf Localization | Streamlit Deployment"
)
