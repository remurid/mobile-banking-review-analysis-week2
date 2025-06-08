from google_play_scraper import Sort, reviews
from google_play_scraper import reviews_all
import pandas as pd
from datetime import datetime

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
    """Save DataFrame to CSV."""
    df.to_csv(path, index=False)
