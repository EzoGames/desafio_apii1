from flask import Flask, request, jsonify 
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/")
def exibir_mensagem():

    return "<h1>Bem vindo(a)</h1>"

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute(

            """
            create table if not exists LIVRO(
            id integer primary key autoincrement,
            titulo text not null,
            autor text not null,  
            categoria text not null,
            image_url text not null
                )

            """
        )

init_db()

@app.route("/doar", methods =["POST"])

def doar():

    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
            INSERT INTO LIVRO (titulo, categoria,autor,image_url)
            VALUES ("{titulo}","{categoria}","{autor}","{image_url}")
""")

    conn.commit() 

    return jsonify({"mensagem":"Livro cadastrado com sucesso"}), 201

@app.route("/livros", methods=["GET"])
def listar_livros():
    with sqlite3.connect("database.db") as conn:

        livros = conn.execute("SELECT * FROM LIVRO").fetchall()

        print (f"Aqui estão os livros:{livros}")

        livros_formatados= []

        for item in livros:
            dicionario_livros={
            "id":item[0],
            "titulo":item[1],
            "categoria":item[2],
            "autor":item[3],
            "image_url":item[4]
        }
        
            livros_formatados.append(dicionario_livros)

    return jsonify(livros_formatados), 200


if __name__ == "__main__":
 
 
    app.run(debug=True)