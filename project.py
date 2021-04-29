from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data import db_session
from data.users import User
from data.chat import Chats
from form.user import RegisterForm
from data.login_form import LoginForm
from data.chats import WriteForm
from data.add import AddForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    db_sess.commit()


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("off.html", m=True)
    else:
        return render_template("off.html", m=False)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if not current_user.is_authenticated:
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.name == form.name.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)
    else:
        return redirect('/chat')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/chat")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)
    else:
        return redirect('/chat')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/chat', methods=['GET', 'POST'])
def all_chats():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        chat = db_sess.query(Chats).filter((Chats.name_to == current_user.name),
                                           (Chats.message_to_user == 1))
        chat1 = db_sess.query(Chats).filter((Chats.name_out == current_user.name),
                                            (Chats.message_to_user == 1))
        res = chat.first()
        res1 = chat1.first()
        if res:
            return render_template("index.html", chat=chat, empty=False, l=True)
        else:
            if res1:
                return render_template("index.html", chat=chat1, empty=False, l=False)
            else:
                return render_template("index.html", chat=chat, empty=True)
    return redirect('/register')


@app.route('/chat/<name_out>/<name_to>', methods=['GET', 'POST'])
@login_required
def messages(name_out, name_to):
    form = WriteForm()
    if form.validate_on_submit():
        if type(form.text.data) == 'NoneType':
            if current_user.name == name_to:
                db_sess = db_session.create_session()
                chat = db_sess.query(Chats).filter(
                    (Chats.name_to == current_user.name) | (Chats.name_out ==
                                                            current_user.name))
                return render_template("chats.html", chat=chat, name=name_out, form=form,
                                       message="Введите сообщение")
            elif current_user.name == name_out:
                db_sess = db_session.create_session()
                chat = db_sess.query(Chats).filter(
                    (Chats.name_to == current_user.name) | (Chats.name_out ==
                                                            current_user.name))
                return render_template("chats.html", chat=chat, name=name_to, form=form,
                                       message="Введите сообщение")
        db_sess = db_session.create_session()
        if current_user.name == name_out:
            chat1 = db_sess.query(Chats).filter((Chats.name_out == current_user.name)).all()
            res1 = chat1[-1]
            ch = db_sess.query(Chats).all()
            ch1 = ch[-1]
            chat = Chats(
                id=ch1.id + 1,
                name_out=current_user.name,
                name_to=name_to,
                text=str(form.text.data),
                message_to_user=res1.message_to_user + 1
            )
        else:
            chat = db_sess.query(Chats).filter((Chats.name_to == current_user.name))
            res = chat.first()
            ch = db_sess.query(Chats).all()
            ch1 = ch[-1]
            chat = Chats(
                id=ch1.id + 1,
                name_out=current_user.name,
                name_to=name_out,
                text=str(form.text.data),
                message_to_user=res.message_to_user + 1
            )
        db_sess.add(chat)
        db_sess.commit()
        return redirect(f'/chat/{name_out}/{name_to}')
    else:
        if current_user.is_authenticated and current_user.name == name_to:
            db_sess = db_session.create_session()
            chat = db_sess.query(Chats).filter(((Chats.name_to == name_out) | (Chats.name_to
                                                                               == name_to)),
                                               ((Chats.name_out ==
                                                 name_to) | (Chats.name_out == name_out)))
            return render_template("chats.html", chat=chat, name=name_out, form=form)
        elif current_user.is_authenticated and current_user.name == name_out:
            db_sess = db_session.create_session()
            chat = db_sess.query(Chats).filter(((Chats.name_to == name_out) | (Chats.name_to
                                                                               == name_to)),
                                               ((Chats.name_out ==
                                                 name_to) | (Chats.name_out == name_out)))
            return render_template("chats.html", chat=chat, name=name_to, form=form)
        else:
            return ""


@app.route('/add_chat', methods=['GET', 'POST'])
@login_required
def add_chat():
    form = AddForm()
    if form.validate_on_submit():
        if type(form.text.data) == 'NoneType':
            return render_template("add.html", form=form,
                                   message="Введите сообщение")
        db_sess = db_session.create_session()
        if current_user.name == form.name.data:
            return render_template("add.html", form=form,
                                   message="Введёно название ваще аккаунта")
        chat = db_sess.query(Chats).filter(Chats.name_to == current_user.name, Chats.name_out ==
                                           form.name.data)
        chat1 = db_sess.query(Chats).filter(Chats.name_to == form.name.data, Chats.name_out ==
                                            current_user.name)
        res = chat.first()
        res1 = chat1.first()
        ch = db_sess.query(Chats).all()
        if ch != []:
            ch1 = ch[-1]
        if res:
            if ch != []:
                chat = Chats(
                    id=ch1.id + 1,
                    name_out=current_user.name,
                    name_to=form.name.data,
                    text=str(form.text.data),
                    message_to_user=res.message_to_user + 1
                )
            else:
                chat = Chats(
                    id=1,
                    name_out=current_user.name,
                    name_to=form.name.data,
                    text=str(form.text.data),
                    message_to_user=res.message_to_user + 1
                )
        elif res1:
            if ch != []:
                chat = Chats(
                    id=ch1.id + 1,
                    name_out=current_user.name,
                    name_to=form.name.data,
                    text=str(form.text.data),
                    message_to_user=res1.message_to_user + 1
                )
            else:
                chat = Chats(
                    id=1,
                    name_out=current_user.name,
                    name_to=form.name.data,
                    text=str(form.text.data),
                    message_to_user=res1.message_to_user + 1
                )
        else:
            if ch != []:
                chat = Chats(
                    id=ch1.id + 1,
                    name_out=current_user.name,
                    name_to=form.name.data,
                    text=str(form.text.data),
                    message_to_user=1
                )
            else:
                chat = Chats(
                    id=1,
                    name_out=current_user.name,
                    name_to=form.name.data,
                    text=str(form.text.data),
                    message_to_user=1
                )
        db_sess.add(chat)
        db_sess.commit()
        return redirect(f'/chat/{current_user.name}/{form.name.data}')
    return render_template("add.html", form=form)


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
