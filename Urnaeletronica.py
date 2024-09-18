import sqlite3
import PySimpleGUI as sg
from datetime import datetime 

# Conecta ao banco de dados
def conectar_db():
    return sqlite3.connect('urna_eletronica.db')

def criar_tabela():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato TEXT,
            numero TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela()

def registrar_voto(candidato, numero):
    conn = conectar_db()
    cursor = conn.cursor()
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO votos (candidato, numero, data_hora)
        VALUES (?, ?, ?)
    ''', (candidato, numero, data_hora))
    conn.commit()
    conn.close()
    print(f"Voto registrado: Candidato: {candidato}, Número: {numero}, Data e Hora: {data_hora}")

def visualizar_dados():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM votos")
        votos = cursor.fetchall()
        conn.close()

        dados = ""
        for voto in votos:
            dados += f"ID: {voto[0]}, Candidato: {voto[1]}, Número: {voto[2]}, Data e Hora: {voto[3]}\n"

        return dados

    except sqlite3.Error as e:
        return f"Erro ao consultar os dados: {e}"

def determinar_vencedor():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT candidato, COUNT(*) FROM votos GROUP BY candidato")
        votos_contagem = cursor.fetchall()
        conn.close()

        if not votos_contagem:
            return "Nenhum voto registrado."

        # Encontrar o candidato com o maior número de votos
        vencedor = max(votos_contagem, key=lambda item: item[1])
        return f"Vencedor: {vencedor[0]} com {vencedor[1]} votos."

    except sqlite3.Error as e:
        return f"Erro ao determinar o vencedor: {e}"

# Lista de candidatos
candidatos = {
    "12": "Candidato 1",
    "34": "Candidato 2",
    "56": "Candidato 3",
}

# Layout da interface
layout = [
    [sg.Text("Digite o número do candidato:")],
    [sg.Input(key='-INPUT-', size=(20,1))],
    [sg.Button("Confirmar"), sg.Button("Branco"), sg.Button("Cancelar")],
    [sg.Output(size=(50, 10), key='-OUTPUT-')],
    [sg.Button("Finalizar Eleição")],
    [sg.Button("Visualizar Resultados")],
    [sg.Multiline(size=(50, 10), key='-RESULTADOS-', disabled=True)],
    [sg.Text(size=(50, 2), key='-VENCEDOR-')]  # Adiciona um campo para exibir o vencedor
]

# Criação da janela
window = sg.Window("Urna Eletrônica", layout)

# Loop de eventos
while True:
    event, values = window.read()

    # Fechar o programa
    if event == sg.WINDOW_CLOSED:
        break

    # Verificar se o botão "Confirmar" foi pressionado
    if event == "Confirmar":
        numero = values['-INPUT-']
        if numero in candidatos:
            candidato = candidatos[numero]
            registrar_voto(candidato, numero)  # Registrar o voto no banco de dados
            print(f"Voto computado para {candidato}")
        else:
            registrar_voto("Nulo", numero)  # Registrar voto nulo no banco de dados
            print("Voto nulo computado.")
        window['-INPUT-'].update('')

    # Verificar se o botão "Branco" foi pressionado
    elif event == "Branco":
        registrar_voto("Nulo", "Branco")  # Registrar voto em branco no banco de dados
        print("Voto em branco computado.")
        window['-INPUT-'].update('')

    # Verificar se o botão "Cancelar" foi pressionado
    elif event == "Cancelar":
        window['-INPUT-'].update('')

    # Verificar se o botão "Finalizar Eleição" foi pressionado
    elif event == "Finalizar Eleição":
        print("Resultados Finais:")
        
        # Mostrar o vencedor na interface
        vencedor = determinar_vencedor()
        window['-VENCEDOR-'].update(vencedor)
        
        # Exibir uma janela modal para o vencedor antes de fechar
        sg.popup(vencedor, title="Vencedor da Eleição")
        break

    # Verificar se o botão "Visualizar Resultados" foi pressionado
    elif event == "Visualizar Resultados":
        resultados = visualizar_dados()
        window['-RESULTADOS-'].update(resultados)

# Fecha a janela
window.close()
