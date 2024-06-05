from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Column, DateTime, Boolean, ForeignKey
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime
import os 


BASE_DIR = os.path.abspath('__init__.py')
db = SQLAlchemy()
login_manager = LoginManager()
app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'asdasdadad'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dev.sqlite" #os.path.join(BASE_DIR, 'dev.sqlite')
db.init_app(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)
# app.config['MYSQL_USER'] = 'user'

app.app_context().push()

@login_manager.user_loader
def load_user(pk):
    return User.query.get(pk)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(Integer, nullable=False, default='User' + str(id))
    password = Column(String(42), nullable=False)
    notes = db.relationship('NotesModel', backref='user', lazy=True)
    category = db.relationship('CategoryModel', backref='user', lazy=True)
    

    def hash_password(self):
        spassword = bcrypt.generate_password_hash(self.password)
        self.password = spassword

    def save(self):
        self.hash_password()
        db.session.add(self)
        db.session.commit()

class CategoryModel(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String(256), nullable=False, unique=True)
    notes = db.relationship('NotesModel', backref='category', lazy=True)

    def __str__(self):
        return self.title
    
    def save(self):
        print(f'{self.title} category added')
        db.session.add(self)
        db.session.commit()

    
        
    

class NotesModel(db.Model):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(256), nullable=False)
    date_created = Column(DateTime(), default=datetime.now())
    status = Column(Boolean, default=False)
    
    def __str__(self):
        return self.title
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        print(f'Notes ID#: {self.id} created')

    