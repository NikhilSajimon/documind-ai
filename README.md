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