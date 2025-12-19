import logging
import requests
from typing import List, Dict
from . import URL_BASE


logger = logging.getLogger(__name__)


def get_all_categories(token: str) -> List[Dict[str, str]]:
    '''
    Recupera a lista de todas as categorias de livros cadastradas.

    Args:
        token: Token JWT de autenticação.

    Returns:
        Uma lista de dicionários contendo as categorias. Ex: [{'category': 'Art'}].
        Retorna uma lista vazia [] em caso de erro ou falha de autenticação.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f'{URL_BASE}/categories', headers=headers, timeout=5)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'Erro de requisição em get_all_categories: {e}')
        return []
    except Exception as e:
        logger.error(f'Erro inesperado em get_all_categories: {e}')
        return []