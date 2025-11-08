## DocuMind: Intelligent Document Layout Analysis

A deep learning system for document layout parsing and and highly accurate information extraction, built with PyTorch and designed for enterprise automation.

-----

### 💡 Project Motivation and Business Value

Every modern enterprise relies on extracting data from semi-structured documents (invoices, forms, reports). This project addresses the critical industry pain point of manual data entry, which is costly, slow, and error-prone.

**DocuMind** automates the entire document-to-data pipeline, demonstrating proficiency in **Intelligent Document Processing (IDP)**—a key domain in enterprise AI.

-----

### 🚀 Key Features

  * **Generalized Layout Analysis:** Utilizes **LayoutLM** to understand and classify document regions (headers, tables, paragraphs) regardless of vendor or template variation.
  * **High-Accuracy Information Extraction:** Localizes and extracts specific, critical fields (e.g., Total Amount, Invoice Date) and converts them into structured JSON output.
  * **Multi-Modal Processing:** Integrates both **Textual** and **Spatial (2D Layout)** features for robust performance on noisy scans and complex forms.
  * **Web Interface for Inference:** Provides a user-friendly Streamlit application for easy image upload and visual validation of extracted bounding boxes.

-----

### 💻 Technology Stack

| Category | Component | Purpose |
| :--- | :--- | :--- |
| **Deep Learning Framework** | PyTorch | Core ML framework for model definition and training. |
| **Core Model** | LayoutLMv2 / LayoutXLM | State-of-the-art Vision-Language model for document understanding. |
| **Data Handling** | Hugging Face `transformers` & `datasets` | Tooling for tokenization, data loading, and model management. |
| **Backend/API** | FastAPI | High-performance, asynchronous API for serving the extraction model. |
| **Frontend/Demo** | Streamlit | Rapidly developed web interface for demonstration and visualization. |
| **Data Sources** | SROIE, FUNSD | Used for fine-tuning to ensure generalization across receipts and forms. |

-----

### 📁 Project Structure

This outlines the essential directories and files for the project codebase:

```
documind-ai/
|-- data/
|   |-- raw/              # Original SROIE and FUNSD datasets
|   |-- processed/        # Tokenized and normalized data ready for PyTorch Dataset
|-- model/
|   |-- checkpoints/      # Saved weights (.pth) for the fine-tuned LayoutLM model
|   |-- idp_extractor.py  # Core class encapsulating the inference pipeline
|-- scripts/
|   |-- train.py          # Main training loop script
|   |-- eda_notebook.ipynb # Exploratory Data Analysis (EDA) and visualizations
|-- app/
|   |-- api.py            # FastAPI service for the inference endpoint
|   |-- web_app.py        # Streamlit interface code
|-- requirements.txt      # All necessary Python dependencies
|-- README.md
```

-----

### 📊 Defined Success Metrics

The system will be evaluated based on its ability to perform robustly across various document types:

| Metric | Target | Rationale |
| :--- | :--- | :--- |
| **Field Detection Accuracy** | $>95\%$ F1-Score (Entity Level) | Minimizes manual correction effort required after extraction. |
| **Data Normalization** | $100\%$ Consistency | Ensures all extracted dates and monetary values are standardized. |
| **Generalization** | Successful extraction from SROIE & FUNSD | Confirms the model can adapt to multiple layout structures. |


### Project Status: Day 2 (Essential EDA)

**Current Focus:** Generating analytical proof to justify the technical approach (LayoutLM).

| Day | Task Focus | Status |
| :--- | :--- | :--- |
| **Day 1** | Foundation & Analysis | **COMPLETE** ✅ |
| **Day 2** | **Essential Document AI EDA** | **COMPLETE** (Analysis Phase) |
| **Day 3** | Project Review & Label Alignment Start | Upcoming |

---

### 2. Day 2 Achievements: Technical Justification

Day 2 focused on transforming raw data analysis into visual evidence, validating the core architectural decisions of the **LayoutIQ** system.

#### A. Implementation: Normalization

* **Objective:** To handle varying document sizes by creating a fixed spatial reference.
* **Achievement:** Implemented and verified the **`normalize_bbox` function**, which scales all raw pixel coordinates to a universal $\mathbf{0} \text{ to } \mathbf{1000}$ range. This eliminates instability caused by document size variance.

#### B. Exploratory Data Analysis (EDA) Findings

The following data points prove the necessity of using the **LayoutLM** model over simpler alternatives:

| EDA Finding | Proof Point | Architectural Impact |
| :--- | :--- | :--- |
| **Label Distribution** (Chart Generated) | Confirmed the FUNSD dataset is **densely annotated**, with approximately **77% meaningful entities** (Question/Answer). | Proves the challenge is **differentiating and linking** closely packed entities, not just finding them (justifies complex linkage model). |
| **Spatial Clustering** (Scatter Plot Generated) | Plots of normalized coordinates show that key fields are **not random**. They cluster vertically on the left (Questions) and centrally/right (Answers).  | **Justifies `bbox` Input:** Provides visual evidence that **layout is the core feature** needed to correctly associate answers with their questions. |
| **Layout Variance** (Table Generated) | Confirmed original document widths and heights vary significantly across the dataset (e.g., $W=762$ up to $W=1200$). | **Validates Normalization:** Explicitly justifies the need for the $\mathbf{0} \text{ to } \mathbf{1000}$ scaling implemented. |

---
day 3