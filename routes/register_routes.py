from flask import Blueprint, render_template, request, redirect, session
from flask_mysqldb import MySQL
import bcrypt

from app import mysql

bp = Blueprint('register', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        # 检查用户名和邮箱是否已经存在
        cur.execute("SELECT * FROM users WHERE name = %s OR email = %s", (name, email))
        user = cur.fetchone()

        if user:
            error = '用户名或电子邮件已存在。'
            return render_template('register.html', error=error)
        else:
            # 插入新用户
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            session['name'] = name
            return redirect('/')
    return render_template('register.html')