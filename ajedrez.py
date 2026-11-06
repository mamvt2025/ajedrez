import random
import streamlit as st

st.set_page_config(page_title="Ajedrez Valdivieso ♟️", page_icon="♟️", layout="centered")

# Piezas Unicode estándar
PIEZAS = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',  # Negras
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',  # Blancas
    '.': ' '
}


def crear_tablero_inicial():
    return [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]


if "tablero" not in st.session_state:
    st.session_state.tablero = crear_tablero_inicial()
if "seleccion" not in st.session_state:
    st.session_state.seleccion = None
if "turno" not in st.session_state:
    st.session_state.turno = "BLANCAS"

st.title("♟️ Ajedrez Valdivieso (Sin Librerías Extra)")

st.sidebar.markdown(f"### Turno actual: **{st.session_state.turno}**")
if st.sidebar.button("🔄 Reiniciar Tablero"):
    st.session_state.tablero = crear_tablero_inicial()
    st.session_state.seleccion = None
    st.session_state.turno = "BLANCAS"
    st.rerun()

st.markdown("""
    <style>
    .stButton > button {
        font-size: 28px !important;
        height: 60px !important;
        width: 100% !important;
        padding: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Renderizar tablero 8x8 con botones interactivos
cols_letras = st.columns([0.5] + [1] * 8)
cols_letras[0].write("")
for idx, letra in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
    cols_letras[idx + 1].markdown(f"**<center>{letra}</center>**", unsafe_allow_html=True)

for i in range(8):
    cols = st.columns([0.5] + [1] * 8)
    cols[0].markdown(f"**{8 - i}**")
    for j in range(8):
        pieza_cod = st.session_state.tablero[i][j]
        pieza_simbolo = PIEZAS.get(pieza_cod, ' ')

        # Color del botón seleccionado
        es_seleccionado = st.session_state.seleccion == (i, j)
        label = f"📍 {pieza_simbolo}" if es_seleccionado else (pieza_simbolo if pieza_simbolo != ' ' else " ")

        with cols[j + 1]:
            if st.button(label, key=f"cell_{i}_{j}"):
                if st.session_state.seleccion is None:
                    if pieza_cod != '.':
                        st.session_state.seleccion = (i, j)
                        st.rerun()
                else:
                    orig_i, orig_j = st.session_state.seleccion
                    if (orig_i, orig_j) == (i, j):
                        st.session_state.seleccion = None
                    else:
                        # Mover pieza
                        st.session_state.tablero[i][j] = st.session_state.tablero[orig_i][orig_j]
                        st.session_state.tablero[orig_i][orig_j] = '.'
                        st.session_state.seleccion = None
                        st.session_state.turno = "NEGRAS" if st.session_state.turno == "BLANCAS" else "BLANCAS"
                    st.rerun()