from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail

def send_async_email(app,msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e

# 为了解决页面等待问题，开启多线程异步发送E-mail
def send_email(to,subject,template,**kwargs):
    msg = Message('[书漂]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template,**kwargs)
    app =current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app,msg])
    thr.start()



