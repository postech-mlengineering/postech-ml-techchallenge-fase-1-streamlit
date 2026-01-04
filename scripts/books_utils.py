import logging
import requests
from scripts import URL_BASE
from typing import List, Dict, Optional, Union, Any


logger = logging.getLogger(__name__)


def get_all_book_titles(token: str) -> List[Dict[str, str]]:
    '''
    Obtém a lista de todos os títulos de livros disponíveis.

    Args:
        token: Token JWT de autenticação.

    Returns:
        Uma lista de dicionários contendo os títulos. Ex: [{'title': '...'}].
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f'{URL_BASE}/books/titles', headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []


def get_book_details(token: str, book_id: Union[int, str]) -> Optional[Dict[str, Any]]:
    '''
    Recupera as informações detalhadas de um livro específico pelo seu ID.

    Args:
        token: Token JWT de autenticação.
        book_id: Identificador único do livro.

    Returns:
        Dicionário com os detalhes do livro ou None se houver falha.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f'{URL_BASE}/books/details/{book_id}', headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f'error: {e}')
        return None


def get_books_by_search(
    token: str, 
    title: Optional[str] = None, 
    genre: Optional[str] = None
) -> Union[List[Dict[str, Any]], Dict[str, str]]:
    '''
    Busca livros filtrando por título e/ou gênero.

    Args:
        token: Token JWT de autenticação.
        title: Parte do título do livro (opcional).
        genre: Gênero/Categoria do livro (opcional).

    Returns:
        Lista de livros encontrados ou dicionário com mensagem de erro da API.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    params = {}
    if title: params['title'] = title
    if genre: params['genre'] = genre
    
    try:
        response = requests.get(f'{URL_BASE}/books/search', headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        
        if response.status_code in [400, 404]:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []


def get_books_by_price_range(
    token: str, 
    min_price: float, 
    max_price: float
) -> List[Dict[str, Any]]:
    '''
    Filtra livros dentro de uma faixa de preço específica.

    Args:
        token: Token JWT de autenticação.
        min_price: Preço mínimo.
        max_price: Preço máximo.

    Returns:
        Lista de livros que atendem aos critérios de preço.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    params = {'min': min_price, 'max': max_price}
    try:
        response = requests.get(f'{URL_BASE}/books/price-range', headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []


def get_top_rated(token: str, limit: int = 1000) -> List[Dict[str, Any]]:
    '''
    Retorna os livros com as melhores avaliações.

    Args:
        token: Token JWT de autenticação.
        limit: Quantidade máxima de resultados (padrão: 10).

    Returns:
        Lista de livros mais bem avaliados.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    params = {'limit': limit}
    try:
        response = requests.get(f'{URL_BASE}/books/top-rated', headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []