from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].lower()
    email = request.form['email'].lower()
    password = request.form['password']
    role = request.form['role']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        flash('Nome de usuário ou E-mail já cadastrado. Escolha outro.', 'error')
        return redirect(url_for('index'))
    else:
        cursor.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)', (username, email, password, role))
        conn.commit()
        conn.close()
        flash('Registro Bem-Sucedido!')
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].lower()
    password = request.form['password']

    if username == 'admin' and password == 'root':
        session['username'] = 'admin'
        return render_template('dashboard.html', username='admin')
    else:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return render_template('dashboard.html', username=user[1])
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
            return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def contact():
    contactname = request.form['contactname']
    contactemail = request.form['contactemail']
    company = request.form['company']
    message = request.form['message']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contact (contactname, contactemail, company, message) VALUES (?, ?, ?, ?)', (contactname, contactemail, company, message))
    conn.commit()
    conn.close()
    flash('Enviado com sucesso!')
    return redirect(url_for('contato'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        flash('Você precisa estar logado para acessar o painel de controle.', 'error')
        return redirect(url_for('index'))

@app.route('/api/vendas', methods=['GET'])
def obter_dados_vendas():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT username, vendasmes FROM users WHERE role = "vendedor" ORDER BY vendasmes DESC')
    dados_vendas = cursor.fetchall()

    conn.close()

    vendas_json = []
    for vendasmes in dados_vendas:
        username, vendasmes = vendasmes
        vendas_json.append({'username': username, 'vendasmes': vendasmes})

    return jsonify(vendas_json)

@app.route('/adicionar_vendas', methods=['POST'])
def adicionar_vendas():
    if 'username' in session:
        username = session['username']
        quantidade_vendas = int(request.form['quantidadeVendas'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET vendasmes = ? WHERE username = ?', (quantidade_vendas, username))
        conn.commit()
        conn.close()

        flash('Quantidade de vendas adicionada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Você precisa estar logado para adicionar vendas.', 'error')
        return redirect(url_for('index'))

@app.route('/api/usuarios', methods=['GET'])
def obter_dados_usuarios():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM users')
    total_usuarios = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM users WHERE role = "vendedor"')
    vendedores = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM users WHERE role = "comprador"')
    compradores = cursor.fetchone()[0]

    conn.close()

    usuarios_json = {
        'total': total_usuarios,
        'vendedores': vendedores,
        'compradores': compradores
    }

    return jsonify(usuarios_json)

if __name__ == '__main__':
    app.run(debug=True)