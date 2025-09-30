import os
import json
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random


# App configuration
apptitle = 'Postech Job Fit - Talent Recommendation System'
st.set_page_config(page_title=apptitle, page_icon="🎯", layout="wide")

dir_path = os.path.dirname(os.path.realpath(__file__))

full_path_joblib = os.path.join(dir_path, 'candidate_mapping.json')

# Load glossary mappings
@st.cache_data
def load_glossary():
    """Load candidate mapping glossary from JSON file"""
    try:
        with open(os.path.join(dir_path, 'candidate_mapping.json'), 'r', encoding='utf-8') as f:
            glossary = json.load(f)
        st.success(f"✅ Loaded glossary with {len(glossary)} mapping categories")
        return glossary
    except Exception as e:
        st.error(f"Error loading glossary: {str(e)}")
        # Return empty glossary as fallback
        return {
            "senioridade_group": {},
            "senioridade_lvl": {},
            "idioma_nvl": {},
            "nivel_academico_lvl": {}
        }

# Load real data for UI testing
@st.cache_data
def load_real_data():
    """Load real candidate data from parquet file"""
    try:
        # Load the parquet file
        
        df_full = pd.read_parquet(os.path.join(dir_path, 'df_join_prospect_base.parquet'))
        
        # Take first 100 records
        df_candidates = df_full.head(100).copy()
        
        # Add index and prospect_code if not present
        if 'index' not in df_candidates.columns:
            df_candidates['index'] = range(len(df_candidates))
        
        if 'prospect_code' not in df_candidates.columns:
            df_candidates['prospect_code'] = [f"PRSP-2025-{i+1:04d}" for i in range(len(df_candidates))]
        
        # Ensure required columns exist, fill with defaults if missing
        required_columns = {
            'nivel_profissional': 'N/A',
            'area_atuacao': 'N/A', 
            'nivel_academico': 'N/A',
            'nivel_ingles': 'N/A',
            'nivel_espanhol': 'N/A',
            'sexo': 'N/A',
            'pcd': 'Não',
            'conhecimentos_tecnicos': 'N/A',
            'cv_pt_cleaned': 'N/A',
            'titulo_profissional': 'N/A',
            'objetivo_profissional': 'N/A',
            'local': 'N/A',
            'remuneracao_numeric': 0
        }
        
        for col, default_value in required_columns.items():
            if col not in df_candidates.columns:
                df_candidates[col] = default_value
            else:
                # Fill NaN values with defaults
                df_candidates[col] = df_candidates[col].fillna(default_value)
        
        st.success(f"✅ Loaded {len(df_candidates)} real candidate records from parquet file")
        
        return df_candidates
        
    except Exception as e:
        st.error(f"Error loading data from parquet file: {str(e)}")
        st.info("Falling back to mock data generation...")
        return generate_mock_data()

