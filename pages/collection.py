import logging
import streamlit as st
from typing import List, Dict, Any, Optional
from scripts.books_utils import (
    get_books_by_search, 
    get_book_details, 
    get_books_by_price_range,
    get_top_rated
)
from scripts.categories_utils import get_all_categories


logger = logging.getLogger(__name__)


def show() -> None:
    '''
    Renderiza a página do catálogo.
    '''
    #inicializa o catálogo no estado da sessão caso ele ainda não exista
    #busca os 10 livros mais bem avaliados por padrão
    if 'books_collection' not in st.session_state:
        st.session_state.books_collection = get_top_rated(st.session_state.get('token_acesso'), limit=10)

    #recupera o token de autenticação guardado no login
    token = st.session_state.get('token_acesso')

    st.sidebar.title('Filtros')
    
    #botões que expandem ou recolhem as opções de consulta
    title_genre_filter = st.sidebar.toggle('Título ou Gênero', value=False)
    price_range_filter = st.sidebar.toggle('Faixa de Preço', value=False)
    
    #valores padrão para as variáveis de busca
    title = ''
    option = 'Todas'
    p_min = 0.00
    p_max = 100.00

    #se qualquer um dos botões estiver ligado, mostra o container de inputs
    if title_genre_filter or price_range_filter:
        with st.sidebar.container():

            #bloco de inputs para busca por título ou gênero
            if title_genre_filter:
                st.sidebar.markdown('### Título ou Gênero') 
                title = st.sidebar.text_input('Título', placeholder='Ex: The White Queen', key='input_title')
                
                #busca as categorias via API
                categories = get_all_categories(token)
                options = ['Todas'] + [c['category'] for c in categories] if categories else ['Todas']
                option = st.sidebar.selectbox('Gênero', options=options, key='input_genre')
            
            #linha divisória se ambos os blocos de filtros estiverem ativos
            if title_genre_filter and price_range_filter:
                st.sidebar.divider()

            #bloco de inputs para filtrar por preços
            if price_range_filter:
                st.sidebar.markdown('### Faixa de Preço')
                p_min = st.sidebar.number_input('Mínimo (£)', min_value=0.0, value=0.00, step=1.0, key='input_p_min')
                p_max = st.sidebar.number_input('Máximo (£)', min_value=0.0, value=100.0, step=1.0, key='input_p_max')
            
            st.sidebar.write('')
            #processamento da busca ao clicar no botão 'Aplicar'
            if st.sidebar.button('Aplicar', type='primary', width='stretch'):
                category = None if option == 'Todas' else option
                
                #apenas filtro de preço
                if price_range_filter and not title_genre_filter:
                    st.session_state.books_collection = get_books_by_price_range(token, p_min, p_max)

                #apenas filtro de Título/Gênero
                elif title_genre_filter and not price_range_filter:
                    if not title and not category:
                        st.session_state.books_collection = get_top_rated(token, limit=10)
                    else:
                        st.session_state.books_collection = get_books_by_search(token, title=title if title else None, genre=category)
                    
                #filtro combinado
                elif price_range_filter and title_genre_filter:
                    books_raw = get_books_by_price_range(token, p_min, p_max)
                    if isinstance(books_raw, list):
                        #filtra o resultado da API localmente usando os critérios de título e gênero
                        st.session_state.books_collection = [
                            b for b in books_raw 
                            if (not title or title.lower() in b.get('title', '').lower()) and
                            (not category or b.get('genre') == category)
                        ]
    
    #se os botões forem desligados, volta ao estado original
    else:
        #só executa o reset se a flag 'filtros_ativos' indicar que havia algo filtrado antes
        if st.session_state.get('filtros_ativos', False):
            st.session_state.books_collection = get_top_rated(token, limit=10)
            st.session_state.filtros_ativos = False # Desativa a flag após o reset
            st.rerun() # Reinicia o script para atualizar a visualização imediatamente
        st.sidebar.info('Ative os filtros acima para consulta')

    #se os botões estiverem ligados, marca a flag como True para permitir o reset futuro
    if title_genre_filter or price_range_filter:
        st.session_state.filtros_ativos = True
    
    #conteúdo da página
    st.title('Catálogo')
    
    #coluna auxiliar no cabeçalho para o botão de voltar
    _, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button('←', help='Voltar ao Menu', width='stretch'):
            logger.info('Usuário retornou ao menu.')
            st.session_state.page = 'menu'
            st.rerun()
    st.markdown('---')

    #pega os livros que estão no estado da sessão (seja o padrão ou os filtrados)
    books = st.session_state.books_collection

    st.subheader('Livros')
    #tratamento para lista vazia ou erro da API
    if not books or (isinstance(books, dict) and 'msg' in books):
        st.warning('Nenhum livro encontrado para os filtros aplicados')
    else:
        st.write(f'Exibindo **{len(books)}** resultados')
        
        #lógica para criar um grid de 3 colunas
        for i in range(0, len(books), 3):
            cols = st.columns(3) #cria 3 colunas horizontais
            for j in range(3):
                if i + j < len(books): #verifica se ainda existem livros na lista
                    book = books[i + j]
                    book_id = book.get('id') 
                    
                    with cols[j]:
                        #container com borda para card do livro
                        with st.container(border=True):
                            #html customizado para garantir que todas as imagens tenham o mesmo tamanho no grid
                            url_img = book.get('image_url') or 'https://via.placeholder.com/150x200?text=Sem+Capa'
                            st.markdown(
                                f'''
                                <div style='display: flex; justify-content: center; margin-bottom: 10px;'>
                                    <img src='{url_img}' style='height: 200px; object-fit: contain; border-radius: 4px;'>
                                </div>
                                ''', 
                                unsafe_allow_html=True
                            )
                            
                            #título truncado (limita o tamanho para não quebrar o layout do card)
                            book_title = book.get('title', 'Sem título')
                            st.markdown(f'**{book_title[:35]}...**' if len(book_title) > 35 else f'**{book_title}**')
                            st.write(f'£{book.get("price")}')
                            
                            #exibe a avaliação
                            if book.get('rating'):
                                st.caption(f"⭐ {book.get('rating')}")
                            
                            #botão de detalhes
                            if st.button('Detalhes', key=f'btn_{book_id}_{i+j}', width='stretch'):
                                details(book_id)


