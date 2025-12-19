import streamlit as st
from pages import login, register, menu


PAGES_CONFIG = {
    'login': {
        'title': 'Login', 
        'icon': 'img/logo.ico'
    },
    'register': {
        'title': 'Cadastro', 
        'icon': 'img/logo.ico'
    },
    'menu': {
        'title': 'Início', 
        'icon': 'img/logo.ico'
    },
    'collection': {
        'title': 'Catálogo', 
        'icon': 'img/logo.ico'
    },
    'stats': {
        'title': 'Estatísticas', 
        'icon': 'img/logo.ico'
    }
}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'

current = PAGES_CONFIG.get(st.session_state.page, PAGES_CONFIG['login'])

st.set_page_config(
    page_title=current['title'],
    page_icon=current['icon'],
    layout='wide',
    initial_sidebar_state='collapsed' 
)

if not st.session_state.logged_in:
    if st.session_state.page == 'register':
        register.show()
    else:
        login.show()
else:
    # Roteador com nomes collection e stats
    if st.session_state.page == 'menu':
        menu.show()
    elif st.session_state.page == 'collection':
        from pages import collection
        collection.show()
    elif st.session_state.page == 'stats':
        from pages import stats
        stats.show()
    else:
        st.session_state.page = 'menu'
        st.rerun()