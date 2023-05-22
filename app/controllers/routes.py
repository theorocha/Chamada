from flask import render_template, redirect, url_for
from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
from app import app, bcrypt, login_manager, db

from app.models.tables import User, Chamada, presenca
from app.models.forms import LoginForm, RegisterForm, ClassForm, PresentForm





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template('home.html')
    




@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)




@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html' , aulas = Chamada.query.all())


@app.route("/aula/<name>", methods=['GET', 'POST'])
@login_required
def aula(name):
    return render_template('aula.html' , alunos = presenca.query.filter_by(name = name), name=name)





@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = ClassForm()
    if form.validate_on_submit():
        nova_chamada = Chamada(name=form.name.data, password=form.password.data)
        db.session.add(nova_chamada)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("create.html", form=form)






@app.route("/confirm", methods=['GET', 'POST'])
@login_required
def confirm():
    form = PresentForm()
    
    if form.validate_on_submit():
        new_presenca = presenca(name=form.name.data, matricula=current_user.username)
        chamada = Chamada.query.filter_by(name=form.name.data).first()
        if chamada:
            if chamada.password == form.password.data:
                db.session.add(new_presenca)
                db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("confirm.html", form=form)



@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
