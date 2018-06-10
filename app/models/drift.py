from app.libs.enums import PendingStatus
from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base

class Drift(Base):
    """
        一次具体的交易信息
    """


    id = Column(Integer, primary_key=True)
    #邮递信息
    recipient_name = Column(String(20), nullable=False) #收件人姓名
    address = Column(String(100), nullable=False)
    mobile = Column(String(20), nullable=False)
    message = Column(String(200))

    #书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    #请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    #赠送人的信息
    gifter_id = Column(Integer) #赠送人id
    gift_id = Column(Integer) #书籍id
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')

    @property
    def pending(self):
        return PendingStatus(self._pending)    #增加了pending属性， 转换为枚举类型   #返回的不在是数字，而是枚举

    @pending.setter
    def pending(self, status):
        self._pending = status.value   #将枚举转换成数字
