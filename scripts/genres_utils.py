import logging
import requests
from scripts import URL_BASE
from typing import List, Dict


logger = logging.getLogger(__name__)


def get_all_genres(token: str) -> List[Dict[str, str]]:
    '''
    Recupera a lista de todas as categorias de livros cadastradas.

    Args:
        token: Token JWT de autenticação.

    Returns:
        Uma lista de dicionários contendo as categorias. Ex: [{'category': 'Art'}].
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f'{URL_BASE}/genres', headers=headers, timeout=5)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'Erro de requisição em get_all_genres: {e}')
        return []
    except Exception as e:
        logger.error(f'Erro inesperado em get_all_genres: {e}')
        return []