from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'story'
mysql = MySQL(app)

# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')  # 将密码转换为字节类型
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        # 检查用户名和邮箱是否已经存在
        cur.execute("SELECT * FROM users WHERE name = %s OR email = %s", (name, email))
        user = cur.fetchone()

        if user:
            error = 'Username or email already exists.'
            return render_template('register.html', error=error)

        # 插入新用户
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        session['name'] = name
        return redirect('/')
    return render_template('register.html')


# 登录路由
@app.route('/login', methods=['GET', 'POST'])
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
                error = 'Invalid email or password.'
                return render_template('login.html', error=error)
        else:
            error = 'Invalid email or password.'
            return render_template('login.html', error=error)
    return render_template('login.html')


# 主页路由
@app.route('/')
def home():
    if 'name' in session:
        name = session['name']
        return render_template('home.html', name=name)
    return redirect('/login')

# 退出登录路由
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)