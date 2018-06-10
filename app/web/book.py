from flask import jsonify,request ,current_app, url_for, render_template, flash
from app.view_models.trade import TradeInfo
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.shupiao_book import ShuPiaoBook
from app.view_models.book import BookViewModel,BookCollection
from . import web 
import json

from flask_login import current_user
from app.models.gift import Gift
from app.models.wish import Wish

@web.route('/book/search/')
def search():
    """
    q:普通关键字orISBN号
    page
    """
    form = SearchForm(request.args)
    books = BookCollection()
    #参数校验

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        shupiao_book = ShuPiaoBook()

        if isbn_or_key == 'isbn':
            shupiao_book.search_by_isbn(q)
        else:
            shupiao_book.search_by_keyword(q,page)

        #dict转str
        books.fill(shupiao_book,q)
        #return json.dumps(books, default = lambda o: o.__dict__)
        #return json.dumps(books),200,{'content-type':'application/json'}

    else :
        flash('搜索关键字错误')
        #return jsonify(form.errors)
    return render_template('search_result.html',books=books,form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    shupiao_book = ShuPiaoBook()
    shupiao_book.search_by_isbn(isbn)
    book = BookViewModel(shupiao_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html', book=book, wishes=trade_wishes_model,
                           gifts=trade_gifts_model, has_in_wishes=has_in_wishes, has_in_gifts=has_in_gifts)
'''
@web.route('/hello')
def hello():
    return 'hello'
'''

'''
@web.route('/test')
def test():
    r = {
        'name':'XXXX',
        'age':'18'
    }
    flash('[q,a,c]',category = 'q')
    flash('aaaaaa',category = 'a')

    return render_template('test.html',data =r)
'''