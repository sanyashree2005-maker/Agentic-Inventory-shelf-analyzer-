# 🛒 Agentic Inventory Alert Bot

A **human-in-the-loop, agentic decision-support system** for identifying empty shelves and generating reliable restocking alerts from retail shelf images.

---

## 📌 Overview

Retail shelf monitoring is often manual, time-consuming, and prone to delayed decisions.  
Many automated systems rely on rigid rules or black-box deep learning models, which can lead to **false alarms and hallucinated outputs**.

This project presents an **Agentic Inventory Alert Bot** that focuses on:
- Correctness over automation
- Explainability over opacity
- Adaptability over fixed thresholds

The system does **not assume** that shelves are empty.  
Instead, it uses **comparative reasoning** to detect shelves that significantly differ from the overall stock pattern.

---

## 🎯 Key Features

- ✅ Step-wise agentic workflow  
- ✅ Human-in-the-loop shelf count confirmation  
- ✅ Shelf-wise comparative analysis  
- ✅ No fixed brightness thresholds  
- ✅ No hallucinated restocking alerts  
- ✅ Adaptive restocking priority (LOW / MEDIUM / HIGH)  
- ✅ Deployment-safe Streamlit application  

---

## 🧠 How the System Works

### 1️⃣ Image Upload
The user uploads a retail shelf image.

### 2️⃣ Shelf Count Confirmation
The user selects and confirms the number of visible product shelves.  
This prevents false detection of ceilings, signage, or floor areas as shelves.

### 3️⃣ Shelf-wise Analysis
- The image is divided into horizontal regions based on the confirmed shelf count.
- Each shelf is analyzed independently.

### 4️⃣ Emptiness Score Calculation
For each shelf:

Higher score → Shelf appears more empty.

### 5️⃣ Comparative Anomaly Detection
- Mean and standard deviation of all shelf scores are computed.
- A shelf is marked empty **only if**:

This ensures:
- Zero empty shelves → zero detected
- Partial emptiness → accurate detection
- No forced or hallucinated alerts

### 6️⃣ Restocking Decision
Based on the ratio of empty shelves:
- **LOW** → No restock required
- **MEDIUM** → Restock can be planned
- **HIGH** → Immediate restocking required

---

## 🤖 Why This Is an Agentic System

- Follows a **Perception → Validation → Decision** loop
- Does not generate outputs before confirming inputs
- Uses contextual comparison instead of rigid rules
- Adapts decisions based on observed shelf distribution
- Allows human intervention at critical stages

---

## 🛠️ Technologies Used

| Component | Technology |
|--------|------------|
| Programming Language | Python 3.10 |
| Web Framework | Streamlit |
| Image Processing | PIL (Pillow) |
| Numerical Analysis | NumPy |
| Deployment | Streamlit Cloud |

---

## 🚀 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py




