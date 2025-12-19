import logging
import requests
from typing import Tuple, Optional, Any
from . import URL_BASE
from streamlit_cookies_controller import CookieController

logger = logging.getLogger(__name__)

controller = CookieController()

def remove_cookies():
    controller.remove('token_acesso')
    controller.remove('username')
    controller.remove('logged_in')
    controller.remove('page')

def get_all_cookies():
    return controller.get('token_acesso'), \
        controller.get('username'), \
        controller.get('logged_in'), \
        controller.get('page')

def get_cookies(key):
    return controller.get(key)

def set_all_cookies(token, usuario, page):
    set_cookies('token_acesso', token)
    set_cookies('username', usuario)
    set_cookies('page', page)
    set_cookies('logged_in', True)

def set_cookies(key, value):
    controller.set(key, value)

def login(usuario: str, senha: str) -> Tuple[Optional[str], Optional[str]]:
    '''
    Realiza a autenticação do usuário e recupera o token JWT.

    Args:
        usuario: O nome de usuário (username).
        senha: A senha do usuário.

    Returns:
        Uma tupla contendo (access_token, erro_msg).
        Se o login for bem-sucedido: (token, None).
        Se falhar: (None, mensagem_de_erro).
    '''
    try:
        endpoint_login = f'{URL_BASE}/auth/login'
        response = requests.post(
            endpoint_login, 
            json={'username': usuario, 'password': senha}, 
            timeout=5
        )
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            set_all_cookies(token, usuario, 'menu')
            return token, None
        try:
            erro_data = response.json()
            msg_erro = erro_data.get('error', 'Credenciais inválidas.')
        except requests.exceptions.JSONDecodeError:
            msg_erro = f'Erro inesperado no servidor (Status: {response.status_code}).'
        
        return None, msg_erro

    except requests.exceptions.ConnectionError:
        logger.error(f'Falha de conexão em login: {URL_BASE}')
        return None, 'Não foi possível conectar ao servidor. Verifique sua conexão.'
    except Exception as e:
        logger.error(f'Erro inesperado no login: {e}')
        return None, f'Erro interno: {str(e)}'


def register(usuario: str, senha: str) -> Tuple[bool, str]:
    '''
    Cria uma nova conta de usuário no sistema.

    Args:
        usuario: O nome de usuário desejado.
        senha: A senha para a nova conta.

    Returns:
        Uma tupla contendo (sucesso, mensagem).
        sucesso: True se a conta foi criada, False caso contrário.
        mensagem: Mensagem de sucesso ou o motivo do erro retornado pela API.
    '''
    try:
        endpoint_register = f'{URL_BASE}/auth/register'
        response = requests.post(
            endpoint_register, 
            json={'username': usuario, 'password': senha}, 
            timeout=5
        )
        
        try:
            dados = response.json()
        except requests.exceptions.JSONDecodeError:
            return False, f'Resposta inválida do servidor (Status: {response.status_code}).'

        if response.status_code == 201:
            return True, dados.get('msg', 'Usuário registrado com sucesso!')
        return False, dados.get('error', 'Falha ao realizar o registro.')

    except requests.exceptions.ConnectionError:
        logger.error(f'Falha de conexão em register: {URL_BASE}')
        return False, 'Erro de conexão: servidor offline.'
    except Exception as e:
        logger.error(f'Erro inesperado no registro: {e}')
        return False, f'Erro inesperado: {str(e)}'