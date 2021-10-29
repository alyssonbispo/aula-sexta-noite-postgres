import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__) 
      

@app.route('/criatabelas', methods=['GET']) 
def criar_tabelas():
    commands = (
        """
        CREATE TABLE clientes (
            cliente_id SERIAL PRIMARY KEY,
            cliente_nome VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE produtos (
                produto_id SERIAL PRIMARY KEY,
                produto_nome VARCHAR(255) NOT NULL
                )
        """)

    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    # create table one by one
    for command in commands:
        cur.execute(command)
    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
    return 'Tabelas criadas!', 200

@app.route('/cliente', methods=['POST']) 
def inserir_clientes():
    my_params = request.form
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("INSERT INTO clientes (cliente_nome) VALUES(%s) ",(my_params.get("nome"),))
    cur.close()
    # commit the changes
    conn.commit()
    return 'Usuário inserido', 200

@app.route('/cliente')
def get_clientes():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes")
    mobile_records = cur.fetchall()
    for row in mobile_records:
        print("Id = ", row[0], )
        print("Nome = ", row[1], "\n")
    
    cur.close()
    return jsonify(mobile_records),200

@app.route('/cliente/<id>')
def get_cliente(id):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes WHERE cliente_id=%s ",(id,))
    mobile_records = cur.fetchall()
    for row in mobile_records:
        print("Id = ", row[0], )
        print("Nome = ", row[1], "\n")
    
    cur.close()
    # commit the changes
    conn.commit()
    return jsonify(mobile_records),200

@app.route('/cliente/<id>', methods=['PATCH'])
def update_cliente(id):
    my_params = request.form
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("UPDATE clientes SET cliente_nome = %s WHERE cliente_id=%s ",(my_params.get("novo_nome"), id))
    cur.close()
    # commit the changes
    conn.commit()
    return "Cliente Alterado Com Sucesso!", 200

@app.route('/cliente/<id>', methods=['DELETE'])
def delete_cliente(id):
    my_params = request.form
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE cliente_id=%s ",(id))
    cur.close()
    # commit the changes
    conn.commit()
    return "Cliente Deletado Com Sucesso!", 200





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
