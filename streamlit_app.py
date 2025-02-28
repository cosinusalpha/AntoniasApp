import streamlit as st
import numpy as np
import random

# Titel der App
st.title("Tic Tac Toe")

# Initialisiere das Spielbrett und den Spielzustand in der Session State
if 'board' not in st.session_state:
    st.session_state.board = np.array([['' for _ in range(3)] for _ in range(3)])
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'  # 'X' beginnt
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'stats_x' not in st.session_state:
    st.session_state.stats_x = 0
if 'stats_o' not in st.session_state:
    st.session_state.stats_o = 0
if 'stats_draw' not in st.session_state:
    st.session_state.stats_draw = 0
if 'mode' not in st.session_state:
    st.session_state.mode = 'Einzelspieler'  # Standardmodus
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'Hoch 😈'  # Standard: Hoch (Minimax)

# Funktion zur Überprüfung des Gewinns
def check_winner(board, player):
    # Überprüfe Zeilen und Spalten
    for i in range(3):
        if np.all(board[i, :] == player) or np.all(board[:, i] == player):
            return True
    # Überprüfe Diagonalen
    if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
        return True
    return False

# Funktion zur Überprüfung von Unentschieden
def check_draw(board):
    return not np.any(board == '')

# Funktion zum Zurücksetzen des Spiels
def reset_game():
    st.session_state.board = np.array([['' for _ in range(3)] for _ in range(3)])
    st.session_state.current_player = 'X'
    st.session_state.winner = None
    st.session_state.game_over = False

