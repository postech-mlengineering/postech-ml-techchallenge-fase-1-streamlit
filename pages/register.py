import logging
import streamlit as st
from scripts.auth_utils import register
from scripts import set_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        st.title('Cadastro')
        st.subheader('Crie sua conta')
        with st.form('form_cadastro', clear_on_submit=True):
            novo_usuario = st.text_input('Novo Usuário')
            nova_senha = st.text_input('Nova Senha', type='password')
            
            _, col2_btn = st.columns([.6, .4])
            with col2_btn:
                cadastrar = st.form_submit_button('Cadastrar', width='stretch')
            
            if cadastrar:
                if not novo_usuario or not nova_senha:
                    st.error('Por favor, preencha todos os campos.')
                else:
                    sucesso, info = register(novo_usuario, nova_senha)
                    if sucesso:
                        #gerenciando sessao
                        set_cookies('token_acesso', info.get('access_token'))
                        set_cookies('user_id', str(info.get('user_id')))
                        set_cookies('username', novo_usuario)
                        set_cookies('logged_in', True)
                        set_cookies('page', 'preferences') 
                        st.rerun()
                    else:
                        st.error(info)
        if st.button('Já tem uma conta? Faça Login', width='stretch'):
            set_cookies('page', 'login') 
            st.rerun()