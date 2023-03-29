from translator import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=70), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    score = db.Column(db.Integer())

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, text_password):
        self.password_hash = bcrypt.generate_password_hash(text_password)
    
    def check_password(self, password_attempt):
        return bcrypt.check_password_hash(self.password_hash, password_attempt)