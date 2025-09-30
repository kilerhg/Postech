# Job Fit - Talent Recommendation System

## Overview

A comprehensive Streamlit application that uses advanced NLP and machine learning techniques to match job descriptions with candidate profiles. Built on top of a TF-IDF vectorization system with Portuguese language processing.

## Features

### 🔍 Job Description Matching
- Input any job description and find the best matching candidates
- AI-powered similarity scoring
- Configurable match thresholds
- Detailed candidate profiles with skills preview

### 👥 Similar Candidates
- Find candidates similar to existing profiles
- Useful for building teams or finding backup candidates
- Similarity scoring based on skills and experience

### 📊 System Analytics  
- Real-time system metrics and performance data
- Candidate distribution visualizations
- Educational and professional level analysis
- Memory usage and vocabulary statistics

## Technology Stack

- **Frontend:** Streamlit
- **ML/NLP:** scikit-learn, TF-IDF Vectorization
- **Language Processing:** NLTK, spaCy (Portuguese)
- **Visualization:** Plotly
- **Data Processing:** pandas, numpy

## Installation

1. Install dependencies:
```bash
pip install -r requirements_job_fit.txt
```

2. Download required NLTK data:
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('rslp')
```

3. Install spaCy Portuguese model:
```bash
python -m spacy download pt_core_news_sm
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run job_fit_app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Choose your mode:
   - **Job Description Matching:** Enter job requirements to find matching candidates
   - **Similar Candidates:** Find candidates similar to existing profiles  
   - **System Analytics:** View system statistics and data distributions

## Data Requirements

The application expects the following pre-processed data files:

```
/data/gold/
├── talent_vectorizer.pkl          # Pre-trained TF-IDF vectorizer
├── talent_pool_vectors_combined.parquet  # TF-IDF vectors for all candidates
└── candidate_mapping.json         # Candidate index mapping

/data/silver/processed/
└── application_processed.csv      # Cleaned candidate profiles
```

## Key Features

### Intelligent Matching Algorithm
- Uses TF-IDF vectorization with Portuguese language processing
- Cosine similarity for accurate matching
- Configurable similarity thresholds
- Memory-efficient batch processing

### User-Friendly Interface
- Clean, intuitive design
- Real-time search results
- Interactive visualizations
- Responsive layout

### Performance Optimized
- Cached model loading
- Efficient similarity computation
- Scalable architecture
- Fast response times

## Example Usage

### Job Description Matching
```
Input: "Desenvolvedor Python sênior com Django e AWS"
Output: Top matching candidates with similarity scores and skill previews
```

### Similar Candidates
```
Input: Candidate #123 (Senior Python Developer)
Output: Similar developers with comparable skills and experience
```

## Model Performance

- **Dataset Size:** 42,000+ candidate profiles
- **Vocabulary:** 10,000+ unique terms
- **Processing Time:** < 1 second for most queries
- **Memory Usage:** ~50MB for TF-IDF matrix

## Architecture

```
User Input → Text Processing → TF-IDF Vectorization → Similarity Computation → Ranked Results
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Postech Challenge 5 - Data Science specialization.