# Generate mock data for UI testing (fallback)
@st.cache_data
def generate_mock_data():
    """Generate mock candidate data for UI development (fallback)"""
    np.random.seed(42)
    
    # Define realistic options
    niveis_profissionais = ['Junior', 'Pleno', 'Senior', 'Especialista', 'Coordenador', 'Gerente', 'Analista']
    areas_atuacao = ['Tecnologia da Informação', 'Desenvolvimento de Software', 'Análise de Sistemas', 
                     'Banco de Dados', 'Infraestrutura', 'Data Science', 'DevOps', 'Frontend', 'Backend']
    niveis_academicos = ['Superior Completo', 'Pós-graduação', 'MBA', 'Mestrado', 'Superior Incompleto']
    niveis_ingles = ['Básico', 'Intermediário', 'Avançado', 'Fluente']
    
    # Skills pool
    skills_pool = [
        'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'PostgreSQL', 'MongoDB',
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'Git', 'Linux', 'Django', 'Flask',
        'Machine Learning', 'Data Science', 'Pandas', 'NumPy', 'TensorFlow', 'Scikit-learn',
        'HTML', 'CSS', 'Vue.js', 'Angular', 'Spring Boot', 'Microservices', 'REST API'
    ]
    
    mock_candidates = []
    for i in range(100):  # Generate 100 mock candidates
        nivel = np.random.choice(niveis_profissionais)
        area = np.random.choice(areas_atuacao)
        academico = np.random.choice(niveis_academicos)
        ingles = np.random.choice(niveis_ingles)
        
        # Additional fields for filtering
        espanhol = np.random.choice(['Básico', 'Intermediário', 'Avançado', 'Fluente'])
        sexo = np.random.choice(['Masculino', 'Feminino'])
        pcd = np.random.choice(['Sim', 'Não'], p=[0.1, 0.9])  # 10% PCD representation
        
        # Generate random location from the new location options
        locations = ["", "são paulo", "minas gerais", "rio de janeiro", "paraná", "ceará", "bahia", "distrito federal", "rio grande do sul", "mato grosso", "amapá", "pernambuco", "santa catarina", "goiás", "mato grosso do sul", "paraíba", "alagoas", "sergipe", "rio grande do norte", "maranhão", "piauí", "amazonas", "pará", "tocantins", "rondônia", "roraima", "acre"]
        local = np.random.choice(locations)
        
        # Generate prospect code (unique identifier)
        # Format: PRSP-YYYY-NNNN (PRSP = Prospect, YYYY = year, NNNN = sequential number)
        prospect_code = f"PRSP-2025-{i+1:04d}"
        
        n_skills = np.random.randint(3, 8)
        skills = np.random.choice(skills_pool, size=n_skills, replace=False)
        skills_text = ', '.join(skills)
        
        cv_text = f"Profissional {nivel.lower()} com experiência em {area.lower()}. " \
                  f"Conhecimentos em {skills_text}. Formação: {academico}. Inglês {ingles.lower()}."
        
        candidate = {
            'index': i,
            'prospect_code': prospect_code,
            'nivel_profissional': nivel,
            'area_atuacao': area,
            'nivel_academico': academico,
            'nivel_ingles': ingles,
            'nivel_espanhol': espanhol,
            'sexo': sexo,
            'pcd': pcd,
            'conhecimentos_tecnicos': skills_text,
            'cv_pt_cleaned': cv_text,
            'titulo_profissional': f"{nivel} {area}",
            'objetivo_profissional': f"Atuar como {nivel.lower()} em {area.lower()}",
            'local': local,
            'remuneracao_numeric': np.random.randint(3000, 15000)
        }
        mock_candidates.append(candidate)
    
    return pd.DataFrame(mock_candidates)

# Mock recommendation system for UI development
class MockTalentRecommendationSystem:
    def __init__(self, df_application):
        self.df_application = df_application
        
    def get_similar_candidates(self, candidate_idx, top_n=10, similarity_threshold=0.1):
        """Mock similar candidates with random similarity scores"""
        if candidate_idx >= len(self.df_application):
            return []
        
        # Generate random similar candidates
        available_indices = list(range(len(self.df_application)))
        available_indices.remove(candidate_idx)  # Remove self
        
        n_results = min(top_n, len(available_indices))
        similar_indices = random.sample(available_indices, n_results)
        
        results = []
        for idx in similar_indices:
            # Generate random similarity score above threshold
            score = random.uniform(similarity_threshold, 0.95)
            
            candidate_info = {
                'index': idx,
                'prospect_code': self.df_application.iloc[idx]['prospect_code'],
                'similarity_score': score,
                'nivel_profissional': self.df_application.iloc[idx]['nivel_profissional'],
                'area_atuacao': self.df_application.iloc[idx]['area_atuacao'],
                'nivel_academico': self.df_application.iloc[idx]['nivel_academico'],
                'nivel_ingles': self.df_application.iloc[idx]['nivel_ingles'],
                'nivel_espanhol': self.df_application.iloc[idx]['nivel_espanhol'],
                'local': self.df_application.iloc[idx]['local'],
                'titulo': self.df_application.iloc[idx]['cv_pt_cleaned'][:300] + '...'
            }
            results.append(candidate_info)
        
        # Sort by similarity score
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results
    
    def recommend_for_job_description(self, job_description, top_n=10):
        """Mock job matching with random match scores"""
        # Generate random candidates with match scores
        available_indices = list(range(len(self.df_application)))
        n_results = min(top_n, len(available_indices))
        selected_indices = random.sample(available_indices, n_results)
        
        results = []
        for idx in selected_indices:
            # Generate random match score (higher for senior roles)
            base_score = random.uniform(0.1, 0.9)
            if 'Senior' in self.df_application.iloc[idx]['nivel_profissional']:
                base_score = max(base_score, random.uniform(0.4, 0.9))
            
            candidate_info = {
                'index': idx,
                'prospect_code': self.df_application.iloc[idx]['prospect_code'],
                'match_score': base_score,
                'nivel_profissional': self.df_application.iloc[idx]['nivel_profissional'],
                'area_atuacao': self.df_application.iloc[idx]['area_atuacao'],
                'nivel_academico': self.df_application.iloc[idx]['nivel_academico'],
                'nivel_ingles': self.df_application.iloc[idx]['nivel_ingles'],
                'nivel_espanhol': self.df_application.iloc[idx]['nivel_espanhol'],
                'local': self.df_application.iloc[idx]['local'],
                'titulo': self.df_application.iloc[idx]['titulo'][:300] + '...'
            }
            results.append(candidate_info)
        
        # Sort by match score
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results

