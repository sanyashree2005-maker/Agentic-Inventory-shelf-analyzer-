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
    Upload a retail shelf image to detect **empty shelves**, 
    visualize them clearly, and generate **adaptive restocking alerts**.
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
# Helper: Estimate Shelf Rows (Geometry)
# --------------------------------------------------
def estimate_shelf_count(image, min_shelf_height=90):
    height = image.size[1]
    return max(1, height // min_shelf_height)

# --------------------------------------------------
# Helper: Check if Region is Actually a Shelf
# --------------------------------------------------
def is_valid_shelf(region, edge_threshold=20):
    """
    Uses texture (edge density) to check if products exist.
    Smooth regions (floor/ceiling) are ignored.
    """
    gray = np.mean(region, axis=2)
    edges = np.abs(np.diff(gray, axis=1))
    edge_density = edges.mean()
    return edge_density > edge_threshold

# --------------------------------------------------
# Agentic Analysis Logic
# --------------------------------------------------
def agentic_inventory_analysis(image: Image.Image):
    img_array = np.array(image)
    height, width, _ = img_array.shape

    estimated_shelves = estimate_shelf_count(image)
    shelf_height = height // estimated_shelves

    empty_shelves = []
    shelf_status = []
    valid_shelves = []

    for i in range(estimated_shelves):
        y1 = i * shelf_height
        y2 = min((i + 1) * shelf_height, height)

        region = img_array[y1:y2, :, :]

        # 🔑 NEW: Ignore non-shelf regions
        if not is_valid_shelf(region):
            continue

        valid_shelves.append(i)
        brightness = region.mean()

        if brightness < 130:
            empty_shelves.append(i)
            shelf_status.append("EMPTY")
        else:
            shelf_status.append("STOCKED")

    actual_shelves = len(valid_shelves)

    if actual_shelves == 0:
        return 0, [], [], "NO SHELVES DETECTED", "LOW"

    empty_ratio = len(empty_shelves) / actual_shelves

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

    return actual_shelves, empty_shelves, shelf_status, decision, priority

# --------------------------------------------------
# Draw Bounding Boxes (Only Empty & Valid Shelves)
# --------------------------------------------------
def draw_bounding_boxes(image, empty_shelves, estimated_shelves):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    shelf_height = height // estimated_shelves

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

    st.image(image, caption="Uploaded Shelf Image", use_column_width=True)

    st.subheader("🔍 Agent Analysis")

    shelves, empty_shelves, shelf_status, decision, priority = agentic_inventory_analysis(image)

    st.write(f"**Valid Shelves Detected:** {shelves}")
    st.write(f"**Empty Shelves:** {len(empty_shelves)}")
    st.write(f"**Decision:** {decision}")
    st.write(f"**Priority Level:** {priority}")

    if priority == "HIGH":
        st.error("🚨 High urgency: Immediate restocking required.")
    elif priority == "MEDIUM":
        st.warning("⚠️ Medium urgency: Plan restocking soon.")
    else:
        st.success("✅ Low urgency: Stock levels acceptable.")

    st.divider()

    boxed_image = draw_bounding_boxes(image.copy(), empty_shelves, estimate_shelf_count(image))

    st.subheader("🟥 Visual Restock Indicators")
    st.image(
        boxed_image,
        caption="Only real empty shelves are highlighted",
        use_column_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Shelf-Aware & Explainable | Streamlit Deployment"
)
