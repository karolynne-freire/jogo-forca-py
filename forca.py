from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'segredo'  # Necessário para sessão

PALAVRA = "python"

@app.route("/", methods=["GET", "POST"])
def index():
    if "letras_usuario" not in session:
        session["letras_usuario"] = []
        session["chances"] = 4
        session["ganhou"] = False

    if request.method == "POST":
        tentativa = request.form.get("letra").lower()
        if tentativa not in session["letras_usuario"]:
            session["letras_usuario"].append(tentativa)
            if tentativa not in PALAVRA:
                session["chances"] -= 1

        session["ganhou"] = all(letra in session["letras_usuario"] for letra in PALAVRA)

        if session["ganhou"] or session["chances"] <= 0:
            return redirect(url_for('fim'))

    exibicao = " ".join([letra if letra in session["letras_usuario"] else "_" for letra in PALAVRA])
    return render_template("index.html", exibicao=exibicao, chances=session["chances"])

@app.route("/fim")
def fim():
    ganhou = session["ganhou"]
    palavra = PALAVRA
    session.clear()  # limpa o jogo após o fim
    return render_template("fim.html", ganhou=ganhou, palavra=palavra)

if __name__ == "__main__":
    app.run(debug=True)