def standardize_candidate_data(df, glossary):
    """Apply glossary mappings to standardize candidate data"""
    df_standardized = df.copy()
    
    # Standardize seniority levels using senioridade_group mapping
    if 'senioridade_group' in glossary:
        seniority_mapping = glossary['senioridade_group']
        df_standardized['nivel_profissional_std'] = df_standardized['nivel_profissional'].map(
            lambda x: seniority_mapping.get(x, x) if pd.notna(x) else x
        )
    
    # Add numeric levels for sorting and filtering
    if 'senioridade_lvl' in glossary:
        seniority_levels = glossary['senioridade_lvl']
        df_standardized['seniority_level'] = df_standardized['nivel_profissional_std'].map(
            lambda x: seniority_levels.get(x, 0) if pd.notna(x) else 0
        )
    
    if 'idioma_nvl' in glossary:
        language_levels = glossary['idioma_nvl']
        df_standardized['english_level'] = df_standardized['nivel_ingles'].map(
            lambda x: language_levels.get(x, 0) if pd.notna(x) else 0
        )
        df_standardized['spanish_level'] = df_standardized['nivel_espanhol'].map(
            lambda x: language_levels.get(x, 0) if pd.notna(x) else 0
        )
    
    if 'nivel_academico_lvl' in glossary:
        academic_levels = glossary['nivel_academico_lvl']
        df_standardized['academic_level'] = df_standardized['nivel_academico'].map(
            lambda x: academic_levels.get(x, 0) if pd.notna(x) else 0
        )
    
    return df_standardized

