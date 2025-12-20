import logging
import requests
from scripts import set_all_cookies, URL_BASE
from typing import Tuple, Optional, Union, Dict, Any


logger = logging.getLogger(__name__)


def login(usuario: str, senha: str) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    '''
    Realiza a autenticação do usuário e recupera o token JWT e o User ID.

    Returns:
        Uma tupla contendo (access_token, user_id, erro_msg).
    '''
    try:
        response = requests.post(
            f'{URL_BASE}/auth/login', 
            json={'username': usuario, 'password': senha}, 
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user_id = data.get('user_id')
            set_all_cookies(token, user_id, usuario, 'menu')
            return token, user_id, None
        try:
            data = response.json()
            msg_erro = data.get('error', 'Credenciais inválidas.')
        except Exception:
            msg_erro = f'Erro no servidor (Status {response.status_code})'
        return None, None, msg_erro
    except requests.exceptions.ConnectionError:
        logger.error(f'Falha de conexão: {URL_BASE}')
        return None, None, 'Não foi possível conectar ao servidor.'
    except Exception as e:
        logger.error(f'error: {e}')
        return None, None, f'error: {str(e)}'


def register(usuario: str, senha: str) -> Tuple[bool, Union[str, Dict[str, Any]]]:
    '''
    Cria uma nova conta de usuário no sistema e retorna os dados de autenticação.

    Args:
        usuario: O nome de usuário desejado.
        senha: A senha para a nova conta.

    Returns:
        Uma tupla contendo (sucesso, dados_ou_mensagem).
    '''
    try:
        response = requests.post(
            f'{URL_BASE}/auth/register', 
            json={'username': usuario, 'password': senha}, 
            timeout=5
        )
        try:
            dados = response.json()
        except requests.exceptions.JSONDecodeError:
            return False, f'Resposta inválida do servidor (Status: {response.status_code}).'

        if response.status_code == 201:
            return True, dados
        return False, dados.get('error', 'Falha ao realizar o registro.')
    except requests.exceptions.ConnectionError:
        logger.error(f'Falha de conexão em register: {URL_BASE}')
        return False, 'Erro de conexão: servidor offline.'
    except Exception as e:
        logger.error(f'Erro inesperado no registro: {e}')
        return False, f'Erro inesperado: {str(e)}'