import sqlite3

def mostrar_resultados():
    # Conecta ao banco de dados
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    
    # Consulta SQL para contar os votos por candidato
    cursor.execute("SELECT candidato, COUNT(*) FROM votos GROUP BY candidato")
    resultados = cursor.fetchall()

    # Exibe os resultados
    print("Resultados Finais:")
    for resultado in resultados:
        print(f"{resultado[0]}: {resultado[1]} votos")
    
    # Fecha a conexão
    conn.close()

# Chamando a função para mostrar os resultados
mostrar_resultados()