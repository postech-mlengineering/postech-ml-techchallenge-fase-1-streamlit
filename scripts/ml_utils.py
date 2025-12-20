import logging
import requests
from scripts import URL_BASE
from typing import List, Dict, Tuple, Optional, Any


logger = logging.getLogger(__name__)


def get_user_preferences(token: str, user_id: int) -> Optional[List[Dict[str, Any]]]:
    '''
    Recupera o histórico de recomendações (preferências) de um usuário específico.

    Args:
        token: Token JWT de autenticação.
        user_id: Identificador único do usuário.

    Returns:
        Lista de dicionários com as recomendações e detalhes dos livros ou None se houver falha.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        url = f'{URL_BASE}/ml/user-preferences/{user_id}'
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            logger.warning(f'Nenhum histórico encontrado para o usuário id {user_id}.')
            return []
        logger.error(f'error: {response.status_code} - {response.text}')
        return None
    except Exception as e:
        logger.error(f'error: {e}')
        return None


def input_user_preferences(token: str, book_id: int) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    '''
    Envia o título do livro para a API via GET (conforme a rota Flask) para salvar recomendações.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        from scripts.books_utils import get_book_details
        detalhes = get_book_details(token, book_id)
        
        if not detalhes:
            return None, 'Erro na API'

        book_title = detalhes.get('title')

        payload = {'title': book_title}
        response = requests.get(f'{URL_BASE}/ml/predictions', json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.json(), None
            
        try:
            error_msg = response.json().get("error", 'Erro ao processar recomendações.')
        except:
            error_msg = f'Erro no servidor (Status {response.status_code})'
            
        return None, error_msg
    except Exception as e:
        logger.error(f'Erro em input_user_preference: {e}')
        return None, str(e)