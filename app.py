from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'

db = SQLAlchemy(app)
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    url = db.Column(db.String(220), unique=True, nullable=False)
    tags = db.Column(db.String(300))
    def __init__(self, name, description, url, tags):
        self.name = name
        self.description = description
        self.url = url
        self.tags = tags


@app.route('/')
def index():
    links = Link.query.all()
    return render_template('index.html', links=links)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        link = Link(request.form['name'], request.form['description'], request.form['url'], request.form['tags'])
        db.session.add(link)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    link = Link.query.get(id)
    if request.method == 'POST':
        link.name = request.form['name']
        link.description = request.form['description']
        link.url = request.form['url']
        link.tags = request.form['tags']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', link=link)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    link = Link.query.get(id)
    db.session.delete(link)
    db.session.commit()
    return redirect(url_for('index'))
    # return render_template('delete.html', link=link)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)