def create_match_score_gauge(score, title="Match Score"):
    """Create a gauge chart for match scores"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,  # Convert to percentage
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': 'red'},
                {'range': [30, 60], 'color': 'orange'},
                {'range': [60, 80], 'color': 'yellow'},
                {'range': [80, 100], 'color': 'green'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(t=30, b=0, l=0, r=0))
    return fig

def main():
    st.title('🎯 Job Fit - Talent Recommendation System')
    st.markdown("**Find the best talent matches for your job descriptions or discover similar candidates**")
    
    # Load glossary and real data for development
    st.info("📊 **Real Data Mode** - Loading candidate data and glossary")
    
    with st.spinner('Loading glossary and candidate data...'):
        glossary = load_glossary()
        df_application = load_real_data()

    st.info("""
        **Como funciona:**
        
        1. Digite a descrição da vaga
        2. Configure os filtros ao lado
        3. Nossa IA analisa e encontra candidatos
        4. Resultados rankeados por compatibilidade
        """)
    
    # Initialize mock recommendation system
    talent_recommender = MockTalentRecommendationSystem(df_application)
    
    # Standardize candidate data using glossary
    df_application_std = standardize_candidate_data(df_application, glossary)
    
    # Main Job Description Matching Interface
    st.header("🔍 Find Candidates for Job Description")
    
    # Sidebar Filters
    st.sidebar.header("🔧 Filtros")
    
    # General Filters
    st.sidebar.markdown("### Filtros Gerais")
    
    # Local filter
    local_options = ["Todos", "são paulo", "minas gerais", "rio de janeiro", "paraná", "ceará", "bahia", "distrito federal", "rio grande do sul", "mato grosso", "amapá", "pernambuco", "santa catarina", "goiás", "mato grosso do sul", "paraíba", "alagoas", "sergipe", "rio grande do norte", "maranhão", "piauí", "amazonas", "pará", "tocantins", "rondônia", "roraima", "acre"]
    saved_local = st.session_state.get('local_filter', 'Todos')
    local_index = 0 if st.session_state.get('filters_reset', False) else (local_options.index(saved_local) if saved_local in local_options else 0)
    local_filter = st.sidebar.selectbox(
        "Local:",
        local_options,
        index=local_index,
        help="Filtrar por localização",
        key="local_filter"
    )
    
    # Academic level filter (using glossary values)
    academic_levels = ["Todos"] + list(glossary.get('nivel_academico_lvl', {}).keys())
    saved_academic = st.session_state.get('nivel_academico_filter', 'Todos')
    academic_index = 0 if st.session_state.get('filters_reset', False) else (academic_levels.index(saved_academic) if saved_academic in academic_levels else 0)
    nivel_academico_filter = st.sidebar.selectbox(
        "Nível Acadêmico:",
        academic_levels,
        index=academic_index,
        help="Filtrar por nível de educação (valores padronizados)",
        key="nivel_academico_filter"
    )
    
    # English level filter (using glossary values)
    language_levels = ["Todos"] + list(glossary.get('idioma_nvl', {}).keys())
    saved_english = st.session_state.get('nivel_ingles_filter', 'Todos')
    english_index = 0 if st.session_state.get('filters_reset', False) else (language_levels.index(saved_english) if saved_english in language_levels else 0)
    nivel_ingles_filter = st.sidebar.selectbox(
        "Nível de Inglês:",
        language_levels,
        index=english_index,
        help="Filtrar por nível de inglês (valores padronizados)",
        key="nivel_ingles_filter"
    )
    
    # Spanish level filter (using glossary values)
    saved_spanish = st.session_state.get('nivel_espanhol_filter', 'Todos')
    spanish_index = 0 if st.session_state.get('filters_reset', False) else (language_levels.index(saved_spanish) if saved_spanish in language_levels else 0)
    nivel_espanhol_filter = st.sidebar.selectbox(
        "Nível de Espanhol:",
        language_levels,
        index=spanish_index,
        help="Filtrar por nível de espanhol (valores padronizados)",
        key="nivel_espanhol_filter"
    )
    
    # Professional level filter (using standardized values from glossary)
    professional_levels = ["Todos"] + list(glossary.get('senioridade_lvl', {}).keys())
    saved_professional = st.session_state.get('nivel_profissional_filter', 'Todos')
    professional_index = 0 if st.session_state.get('filters_reset', False) else (professional_levels.index(saved_professional) if saved_professional in professional_levels else 0)
    nivel_profissional_filter = st.sidebar.selectbox(
        "Nível Profissional:",
        professional_levels,
        index=professional_index,
        help="Filtrar por nível profissional (valores padronizados pelo glossário)",
        key="nivel_profissional_filter"
    )
    
    st.sidebar.markdown("---")
    
    # Affirmative Action Filters
    st.sidebar.markdown("### Filtros Vagas Afirmativas")
    
    # Gender affirmative action
    vaga_afirmativa_sexo = st.sidebar.checkbox(
        "Vaga afirmativa para mulheres?",
        value=False if st.session_state.get('filters_reset', False) else st.session_state.get('vaga_afirmativa_sexo', False),
        help="Marcar se a vaga é destinada especificamente para mulheres",
        key="vaga_afirmativa_sexo"
    )
    
    if vaga_afirmativa_sexo:
        sexo_filter = "Feminino"
        st.sidebar.info("🚺 Filtro ativo: Candidatas do sexo feminino")
    else:
        sexo_filter = "Todos"
    
    # PCD affirmative action
    vaga_afirmativa_pcd = st.sidebar.checkbox(
        "Vaga afirmativa para PcD?",
        value=False if st.session_state.get('filters_reset', False) else st.session_state.get('vaga_afirmativa_pcd', False),
        help="Marcar se a vaga é destinada especificamente para Pessoas com Deficiência",
        key="vaga_afirmativa_pcd"
    )
    
    if vaga_afirmativa_pcd:
        pcd_filter = "Sim"
        st.sidebar.info("♿ Filtro ativo: Candidatos PcD")
    else:
        pcd_filter = "Todos"
    
    st.sidebar.markdown("---")
    
    # Clear reset flag after all widgets are created
    if st.session_state.get('filters_reset', False):
        st.session_state.filters_reset = False
    
    # Filter summary
    active_filters = []
    if local_filter != "Todos":
        active_filters.append(f"Local: {local_filter}")
    if nivel_academico_filter != "Todos":
        active_filters.append(f"Acadêmico: {nivel_academico_filter}")
    if nivel_ingles_filter != "Todos":
        active_filters.append(f"Inglês: {nivel_ingles_filter}")
    if nivel_espanhol_filter != "Todos":
        active_filters.append(f"Espanhol: {nivel_espanhol_filter}")
    if nivel_profissional_filter != "Todos":
        active_filters.append(f"Profissional: {nivel_profissional_filter}")
    if vaga_afirmativa_sexo:
        active_filters.append("Vaga para mulheres")
    if vaga_afirmativa_pcd:
        active_filters.append("Vaga PcD")
    
    if active_filters:
        st.sidebar.markdown("**Filtros Ativos:**")
        for filter_text in active_filters:
            st.sidebar.write(f"• {filter_text}")
    else:
        st.sidebar.info("Nenhum filtro ativo")
    
    # Initialize reset flag if not exists
    if 'filters_reset' not in st.session_state:
        st.session_state.filters_reset = False
    
    # Clear filters button
    if st.sidebar.button("🗑️ Limpar Filtros"):
        # Set reset flag and clear all filter keys
        st.session_state.filters_reset = True
        # Remove all filter session state keys
        keys_to_remove = ['local_filter', 'nivel_academico_filter', 'nivel_ingles_filter', 
                         'nivel_espanhol_filter', 'nivel_profissional_filter', 
                         'vaga_afirmativa_sexo', 'vaga_afirmativa_pcd']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    # Glossary information
    with st.sidebar.expander("📚 Glossário de Padronização", expanded=False):
        st.markdown("**Mapeamentos aplicados aos dados:**")
        
        if glossary.get('senioridade_group'):
            st.markdown("**Níveis Profissionais:**")
            for original, standardized in list(glossary['senioridade_group'].items())[:5]:
                st.write(f"• {original} → {standardized}")
            if len(glossary['senioridade_group']) > 5:
                st.write(f"... e mais {len(glossary['senioridade_group']) - 5} mapeamentos")
        
        if glossary.get('idioma_nvl'):
            st.markdown("**Níveis de Idioma:**")
            for level, score in glossary['idioma_nvl'].items():
                st.write(f"• {level}: {score}")
    
    # Main content area (full width now)
    # Job description input
    job_description = st.text_area(
        "Enter Job Description:",
        height=200,
        placeholder="""Example:
