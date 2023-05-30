#Trabalho de IA
#Aluno: Antonio Marques Soares de Souza, RGA: 202021901003
#Aluno: Gabriel de Souza Fialho, RGA:202021901019
#Jogo da Velha - Com 3 níveis de dificuldade

import tkinter as tk
from tkinter import messagebox
import random

# Função para exibir uma mensagem de vitória ou empate
def show_message(message):
    messagebox.showinfo("Resultado", message)

# Função para atualizar o texto do botão clicado
def update_button_text(row, col):
    button = buttons[row][col]
    if button["text"] == " ":
        button["text"] = "X"
        button["state"] = tk.DISABLED
        if check_winner("X"):
            show_message("Você venceu!")
            reset_game()
            choose_difficulty()
        elif is_board_full():
            show_message("Deu Velha!")
            reset_game()
        else:
            make_computer_move()

# Função para fazer a jogada do computador (Inteligência Artificial)
def make_computer_move():
    difficulty = difficulty_var.get()

    if difficulty == "Fácil":
        make_computer_move_easy()
    elif difficulty == "Médio":
        make_computer_move_medium()
    elif difficulty == "Difícil":
        make_computer_move_hard()

    if check_winner("O"):
        show_message("O computador ganhou!")
        reset_game()
        choose_difficulty()
    elif is_board_full():
        show_message("Deu Velha!")
        reset_game()

# Função para fazer a jogada do computador no nível fácil (jogada aleatória)
def make_computer_move_easy():
    available_buttons = []
    for row in range(3):
        for col in range(3):
            button = buttons[row][col]
            if button["text"] == " ":
                available_buttons.append(button)

    if available_buttons:
        button = random.choice(available_buttons)
        button["text"] = "O"
        button["state"] = tk.DISABLED

# Função para fazer a jogada do computador no nível médio
def make_computer_move_medium():
    # Verificar se há uma jogada que resulta em vitória imediata para o computador
    for row in range(3):
        for col in range(3):
            if buttons[row][col]["text"] == " ":
                # Faz a jogada e verifica se venceu
                buttons[row][col]["text"] = "O"
                if check_winner("O"):
                    return
                else:
                    # Desfaz a jogada
                    buttons[row][col]["text"] = " "

    # Verificar se há uma jogada que bloqueia uma possível vitória do jogador
    for row in range(3):
        for col in range(3):
            if buttons[row][col]["text"] == " ":
                # Faz a jogada e verifica se o jogador pode vencer
                buttons[row][col]["text"] = "X"
                if check_winner("X"):
                    # Bloqueia a jogada do jogador
                    buttons[row][col]["text"] = "O"
                    buttons[row][col]["state"] = tk.DISABLED
                    return
                else:
                    # Desfaz a jogada
                    buttons[row][col]["text"] = " "

    make_computer_move_easy()

# Função para fazer a jogada do computador no nível difícil
# Utiliza o algoritmo Minimax para buscar a melhor jogada
def make_computer_move_hard():
    best_score = float("-inf")
    best_move = None

    for row in range(3):
        for col in range(3):
            if buttons[row][col]["text"] == " ":
                buttons[row][col]["text"] = "O"
                score = minimax(buttons, 0, False)
                buttons[row][col]["text"] = " "

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        row, col = best_move
        buttons[row][col]["text"] = "O"
        buttons[row][col]["state"] = tk.DISABLED

# Função para avaliar a pontuação no algoritmo Minimax
def evaluate(board):
    if check_winner("O"):
        return 1
    elif check_winner("X"):
        return -1
    else:
        return 0

# Função para verificar se há um vencedor
def check_winner(symbol):
    # Verificar linhas
    for row in range(3):
        if buttons[row][0]["text"] == buttons[row][1]["text"] == buttons[row][2]["text"] == symbol:
            return True

    # Verificar colunas
    for col in range(3):
        if buttons[0][col]["text"] == buttons[1][col]["text"] == buttons[2][col]["text"] == symbol:
            return True

    # Verificar diagonais
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] == symbol:
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] == symbol:
        return True

    return False

# Função para verificar se o tabuleiro está completo
def is_board_full():
    return all(button["text"] != " " for row in buttons for button in row)

# Função para resetar o jogo
def reset_game():
    for row in range(3):
        for col in range(3):
            buttons[row][col]["text"] = " "
            buttons[row][col]["state"] = tk.NORMAL

# Função para escolher a dificuldade do jogo
def choose_difficulty():
    difficulty_frame.pack()
    game_frame.pack_forget()

# Função para iniciar o jogo
def start_game():
    difficulty_frame.pack_forget()
    game_frame.pack()

# Função para calcular a pontuação Minimax
def minimax(board, depth, is_maximizing):
    if check_winner("O"):
        return 1
    elif check_winner("X"):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = float("-inf")
        for row in range(3):
            for col in range(3):
                if board[row][col]["text"] == " ":
                    board[row][col]["text"] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col]["text"] = " "
                    best_score = max(score, best_score)
                    if depth == 0 and best_score == 1:
                        return best_score
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col]["text"] == " ":
                    board[row][col]["text"] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col]["text"] = " "
                    best_score = min(score, best_score)
                    if depth == 0 and best_score == -1:
                        return best_score
        return best_score

# Criação da janela principal
window = tk.Tk()
window.title("Jogo da Velha")
window.geometry("300x300")

# Frame para seleção de dificuldade
difficulty_frame = tk.Frame(window)

difficulty_label = tk.Label(difficulty_frame, text="Escolha a dificuldade:")
difficulty_label.pack(pady=10)

difficulty_var = tk.StringVar()
difficulty_var.set("Fácil")

difficulty_options = ["Fácil", "Médio", "Difícil"]
difficulty_menu = tk.OptionMenu(difficulty_frame, difficulty_var, *difficulty_options)
difficulty_menu.pack(pady=10)

start_button = tk.Button(difficulty_frame, text="Iniciar Jogo", command=start_game)
start_button.pack(pady=10)

# Frame para o jogo
game_frame = tk.Frame(window)

# Criação dos botões
buttons = []
for row in range(3):
    row_buttons = []
    for col in range(3):
        button = tk.Button(game_frame, text=" ", width=10, height=5,
                           command=lambda r=row, c=col: update_button_text(r, c))
        button.grid(row=row, column=col, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Execução da janela principal
choose_difficulty()
window.mainloop()

