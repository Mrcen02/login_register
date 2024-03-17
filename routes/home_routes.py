from flask import Blueprint, render_template, session, redirect

bp = Blueprint('home', __name__)

@bp.route('/')
def home():
    if 'name' in session:
        name = session['name']
        return render_template('home.html', name=name)
    return redirect('/login')