# Funktion für den Computerzug (zufällig)
def computer_move_random(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    if empty_cells:
        move = random.choice(empty_cells)
        board[move[0]][move[1]] = 'O'

# Funktion für den Computerzug (Minimax-Algorithmus)
def computer_move_minimax(board):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        board[best_move[0]][best_move[1]] = 'O'

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    elif check_winner(board, 'X'):
        return -1
    elif check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

# Funktion für den Computerzug basierend auf dem Schwierigkeitsgrad
def computer_move(board):
    if st.session_state.difficulty.startswith('Leicht'):
        computer_move_random(board)
    elif st.session_state.difficulty.startswith('Mittel'):
        # Einfacher Algorithmus
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    if check_winner(board, 'O'):
                        return
                    board[i][j] = ''
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    if check_winner(board, 'X'):
                        board[i][j] = 'O'
                        return
                    board[i][j] = ''
        computer_move_random(board)
    elif st.session_state.difficulty.startswith('Hoch'):
        computer_move_minimax(board)

# Funktion zur Handhabung eines Spielzugs
def handle_move(i, j):
    if not st.session_state.game_over and st.session_state.board[i][j] == '':
        if st.session_state.mode == 'Einzelspieler':
            if st.session_state.current_player == 'X':
                # Spielerzug
                st.session_state.board[i][j] = 'X'
                if check_winner(st.session_state.board, 'X'):
                    st.session_state.winner = 'X'
                    st.session_state.game_over = True
                    st.session_state.stats_x += 1
                elif check_draw(st.session_state.board):
                    st.session_state.winner = 'Unentschieden'
                    st.session_state.game_over = True
                    st.session_state.stats_draw += 1
                else:
                    # Computerzug ausführen
                    computer_move(st.session_state.board)
                    if check_winner(st.session_state.board, 'O'):
                        st.session_state.winner = 'O'
                        st.session_state.game_over = True
                        st.session_state.stats_o += 1
                    elif check_draw(st.session_state.board):
                        st.session_state.winner = 'Unentschieden'
                        st.session_state.game_over = True
                        st.session_state.stats_draw += 1
                    else:
                        st.session_state.current_player = 'X'
        elif st.session_state.mode == 'Mehrspieler':
            # Spieler X und O wechseln sich ab
            st.session_state.board[i][j] = st.session_state.current_player
            if check_winner(st.session_state.board, st.session_state.current_player):
                st.session_state.winner = st.session_state.current_player
                st.session_state.game_over = True
                if st.session_state.current_player == 'X':
                    st.session_state.stats_x += 1
                else:
                    st.session_state.stats_o += 1
            elif check_draw(st.session_state.board):
                st.session_state.winner = 'Unentschieden'
                st.session_state.game_over = True
                st.session_state.stats_draw += 1
            else:
                # Wechsle den Spieler
                st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

# Sidebar Einstellungen
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #b5e2ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Auswahl des Spielmodus in der Sidebar
st.sidebar.header("Einstellungen")
mode_options = ['Einzelspieler', 'Mehrspieler']
st.session_state.mode = st.sidebar.selectbox("Spielmodus", mode_options, index=0)

# Auswahl des Schwierigkeitsgrads (nur im Einzelspielermodus)
if st.session_state.mode == 'Einzelspieler':
    difficulty_options = ['Leicht 😊', 'Mittel 😐', 'Hoch 😈']
    st.session_state.difficulty = st.sidebar.selectbox("Schwierigkeitsgrad", difficulty_options, index=2)
else:
    st.session_state.difficulty = None

# Spielstatistiken in der Sidebar
st.sidebar.header("Spielstatistiken")
if st.session_state.mode == 'Einzelspieler':
    st.sidebar.write(f"Deine Siege (X): {st.session_state.stats_x} 🏆")
    st.sidebar.write(f"Computer Siege (O): {st.session_state.stats_o} 🤖")
    st.sidebar.write(f"Unentschieden: {st.session_state.stats_draw} 🤝")
else:
    st.sidebar.write(f"Spieler X Siege: {st.session_state.stats_x} 🏆")
    st.sidebar.write(f"Spieler O Siege: {st.session_state.stats_o} 🏅")
    st.sidebar.write(f"Unentschieden: {st.session_state.stats_draw} 🤝")

# Erstelle eine bessere visuelle Darstellung des Spielfelds mit Buttons
st.markdown(
    """
    <style>
    /* Stil für das Spielbrett */
    .gameboard-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    /* Stil für die Buttons im Spielbrett */
    .gameboard-container .stButton > button {
        width: 80px;
        height: 80px;
        font-size: 32px;
        font-weight: bold;
        margin: 3px;
        border: 2px solid #333;
        border-radius: 0;
        background-color: #f0f0f0;
        transition: background-color 0.3s;
    }

    /* Hover-Effekt für leere Zellen */
    .gameboard-container .stButton > button:hover:not([disabled]) {
        background-color: #e0e0e0;
    }

    /* Stil für belegte Zellen */
    .gameboard-container .stButton > button[disabled] {
        opacity: 1;
        color: #000;
    }

    /* X und O unterschiedlich färben */
    .gameboard-container .stButton > button[disabled]:contains("X") {
        color: #0066cc;
    }
    .gameboard-container .stButton > button[disabled]:contains("O") {
        color: #cc0000;
    }

    /* Responsive Design für mobile Geräte */
    @media (max-width: 640px) {
        .gameboard-container .stButton > button {
            width: 60px;
            height: 60px;
            font-size: 24px;
            margin: 2px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Zeige die Anleitung an
st.markdown("### Klicke auf ein Feld, um deinen Zug zu machen!")

# Container für das Spielbrett
st.markdown('<div class="gameboard-container">', unsafe_allow_html=True)

# Erstelle das Spielbrett mit 3 Spalten
col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    # Für jede Zeile im Spielfeld
    for i in range(3):
        # Erstelle 3 Spalten für jede Zeile des Spielbretters
        cols = st.columns(3)
        for j in range(3):
            # Ermittle den Button-Text basierend auf dem Spielbrettstatus
            cell_value = st.session_state.board[i][j]
            button_text = cell_value if cell_value != '' else " "
            
            # Erstelle den Button für jede Zelle
            clicked = cols[j].button(
                button_text,
                key=f"cell_{i}_{j}",
                disabled=(cell_value != '' or st.session_state.game_over)
            )
            
            # Wenn der Button geklickt wurde, führe den Zug aus
            if clicked:
                handle_move(i, j)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Anzeige des aktuellen Spielers oder des Gewinners
if st.session_state.winner:
    if st.session_state.winner == 'Unentschieden':
        st.success("Unentschieden! 🤝")
    else:
        if st.session_state.mode == 'Einzelspieler':
            if st.session_state.winner == 'X':
                st.success("Du hast gewonnen! 🎉")
            else:
                st.success("Computer hat gewonnen! 🤖")
        elif st.session_state.mode == 'Mehrspieler':
            st.success(f"Spieler {st.session_state.winner} hat gewonnen! 🎉")
else:
    if st.session_state.mode == 'Einzelspieler':
        st.info(f"Aktueller Spieler: {st.session_state.current_player} 🕹️")
    elif st.session_state.mode == 'Mehrspieler':
        st.info(f"Aktueller Spieler: {st.session_state.current_player} 👥")

# Schaltfläche zum Zurücksetzen des Spiels
if st.button("Neues Spiel starten 🎲", key="reset_button"):
    reset_game()
    st.rerun()