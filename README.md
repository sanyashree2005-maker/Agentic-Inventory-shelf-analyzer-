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

