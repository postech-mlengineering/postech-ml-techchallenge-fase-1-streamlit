import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from scripts.stats_utils import get_stats_overview, get_stats_by_genre
from scripts import get_cookies, set_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    '''Conteúdo da página de estatísticas'''
    #gerenciando sessao
    set_cookies('page', 'stats')
    token = get_cookies('access_token')

    #título
    col1, col2 = st.columns([.05, .95])
    with col1:
        st.image('img/logo2.png', width='stretch')
    with col2:
        st.title('Books2Scrape | Estatísticas')
    
    #botao de voltar
    _, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button('←', help='Voltar ao Menu', width='stretch'):
            set_cookies('page', 'menu')
            st.rerun()
    st.markdown('---')

    #buscando dados
    with st.spinner('Buscando dados da API...'):
        overview_data = get_stats_overview(token)
        genres_raw = get_stats_by_genre(token)

    if not overview_data or not genres_raw:
        st.error('Erro na comunicação com a API ou dados não encontrados.')
        return

    #construindo dataframe
    df_stats_genres = pd.DataFrame(genres_raw)
    df_stats_overview = pd.DataFrame(overview_data.get('rating_distribution', []))

    #ordenando dados
    df_stats_genres = df_stats_genres.sort_values('avg_price', ascending=False)
    df_stats_overview = df_stats_overview.sort_values('total', ascending=False)

    #cartões
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Gêneros', len(df_stats_genres), border=True)
    with col2:
        total_livros = df_stats_genres['total'].sum() if not df_stats_genres.empty else 0
        st.metric('Livros', int(total_livros), border=True)
    with col3:
        preco_medio = df_stats_genres['avg_price'].mean() if not df_stats_genres.empty else 0
        st.metric('Preço Médio', f'£{preco_medio:.2f}', border=True)

    #gráficos
    col1, col2 = st.columns(2)
    pallete = px.colors.sequential.Blues
    
    with col1:
        st.markdown('### Preço por Gênero')
        if not df_stats_genres.empty:
            fig_bar = px.bar(
                df_stats_genres.sort_values('avg_price', ascending=True),
                x='avg_price',
                y='genre',
                orientation='h',
                color='avg_price',
                color_continuous_scale=pallete,
                template='plotly_white',
                labels={'avg_price': 'Preço Médio (£)', 'genre': 'Gênero'}
            )
            fig_bar.update_layout(coloraxis_showscale=False, height=550, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_bar, width='stretch')
        else:
            st.warning('Selecione ao menos um gênero.')

    with col2:
        st.markdown('### Distribuição de Avaliações')
        if not df_stats_overview.empty:
            fig_pie = px.pie(
                df_stats_overview,
                values='total',
                names='rating',
                hole=0.5,
                color_discrete_sequence=pallete,
                template='plotly_white'
            )
            fig_pie.update_layout(height=550, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_pie, width='stretch')
        else:
            st.warning('Selecione ao menos uma avaliação.')

    #analitico
    st.markdown('### Analítico')
    if not df_stats_genres.empty:
        df_display = df_stats_genres[['genre', 'total', 'avg_price']].copy()
        df_display.columns = ['Gênero', 'Quantidade', 'Preço (£)']
        st.dataframe(
            df_display.style.background_gradient(subset=['Preço (£)'], cmap='Blues')
            .format({'Preço (£)': '{:.2f}'}),
            width='stretch',
            hide_index=True
        )