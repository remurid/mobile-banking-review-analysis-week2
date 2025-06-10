import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# Utility functions for insights and visualization

def load_data(path=None):
    # Always resolve to absolute path for robustness
    if path is None:
        path = os.path.abspath(os.path.join('data', 'all_banks_reviews_analyzed.csv'))
    else:
        path = os.path.abspath(path)
    if not os.path.exists(path):
        print(f"File not found: {path}\nPlease run the 'run_all_workflow.ipynb' notebook to generate the analyzed data file.")
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)

def get_sentiment_counts(df, by='bank'):
    return df.groupby([by, 'sentiment_label']).size().unstack(fill_value=0)

def plot_sentiment_bar(sentiment_counts, save_path=None):
    ax = sentiment_counts.plot(kind='bar', stacked=True, figsize=(10,6))
    plt.title('Sentiment Distribution by Bank')
    plt.ylabel('Number of Reviews')
    plt.xlabel('Bank')
    plt.legend(title='Sentiment')
    plt.tight_layout()
    if save_path:
        dir_path = os.path.dirname(save_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        plt.savefig(save_path)
    plt.show()

def plot_rating_distribution(df, by='bank', save_path=None):
    plt.figure(figsize=(10,6))
    sns.boxplot(x=by, y='rating', data=df)
    plt.title('Rating Distribution by Bank')
    plt.ylabel('Rating')
    plt.xlabel('Bank')
    plt.tight_layout()
    if save_path:
        dir_path = os.path.dirname(save_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        plt.savefig(save_path)
    plt.show()

def plot_keyword_cloud(df, bank=None, save_path=None):
    if bank:
        text = ' '.join(df[df['bank'] == bank]['review_clean'].dropna().astype(str))
    else:
        text = ' '.join(df['review_clean'].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Keyword Cloud {f"for {bank}" if bank else "(All Banks)"}')
    if save_path:
        dir_path = os.path.dirname(save_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        plt.savefig(save_path)
    plt.show()

def get_top_themes(df, n=5, by='bank'):
    from collections import Counter
    result = {}
    for bank in df[by].unique():
        themes = df[df[by]==bank]['themes'].dropna().astype(str).str.split(', ')
        flat = [item for sublist in themes for item in sublist]
        counts = Counter(flat)
        result[bank] = counts.most_common(n)
    return result

def get_drivers_and_pain_points(df, by='bank'):
    # Example: drivers = most common themes in POSITIVE, pain points = most common in NEGATIVE
    result = {}
    for bank in df[by].unique():
        pos = df[(df[by]==bank) & (df['sentiment_label']=='POSITIVE')]['themes'].dropna().astype(str).str.split(', ')
        neg = df[(df[by]==bank) & (df['sentiment_label']=='NEGATIVE')]['themes'].dropna().astype(str).str.split(', ')
        pos_flat = [item for sublist in pos for item in sublist]
        neg_flat = [item for sublist in neg for item in sublist]
        from collections import Counter
        drivers = Counter(pos_flat).most_common(2)
        pain_points = Counter(neg_flat).most_common(2)
        result[bank] = {'drivers': drivers, 'pain_points': pain_points}
    return result
