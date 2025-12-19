import streamlit as st
from scripts.auth_utils import remove_cookies, set_cookies

def show():
    st.markdown( #esconde sidebar
        '''
        <style>
            [data-testid='stSidebar'] {
                display: none !important;
            }
            [data-testid='stSidebarNav'] {
                display: none !important;
            }
            /* Esconde o botão (setinha) que abre a sidebar manualmente */
            button[kind='headerNoPadding'] {
                display: none !important;
            }
        </style>
        ''',
        unsafe_allow_html=True
    )
    st.title('Books2Scrape')
    _, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button('Sair', help='Sair do aplicativo', width='stretch'):
            st.session_state.logged_in = False
            st.session_state.page = 'login'
            remove_cookies()
            st.rerun()

    st.subheader('Início')
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader('Acervo')
            image, text = st.columns(2)
            with image:
                st.image('img/collection.png', caption='Exploração de Acervo')
            with text:
                st.markdown(
                    '''
                    <div style='text-align: justify;'>
                        Acesso completo ao acervo de livros. Permite navegar por categorias, 
                        verificar preços e disponibilidade em tempo real, facilitando a 
                        gestão de inventário e consulta rápida.
                    </div>
                    ''', 
                    unsafe_allow_html=True
                )
            if st.button('Acessar', width='stretch', key='button_collection'):
                set_cookies('page', 'collection')
                st.session_state.page = 'collection'
                st.rerun()
    with col2:
        with st.container(border=True):
            st.subheader('Estatísticas')
            image, text = st.columns(2)
            with image:
                st.image('img/stats.png', caption='Análise de Dados')
            with text:
                st.markdown(
                    '''
                    <div style='text-align: justify;'>
                        Visão analítica dos dados do acervo. Gráficos de distribuição de 
                        preços, avaliações médias e métricas por categoria.
                    </div>
                    ''', 
                    unsafe_allow_html=True
                )
            if st.button('Acessar', width='stretch', key='button_stats'):
                set_cookies('page', 'stats')
                st.session_state.page = 'stats'
                st.rerun()