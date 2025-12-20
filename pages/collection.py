import logging
import streamlit as st
from scripts.books_utils import (
    get_books_by_search, 
    get_book_details, 
    get_books_by_price_range,
    get_top_rated
)
from scripts.categories_utils import get_all_categories
from scripts.ml_utils import get_user_preferences 
from scripts import get_cookies, set_cookies


logger = logging.getLogger(__name__)


def show() -> None:
    #gerenciando sessao
    set_cookies('page', 'collection')
    token = get_cookies('token_acesso')
    user_id = get_cookies('user_id')

    #filtros
    st.sidebar.title('Filtros')
    title_genre_filter = st.sidebar.toggle('Título ou Gênero', value=False)
    price_range_filter = st.sidebar.toggle('Faixa de Preço', value=False)
    
    title = ''
    option = 'Todas'
    p_min = 0.00
    p_max = 100.00

    if title_genre_filter or price_range_filter:
        with st.sidebar.container():
            if title_genre_filter:
                st.sidebar.markdown('### Título ou Gênero') 
                title = st.sidebar.text_input('Título', placeholder='Ex: The White Queen', key='input_title')
                categories = get_all_categories(token)
                options = ['Todas'] + [c['category'] for c in categories] if categories else ['Todas']
                option = st.sidebar.selectbox('Gênero', options=options, key='input_genre')
            if title_genre_filter and price_range_filter:
                st.sidebar.divider()
            if price_range_filter:
                st.sidebar.markdown('### Faixa de Preço')
                p_min = st.sidebar.number_input('Mínimo (£)', min_value=0.0, value=0.00, step=1.0)
                p_max = st.sidebar.number_input('Máximo (£)', min_value=0.0, value=100.0, step=1.0)
            st.sidebar.write('')
            if st.sidebar.button('Aplicar', type='primary', width='stretch'):
                category = None if option == 'Todas' else option
                
                if price_range_filter and not title_genre_filter:
                    st.session_state.books_collection = get_books_by_price_range(token, p_min, p_max)
                elif title_genre_filter and not price_range_filter:
                    if not title and not category:
                        st.session_state.books_collection = get_top_rated(token, limit=10)
                    else:
                        st.session_state.books_collection = get_books_by_search(token, title=title or None, genre=category)
                elif price_range_filter and title_genre_filter:
                    books_raw = get_books_by_price_range(token, p_min, p_max)
                    if isinstance(books_raw, list):
                        st.session_state.books_collection = [
                            b for b in books_raw 
                            if (not title or title.lower() in b.get('title', '').lower()) and
                            (not category or b.get('genre') == category)
                        ]
                st.session_state.filtros_ativos = True
    else:
        if st.session_state.get('filtros_ativos', False):
            st.session_state.books_collection = get_top_rated(token, limit=10)
            st.session_state.filtros_ativos = False
            st.rerun()
        st.sidebar.info('Ative os filtros acima para consulta')

    #título
    st.title('Acervo')
    #botao de voltar
    _, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button('←', help='Voltar ao Menu', width='stretch'):
            set_cookies('page', 'menu')
            st.rerun()
    st.markdown('---')

    #recomendações
    st.subheader('⭐ Recomendados para você')
    with st.container(border=True):
        user_id = int(user_id) if user_id else 0
        prefs = get_user_preferences(token, user_id)
        st.session_state.user_prefs = prefs if isinstance(prefs, list) else []
        if 'pref_index' not in st.session_state:
            st.session_state.pref_index = 0
        user_prefs = st.session_state.user_prefs
        col1, col2, col3 = st.columns([.1, .8, .1])
        with col1:
            if st.button('←', disabled=st.session_state.pref_index == 0, key='prev_pref', width='stretch'):
                st.session_state.pref_index = max(0, st.session_state.pref_index - 3)
                st.rerun()
        with col2:
            total = len(user_prefs)
            atual = (st.session_state.pref_index // 3) + 1
            total_paginas = (total + 2) // 3
            st.markdown(f'<p style="text-align: center; color: gray;">{atual} de {total_paginas}</p>', unsafe_allow_html=True)
        with col3:
            if st.button('→', disabled=st.session_state.pref_index + 3 >= total, key='next_pref', width='stretch'):
                st.session_state.pref_index += 3
                st.rerun()
        idx = st.session_state.pref_index
        livros_visiveis = user_prefs[idx : idx + 3]
        cols_pref = st.columns(3)
        for i, book in enumerate(livros_visiveis):
            with cols_pref[i]:
                with st.container(border=True):
                    url_img = book.get('image_url') or 'https://via.placeholder.com/150x200?text=Sem+Capa'
                    st.markdown(
                        f'''
                            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                                <img src="{url_img}" style="height: 200px; object-fit: contain; border-radius: 4px;">
                            </div>
                        ''', 
                        unsafe_allow_html=True
                    )
                    titulo = book.get('title', 'Sem título')
                    st.markdown(f'**{titulo[:25]}...**' if len(titulo) > 25 else f'**{titulo}**')
                    st.caption(f"🔥 {book.get('similarity_score', 0):.2%} similar")
                    if st.button('Detalhes', key=f'btn_pref_{book.get("id")}_{idx+i}', width='stretch'):
                        details(book.get('id'), token)
    
    #acervo
    #inicializa o catálogo no estado da sessão
    if 'books_collection' not in st.session_state:
        st.session_state.books_collection = get_top_rated(token, limit=10)
    books = st.session_state.books_collection
    st.subheader('Melhores avaliações')
    if not books or (isinstance(books, dict) and 'msg' in books):
        st.warning('Nenhum livro encontrado para os filtros aplicados')
    else:
        for i in range(0, len(books), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(books):
                    book = books[i + j]
                    with cols[j]:
                        with st.container(border=True):
                            url_img = book.get('image_url') or 'https://via.placeholder.com/150x200?text=Sem+Capa'
                            st.markdown(
                                f'''
                                    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                                        <img src="{url_img}" style="height: 200px; object-fit: contain; border-radius: 4px;">
                                    </div>
                                ''', 
                                unsafe_allow_html=True
                            )
                            book_title = book.get('title', 'Sem título')
                            st.markdown(f'**{book_title[:35]}...**' if len(book_title) > 35 else f'**{book_title}**')
                            st.write(f'£{book.get("price")}')
                            if book.get('rating'): st.caption(f"⭐ {book.get('rating')}")
                            if st.button('Detalhes', key=f'btn_{book.get("id")}_{i+j}', width='stretch'):
                                details(book.get('id'), token)


@st.dialog('Detalhes')
def details(book_id: int, token: str) -> None:
    '''
    Exibe uma janela de diálogo com as informações detalhadas de um livro.

    Args:
        book_id (int): O identificador único do livro.
        token (str): O token de autenticação para a requisição da API.

    Returns:
        None
    '''
    try:
        detalhes = get_book_details(token, book_id)
        if detalhes:
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(detalhes.get('image_url', ''), width='stretch')
            with c2:
                st.subheader(detalhes.get('title'))
                st.write(f'**Gênero:** {detalhes.get("genre")}')
                st.write(f'**Preço:** £{detalhes.get("price_incl_tax")}')
            st.divider()
            st.write(detalhes.get('description', 'Sem descrição disponível.'))
    except Exception as e:
        logger.exception(f'error: {e}')
        st.error('Erro ao carregar detalhes.')