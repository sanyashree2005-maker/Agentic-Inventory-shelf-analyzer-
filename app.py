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
# Agentic Analysis Logic (Adaptive)
# --------------------------------------------------
def agentic_inventory_analysis(image: Image.Image, shelves=3):
    """
    Shelf-wise adaptive agentic decision logic
    """

    img_array = np.array(image)
    height, width, _ = img_array.shape
    shelf_height = height // shelves

    empty_shelves = []
    shelf_status = []

    for i in range(shelves):
        y1 = i * shelf_height
        y2 = (i + 1) * shelf_height

        shelf_region = img_array[y1:y2, :, :]
        brightness = shelf_region.mean()

        # Perception rule (proxy for emptiness)
        if brightness < 130:
            empty_shelves.append(i)
            shelf_status.append("EMPTY")
        else:
            shelf_status.append("STOCKED")

    # -------------------------------
    # Adaptive urgency calculation
    # -------------------------------
    empty_count = len(empty_shelves)
    empty_ratio = empty_count / shelves

    if empty_ratio == 0:
        decision = "NO RESTOCK REQUIRED"
        priority = "LOW"
    elif empty_ratio <= 0.25:
        decision = "RESTOCK CAN BE PLANNED"
        priority = "LOW"
    elif empty_ratio <= 0.6:
        decision = "RESTOCK ADVISED"
        priority = "MEDIUM"
    else:
        decision = "IMMEDIATE RESTOCK REQUIRED"
        priority = "HIGH"

    return empty_shelves, shelf_status, decision, priority

# --------------------------------------------------
# Draw Bounding Boxes on Empty Shelves
# --------------------------------------------------
def draw_bounding_boxes(image, empty_shelves, shelves=3):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    shelf_height = height // shelves

    for shelf in empty_shelves:
        y1 = shelf * shelf_height
        y2 = (shelf + 1) * shelf_height

        draw.rectangle(
            [(0, y1), (width, y2)],
            outline="red",
            width=4
        )

        draw.text(
            (10, y1 + 10),
            f"Shelf {shelf + 1} – Needs Restock",
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

    empty_shelves, shelf_status, decision, priority = agentic_inventory_analysis(image)

    st.write(f"**Total Shelves Analysed:** {len(shelf_status)}")
    st.write(f"**Empty Shelves Detected:** {len(empty_shelves)}")
    st.write(f"**Decision:** {decision}")
    st.write(f"**Priority Level:** {priority}")

    # Priority-based messaging
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

    # Visual localization
    boxed_image = draw_bounding_boxes(image.copy(), empty_shelves)

    st.subheader("🟥 Visual Restock Indicators")
    st.image(
        boxed_image,
        caption="Shelves highlighted for restocking",
        use_column_width=True
    )

    st.divider()

    st.subheader("🤖 Agent Explanation")
    st.markdown(
        """
        - The agent **segments the shelf image into logical shelf regions**
        - Each shelf is **independently perceived**
        - Brightness is used as a **proxy indicator of emptiness**
        - The agent **quantifies impact** instead of binary alerts
        - Urgency is **adaptively decided** to avoid false alarms
        """
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Agentic Inventory Alert Bot | Adaptive Shelf-Level Decision Making | Streamlit Deployment"
)
