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

class TalentRecommendationSystem:
    """
    Sistema de recomendação de talentos usando TF-IDF e similaridade do cosseno.
    Atualizado para funcionar com dados filtrados do Streamlit.
    """

    def __init__(self, df_application, vectorizer):
        """
        Inicializa o sistema de recomendação.

        Parâmetros
        ----------
        df_application : pd.DataFrame
            DataFrame contendo os dados dos candidatos (já filtrado).
        vectorizer : TfidfVectorizer
            Vetorizador TF-IDF treinado.
        """
        self.df_application = df_application
        self.vectorizer = vectorizer

    def _vectorize_job_description(self, job_description):
        """Converte descrição da vaga em vetor TF-IDF usando o vetorizador treinado"""
        campo_vetor = 'job_description'
        df_input = pd.DataFrame({'job_description': [job_description]})
        
        # Transforma usando o mesmo vetorizador (não aplicar fit, apenas transform)
        X_tfidf_input = self.vectorizer.transform(df_input[campo_vetor].fillna(""))
        
        # Converte para formato de array
        job_vector = X_tfidf_input.toarray()[0]
        
        return job_vector

    def recommend_for_job_description(self, job_description, top_n=10):
        """
        Encontra candidatos mais similares a uma descrição de vaga.

        Parâmetros
        ----------
        job_description : str
            Descrição da vaga em texto.
        top_n : int, opcional, default=10
            Número de candidatos a retornar.

        Retorno
        -------
        results : list of dict
            Lista de dicionários com informações dos candidatos recomendados.
        """
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Converte descrição da vaga em vetor
        job_vector = self._vectorize_job_description(job_description)
        job_vector = job_vector.reshape(1, -1)  # Garante formato correto
        
        # Obtém vetores dos candidatos
        if 'vetor_cv' in self.df_application.columns:
            # Usa vetores pré-computados se disponíveis
            candidate_vectors = np.vstack([
                v if isinstance(v, np.ndarray) else np.array(v) 
                for v in self.df_application['vetor_cv'].values
            ])
        else:
            # Fallback: vetoriza texto do CV usando o vetorizador
            cv_column = self._find_cv_column()
            if cv_column:
                candidate_texts = self.df_application[cv_column].fillna("")
                candidate_vectors = self.vectorizer.transform(candidate_texts).toarray()
            else:
                raise ValueError("Nenhuma coluna de CV adequada encontrada nos dados")
        
        # Garante que as dimensões sejam compatíveis
        min_features = min(job_vector.shape[1], candidate_vectors.shape[1])
        job_vector = job_vector[:, :min_features]
        candidate_vectors = candidate_vectors[:, :min_features]
        
        # Calcula similaridade do cosseno
        similarities = cosine_similarity(job_vector, candidate_vectors)[0]

        # Seleciona os melhores candidatos
        top_indices = np.argsort(similarities)[::-1][:top_n]
        top_scores = similarities[top_indices]

        # Monta os resultados
        results = []
        for idx, score in zip(top_indices, top_scores):
            candidate_info = {
                'index': int(idx),
                'prospect_code': self.df_application.iloc[idx].get('prospect_code', f'CAND-{idx}'),
                'match_score': float(score),
                'nivel_profissional': self.df_application.iloc[idx].get('nivel_profissional', 'N/A'),
                'area_atuacao': self.df_application.iloc[idx].get('area_atuacao', 'N/A'),
                'nivel_academico': self.df_application.iloc[idx].get('nivel_academico', 'N/A'),
                'nivel_ingles': self.df_application.iloc[idx].get('nivel_ingles', 'N/A'),
                'nivel_espanhol': self.df_application.iloc[idx].get('nivel_espanhol', 'N/A'),
                'local': self.df_application.iloc[idx].get('local', 'N/A'),
                'titulo': str(self.df_application.iloc[idx].get('cv_pt_cleaned', ''))[:300] + '...'
            }
            results.append(candidate_info)

        return results
    
    def get_similar_candidates(self, candidate_idx, top_n=10, similarity_threshold=0.1):
        """Encontra candidatos similares a um candidato específico"""
        if candidate_idx >= len(self.df_application):
            return []
        
        if 'vetor_cv' not in self.df_application.columns:
            return []
            
        # Obtém vetor do candidato alvo
        target_vector = self.df_application.iloc[candidate_idx]['vetor_cv']
        if not isinstance(target_vector, np.ndarray):
            target_vector = np.array(target_vector)
        target_vector = target_vector.reshape(1, -1)
        
        # Obtém todos os vetores dos candidatos
        candidate_vectors = np.vstack([
            v if isinstance(v, np.ndarray) else np.array(v) 
            for v in self.df_application['vetor_cv'].values
        ])
        
        # Calcula similaridades
        similarities = cosine_similarity(target_vector, candidate_vectors)[0]
        
        # Remove candidato atual e aplica threshold
        similarities[candidate_idx] = -1
        valid_indices = np.where(similarities >= similarity_threshold)[0]
        
        if len(valid_indices) == 0:
            return []
        
        # Obtém candidatos mais similares
        sorted_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]][:top_n]
        
        results = []
        for idx in sorted_indices:
            candidate_info = {
                'index': int(idx),
                'prospect_code': self.df_application.iloc[idx].get('prospect_code', f'CAND-{idx}'),
                'similarity_score': float(similarities[idx]),
                'nivel_profissional': self.df_application.iloc[idx].get('nivel_profissional', 'N/A'),
                'area_atuacao': self.df_application.iloc[idx].get('area_atuacao', 'N/A'),
                'nivel_academico': self.df_application.iloc[idx].get('nivel_academico', 'N/A'),
                'nivel_ingles': self.df_application.iloc[idx].get('nivel_ingles', 'N/A'),
                'nivel_espanhol': self.df_application.iloc[idx].get('nivel_espanhol', 'N/A'),
                'local': self.df_application.iloc[idx].get('local', 'N/A'),
                'titulo': str(self.df_application.iloc[idx].get('cv_pt_cleaned', ''))[:300] + '...'
            }
            results.append(candidate_info)
        
        return results
    
    def _find_cv_column(self):
        """Encontra a melhor coluna de texto do CV no dataset"""
        possible_columns = ['cv_pt', 'cv_pt_cleaned', 'cv_text', 'cv', 'resume']
        for col in possible_columns:
            if col in self.df_application.columns:
                return col
        return None