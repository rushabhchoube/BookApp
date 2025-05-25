from flask import Flask, redirect, url_for, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir,"mydatabase.db")
)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Book(db.Model):
    name = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(100), nullable=False)

@app.route('/addbook')
def addbook():
    return render_template('addbook.html')

@app.route('/submitbook', methods=['POST'])
def submitbook():
    name = request.form['name']
    author = request.form['author']
    book = Book(name=name, author=author)
    db.session.add(book)
    db.session.commit()
    return redirect('/boks')

@app.route('/updatebooks')
def updatebooks():
    books = Book.query.all()
    return render_template('updatebook.html',books=books)

@app.route('/update',methods=["POST"])
def update():
    oldname = request.form['oldname']
    newname = request.form['newname']
    newauthor = request.form['newauthor']
    book = Book.query.filter_by(name=oldname).first()
    book.name = newname
    book.author = newauthor
    db.session.commit()

    return redirect('/boks')
    
@app.route('/delete',methods=['POST'])
def delete():
    name = request.form['name']
    book = Book.query.filter_by(name=name).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('/boks')

@app.route('/')
def home():
    return '<h1>This is an home page</h1>'

@app.route('/new')
def new():
    return '<h1> This is a new page <h1>'

@app.route('/demo')
def demo():
    return '<h1> This is a demo page <h1>'

#variables
@app.route('/profile/<username>')
def profile(username):
    return '<h1> This is a Profile page for %s <h1>' % username

@app.route('/pr/<int:id>')
def pr(id):
    return '<h1> This is a pr page for %d <h1>' % id

@app.route('/admin')
def admin():
    return 'Welcome Admin'

@app.route('/guest/<guest>')
def guest(guest):
    return 'Welcome guest %s' % guest

# redirect and url_for
@app.route('/user/<user>')
def welcome_user(user):
    if user == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('guest',guest=user))
    
# recieving requests
@app.route('/c')
def ind():
    return 'This is a request made by client %s' % request.headers

#render template
@app.route('/template')
def template():
    return render_template('index.html')

# passing dynamic data to templates
@app.route('/profilepage/<username>')
def profilepage(username):
    return render_template('profile.html',username=username,isActive=False)

@app.route('/books')
def books():
    books = ['book1','book2','book3']
    return render_template('books.html',books=books)

@app.route('/boks')
def boks():
    # books = [{'name':'Book1','author':'Author1','cover':'https://5.imimg.com/data5/IU/SQ/GD/SELLER-43618059/book-cover-page-design.jpg'},
    #          {'name':'Book2','author':'Author2','cover':'https://5.imimg.com/data5/IU/SQ/GD/SELLER-43618059/book-cover-page-design.jpg'},
    #          {'name':'Book3','author':'Author3','cover':'https://5.imimg.com/data5/IU/SQ/GD/SELLER-43618059/book-cover-page-design.jpg'}]
    books = Book.query.all()
    return render_template('boks.html',books=books)


if __name__ == '__main__':
    #Debugger mode
    app.run(debug=True)
