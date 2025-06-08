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

## Requirements

- Python 3.8+
- Install dependencies with:

   ```powershell
   pip install -r requirements.txt
   ```

PyTorch is required for running the sentiment analysis pipeline. For more details, see [PyTorch installation guide](https://pytorch.org/get-started/locally/).

## Usage

To run the sentiment analysis pipeline for all banks:

```powershell
python scripts/sentiment_analysis.py
```

## Results
- 1,200+ reviews collected with <5% missing data.
- Clean, analysis-ready CSVs for each bank and all banks combined.

---

Feel free to update this README with further analysis or results!