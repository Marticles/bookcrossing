from . import web
from flask import render_template, flash, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models.base import db
from app.models.gift import Gift
from app.models.drift import Drift
from app.models.wish import Wish
from app.models.user import User
from app.forms.book import DriftForm
from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection,DriftViewModel
from app.libs.email import send_email
from sqlalchemy import desc,or_

@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required  #判断是否登陆
def send_drift(gid):  #该方法是索要书籍
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是自己的，不能向自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_coins.html', coins=current_user.coins)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)    #赠送书籍页面保存信息
        #交易通知的方式，邮箱，短信
        send_email(current_gift.user.email, '有人想要这本书', 'email/get_gift.html', wisher=current_user, gift=current_gift)
        return redirect(url_for('web.pending'))
    gifter = current_gift.user.summary    #id没用， 是relationship来操作另一个表

    return render_template('drift.html', gifter=gifter, user_coins=current_user.coins, form=form)



@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()
    view_model = DriftViewModel.pending(drifts)
    return render_template('pending.html', drifts=view_model)

@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did): #拒绝操作（书籍的赠送者操作）
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id, Drift.id == did).first_or_404()#filter是范围操作，要有双等于号，  filter_by是具体指操作
        drift.pending = PendingStatus.Reject
        #requester = User.query.get_or_404(Drift.requester_id)
        current_user.coins += 1
    return redirect(url_for('web.pending'))

@login_required
@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(requester_id == current_user.id,id = did).first_or_404()
        deft.pending = PendingStatus.Redraw
        current_user.coins += 1
    return redirect(url_for('web.pending'))




@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):  #邮递
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id = current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.coins += 1
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True  #礼物是否成功赠送
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id, launched=False).update({Wish.launched:True}) #心愿是否达成
    #以上改变launched的值， 是两种写法
    #以上改变launched的值， 是两种写法
    return redirect(url_for('web.pending'))

def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        #drift.message = drift_form.message.data
        drift_form.populate_obj(drift)    #复制信息，保证form和模型中的字段名称一致

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.coins -= 1
        db.session.add(drift)