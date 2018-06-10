from app.models.base import db, Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,desc,func
from sqlalchemy.orm import relationship
from app.models.shupiao_book import ShuPiaoBook

class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls,uid):
        wishes = Wish.query.filter_by(uid=uid,launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gifts_counts(cls,isbn_list):
        from app.models.gift import Gift
        #不同于filter_by,filter接受条件表达式
        count_list = db.session.query(func.count(Gift.id),Wish.isbn).filter(Gift.launched == False,
            Gift.isbn.in_(isbn_list),Gift.status == 1).group_by(Gift.isbn).all()

        count_list = [{'count':w[0],'isbn':w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        shupiao_book = ShuPiaoBook()
        shupiao_book.search_by_isbn(self.isbn)
        return shupiao_book.first
