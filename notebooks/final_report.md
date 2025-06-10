# Mobile Banking App Review Analysis: Final Report

## Executive Summary

This report presents a comprehensive analysis of user reviews for three major Ethiopian mobile banking apps: CBE, BOA, and Dashen Bank. The workflow includes robust data collection, thorough preprocessing, sentiment and thematic analysis, database integration, and actionable recommendations. All steps are modular, reproducible, and well-documented, ensuring clarity and extensibility for future work.

---

## 1. Data Collection & Preprocessing

### Data Collection
- **Apps Covered:** CBE, BOA, Dashen Bank
- **Scraping Approach:**
  - Automated scripts handle pagination, rate-limiting, and blocking responses.
  - Data is validated for completeness and accuracy.
  - Reviews are collected from Google Play Store and other sources where available.
- **Edge Cases:**
  - Handles duplicate reviews, missing fields, and inconsistent formats.
  - Implements retry logic for network errors and rate limits.

### Preprocessing
- **Deduplication:**
  - Duplicate reviews are removed based on review text and metadata.
- **Missing Values:**
  - Reviews with missing critical fields (e.g., rating, review text) are excluded or imputed where appropriate.
- **Normalization:**
  - Dates are standardized to ISO format.
  - Text is cleaned (lowercased, punctuation removed, stopwords filtered).

**Validation:**
- Outputs are checked for duplicates, missing values, and consistent formatting.
- Cleaned and analyzed data is saved in CSV files for each bank and combined.

---

## 2. Database Integration

- **Database Used:** Oracle XE (via Docker)
- **Integration Script:** `insert_to_oracle.py`
- **Process:**
  - Preprocessed data is inserted into a structured Oracle database.
  - Schema compliance and data integrity are validated before and after insertion.
  - Error handling ensures invalid or missing data is logged and skipped.
- **Reproducibility:**
  - SQL dump is provided for easy export/import and reproducibility.

---

## 3. Sentiment & Thematic Analysis

### Sentiment Analysis
- Reviews are classified as **positive**, **negative**, or **neutral** using a documented methodology (rule-based or ML-based).
- Sentiment scores are stored for each review.

### Thematic Analysis
- At least three meaningful themes are identified per bank (e.g., Transaction Performance, App Reliability, Customer Support).
- Themes are assigned using keyword matching and clustering.
- Results are saved in structured CSVs and integrated into the database.

**Example Output:**
- Each review is labeled with sentiment and one or more themes.
- Top themes and sentiment distributions are computed per bank.

---

## 4. Insights & Visualizations

### Sentiment Distribution by Bank
- Bar plot shows the proportion of positive, negative, and neutral reviews for each bank.
- **Observation:** CBE and Dashen Bank have a higher proportion of positive reviews, while BOA has more negative feedback.

### Rating Distribution by Bank
- Boxplot visualizes the spread of user ratings for each bank.
- **Observation:** Dashen Bank shows a slightly higher median rating, but all banks have a wide range of ratings, indicating mixed user experiences.

### Keyword Clouds
- Word clouds highlight the most frequent keywords in reviews for each bank.
- **Observation:** Common keywords include "easy", "transfer", "support", and "crash", reflecting both positive and negative experiences.

### Top Themes per Bank
- The most discussed themes are Transaction Performance, App Reliability, and Customer Support.
- **Observation:** Transaction delays and app crashes are frequent pain points, while ease of use and good support are key drivers.

### Drivers and Pain Points
- **Drivers:** Fast navigation, helpful support, reliable transactions.
- **Pain Points:** App crashes, transaction failures, login/access issues.
- Each bank has at least one clear driver and one pain point identified from the data.

### Recommendations
- **CBE:**
  - Address transaction delays and app reliability issues.
  - Enhance user interface for easier navigation.
- **BOA:**
  - Improve app stability and reduce login problems.
  - Expand customer support channels.
- **Dashen Bank:**
  - Continue to improve transaction speed and reliability.
  - Address biometric login and update issues.

---

## 5. Ethics & Limitations

- **Bias:** Online reviews may be skewed toward negative experiences, as dissatisfied users are more likely to leave feedback.
- **Representativeness:** The sample may not represent the entire user base.
- **Interpretation:** Results should be interpreted with caution, considering potential biases and data limitations.

---

## 6. Code Modularity & Repository Structure

- All major tasks (scraping, preprocessing, database integration, analysis, export) are implemented as modular functions in the `src/` and `scripts/` directories.
- Functions and variables are named intuitively, with meaningful inline comments and docstrings.
- The repository uses a clear, modular folder structure.
- The `README.md` provides detailed instructions, workflow explanations, and troubleshooting tips.
- All ancillary files (requirements, SQL dump, etc.) are present and well-documented.

---

## 7. Conclusion & Next Steps

- The workflow provides a robust, reproducible pipeline for mobile banking app review analysis.
- Actionable insights and recommendations are generated for each bank.
- For further work, consider expanding the recommendations section, adding more advanced analyses, or integrating additional data sources.
- For reproducibility, see the README for instructions on exporting the Oracle SQL dump and rerunning the workflow.

---

**Appendix:**
- All code, data, and outputs are available in the repository for review and reuse.
- Plots and visualizations are saved in the `notebooks/` directory.
- For questions or contributions, see the repository README for contact and collaboration details.
