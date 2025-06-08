# sentiment_analysis.py
"""
Script and class for sentiment and thematic analysis of bank app reviews.
"""
import os
import pandas as pd
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from collections import Counter

class ReviewAnalyzer:
    def __init__(self, data_path, bank_name, out_dir="./data"):
        self.data_path = data_path
        self.bank_name = bank_name
        self.out_dir = out_dir
        self.df = pd.read_csv(data_path)
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.nlp = spacy.load("en_core_web_sm")

    def preprocess(self):
        self.df["review_clean"] = self.df["review"].astype(str).str.lower().str.replace(r"[^a-z0-9\s]", "", regex=True)

    def analyze_sentiment(self):
        results = self.sentiment_analyzer(self.df["review"].tolist(), truncation=True)
        self.df["sentiment_label"] = [r["label"] for r in results]
        self.df["sentiment_score"] = [r["score"] for r in results]

    def extract_keywords(self, top_n=15):
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=1000)
        X = vectorizer.fit_transform(self.df["review_clean"])
        tfidf_scores = X.sum(axis=0).A1
        keywords = [k for k, _ in sorted(zip(vectorizer.get_feature_names_out(), tfidf_scores), key=lambda x: -x[1])][:top_n]
        self.keywords = keywords
        return keywords

    def cluster_themes(self):
        # Simple rule-based grouping for demonstration
        themes = {
            "Account Access Issues": ["login", "log in", "sign in", "password", "access", "locked"],
            "Transaction Performance": ["transfer", "transaction", "send", "receive", "delay", "slow"],
            "User Interface & Experience": ["ui", "interface", "design", "easy", "difficult", "navigate", "user friendly"],
            "Customer Support": ["support", "help", "customer", "service", "branch", "staff"],
            "App Reliability": ["crash", "bug", "error", "issue", "problem", "fix", "update"]
        }
        def assign_theme(text):
            found = []
            for theme, keys in themes.items():
                for k in keys:
                    if k in text:
                        found.append(theme)
                        break
            return ", ".join(found) if found else "Other"
        self.df["themes"] = self.df["review_clean"].apply(assign_theme)

    def save_results(self):
        out_path = os.path.join(self.out_dir, f"{self.bank_name}_reviews_analyzed.csv")
        self.df.to_csv(out_path, index=False)
        print(f"Saved analysis to {out_path}")

    def run_pipeline(self):
        self.preprocess()
        self.analyze_sentiment()
        self.extract_keywords()
        self.cluster_themes()
        self.save_results()

if __name__ == "__main__":
    # Example usage for all banks
    banks = [
        ("./data/CBE_reviews_cleaned.csv", "CBE"),
        ("./data/BOA_reviews_cleaned.csv", "BOA"),
        ("./data/Dashen Bank_reviews_cleaned.csv", "Dashen Bank"),
    ]
    for path, name in banks:
        analyzer = ReviewAnalyzer(path, name)
        analyzer.run_pipeline()
