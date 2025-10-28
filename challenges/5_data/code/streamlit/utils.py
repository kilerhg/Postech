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
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import glob
import spacy.cli
import spacy

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download('rslp')
# spacy.cli.download("pt_core_news_sm")

# inicializa stemmer
from nltk.stem import RSLPStemmer
stemmer = RSLPStemmer()

# carregar modelo para português
# nlp = spacy.load("pt_core_news_sm")

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

# def remove_person_names(text: str) -> str:
#     doc = nlp(text)
#     return " ".join([token.text for token in doc if token.ent_type_ != "PER"])

def tokenizer(text: str):
    stop_words_br = set(nltk.corpus.stopwords.words("portuguese"))
    #stop_words_en = set(nltk.corpus.stopwords.words("english"))
    if isinstance(text, str):
        text = normalize_str(text)                                              # normaliza string
        # text = remove_person_names(text)                                        # remove nomes
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

def job_description_vector(cv_input, vectorizer):

    campo_vetor = 'cv_pt'

    # Ensure cv_input is a list, even if it's a single string
    if isinstance(cv_input, str):
        cv_input = [cv_input]

    df_input = pd.DataFrame({'cv_pt': cv_input})

    # Transformar usando o mesmo vetorizador (não aplicar fit, apenas transform)
    X_tfidf_input = vectorizer.transform(df_input[campo_vetor].fillna(""))

    # Converter para formato de array e armazenar em um DataFrame
    df_input_job_desc = pd.DataFrame({
        'vetor_cv': [X_tfidf_input.toarray()[0]]  # Armazena o vetor completo
    })
    df_input_job_desc = df_input_job_desc.reset_index(drop=True)
    return df_input_job_desc

class TalentRecommendationSystem:
    """
    Classe para recomendação de candidatos com base em similaridade de texto
    utilizando vetores TF-IDF e similaridade do cosseno.
    """

    def __init__(self, df_tfidf, df_tfidf_input, vectorizer):
        """
        Inicializa o sistema de recomendação.

        Parâmetros
        ----------
        df_tfidf : pd.DataFrame
            DataFrame contendo os vetores TF-IDF dos candidatos.
        df_tfidf_input : pd.DataFrame
            DataFrame contendo o vetor TF-IDF da descrição de vaga.
        vectorizer : TfidfVectorizer
            Vetorizador usado para transformar os textos.
        """
        self.df_tfidf = df_tfidf
        self.df_tfidf_input = df_tfidf_input
        self.vectorizer = vectorizer
        self.similarity_cache = {}

    def recommend_for_job_description(self, top_n=10):
        """
        Encontra os candidatos mais similares a uma descrição de vaga.

        Parâmetros
        ----------
        top_n : int, opcional, default=10
            Número de candidatos a retornar.

        Retorno
        -------
        results : list of dict
            Lista de dicionários com informações dos candidatos recomendados.
        """
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Obtém o vetor da vaga e garante o formato correto
        job_vector = self.df_tfidf_input['vetor_cv'].values[0]
        if len(job_vector.shape) == 1:
            job_vector = job_vector.reshape(1, -1)
            
        # Obtém os vetores dos candidatos e garante o formato correto
        candidate_vectors = np.vstack([v for v in self.df_tfidf['vetor_cv'].values])
        
        # Force candidate_vectors to fit job_vector size
        job_vector_size = job_vector.shape[1]
        candidate_vector_size = candidate_vectors.shape[1]
        
        if job_vector_size != candidate_vector_size:
            if job_vector_size < candidate_vector_size:
                # Truncate candidate vectors to match job vector size
                candidate_vectors = candidate_vectors[:, :job_vector_size]
            else:
                # Pad candidate vectors with zeros to match job vector size
                padding = np.zeros((candidate_vectors.shape[0], job_vector_size - candidate_vector_size))
                candidate_vectors = np.hstack([candidate_vectors, padding])
        
        # Calcula a similaridade com todos os candidatos
        similarities = cosine_similarity(job_vector, candidate_vectors)[0]

        # Seleciona os melhores candidatos
        top_indices = np.argsort(similarities)[::-1][:top_n]
        top_scores = similarities[top_indices]

        # Monta os resultados
        results = []
        for idx, score in zip(top_indices, top_scores):
            candidate_info = {
                'index': int(idx),
                'match_score': float(score),
                'nivel_profissional': self.df_tfidf.iloc[idx].get('nivel_profissional', 'N/A'),
                'area_atuacao': self.df_tfidf.iloc[idx].get('area_atuacao', 'N/A'),
                'nivel_academico': self.df_tfidf.iloc[idx].get('nivel_academico', 'N/A'),
                'conhecimentos_preview': str(self.df_tfidf.iloc[idx].get('cv_pt', ''))[:200] + '...'
            }
            results.append(candidate_info)

        return results