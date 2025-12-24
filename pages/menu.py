import logging
import streamlit as st
from scripts import remove_cookies, set_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    '''Conteúdo da página de menu'''
    #css para ocultar sidebar
    st.markdown(
        '''
        <style>
            [data-testid='stSidebar'] { display: none !important; }
            [data-testid='stSidebarNav'] { display: none !important; }
            button[kind='headerNoPadding'] { display: none !important; }
        </style>
        ''',
        unsafe_allow_html=True
    )
    #título
    col1, col2 = st.columns([.05, .95])
    with col1:
        st.image('img/logo2.png', width='stretch')
    with col2:
        st.title('Books2Scrape | Menu')
    _, col2 = st.columns([0.9, 0.1])

    #botão de sair
    with col2:
        if st.button('Sair', help='Sair do aplicativo', width='stretch'):
            remove_cookies()
            st.session_state.clear() 
            st.rerun()

    st.markdown('---')

    #opções
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader('Acervo')
            img_col, text_col = st.columns([0.4, 0.6])
            with img_col:
                st.image('img/collection.png', width='stretch')
            with text_col:
                st.write(
                    '''
                        Navegue pelo acervo completo, use filtros de preço e
                        gênero e veja recomendações baseadas no seu perfil.
                    '''
                )
            if st.button('Acessar', width='stretch', key='btn_coll'):
                set_cookies('page', 'collection')
                st.rerun()
    with col2:
        with st.container(border=True):
            st.subheader('Estatísticas')
            img_col, text_col = st.columns([0.4, 0.6])
            with img_col:
                st.image('img/stats.png', width='stretch')
            with text_col:
                st.write(
                    '''
                        Visualize análises sobre preços, gêneros e
                        distribuição de avaliações de todo o acervo.
                    '''
                )
            if st.button('Acessar', width='stretch', key='btn_stats'):
                set_cookies('page', 'stats')
                st.rerun()