Procuramos um desenvolvedor Python sênior com experiência em:
- Desenvolvimento web com Django ou Flask
- Bancos de dados PostgreSQL e MongoDB
- APIs REST e microserviços
- Docker e Kubernetes
- Machine Learning com scikit-learn
- Experiência com AWS ou Azure
""",
        help="Describe the job requirements, skills, and qualifications needed"
    )
    
    # Search parameters
    col_params1, col_params2 = st.columns(2)
    with col_params1:
        top_n = st.slider("Número de candidatos:", 1, 20, 10)
    with col_params2:
        min_score = st.slider("Score mínimo:", 0.0, 1.0, 0.1, 0.05)        
    
    # Search button
    if st.button("🔎 Buscar Candidatos Compatíveis", type="primary"):
        if job_description.strip():
            with st.spinner('Analisando descrição da vaga e aplicando filtros...'):
                # Get all matches first
                all_matches = talent_recommender.recommend_for_job_description(job_description, len(df_application))
                
                # Apply filters to the matches using standardized data
                filtered_matches = []
                for match in all_matches:
                    candidate = df_application_std.iloc[match['index']]
                    
                    # Apply general filters
                    if local_filter != "Todos":
                        if candidate.get('local', '') != local_filter:
                            continue
                    
                    if nivel_academico_filter != "Todos":
                        if candidate.get('nivel_academico', '') != nivel_academico_filter:
                            continue
                    
                    if nivel_ingles_filter != "Todos":
                        if candidate.get('nivel_ingles', '') != nivel_ingles_filter:
                            continue
                    
                    if nivel_espanhol_filter != "Todos":
                        if candidate.get('nivel_espanhol', '') != nivel_espanhol_filter:
                            continue
                    
                    if nivel_profissional_filter != "Todos":
                        # Use standardized professional level for filtering
                        if candidate.get('nivel_profissional_std', '') != nivel_profissional_filter:
                            continue
                    
                    # Apply affirmative action filters
                    if vaga_afirmativa_sexo:
                        if candidate.get('sexo', '') != 'Feminino':
                            continue
                    
                    if vaga_afirmativa_pcd:
                        if candidate.get('pcd', '') != 'Sim':
                            continue
                    
                    # Apply minimum score filter
                    if match['match_score'] >= min_score:
                        filtered_matches.append(match)
                
                # Limit to top_n results
                filtered_matches = filtered_matches[:top_n]
                
                if filtered_matches:
                    st.success(f"Encontrados {len(filtered_matches)} candidatos compatíveis com os filtros aplicados!")
                    
                    # Display filter summary in results
                    if active_filters:
                        with st.expander("📋 Filtros Aplicados na Busca", expanded=False):
                            for filter_text in active_filters:
                                st.write(f"✓ {filter_text}")
                    
                    # Display results
                    for i, candidate in enumerate(filtered_matches, 1):
                        with st.expander(f"#{i} - {candidate.get('prospect_code', 'N/A')} - Score: {candidate['match_score']:.1%} - {candidate.get('nivel_profissional', 'N/A')}"):
                            col_gauge, col_details = st.columns([1, 2])
                            
                            with col_gauge:
                                fig = create_match_score_gauge(candidate['match_score'])
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col_details:
                                st.markdown(f"**Código Prospect:** {candidate.get('prospect_code', 'N/A')}")
                                st.markdown(f"**Nível Profissional:** {candidate.get('nivel_profissional', 'N/A')}")
                                st.markdown(f"**Área de Atuação:** {candidate.get('area_atuacao', 'N/A')}")
                                st.markdown(f"**Nível Acadêmico:** {candidate.get('nivel_academico', 'N/A')}")
                                st.markdown(f"**Nível de Inglês:** {candidate.get('nivel_ingles', 'N/A')}")
                                st.markdown(f"**Nível de Espanhol:** {candidate.get('nivel_espanhol', 'N/A')}")
                                st.markdown(f"**Local:** {candidate.get('local', 'N/A')}")
                                st.markdown(f"**Titulo:** {candidate.get('titulo', 'N/A')}")
                                
                                # Show affirmative action indicators if applicable
                                if vaga_afirmativa_sexo or vaga_afirmativa_pcd:
                                    st.markdown("**Critérios de Inclusão:**")
                                    if vaga_afirmativa_sexo:
                                        st.markdown("🚺 Candidata do sexo feminino")
                                    if vaga_afirmativa_pcd:
                                        st.markdown("♿ Pessoa com Deficiência")
                                
                else:
                    st.warning("Nenhum candidato encontrado com os filtros aplicados. Tente:")
                    st.write("• Reduzir o score mínimo")
                    st.write("• Remover alguns filtros")
                    st.write("• Ampliar os critérios de busca")
        else:
            st.error("Por favor, insira uma descrição da vaga para buscar candidatos.")

    # Footer
    st.markdown("---")
    st.markdown("**Postech Job Fit System** - Built with Streamlit, scikit-learn, and advanced NLP techniques")

if __name__ == "__main__":
    main()
