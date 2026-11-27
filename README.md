# Medical-Chatbot-QA-System

A Streamlit prototype for asking natural-language questions about medical discharge summaries. It extracts text from scanned documents with OCR, stores structured records in MongoDB, indexes their text for semantic retrieval with Pinecone, and uses Google's Gemini API to generate answers grounded in the retrieved records.

> **Project scope:** This is an educational prototype, not a medical device or production patient-record system. It currently works with discharge-summary data; implant-record management and cross-hospital access are future goals, not implemented features.

## What it does

- Extracts text from discharge-summary images using Tesseract OCR.
- Converts the extracted text into structured fields such as diagnosis, medications, procedures, and follow-up information.
- Stores those records in MongoDB and creates vector embeddings for semantic search.
- Retrieves up to five relevant records for a question and asks Gemini to answer using only the retrieved context.
- Provides a Streamlit chat interface for asking questions about the indexed records.

Example questions:

- What diagnosis and hospital course are documented?
- Which medications or procedures are listed?
- What follow-up instructions appear in the records?

## How it works

```text
Scanned discharge summaries
        |
        v
Tesseract OCR --> Field extraction --> MongoDB
                                      |
                                      v
                         Sentence Transformer embeddings
                                      |
                                      v
                                 Pinecone
                                      |
User question --> Semantic retrieval --> Gemini answer --> Streamlit UI
```

## Technology

- Python
- Streamlit
- Tesseract OCR and `pytesseract`
- MongoDB
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Pinecone
- Google Gemini API

## Requirements

- Python and pip
- Tesseract OCR installed on your computer and available on `PATH`
- A MongoDB connection string
- A Pinecone API key and an existing Pinecone index
- A Gemini API key

The Pinecone index must use **384 dimensions** and a similarity metric compatible with the application (the included setup example uses cosine). The embedding model downloads when first used.

## Setup

1. Clone the repository and open its directory:

   ```bash
   git clone https://github.com/AT0518/Medical-Chatbot-QA-System.git
   cd Medical-Chatbot-QA-System
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install Tesseract OCR for your operating system. Confirm that the `tesseract` executable is available on `PATH`. If it is not, configure the Tesseract executable path for `pytesseract` in `src_code/ocr.py`.

5. Create a `.env` file in the repository root using `.env.example` as a template:

   ```dotenv
   MONGODB_URI=your_mongodb_connection_string
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=medical-rag
   GEMINI_API_KEY=your_gemini_api_key
   ```

   `GOOGLE_API_KEY` is also accepted as an alternative to `GEMINI_API_KEY`. Keep real credentials private; do not commit `.env`.

6. Create a Pinecone index named as configured by `PINECONE_INDEX_NAME` (default: `medical-rag`) with dimension `384`.

## Prepare and index the sample records

The current ingestion path reads filenames from `data/discharge_summaries_ground_truth.csv` and expects the corresponding images under `data/discharge_summaries/`. The repository includes sample discharge-summary data in this layout.

With the virtual environment active and `.env` configured, run:

```bash
python -c "from src_code.main import main; print(main(create_embedding=True))"
```

This runs OCR, stores the extracted records in MongoDB, generates embeddings, and upserts them into Pinecone. Run ingestion before asking questions in the app. Ingestion inserts records into the configured MongoDB collection; avoid repeatedly running it against the same collection unless duplicate records are acceptable or you have prepared the database.

## Run the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser and ask questions in the chat.

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `MONGODB_URI` | Yes | MongoDB connection string used for medical records. |
| `PINECONE_API_KEY` | Yes | Pinecone API key. |
| `PINECONE_INDEX_NAME` | No | Pinecone index name; defaults to `medical-rag`. |
| `GEMINI_API_KEY` | Yes* | Gemini API key used to generate answers. |
| `GOOGLE_API_KEY` | Yes* | Alternative environment variable for the Gemini API key. |

\* Configure either `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

## Important limitations and privacy

- Generated answers may be incomplete or incorrect. Check important information against the original records and consult a qualified healthcare professional.
- This tool does not assess implant quality, suitability, lifespan, or whether an implant should be replaced.
- The prototype does not implement patient consent workflows, hospital identity/access controls, audit trails, or production-grade security.
- Do not use real patient-identifiable information with this prototype unless you have independently implemented and validated the required privacy, security, and legal safeguards.
- OCR and field extraction can make mistakes, especially with low-quality scans.

## Repository structure

```text
.
├── app.py                         # Streamlit chat interface
├── data/
│   ├── discharge_summaries/        # Sample discharge-summary images
│   └── discharge_summaries_ground_truth.csv
├── src_code/
│   ├── main.py                     # Ingestion and question-answering orchestration
│   ├── ocr.py                      # OCR and dataset loading
│   ├── regex_helper.py             # Discharge-summary field extraction
│   ├── mongo_helper.py             # MongoDB access
│   ├── embedding_helper.py         # Text embeddings
│   ├── pinecone_helper.py          # Vector indexing and retrieval
│   └── call_llm.py                 # Gemini API calls
├── .env.example                    # Environment-variable template
└── requirements.txt                # Python dependencies
```

## Future direction

The broader project idea is to make medical records easier to retrieve when paper copies are lost or unavailable. A future implant-record system could let authorized care teams review a patient's documented implant information with the patient's consent. That capability would require secure identity and access management, explicit consent, auditability, data governance, and clinical validation; it is not provided by this prototype.
