# Imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# My app
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"
db = SQLAlchemy(app)


class Movimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.Integer, default=0)
    valor = db.Column(db.Float, default=0.0)
    data_add = db.Column(db.DateTime, default=datetime.utcnow)
    data_update = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Movimento {self.id}"



# ROUTES

# página inicial
@app.route("/", methods=["POST", "GET"])
def index():
    # POST
    if request.method == "POST":
        descricao = request.form["descricao"]
        tipo = request.form["tipo"]
        valor = request.form["valor"]
        new_movimento = Movimento(descricao=descricao, tipo=tipo, valor=valor)
        try:
            db.session.add(new_movimento)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"

    #GET
    if request.method == "GET":
        movimentos = Movimento.query.order_by(Movimento.data_add).all()
        return render_template("index.html", movimentos=movimentos)

# excluir movimento
@app.route("/delete/<int:id>")
def delete_movimento(id:int):
    movimento = Movimento.query.get_or_404(id)
    try:
        db.session.delete(movimento)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

# editar movimento
@app.route("/update/<int:id>", methods=["POST", "GET"])
def update_movimento(id:int):
    movimento = Movimento.query.get_or_404(id)
    if request.method == "POST":
        movimento.descricao = request.form['descricao']
        movimento.tipo = request.form['tipo']
        movimento.valor = request.form['valor']
        movimento.data_update = datetime.utcnow()
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    
    if request.method == "GET":
        return render_template("update.html", movimento=movimento)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)