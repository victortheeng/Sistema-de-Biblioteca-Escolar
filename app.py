import os
import sqlite3
from datetime import date, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "biblioteca.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
app.config["DATABASE"] = DB_PATH

def get_db():
    if "db" not in g:
        os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS Usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        perfil TEXT NOT NULL DEFAULT 'bibliotecario'
    );
    CREATE TABLE IF NOT EXISTS Livro (
        id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        categoria TEXT NOT NULL,
        quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0)
    );
    CREATE TABLE IF NOT EXISTS Emprestimo (
        id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
        data_emprestimo TEXT NOT NULL,
        data_devolucao TEXT,
        data_prevista TEXT NOT NULL,
        id_usuario INTEGER NOT NULL,
        id_livro INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'ativo' CHECK(status IN ('ativo','devolvido')),
        FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
        FOREIGN KEY (id_livro) REFERENCES Livro(id_livro)
    );
    """)
    if db.execute("SELECT COUNT(*) FROM Usuario").fetchone()[0] == 0:
        users = [
            ("Ana Souza","ana@escola.com",generate_password_hash("123456"),"bibliotecario"),
            ("Carlos Lima","carlos@escola.com",generate_password_hash("123456"),"bibliotecario"),
            ("Marina Alves","marina@escola.com",generate_password_hash("123456"),"bibliotecario")
        ]
        db.executemany("INSERT INTO Usuario(nome,email,senha,perfil) VALUES(?,?,?,?)", users)
    if db.execute("SELECT COUNT(*) FROM Livro").fetchone()[0] == 0:
        books = [
            ("Dom Casmurro","Machado de Assis","Literatura",8),
            ("O Pequeno Príncipe","Antoine de Saint-Exupéry","Infantil",5),
            ("Quarto de Despejo","Carolina Maria de Jesus","Literatura",4),
            ("Capitães da Areia","Jorge Amado","Literatura",6),
            ("A Revolução dos Bichos","George Orwell","Ficção",3)
        ]
        db.executemany("INSERT INTO Livro(titulo,autor,categoria,quantidade) VALUES(?,?,?,?)", books)
    if db.execute("SELECT COUNT(*) FROM Emprestimo").fetchone()[0] == 0:
        today = date.today()
        loans = [
            ((today-timedelta(days=8)).isoformat(),(today+timedelta(days=6)).isoformat(),1,1,"ativo"),
            ((today-timedelta(days=5)).isoformat(),(today+timedelta(days=9)).isoformat(),2,2,"ativo"),
            ((today-timedelta(days=20)).isoformat(),(today-timedelta(days=6)).isoformat(),3,3,"devolvido"),
            ((today-timedelta(days=3)).isoformat(),(today+timedelta(days=11)).isoformat(),1,4,"ativo"),
            ((today-timedelta(days=2)).isoformat(),(today+timedelta(days=12)).isoformat(),2,1,"ativo")
        ]
        for loan_date, due, user_id, book_id, status in loans:
            returned = (today-timedelta(days=6)).isoformat() if status == "devolvido" else None
            db.execute("""INSERT INTO Emprestimo(data_emprestimo,data_prevista,data_devolucao,id_usuario,id_livro,status)
                          VALUES(?,?,?,?,?,?)""", (loan_date,due,returned,user_id,book_id,status))
            if status == "ativo":
                db.execute("UPDATE Livro SET quantidade=quantidade-1 WHERE id_livro=?", (book_id,))
    db.commit()

@app.before_request
def ensure_db():
    init_db()

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("senha","")
        user = get_db().execute("SELECT * FROM Usuario WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["senha"], password):
            session.clear()
            session["user_id"] = user["id_usuario"]
            session["user_name"] = user["nome"]
            flash("Bem-vindo(a) ao sistema!", "success")
            return redirect(url_for("dashboard"))
        flash("E-mail ou senha inválidos.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "success")
    return redirect(url_for("login"))

@app.route("/")
@login_required
def dashboard():
    db=get_db()
    stats = {
        "books": db.execute("SELECT COUNT(*) FROM Livro").fetchone()[0],
        "loans": db.execute("SELECT COUNT(*) FROM Emprestimo WHERE status='ativo'").fetchone()[0],
        "users": db.execute("SELECT COUNT(*) FROM Usuario").fetchone()[0]
    }
    recent = db.execute("""SELECT e.*,u.nome AS usuario,l.titulo AS livro
        FROM Emprestimo e JOIN Usuario u ON u.id_usuario=e.id_usuario
        JOIN Livro l ON l.id_livro=e.id_livro ORDER BY e.id_emprestimo DESC LIMIT 5""").fetchall()
    return render_template("dashboard.html", stats=stats, recent=recent)

@app.route("/livros", methods=["GET","POST"])
@login_required
def books():
    db=get_db()
    if request.method=="POST":
        title=request.form.get("titulo","").strip()
        author=request.form.get("autor","").strip()
        category=request.form.get("categoria","").strip()
        try: quantity=int(request.form.get("quantidade","0"))
        except ValueError: quantity=-1
        if not title or not author or not category or quantity < 0:
            flash("Preencha todos os campos e informe quantidade igual ou maior que zero.","error")
        else:
            db.execute("INSERT INTO Livro(titulo,autor,categoria,quantidade) VALUES(?,?,?,?)",(title,author,category,quantity))
            db.commit(); flash("Livro cadastrado com sucesso!","success")
        return redirect(url_for("books"))
    term=request.args.get("q","").strip()
    rows=db.execute("""SELECT * FROM Livro WHERE titulo LIKE ? OR autor LIKE ? OR categoria LIKE ? ORDER BY titulo""",
                    (f"%{term}%",f"%{term}%",f"%{term}%")).fetchall()
    return render_template("books.html", books=rows, term=term)

@app.route("/livros/<int:book_id>/editar", methods=["POST"])
@login_required
def edit_book(book_id):
    title=request.form.get("titulo","").strip()
    author=request.form.get("autor","").strip()
    category=request.form.get("categoria","").strip()
    try: quantity=int(request.form.get("quantidade","-1"))
    except ValueError: quantity=-1
    db=get_db()
    if not title or not author or not category or quantity<0:
        flash("Dados inválidos. Quantidade deve ser zero ou maior.","error")
    else:
        active=db.execute("SELECT COUNT(*) FROM Emprestimo WHERE id_livro=? AND status='ativo'",(book_id,)).fetchone()[0]
        # quantity stores units currently available; do not allow a negative inventory.
        db.execute("UPDATE Livro SET titulo=?,autor=?,categoria=?,quantidade=? WHERE id_livro=?",
                   (title,author,category,quantity,book_id))
        db.commit(); flash("Livro atualizado.","success")
    return redirect(url_for("books"))

@app.route("/livros/<int:book_id>/excluir", methods=["POST"])
@login_required
def delete_book(book_id):
    db=get_db()
    loans=db.execute("SELECT COUNT(*) FROM Emprestimo WHERE id_livro=?",(book_id,)).fetchone()[0]
    if loans:
        flash("Não é possível excluir: há empréstimos vinculados ao livro.","error")
    else:
        db.execute("DELETE FROM Livro WHERE id_livro=?",(book_id,));db.commit()
        flash("Livro excluído.","success")
    return redirect(url_for("books"))

@app.route("/emprestimos", methods=["GET","POST"])
@login_required
def loans():
    db=get_db()
    if request.method=="POST":
        user_id=request.form.get("id_usuario","")
        book_id=request.form.get("id_livro","")
        loan_date=request.form.get("data_emprestimo","")
        due=request.form.get("data_prevista","")
        user=db.execute("SELECT id_usuario FROM Usuario WHERE id_usuario=?",(user_id,)).fetchone()
        book=db.execute("SELECT * FROM Livro WHERE id_livro=?",(book_id,)).fetchone()
        if not user or not book or not loan_date or not due or due < loan_date:
            flash("Confira os dados e as datas do empréstimo.","error")
        elif book["quantidade"] < 1:
            flash("Livro sem unidades disponíveis. Empréstimo não realizado.","error")
        else:
            db.execute("""INSERT INTO Emprestimo(data_emprestimo,data_prevista,id_usuario,id_livro,status)
                          VALUES(?,?,?,?, 'ativo')""",(loan_date,due,user_id,book_id))
            db.execute("UPDATE Livro SET quantidade=quantidade-1 WHERE id_livro=?",(book_id,))
            db.commit();flash("Empréstimo registrado. Estoque atualizado.","success")
        return redirect(url_for("loans"))
    users=db.execute("SELECT id_usuario,nome FROM Usuario ORDER BY nome").fetchall()
    books=db.execute("SELECT id_livro,titulo,quantidade FROM Livro ORDER BY titulo").fetchall()
    history=db.execute("""SELECT e.*,u.nome AS usuario,l.titulo AS livro
       FROM Emprestimo e JOIN Usuario u ON u.id_usuario=e.id_usuario
       JOIN Livro l ON l.id_livro=e.id_livro ORDER BY e.id_emprestimo DESC""").fetchall()
    return render_template("loans.html",users=users,books=books,loans=history,today=date.today().isoformat(),default_due=(date.today()+timedelta(days=14)).isoformat())

@app.route("/emprestimos/<int:loan_id>/devolver", methods=["POST"])
@login_required
def return_loan(loan_id):
    db=get_db()
    loan=db.execute("SELECT * FROM Emprestimo WHERE id_emprestimo=?",(loan_id,)).fetchone()
    if not loan:
        flash("Empréstimo não encontrado.","error")
    elif loan["status"]=="devolvido":
        flash("Este empréstimo já foi devolvido.","error")
    else:
        db.execute("UPDATE Emprestimo SET status='devolvido',data_devolucao=? WHERE id_emprestimo=?",(date.today().isoformat(),loan_id))
        db.execute("UPDATE Livro SET quantidade=quantidade+1 WHERE id_livro=?",(loan["id_livro"],))
        db.commit();flash("Devolução registrada e estoque atualizado.","success")
    return redirect(url_for("loans"))

@app.route("/relatorios")
@login_required
def reports():
    db=get_db()
    popular=db.execute("""SELECT l.titulo,l.autor,COUNT(e.id_emprestimo) AS total
       FROM Livro l LEFT JOIN Emprestimo e ON e.id_livro=l.id_livro
       GROUP BY l.id_livro ORDER BY total DESC,l.titulo LIMIT 10""").fetchall()
    overdue=db.execute("""SELECT e.*,u.nome AS usuario,l.titulo AS livro FROM Emprestimo e
       JOIN Usuario u ON u.id_usuario=e.id_usuario JOIN Livro l ON l.id_livro=e.id_livro
       WHERE e.status='ativo' AND e.data_prevista < ? ORDER BY e.data_prevista""",(date.today().isoformat(),)).fetchall()
    return render_template("reports.html",popular=popular,overdue=overdue)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"),404

if __name__ == "__main__":
    app.run(debug=True)
