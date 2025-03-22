import sqlite3
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect
import io
import base64
import time

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_bd():
    return sqlite3.connect("sgr.db")

# Página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Página de login
@app.route('/login')
def login():
    time.sleep(2)
    return render_template('login.html')

# Página de registro
@app.route('/register')
def register():
    time.sleep(2)
    return render_template('register.html')

# Página "Sobre"
@app.route('/about')
def about():
    return render_template('about.html')

# Página de contato
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Página da dashboard com lista de avarias
@app.route('/dashboard')
def dashboard():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM avarias")
    avarias = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', avarias=avarias)

# Adicionar nova avaria
@app.route('/add_avaria', methods=['POST'])
def add_avaria():
    tipo = request.form.get("tipo")
    descricao = request.form.get("descricao")
    status = "Pendente"

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO avarias (tipo, descricao, status) VALUES (?, ?, ?)", (tipo, descricao, status))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

# Atualizar status da avaria
@app.route('/update_avaria/<int:avaria_id>', methods=['POST'])
def update_avaria(avaria_id):
    novo_status = request.form.get("status")
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE avarias SET status = ? WHERE id = ?", (novo_status, avaria_id))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

# Gerar gráfico de avarias
def gerar_grafico():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM avarias GROUP BY status")
    dados = cursor.fetchall()
    conn.close()

    if not dados:
        return None

    labels = [row[0] for row in dados]
    valores = [row[1] for row in dados]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, valores, color=['red', 'orange', 'green'])
    plt.xlabel("Status das Avarias")
    plt.ylabel("Quantidade")
    plt.title("Relatório de Avarias")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    grafico_base64 = base64.b64encode(img.getvalue()).decode()

    return grafico_base64

# Página do relatório
@app.route('/relatorio')
def relatorio():
    grafico = gerar_grafico()
    return render_template('relatorio.html', grafico=grafico)

# Rodar o app
if __name__ == '__main__':
    app.run(debug=True)
