<<<<<<< HEAD
from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import re

def clean_text(text: str) -> str:
    # Remove headers, footers, and quotes as per requirements
    # This prevents the model from overfitting on metadata
    text = re.sub(r'(From:\s+.*\n?)|(Subject:\s+.*\n?)|(Reply-To:\s+.*\n?)|(Organization:\s+.*\n?)', '', text)
    text = re.sub(r'Lines:\s+\d+', '', text)
    text = re.sub(r'(\n|>).*\s?writes:', '', text)
    text = re.sub(r'--\n(.*\n)*', '', text)
    return text.strip()

def load_news_data(subset='all'):
    # Loading 20 newsgroups; subset='all' gives us ~18k-20k docs
    data = fetch_20newsgroups(subset=subset, remove=('headers', 'footers', 'quotes'))
    df = pd.DataFrame({'text': data.data})
    df['text'] = df['text'].apply(clean_text)
    # Filter out empty or extremely short strings
    df = df[df['text'].str.len() > 20].reset_index(drop=True)
=======
from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import re

def clean_text(text: str) -> str:
    # Remove headers, footers, and quotes as per requirements
    # This prevents the model from overfitting on metadata
    text = re.sub(r'(From:\s+.*\n?)|(Subject:\s+.*\n?)|(Reply-To:\s+.*\n?)|(Organization:\s+.*\n?)', '', text)
    text = re.sub(r'Lines:\s+\d+', '', text)
    text = re.sub(r'(\n|>).*\s?writes:', '', text)
    text = re.sub(r'--\n(.*\n)*', '', text)
    return text.strip()

def load_news_data(subset='all'):
    # Loading 20 newsgroups; subset='all' gives us ~18k-20k docs
    data = fetch_20newsgroups(subset=subset, remove=('headers', 'footers', 'quotes'))
    df = pd.DataFrame({'text': data.data})
    df['text'] = df['text'].apply(clean_text)
    # Filter out empty or extremely short strings
    df = df[df['text'].str.len() > 20].reset_index(drop=True)
>>>>>>> fd552f28aad4f45ea86cd8f3991a2913752c2073
    return df['text'].tolist()