import logging
import streamlit as st
from streamlit_cookies_controller import CookieController
from typing import Tuple, Optional, Any


logger = logging.getLogger(__name__)


def remove_cookies() -> None:
    '''
    Remove todos os cookies de sessão relacionados à autenticação e navegação.
    '''
    controller.remove('access_token')
    controller.remove('user_id')
    controller.remove('username')
    controller.remove('logged_in')
    controller.remove('page')


def get_all_cookies() -> Tuple[Optional[str], Optional[int], Optional[str], Optional[bool], Optional[str]]:
    '''
    Recupera os valores de todos os cookies principais da aplicação.

    Returns:
        Uma tupla contendo (access_token, user_id, username, logged_in, page).
    '''
    return (
        controller.get('access_token'),
        controller.get('user_id'),
        controller.get('username'),
        controller.get('logged_in'),
        controller.get('page')
    )


def get_cookies(key: str) -> Any:
    '''
    Recupera o valor de um cookie específico através da sua chave.

    Args:
        key (str): O nome do cookie que deseja recuperar.

    Returns:
        O valor armazenado no cookie ou None se não existir.
    '''
    return controller.get(key)


def set_all_cookies(token: str, user_id: int, usuario: str, page: str) -> None:
    '''
    Define simultaneamente todos os cookies necessários para o estado de login.

    Args:
        token (str): Token JWT ou de acesso.
        user_id (int): Identificador único do usuário.
        usuario (str): Nome de exibição do usuário.
        page (str): Nome da página atual para persistência de navegação.
    '''
    set_cookies('access_token', token)
    set_cookies('user_id', user_id)
    set_cookies('username', usuario)
    set_cookies('page', page)
    set_cookies('logged_in', True)


def set_cookies(key: str, value: Any) -> None:
    '''
    Armazena um valor em um cookie específico.

    Args:
        key (str): O nome da chave do cookie.
        value (Any): O valor a ser armazenado.
    '''
    controller.set(key, value)


controller = CookieController()

URL_BASE = 'http://192.168.15.9:5000/api/v1'