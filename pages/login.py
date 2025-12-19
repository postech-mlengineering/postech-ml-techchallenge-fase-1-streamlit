import streamlit as st
from scripts.auth_utils import login


def show():
    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        st.title('Books2Scrape')
        st.subheader('Login')
        
        with st.form('form_login'):
            usuario = st.text_input('Usuário')
            senha = st.text_input('Senha', type='password')
            col1, _ = st.columns([.5, .5])
            _, col2 = st.columns([.7, .3])
            with col2:
                entrar = st.form_submit_button('Entrar', width='stretch')
            if entrar:
                token, erro = login(usuario, senha)
                if token:
                    st.session_state.token_acesso = token
                    st.session_state.usuario = usuario
                    st.session_state.logged_in = True
                    st.session_state.page = 'home'
                    st.rerun()
                else:
                    st.error(erro)
                    
        st.write('Não possui uma conta?')
        if st.button('Cadastre-se', width='stretch'):
                st.session_state.page = 'register'
                st.rerun()