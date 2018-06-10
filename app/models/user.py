from app.models.base import db, Base
from app.models.gift import Gift
from app.models.wish import Wish
from sqlalchemy import Column,Integer,String,Boolean,Float
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app
from app import login_manager

from app.libs.helper import is_isbn_or_key
from app.models.shupiao_book import ShuPiaoBook

class User(UserMixin,Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password',String(128),nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    coins = Column(Float, default=10)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    
    def can_send_drift(self):
        #if self.coins < 1:
        return True

    @property
    def password(self):
        return self._password
        

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        shupiao_book =ShuPiaoBook()
        shupiao_book.search_by_isbn(isbn)
        if not shupiao_book.first:
            return False

        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        
        if not gifting and not wishing:
            return True
        else:
            return False

    #token有效时间为1800s,30mins
    def generate_token(self,expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'id':self.id}).decode('utf-8')



    @staticmethod
    def reset_password(token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            if user is None:
                return False
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            coins=self.coins,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
            )
    


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
