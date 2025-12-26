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
    Upload a retail shelf image, select the number of shelf rows,
    and identify **empty shelf regions** using lightweight agentic logic.
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
# Draw DOT MARKERS for Empty Regions (UX-Friendly)
# --------------------------------------------------
def draw_empty_markers(image, empty_shelves, shelves):
    draw = ImageDraw.Draw(image)
    img_array = np.array(image)

    width, height = image.size
    shelf_height = height // shelves
    radius = 7  # size of marker

    for shelf in empty_shelves:
        y1 = shelf * shelf_height
        y2 = min((shelf + 1) * shelf_height, height)

        shelf_region = img_array[y1:y2, :, :]
        gray = np.mean(shelf_region, axis=2)

        # Divide shelf into vertical segments
        num_segments = 6
        segment_width = width // num_segments

        shelf_mean_brightness = gray.mean()
        shelf_mean_texture = np.abs(np.diff(gray, axis=1)).mean()

        for i in range(num_segments):
            x1 = i * segment_width
            x2 = min((i + 1) * segment_width, width)

            segment = gray[:, x1:x2]
            segment_brightness = segment.mean()
            segment_texture = np.abs(np.diff(segment, axis=1)).mean()

            # Relative emptiness rule (robust)
            if (
                segment_texture < 0.7 * shelf_mean_texture
                and segment_brightness > shelf_mean_brightness
            ):
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                draw.ellipse(
                    [
                        (cx - radius, cy - radius),
                        (cx + radius, cy + radius)
                    ],
                    fill="red",
                    outline="red"
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

    marked_image = draw_empty_markers(image.copy(), empty_shelves, shelves)

    st.subheader("🔴 Visual Restock Indicators")
    st.image(
        marked_image,
        caption="Red dots indicate empty shelf regions",
        use_column_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Lightweight Visual Indicators | Streamlit Deployment"
)
