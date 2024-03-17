from flask import Blueprint, render_template, request, redirect, session
from flask_mysqldb import MySQL
import bcrypt

from app import mysql

bp = Blueprint('login', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            hashed_password = bytes(user[3], 'utf-8')  # 指定正确的编码
            if bcrypt.checkpw(password, hashed_password):
                # 用户名和密码匹配，执行登录操作
                session['name'] = user[1]
                return redirect('/')
            else:
                error = '无效的电子邮件或密码。'
        else:
            error = '无效的电子邮件或密码。'

        return render_template('login.html', error=error)
    return render_template('login.html')