import random
import time
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Ajedrez Didáctico Valdivieso ♟️",
    page_icon="♟️",
    layout="centered",
)

# Piezas Unicode y sus valores para la IA
PIEZAS = {
    'r': '♜',
    'n': '♞',
    'b': '♝',
    'q': '♛',
    'k': '♚',
    'p': '♟',  # Negras (PC)
    'R': '♖',
    'N': '♘',
    'B': '♗',
    'Q': '♕',
    'K': '♔',
    'P': '♙',  # Blancas (Jugador)
    '.': ' ',
}

VALORES = {
    'p': 10,
    'n': 30,
    'b': 30,
    'r': 50,
    'q': 90,
    'k': 900,
    'P': 10,
    'N': 30,
    'B': 30,
    'R': 50,
    'Q': 90,
    'K': 900,
}

# Estilos CSS Limpios y Didácticos
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1b2a47 0%, #0d1527 100%);
        color: #ffffff;
    }
    .board-frame {
        background-color: #5c3a21;
        border: 10px solid #3d2312;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7);
    }
    .stButton > button {
        font-size: 32px !important;
        height: 65px !important;
        width: 100% !important;
        border-radius: 4px !important;
        border: 1px solid rgba(0,0,0,0.2) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def crear_tablero():
    return [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]


# Inicialización del estado de sesión
if 'tablero' not in st.session_state:
    st.session_state.tablero = crear_tablero()
if 'seleccion' not in st.session_state:
    st.session_state.seleccion = None
if 'turno' not in st.session_state:
    st.session_state.turno = 'JUGADOR'
if 'historial' not in st.session_state:
    st.session_state.historial = []

st.title('♟️ Ajedrez Didáctico: Tú vs PC')

# Configuración en la Barra Lateral
st.sidebar.markdown('### 📊 Panel de Control')
dificultad = st.sidebar.selectbox(
    'Selecciona la Dificultad:', ['Fácil', 'Medio', 'Difícil']
)

turno_txt = (
    '🤠 Tu turno (Blancas ⚪)'
    if st.session_state.turno == 'JUGADOR'
    else '🤖 Pensando la PC...'
)
st.sidebar.markdown(f'**Turno actual:** {turno_txt}')

if st.sidebar.button('🔄 Reiniciar Partida', type='primary'):
    st.session_state.tablero = crear_tablero()
    st.session_state.seleccion = None
    st.session_state.turno = 'JUGADOR'
    st.session_state.historial = []
    st.rerun()

st.sidebar.markdown('---')
st.sidebar.markdown('### 💡 Guía Rápida:')
st.sidebar.write('1. Haz clic en una de **tus piezas blancas** para seleccionarla.')
st.sidebar.write('2. Haz clic en la **casilla de destino** para moverla.')


# Lógica de la Inteligencia Artificial con niveles de dificultad
def obtener_movimientos_pc(tablero):
    movimientos = []
    for r_origen in range(8):
        for c_origen in range(8):
            pieza = tablero[r_origen][c_origen]
            if pieza.islower():  # Piezas de la PC (Negras)
                for r_dest in range(8):
                    for c_dest in range(8):
                        destino = tablero[r_dest][c_dest]
                        if destino == '.' or destino.isupper():
                            movimientos.append(
                                (
                                    r_origen,
                                    c_origen,
                                    r_dest,
                                    c_dest,
                                    VALORES.get(destino, 0),
                                )
                            )
    return movimientos


def mover_pc(nivel):
    movs = obtener_movimientos_pc(st.session_state.tablero)
    if movs:
        if nivel == 'Fácil':
            # Movimiento completamente aleatorio
            eleccion = random.choice(movs)
        elif nivel == 'Medio':
            # 50% de probabilidad de elegir un movimiento inteligente o uno al azar
            capturas = [m for m in movs if m[4] > 0]
            if capturas and random.random() > 0.5:
                eleccion = random.choice(capturas)
            else:
                eleccion = random.choice(movs)
        else:  # Difícil
            # Prioriza siempre capturar la pieza de mayor valor posible
            movs.sort(key=lambda x: x[4], reverse=True)
            mejores_movs = [m for m in movs if m[4] == movs[0][4]]
            eleccion = random.choice(mejores_movs)

        r_o, c_o, r_d, c_d, _ = eleccion
        pieza_movida = st.session_state.tablero[r_o][c_o]
        st.session_state.tablero[r_d][c_d] = pieza_movida
        st.session_state.tablero[r_o][c_o] = '.'
        st.session_state.historial.append(
            f'🤖 PC movió {PIEZAS[pieza_movida]} a ({8 - r_d}, {chr(97 + c_d)})'
        )
        st.session_state.turno = 'JUGADOR'


# Renderizado Visual del Tablero
st.markdown('<div class="board-frame">', unsafe_allow_html=True)

# Encabezado de letras (a - h)
cols_letras = st.columns([0.4] + [1] * 8)
cols_letras[0].write('')
for idx, letra in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
    cols_letras[idx + 1].markdown(
        f"<h4 style='text-align: center; color: #f1c40f;'>{letra}</h4>",
        unsafe_allow_html=True,
    )

# Renderizado de casillas del tablero
for i in range(8):
    cols = st.columns([0.4] + [1] * 8)
    cols[0].markdown(
        f"<h4 style='color: #f1c40f; line-height: 60px;'>{8 - i}</h4>",
        unsafe_allow_html=True,
    )

    for j in range(8):
        pieza_cod = st.session_state.tablero[i][j]
        pieza_simbolo = PIEZAS.get(pieza_cod, ' ')
        es_blanca = (i + j) % 2 == 0

        # Colores didácticos del tablero de ajedrez tradicional
        bg_color = '#eeeed2' if es_blanca else '#769656'
        text_color = '#000000' if pieza_cod.isupper() else '#333333'

        # Resaltar casilla seleccionada
        if st.session_state.seleccion == (i, j):
            bg_color = '#baca44'

        with cols[j + 1]:
            label = f'{pieza_simbolo}' if pieza_simbolo != ' ' else ' '

            st.markdown(
                f"""
                <style>
                div[data-testid="stHorizontalBlock"] > div:nth-child({j + 2}) button {{
                    background-color: {bg_color} !important;
                    color: {text_color} !important;
                }}
                </style>
            """,
                unsafe_allow_html=True,
            )

            if st.button(
                label,
                key=f'cell_{i}_{j}',
                disabled=(st.session_state.turno == 'PC'),
            ):
                if st.session_state.seleccion is None:
                    if pieza_cod.isupper():
                        st.session_state.seleccion = (i, j)
                        st.rerun()
                else:
                    orig_i, orig_j = st.session_state.seleccion
                    if (orig_i, orig_j) == (i, j):
                        st.session_state.seleccion = None
                    else:
                        pieza_origen = st.session_state.tablero[orig_i][orig_j]
                        st.session_state.tablero[i][j] = pieza_origen
                        st.session_state.tablero[orig_i][orig_j] = '.'
                        st.session_state.seleccion = None
                        st.session_state.historial.append(
                            f'🤠 Tú moviste {PIEZAS[pieza_origen]} a ({8 - i}, {chr(97 + j)})'
                        )
                        st.session_state.turno = 'PC'
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Turno de la Computadora (IA con nivel seleccionado)
if st.session_state.turno == 'PC':
    with st.spinner('🤖 La PC está calculando su jugada...'):
        time.sleep(0.8)
        mover_pc(dificultad)
        st.rerun()

# Historial de jugadas limpio en un desplegable
with st.expander('📜 Ver Historial de la Partida'):
    if st.session_state.historial:
        for jugada in reversed(st.session_state.historial):
            st.write(jugada)
    else:
        st.write('Aún no hay movimientos registrados.')