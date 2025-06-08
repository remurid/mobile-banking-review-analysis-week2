# scripts/collect_and_preprocess.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from utils import process_all_banks

apps = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen Bank': 'com.dashen.dashensuperapp',
}

if __name__ == "__main__":
    process_all_banks(apps, max_reviews=450, data_dir="./data")