from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

import datetime
from flask import Flask
# from flask_peewee.auth import Auth
# from flask_peewee.db import Database
from peewee import SqliteDatabase,CharField,DateTimeField,Model


from flask import render_template, redirect, request, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user,UserMixin



app = Flask(__name__)

app.secret_key = 'ssshhhh'
app.debug = True

db = SqliteDatabase('login_demo.db')

login_manager = LoginManager()
login_manager.init_app(app)

#使用@login_required前的必要设置
login_manager.login_view = '.login'
login_manager.login_message = '请登录后访问'


'''
AttributeError: ‘User’ object has no attribute ‘is_active’
User需要继承UserMixin,并添加一个user_loader
'''
class User(Model,UserMixin):
    email = CharField()
    password = CharField()
    created = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

@login_manager.user_loader
def user_loader(id):
    user = User.select().where(User.id == id).get()
    return user

db.connect()
#db.create_tables([User])

'''
插入数据三种方法

1.
user = User(email='q-yu@dti.ad.jp',password='123')
user.save()

2.
User.insert(email='q-yu@dti.ad.jp',password='123').execute()

3.
User.create(email='q-yu@dti.ad.jp',password='123')

'''

#User.create(email='q-yu@dti.ad.jp',password='123')


class LoginForm(Form):
    email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])

    class Meta:
        csrf = False



@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #user = User.query.filter_by(email=form.email.data).first()
        user = User.select().where(User.email == form.email.data).get()

        if user is not None and user.password == form.password.data:
            login_user(user)
            flash(u'登陆成功！欢迎回来，%s!' % user.email, 'success')
            #return redirect(request.args.get('next') or url_for('.index'))
            return redirect(url_for('.index'))
        else:
            flash(u'登陆失败！用户名或密码错误，请重新登陆。', 'danger')
    if form.errors:
        flash(u'登陆失败，请尝试重新登陆.', 'danger')

    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已退出登陆。', 'success')
    return redirect(url_for('.index'))


if __name__ == '__main__':
    app.run()