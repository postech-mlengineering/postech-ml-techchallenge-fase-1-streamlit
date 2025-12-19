import logging
import requests
from typing import List, Dict, Any, Optional
from . import URL_BASE

logger = logging.getLogger(__name__)


def get_stats_overview(token: str) -> Optional[Dict[str, Any]]:
    '''
    Recupera indicadores gerais e a distribuição de avaliações da coleção.

    Args:
        token: Token JWT de autenticação.

    Returns:
        Um dicionário contendo:
            - avg_price (float): Média de preço de todos os livros.
            - total_books (int): Quantidade total de registros.
            - rating_distribution (list): Lista de dicts com 'rating' e 'count'.
        Retorna None se a API falhar ou o status for diferente de 200.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f'{URL_BASE}/stats/overview', headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        
        logger.warning(f'Falha ao obter overview. Status: {response.status_code}')
        return None
    except Exception as e:
        logger.error(f'Erro ao buscar overview de stats: {e}')
        return None


def get_stats_by_category(token: str) -> List[Dict[str, Any]]:
    '''
    Recupera métricas detalhadas agrupadas por gênero.

    Args:
        token: Token JWT de autenticação.

    Returns:
        Uma lista de dicionários, onde cada item contém:
            - category (str): Nome da categoria.
            - avg_price (float): Média de preço naquela categoria.
            - total (int): Quantidade de livros pertencentes à categoria.
        Retorna uma lista vazia [] em caso de erro.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f'{URL_BASE}/stats/categories', headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        
        logger.warning(f'Falha ao obter stats por categoria. Status: {response.status_code}')
        return []
    except Exception as e:
        logger.error(f'Erro ao buscar stats por categoria: {e}')
        return []