@st.dialog('Detalhes')
def details(book_id: int) -> None:
    '''
    Renderiza uma janela modal (dialog) com as informações detalhadas de um livro.

    A função consome a API de detalhes para exibir capa, metadados (UPC, estoque, 
    preço com taxas) e a descrição completa do livro.

    Args:
        book_id: O identificador único do livro a ser consultado.

    Note:
        Esta função depende de 'st.session_state.token_acesso' estar devidamente 
        preenchido para autenticar a requisição à API.
    '''
    try:
        detalhes = get_book_details(st.session_state.token_acesso, book_id)
        if detalhes:
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(detalhes.get('image_url', ''), width='stretch')
            with c2:
                st.subheader(detalhes.get('title'))
                st.write(f'**Gênero:** {detalhes.get("genre")}')
                st.write(f'**Avaliação:** {detalhes.get("rating")}')
                st.write(f'**Estoque:** {detalhes.get("availability")} unidades')
                st.write(f'**Preço:** £{detalhes.get("price_incl_tax")}')
                st.write(f'**UPC:** {detalhes.get("upc")}')
            st.divider()
            st.markdown('**Descrição**')
            st.write(detalhes.get('description', 'Sem descrição disponível.'))
        else:
            st.error('Não foi possível carregar os dados deste livro.')
    except Exception as e:
        logger.exception(f'error: {e}')
        st.error('Ocorreu um erro interno ao carregar os detalhes.')