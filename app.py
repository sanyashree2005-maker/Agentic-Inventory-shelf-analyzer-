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
    and clearly identify **which shelves require restocking**
    using minimal visual indicators.
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
    "🧮 Select number of shelf rows (product shelves only)",
    min_value=3,
    max_value=12,
    value=7
)

# --------------------------------------------------
# Helper: Check if band contains products (TEXTURE CHECK)
# --------------------------------------------------
def is_product_shelf(region, texture_threshold=12):
    gray = np.mean(region, axis=2)
    texture = np.abs(np.diff(gray, axis=1)).mean()
    return texture > texture_threshold

# --------------------------------------------------
# Agentic Analysis Logic
# --------------------------------------------------
def agentic_inventory_analysis(image: Image.Image, shelves: int):
    img_array = np.array(image)
    height, width, _ = img_array.shape
    shelf_height = height // shelves

    empty_shelves = []

    # Ignore extreme top & bottom (ceiling / floor)
    top_ignore = int(0.1 * height)
    bottom_ignore = int(0.9 * height)

    for i in range(shelves):
        y1 = i * shelf_height
        y2 = min((i + 1) * shelf_height, height)

        # Skip non-product zones
        if y2 < top_ignore or y1 > bottom_ignore:
            continue

        region = img_array[y1:y2, :, :]

        # 🔑 NEW: validate that this is actually a shelf
        if not is_product_shelf(region):
            continue

        brightness = region.mean()

        # Emptiness proxy (simple & explainable)
        if brightness < 130:
            empty_shelves.append(i)

    empty_ratio = len(empty_shelves) / shelves if shelves > 0 else 0

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
# Draw ONE DOT PER EMPTY SHELF (CLEAN & CLEAR)
# --------------------------------------------------
def draw_shelf_markers(image, empty_shelves, shelves):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    shelf_height = height // shelves
    radius = 9

    for shelf in empty_shelves:
        cx = width // 2
        cy = int((shelf + 0.5) * shelf_height)

        draw.ellipse(
            [(cx - radius, cy - radius), (cx + radius, cy + radius)],
            fill="red",
            outline="red"
        )

        draw.text(
            (cx + radius + 6, cy - radius),
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
        caption="Red dots mark ONLY valid shelves that need restocking",
        use_column_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Shelf-Validated Indicators | Streamlit Deployment"
)
