
class BookViewModel(object):
    def __init__(self, data):
        self.title = data['title']
        self.author = '、'.join(data['author'])
        self.binding = data['binding']
        self.publisher = data['publisher']
        self.image = data['image']
        self.image = self.image.replace('/view/subject/m/public/','//view//subject//m//public/')
        self.price = '￥' + data['price'] if data['price'] else data['price']
        self.isbn = data['isbn13']
        self.pubdate = data['pubdate']
        self.summary = data['summary']
        self.pages = data['pages']

    @property
    def intro(self):
        intros = filter(lambda x : True if x else False,[self.author,self.publisher,self.price])
        return '/'.join(intros)

class BookCollection(object):
    def __int__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, shupiao_book, keyword):
        self.total = shupiao_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in shupiao_book.books]




class _BookViewModel(object):
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books':[],
            'total':0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books':[],
            'total': 0,
            'keyword': keyword 
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(data) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title':data['title'],
            'publisher':data['publisher'],
            'pages':data['pages'] or '',
            'author':'、'.join(data['author']),
            'price':data['price'],
            'summary':data['summary'] or '',
            'image':data['images']['medium']
        }
        return book
