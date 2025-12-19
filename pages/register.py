import streamlit as st
from scripts.auth_utils import register


def show():
    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        st.title('Cadastro')
        st.subheader('Crie sua conta')
        
        with st.form('form_cadastro', clear_on_submit=True):
            novo_usuario = st.text_input('Novo Usuário')
            nova_senha = st.text_input('Nova Senha', type='password')
            _, col2 = st.columns([.7, .3])
            with col2:
                cadastrar = st.form_submit_button('Cadastrar', width='stretch')
            if cadastrar:
                sucesso, msg = register(novo_usuario, nova_senha)
                if sucesso:
                    st.success('Cadastro realizado com sucesso')
                else:
                    st.error(msg)

        if st.button('Login', width='stretch'):
            st.session_state.page = 'login'
            st.rerun()