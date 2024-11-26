import pytest
import libtools as lt

@pytest.fixture
def book_data():
    title = "тайтл"
    author = "аузор"
    year = "еар"
    return title, author, year

def test_book_init(book_data):
    # тестирование инициализации книги
    title, author, year = book_data
    book = lt.Book(title, author, year)

    assert title == book.title
    assert author == book.author
    assert year == book.year

def test_book_id(book_data):
    # тестирование уникальности id и результатов get_id
    title, author, year = book_data
    book1 = lt.Book(title, author, year)
    book2 = lt.Book(title, author, year)

    assert book1.id != book2.id
    assert book1.get_id() != book2.get_id()

def test_lib_init():
    # тестирование инициализации библиотеки
    lib = lt.Library()

    assert lib.book_list == []

def test_add_book(book_data):
    # тестирование добавления книги
    lib = lt.Library()

    title, author, year = book_data

    lib.add_book(title, author, year)

    assert len(lib.book_list) == 1
    # тестирование равенства начальных атрибутов с атрибутами добавленной книги
    book = lib.book_list[0]

    assert title == book.title
    assert author == book.author
    assert year == book.year

def test_remove_book(book_data):
    # тестирование удаления несуществующей книги
    lib = lt.Library()

    with pytest.raises(lt.BookIndexError):
        lib.remove_book(0)

    # тестирование удаления существующей книги
    title, author, year = book_data

    lib.add_book(title, author, year)
    book = lib.book_list[0]

    lib.remove_book(book.id)

    assert len(lib.book_list) == 0

def test_find_book(book_data):
    # поиск книги с неправильной категорией
    lib = lt.Library()
    with pytest.raises(lt.FindKeyError):
        lib.find_book("автор", "Петр первый")

    # поиск книги которой нет
    title, author, year = book_data

    lib.add_book(title, author, year)

    assert lib.find_book("author", "Пётр первый") == []

    # поиск книги которая есть
    book = lib.book_list[0]

    assert lib.find_book("author", "аузор") == [book]