# The Intelligent Task Automator

A Python automation tool that watches a folder for PDF invoices, reads their content, classifies them using AI, and automatically sorts and renames them into categorized folders — all running silently in the background.

## What it does

Drop any PDF invoice into the `invoices/inbox/` folder. The tool detects it instantly, extracts the text, sends it to an AI model, and moves the renamed file into the right category folder automatically.

-------------------------------------------------------------------------------------------------------------
```text
invoices/inbox/march electricity bill.pdf
                ↓
invoices/Electricity/electricity_2026-06-14_march_electricity_bill.pdf
```
-------------------------------------------------------------------------------------------------------------

## Features

- Real-time folder monitoring using watchdog
- PDF text extraction using pdfplumber
- AI-powered classification using Groq (Llama 3.3 70B)
- Auto-rename with category + date + cleaned original name
- Sorts into: Electricity, Food, Rent, Internet, Miscellaneous
- Append-only sorting log at `invoices/sorting_log.txt`
- Safe fallback to Miscellaneous if AI call fails

## Project structure

```text
The-Intelligent-Task-Automator/
│
├── config.py          # constants, paths, folder setup
├── pdf_reader.py      # PDF text extraction
├── ai_classifier.py   # Groq AI classification
├── main.py            # watchdog watcher + file sorter
│
├── .env               # your API key (not committed)
├── .gitignore
├── requirements.txt
│
└── invoices/
├── inbox/         # drop PDFs here
├── Electricity/
├── Food/
├── Rent/
├── Internet/
└── Miscellaneous/
```

## Tech stack

| Tool | Purpose |
|------|---------|
| Python 3.14 | Core language |
| watchdog | Real-time folder monitoring |
| pdfplumber | PDF text extraction |
| Groq API (Llama 3.3 70B) | Invoice classification |
| python-dotenv | Secure API key loading |
| pathlib + shutil | File path handling and moving |

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/shahid-commits/The-Intelligent-Task-Automator
cd The-Intelligent-Task-Automator
```

**2. Create and activate virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Get a free Groq API key**

```bash
Sign up at [console.groq.com](https://console.groq.com) — free tier, no credit card needed.
```

**5. Create your `.env` file**

```bash
GROQ_API_KEY=your_key_here
```

**6. Run the watcher**

```bash
python main.py
```

## Usage
```text
Once running, drop any PDF into `invoices/inbox/`. The terminal shows:

New invoice detected: food invoice march.pdf
Category: food
Moved: food_2026-06-14_food_invoice_march.pdf → Food/
Logged: food | food_2026-06-14_food_invoice_march.pdf

Press `Ctrl+C` to stop.
```

## How it works

```text
watchdog detects new PDF
        ↓
pdfplumber extracts text (first 2 pages, max 1500 chars)
        ↓
Groq AI classifies: "electricity / food / rent / internet / miscellaneous"
        ↓
File renamed: category_date_originalname.pdf
        ↓
shutil moves file to category folder
        ↓
Action logged to sorting_log.txt
```

---

Built from scratch as Project 1 of a self-directed Python learning journey — starting from zero Python knowledge.
