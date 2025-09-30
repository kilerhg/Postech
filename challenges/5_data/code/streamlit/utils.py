import numpy as np
import pandas as pd
import re
import nltk
nltk.download("stopwords")
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
import time
import string
import unicodedata
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
import multiprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import glob
import spacy.cli
import spacy

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download('rslp')
spacy.cli.download("pt_core_news_sm")

# inicializa stemmer
from nltk.stem import RSLPStemmer
stemmer = RSLPStemmer()

# carregar modelo para português
nlp = spacy.load("pt_core_news_sm")

def normalize_accents(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")

def remove_punctuation(text: str) -> str:
    table = str.maketrans({key: " " for key in string.punctuation})
    return text.translate(table)

def normalize_str(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\d+", " ", text)           # remove números
    text = remove_punctuation(text)            # remove pontuação
    text = normalize_accents(text)             # remove acentos
    text = re.sub(r"\s+", " ", text).strip()   # normaliza espaços
    return text

def remove_person_names(text: str) -> str:
    doc = nlp(text)
    return " ".join([token.text for token in doc if token.ent_type_ != "PER"])

def tokenizer(text: str):
    stop_words_br = set(nltk.corpus.stopwords.words("portuguese"))
    #stop_words_en = set(nltk.corpus.stopwords.words("english"))
    if isinstance(text, str):
        text = normalize_str(text)                                              # normaliza string
        text = remove_person_names(text)                                        # remove nomes
        tokens = word_tokenize(text, language="portuguese")                     # tokeniza para a lingua portuguesa
        tokens = [t for t in tokens if t not in stop_words_br and len(t) > 2]
        #tokens = [t for t in tokens if t not in stop_words_en and len(t) > 2]
        tokens = [stemmer.stem(t) for t in tokens]                              # stemiza tokens
        return tokens
    return None

def tokenize_and_vectorize_fixed(df, fitted_vectorizer, filename_prefix, batch_idx):
    """Transform batch using the pre-fitted vectorizer"""
    # Transform (not fit_transform) to use existing vocabulary
    vector_matrix = fitted_vectorizer.transform(df["cv_pt_cleaned"].fillna(""))
    
    # Convert to DataFrame with consistent column names
    df_tfidf = pd.DataFrame(
        vector_matrix.toarray(), 
        columns=fitted_vectorizer.get_feature_names_out(),
        index=df.index  # Preserve original indices
    )
    
    # Save batch
    output_file = f"{filename_prefix}_batch_{batch_idx}.parquet"
    df_tfidf.to_parquet(output_file)
    print(f"Saved batch {batch_idx} with shape {df_tfidf.shape} to {output_file}")
    
    return df_tfidf

# Step 4: Efficient similarity computation for large datasets
def compute_similarity_batched(df_tfidf, batch_size_sim=500, output_prefix='similarity_batch'):
    """Compute cosine similarity in batches to handle large datasets"""
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    n_samples = len(df_tfidf)
    print(f"Computing similarity for {n_samples} samples in batches of {batch_size_sim}")
    
    # Create similarity matrix in batches to manage memory
    similarity_files = []
    
    for i in range(0, n_samples, batch_size_sim):
        batch_end = min(i + batch_size_sim, n_samples)
        batch_data = df_tfidf.iloc[i:batch_end]
        
        # Compute similarity between this batch and ALL data
        batch_similarity = cosine_similarity(batch_data, df_tfidf)
        
        # Save batch similarity
        batch_file = f'/home/lucas-nunes/workspace/Postech/challenges/5_data/data/gold/{output_prefix}_{i}_{batch_end}.npy'
        np.save(batch_file, batch_similarity)
        similarity_files.append(batch_file)
        
        print(f"Computed similarity batch {i}-{batch_end}: {batch_similarity.shape}")
    
    return similarity_files