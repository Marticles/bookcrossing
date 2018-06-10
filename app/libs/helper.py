def is_isbn_or_key(word):
    """
    判断是否是ISBN号
    ISBN13 13个0到9数字
    ISBN10 10个0到9数字，还有‘-’
    """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'

    short_word = word.replace('-','')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'ibsn'
    return isbn_or_key
