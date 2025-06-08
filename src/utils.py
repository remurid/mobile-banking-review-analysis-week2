from google_play_scraper import Sort, reviews
from google_play_scraper import reviews_all
import pandas as pd
from datetime import datetime
import os

def fetch_reviews(app_id, bank_name, lang='en', country='us', n_reviews=400):
    """Fetch reviews for a single app from Google Play Store."""
    result = reviews_all(
        app_id,
        sleep_milliseconds=0,
        lang=lang,
        country=country,
        sort=Sort.NEWEST
    )
    df = pd.DataFrame(result)
    df['bank'] = bank_name
    df['source'] = 'Google Play'
    return df.head(n_reviews)

def fetch_reviews_multiple_banks(apps_info, n_reviews=400):
    """Fetch reviews for multiple banks. apps_info: list of (app_id, bank_name)"""
    all_reviews = []
    for app_id, bank_name in apps_info:
        print(f"Fetching for {bank_name}...")
        df = fetch_reviews(app_id, bank_name, n_reviews=n_reviews)
        all_reviews.append(df)
    return pd.concat(all_reviews, ignore_index=True)

def preprocess_reviews(df):
    """Remove duplicates, handle missing data, normalize dates, and select columns."""
    # Remove duplicates
    df = df.drop_duplicates(subset=['content', 'userName', 'bank'])
    # Handle missing data
    df = df.dropna(subset=['content', 'score', 'at', 'bank'])
    # Normalize date
    df['date'] = pd.to_datetime(df['at']).dt.strftime('%Y-%m-%d')
    # Select and rename columns
    df_clean = df.rename(columns={'content': 'review', 'score': 'rating'})[
        ['review', 'rating', 'date', 'bank', 'source']
    ]
    return df_clean

def save_reviews_to_csv(df, path):
    """Save DataFrame to CSV, creating parent directories if needed."""
    import os
    dir_path = os.path.dirname(path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    df.to_csv(path, index=False)

def clean_text(text):
    """Basic cleaning of review text."""
    if not isinstance(text, str):
        return ""
    return text.strip()

def preprocess_and_save_reviews(app_id, bank_name, max_reviews=400, data_dir="data"):
    """Scrape, clean, and save reviews for a single bank."""
    print(f"Scraping reviews for {bank_name}...")
    reviews = reviews_all(app_id)
    df = pd.DataFrame(reviews)
    if df.empty:
        print(f"⚠️ No reviews found for {bank_name}.")
        return None
    # Rename and select columns
    df = df.rename(columns={
        "content": "review",
        "score": "rating",
        "at": "date"
    })[["review", "rating", "date"]]
    # Clean and preprocess
    df["review"] = df["review"].astype(str).apply(clean_text)
    df["review_length"] = df["review"].apply(len)
    # Remove duplicates and short reviews
    df.drop_duplicates(subset=["review"], inplace=True)
    df.dropna(subset=["review", "rating"], inplace=True)
    df = df[df["review_length"] > 2]
    # Format dates
    df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d") if pd.notnull(x) else None)
    # Add metadata
    df["bank"] = bank_name
    df["source"] = "Google Play Store"
    # Limit to max_reviews
    count = len(df)
    if count < max_reviews:
        print(f"⚠️ Warning: Only {count} valid reviews scraped for {bank_name}.")
    else:
        df = df.head(max_reviews)
        print(f"✅ Collected {max_reviews} reviews for {bank_name}.")
    # Ensure data directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    # Save to CSV
    filename = os.path.join(data_dir, f"{bank_name}_reviews_cleaned.csv")
    df.to_csv(filename, index=False)
    print(f"💾 Saved cleaned reviews to {filename}\n")
    return df

def process_all_banks(apps, max_reviews=400, data_dir="data"):
    """Process all banks and save combined CSV."""
    all_dfs = []
    for bank_name, app_id in apps.items():
        df = preprocess_and_save_reviews(app_id, bank_name, max_reviews, data_dir)
        if df is not None:
            all_dfs.append(df)
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_path = os.path.join(data_dir, "all_banks_reviews_cleaned.csv")
        combined_df.to_csv(combined_path, index=False)
        print(f"✅ Saved combined cleaned reviews for all banks to {combined_path}")
    else:
        print("❌ No reviews processed for any bank.")
