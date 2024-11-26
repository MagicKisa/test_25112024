import pytest
import libtools as lt

def test_book_init():
    title = "тайтл"
    author = "аузор"
    year = "еар"
    book = lt.Book(title, author, year)

    assert title == book.title
    assert author == book.author
    assert year == book.year

    
