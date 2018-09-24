# BookCrossing
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)
![](https://img.shields.io/badge/language-python-orange.svg)

![Image](img/index.PNG)
## Description
BookCrossing is a website based on flask for book exchange which provides the following.

- [x] Search for books: Based on DouBan API
- [x] Upload books
- [x] Send books
- [x] Wish books
- [x] Exchange books: It will send you an eamil
- [x] Retrieve password: It will send you an eamil
- [x] Virtual book coins: For book exchange
- [x] Encrypt password:Salting

## Requirements
* Python3.6.4
* Flask 1.0.2
* Flask-Login 0.4.1
* Flask-Mail 0.9.1
* Flask-SQLAlchemy 2.3.2
* Jinja2 2.10
* Werkzeug 0.14.1
* WTForms 2.2
* itsdangerous 0.24
* cymysql 0.9.10

## Server Environment
![Image](img/server.PNG)

## File Organization
```
-- bookcrossing
    |-- Pipfile
    |-- Pipfile.lock
    |-- app
    |   |-- __init__.py
    |   |-- secure.py
    |   |-- setting.py
    |   |-- forms
    |   |-- libs
    |   |-- models
    |   |   |-- base.py
    |   |   |-- book.py
    |   |   |-- drift.py
    |   |   |-- gift.py
    |   |   |-- shupiao_book.py
    |   |   |-- user.py
    |   |   |-- wish.py
    |   |-- view_models
    |   |   |-- book.py
    |   |   |-- drift.py
    |   |   |-- gift.py
    |   |   |-- trade.py
    |   |   |-- user.py
    |   |   |-- wish.py
    |   |-- web
    |       |-- __init__.py
    |       |-- auth.py
    |       |-- book.py
    |       |-- drift.py
    |       |-- gift.py
    |       |-- main.py
    |       |-- wish.py
    |   |-- static
    |   |-- templates
    |-- test
    |-- run.py
```

##  Screenshot
#### Book details
![Image](img/detail.PNG)
#### Send books 
![Image](img/gift.PNG)
#### Wish books
![Image](img/wish.PNG)
#### Exchange history 
![Image](img/history.PNG)
#### Exchange request
![Image](img/request.PNG)
#### Mail Notifier
![Image](img/email.PNG)




