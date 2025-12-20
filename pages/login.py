import logging
import streamlit as st
from scripts.auth_utils import login
from scripts import get_all_cookies, set_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    _, user_id, _, logged_in, _ = get_all_cookies()
    if logged_in and st.session_state.get('page') != 'register':
        st.session_state.logged_in = True
        st.session_state.page = 'menu'
        st.rerun()

    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        st.title('Books2Scrape')
        st.subheader('Login')
        
        with st.form('form_login'):
            usuario_input = st.text_input('Usuário')
            senha_input = st.text_input('Senha', type='password')
            _, col2 = st.columns([.7, .3])
            with col2:
                entrar = st.form_submit_button('Entrar', width='stretch')
            
            if entrar:
                token_acesso, user_id, error_msg = login(usuario_input, senha_input)
                if token_acesso:
                    #gerenciando sessao
                    set_cookies('token_acesso', token_acesso)
                    set_cookies('user_id', str(user_id))
                    set_cookies('username', usuario_input)
                    set_cookies('logged_in', True)
                    set_cookies('page', 'menu')
                    st.rerun()
                else:
                    st.error(error_msg)
        st.write('Não possui uma conta?')
        if st.button('Cadastre-se', width='stretch'):
            set_cookies('page', 'register') 
            st.session_state.page = 'register'
            st.rerun()