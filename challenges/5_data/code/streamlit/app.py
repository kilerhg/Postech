import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
from datetime import datetime, timedelta


# App configuration
apptitle = 'Postech Job Fit - Talent Recommendation System'
st.set_page_config(page_title=apptitle, page_icon="🎯", layout="wide")

# Generate mock data for UI testing
@st.cache_data
def generate_mock_data():
    """Generate mock candidate data for UI development"""
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
        
        # Generate random location with state
        estados = ['SP', 'RJ', 'MG', 'DF', 'PR', 'RS', 'SC', 'GO', 'BA']
        cidades = {
            'SP': ['São Paulo - SP', 'Campinas - SP', 'Santos - SP'],
            'RJ': ['Rio de Janeiro - RJ', 'Niterói - RJ', 'Petrópolis - RJ'],
            'MG': ['Belo Horizonte - MG', 'Uberlândia - MG', 'Juiz de Fora - MG'],
            'DF': ['Brasília - DF'],
            'PR': ['Curitiba - PR', 'Londrina - PR'],
            'RS': ['Porto Alegre - RS', 'Caxias do Sul - RS'],
            'SC': ['Florianópolis - SC', 'Joinville - SC'],
            'GO': ['Goiânia - GO'],
            'BA': ['Salvador - BA']
        }
        
        estado = np.random.choice(estados)
        local = np.random.choice(cidades[estado])
        
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
            'estado': estado,
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
                'estado': self.df_application.iloc[idx]['estado'],
                'local': self.df_application.iloc[idx]['local'],
                'conhecimentos_preview': self.df_application.iloc[idx]['cv_pt_cleaned'][:300] + '...'
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
                'estado': self.df_application.iloc[idx]['estado'],
                'local': self.df_application.iloc[idx]['local'],
                'conhecimentos_preview': self.df_application.iloc[idx]['cv_pt_cleaned'][:300] + '...'
            }
            results.append(candidate_info)
        
        # Sort by match score
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results

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
    
    # Load mock data for UI development
    st.info("🧪 **UI Development Mode** - Using mock data for interface testing")
    
    with st.spinner('Loading candidate data...'):
        df_application = generate_mock_data()
    
    # Initialize mock recommendation system
    talent_recommender = MockTalentRecommendationSystem(df_application)
    
    # Main Job Description Matching Interface
    st.header("🔍 Find Candidates for Job Description")
    
    # Sidebar Filters
    st.sidebar.header("🔧 Filtros")
    
    # General Filters
    st.sidebar.markdown("### Filtros Gerais")
    
    # Estado filter
    estado_filter = st.sidebar.selectbox(
        "Estado:",
        ["Todos"] + ["SP", "RJ", "MG", "DF", "PR", "RS", "SC", "GO", "BA", "CE", "PE", "ES", "MT", "MS", "PA", "PB", "RN", "AL", "SE", "PI", "RO", "AC", "AM", "RR", "AP", "TO", "MA"],
        help="Filtrar por estado"
    )
    
    # Academic level filter
    nivel_academico_filter = st.sidebar.selectbox(
        "Nível Acadêmico:",
        ["Todos", "Ensino Médio", "Técnico", "Tecnólogo", "Superior Incompleto", "Superior Completo", "Pós-graduação", "MBA", "Mestrado", "Doutorado"],
        help="Filtrar por nível de educação"
    )
    
    # English level filter
    nivel_ingles_filter = st.sidebar.selectbox(
        "Nível de Inglês:",
        ["Todos", "Básico", "Intermediário", "Avançado", "Fluente", "Nativo"],
        help="Filtrar por nível de inglês"
    )
    
    # Spanish level filter
    nivel_espanhol_filter = st.sidebar.selectbox(
        "Nível de Espanhol:",
        ["Todos", "Básico", "Intermediário", "Avançado", "Fluente", "Nativo"],
        help="Filtrar por nível de espanhol"
    )
    
    # Professional level filter
    nivel_profissional_filter = st.sidebar.selectbox(
        "Nível Profissional:",
        ["Todos", "Estagiário", "Trainee", "Junior", "Pleno", "Senior", "Especialista", "Coordenador", "Supervisor", "Gerente", "Diretor", "Analista", "Consultor"],
        help="Filtrar por nível profissional"
    )
    
    st.sidebar.markdown("---")
    
    # Affirmative Action Filters
    st.sidebar.markdown("### Filtros Vagas Afirmativas")
    
    # Gender affirmative action
    vaga_afirmativa_sexo = st.sidebar.checkbox(
        "Vaga afirmativa para mulheres?",
        help="Marcar se a vaga é destinada especificamente para mulheres"
    )
    
    if vaga_afirmativa_sexo:
        sexo_filter = "Feminino"
        st.sidebar.info("🚺 Filtro ativo: Candidatas do sexo feminino")
    else:
        sexo_filter = "Todos"
    
    # PCD affirmative action
    vaga_afirmativa_pcd = st.sidebar.checkbox(
        "Vaga afirmativa para PcD?",
        help="Marcar se a vaga é destinada especificamente para Pessoas com Deficiência"
    )
    
    if vaga_afirmativa_pcd:
        pcd_filter = "Sim"
        st.sidebar.info("♿ Filtro ativo: Candidatos PcD")
    else:
        pcd_filter = "Todos"
    
    st.sidebar.markdown("---")
    
    # Filter summary
    active_filters = []
    if estado_filter != "Todos":
        active_filters.append(f"Estado: {estado_filter}")
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
    
    # Clear filters button
    if st.sidebar.button("🗑️ Limpar Filtros"):
        st.rerun()
    
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
    col_params1, col_params2, col_params3 = st.columns(3)
    with col_params1:
        top_n = st.slider("Número de candidatos:", 1, 20, 10)
    with col_params2:
        min_score = st.slider("Score mínimo:", 0.0, 1.0, 0.1, 0.05)
    with col_params3:
        st.info("""
        **Como funciona:**
        
        1. Digite a descrição da vaga
        2. Configure os filtros ao lado
        3. Nossa IA analisa e encontra candidatos
        4. Resultados rankeados por compatibilidade
        """)
    
    # Search button
    if st.button("🔎 Buscar Candidatos Compatíveis", type="primary"):
        if job_description.strip():
            with st.spinner('Analisando descrição da vaga e aplicando filtros...'):
                # Get all matches first
                all_matches = talent_recommender.recommend_for_job_description(job_description, len(df_application))
                
                # Apply filters to the matches
                filtered_matches = []
                for match in all_matches:
                    candidate = df_application.iloc[match['index']]
                    
                    # Apply general filters
                    if estado_filter != "Todos":
                        if candidate.get('estado', '') != estado_filter:
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
                        if candidate.get('nivel_profissional', '') != nivel_profissional_filter:
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
                                st.markdown(f"**Estado:** {candidate.get('estado', 'N/A')}")
                                st.markdown(f"**Localização:** {candidate.get('local', 'N/A')}")
                                
                                # Show affirmative action indicators if applicable
                                if vaga_afirmativa_sexo or vaga_afirmativa_pcd:
                                    st.markdown("**Critérios de Inclusão:**")
                                    if vaga_afirmativa_sexo:
                                        st.markdown("🚺 Candidata do sexo feminino")
                                    if vaga_afirmativa_pcd:
                                        st.markdown("♿ Pessoa com Deficiência")
                                
                                st.markdown("**Preview das Competências:**")
                                st.text(candidate['conhecimentos_preview'])
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
