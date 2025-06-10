# mobile-banking-review-analysis-week2

## Project Overview
This project collects, preprocesses, and analyzes user reviews for three Ethiopian banks from the Google Play Store.

## Data Collection & Preprocessing
- **Scraping:** Uses `google-play-scraper` to fetch reviews, ratings, and dates for each bank's app.
- **Preprocessing:**
  - Removes duplicates and reviews with missing/very short content.
  - Normalizes date format to `YYYY-MM-DD`.
  - Cleans review text (trims whitespace).
  - Adds metadata columns: `bank`, `source`.
- **Output:**
  - Saves a cleaned CSV for each bank in `data/` (e.g., `CBE_reviews_cleaned.csv`).
  - Combines all reviews into `data/all_banks_reviews_cleaned.csv`.

## How to Run
1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
2. Run the data collection script:
   ```powershell
   python scripts/collect_and_preprocess.py
   ```
3. Cleaned CSVs will appear in the `data/` folder.

## Methodology
- Scrape 400+ reviews per bank (CBE, BOA, Dashen Bank).
- Remove duplicates, missing, and very short reviews.
- Normalize dates and clean text.
- Save per-bank and combined CSVs for analysis.

## File Structure
- `src/utils.py`: Modular functions for scraping, cleaning, and saving reviews.
- `scripts/collect_and_preprocess.py`: Main script to run the workflow.
- `data/`: Output folder for cleaned CSVs.

## Quickstart: Run the Full Workflow in a Notebook

A Jupyter notebook is provided to run all main scripts step-by-step:

1. Open `notebooks/run_all_workflow.ipynb` in VS Code or Jupyter.
2. Run each cell in order to:
   - Collect and preprocess reviews
   - Run sentiment and thematic analysis
   - Insert analyzed data into Oracle

---

## Requirements

- Python 3.8+
- Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

- For Oracle DB:
   - Start Docker Desktop and run:
     ```powershell
     docker compose up -d
     ```
   - Create the `BANKREVIEWS` user (see below).

## Oracle User Setup

Connect as SYSDBA (see below) and run:

```sql
CREATE USER BANKREVIEWS IDENTIFIED BY "P@ssw0rd";
GRANT CONNECT, RESOURCE TO BANKREVIEWS;
ALTER USER BANKREVIEWS QUOTA UNLIMITED ON USERS;
```

## Troubleshooting
- If you see `DPY-4004: invalid number`, check for NaN or invalid values in your CSVs.
- If you see `ORA-28009`, make sure you connect as SYSDBA when creating users.
- If you see `DPI-1047`, install the Oracle Instant Client or use the pure Python `oracledb` package (already in requirements.txt).

---

## Manual Script Usage

You can also run each script individually from the terminal:

```powershell
python scripts/collect_and_preprocess.py
python scripts/sentiment_analysis.py
python scripts/insert_to_oracle.py
```

---

## Data Files
- Cleaned and analyzed CSVs are saved in the `data/` directory.

---

Feel free to update this README with further analysis or results!