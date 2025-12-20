import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from scripts.stats_utils import get_stats_overview, get_stats_by_category
from scripts import get_cookies, set_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    #gerenciando sessao
    set_cookies('page', 'stats')
    token = get_cookies('token_acesso')

    #titulo
    st.title('Estatísticas')
    _, col2 = st.columns([0.9, 0.1])
    #botao de voltar
    with col2:
        if st.button('←', help='Voltar ao Menu', width='stretch'):
            set_cookies('page', 'menu')
            st.rerun()
    st.markdown('---')

    #buscando dados
    with st.spinner('Buscando dados da API...'):
        overview_data = get_stats_overview(token)
        categories_raw = get_stats_by_category(token)

    if not overview_data or not categories_raw:
        st.error('Erro na comunicação com a API ou dados não encontrados.')
        return

    #construindo dataframe
    df_stats_category = pd.DataFrame(categories_raw)
    df_stats_overview = pd.DataFrame(overview_data.get('rating_distribution', []))
    
    #filtros
    st.sidebar.title('Filtros')
    
    opcoes_generos = ['Todos'] + sorted(df_stats_category['category'].unique().tolist())
    selecao_generos = st.sidebar.multiselect('Gênero', options=opcoes_generos, default=['Todos'])

    opcoes_ratings = ['Todos'] + df_stats_overview['rating'].unique().tolist()
    selecao_ratings = st.sidebar.multiselect('Avaliação', options=opcoes_ratings, default=['Todos'])

    #filtrando dados
    if 'Todos' in selecao_generos or not selecao_generos:
        df_stats_category_filtered = df_stats_category.copy()
    else:
        df_stats_category_filtered = df_stats_category[df_stats_category['category'].isin(selecao_generos)].copy()
        
    if 'Todos' in selecao_ratings or not selecao_ratings:
        df_stats_overview_filtered = df_stats_overview.copy()
    else:
        df_stats_overview_filtered = df_stats_overview[df_stats_overview['rating'].isin(selecao_ratings)].copy()

    #ordenando dados
    df_stats_category_filtered = df_stats_category_filtered.sort_values('avg_price', ascending=False)
    df_stats_overview_filtered = df_stats_overview_filtered.sort_values('total', ascending=False)

    #cartões
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Gêneros', len(df_stats_category_filtered), border=True)
    with col2:
        total_livros = df_stats_category_filtered['total'].sum() if not df_stats_category_filtered.empty else 0
        st.metric('Livros', int(total_livros), border=True)
    with col3:
        preco_medio = df_stats_category_filtered['avg_price'].mean() if not df_stats_category_filtered.empty else 0
        st.metric('Preço Médio', f'£{preco_medio:.2f}', border=True)

    #gráficos
    col1, col2 = st.columns(2)
    PALETA_BLUES = px.colors.sequential.Blues
    
    with col1:
        st.markdown('### Preço por Gênero')
        if not df_stats_category_filtered.empty:
            fig_bar = px.bar(
                df_stats_category_filtered.sort_values('avg_price', ascending=True),
                x='avg_price',
                y='category',
                orientation='h',
                color='avg_price',
                color_continuous_scale=PALETA_BLUES,
                template='plotly_white',
                labels={'avg_price': 'Preço Médio (£)', 'category': 'Gênero'}
            )
            fig_bar.update_layout(coloraxis_showscale=False, height=450, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_bar, width='stretch')
        else:
            st.warning('Selecione ao menos um gênero.')

    with col2:
        st.markdown('### Distribuição de Avaliações')
        if not df_stats_overview_filtered.empty:
            fig_pie = px.pie(
                df_stats_overview_filtered,
                values='total',
                names='rating',
                hole=0.5,
                color_discrete_sequence=PALETA_BLUES,
                template='plotly_white'
            )
            fig_pie.update_layout(height=450, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_pie, width='stretch')
        else:
            st.warning('Selecione ao menos uma avaliação.')

    #analitico
    st.markdown('### Analítico')
    if not df_stats_category_filtered.empty:
        df_display = df_stats_category_filtered[['category', 'total', 'avg_price']].copy()
        df_display.columns = ['Gênero', 'Quantidade', 'Preço (£)']
        st.dataframe(
            df_display.style.background_gradient(subset=['Preço (£)'], cmap='Blues')
            .format({'Preço (£)': '{:.2f}'}),
            width='stretch',
            hide_index=True
        )