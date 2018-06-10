from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from app.libs.email import send_email
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from app.view_models.wish import MyWishes
from . import web

@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gifts_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine,gift_count_list)
    return render_template('my_wish.html',wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish() 
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('不要重复添加！')
    return redirect(url_for('web.book_detail',isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):  #向他人赠送此书（满足愿望，赠送书籍）
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(isbn=wish.isbn, uid=current_user.id).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书，添加前，请确保自己可以赠送此书')

    else:
        send_email(wish.user.email, '赠送你书', 'email/satisify_wish.html', wish=wish, gift=gift)
        flash('已发送成功')

    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
