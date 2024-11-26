import pytest
import libtools as lt

@pytest.fixture
def book_data():
    title = "тайтл"
    author = "аузор"
    year = "еар"
    return title, author, year

@pytest.fixture
def lib_with_book(book_data):
    lib = lt.Library()
    title, author, year = book_data

    lib.add_book(title, author, year)
    return lib

@pytest.fixture
def file_with_lib(lib_with_book):
    with open("data.txt", "w") as f:
        f.write(str(lib_with_book))

    return "data.txt"

def test_book_init(book_data):
    # тестирование инициализации книги
    title, author, year = book_data
    book = lt.Book(title, author, year)

    assert title == book.title
    assert author == book.author
    assert year == book.year

def test_book_id(book_data):
    # тестирование уникальности id и результатов get_id
    book1 = lt.Book(*book_data)
    book2 = lt.Book(*book_data)

    assert book1.id != book2.id
    assert book1.get_id() != book2.get_id()

def test_lib_init():
    # тестирование инициализации библиотеки
    lib = lt.Library()

    assert lib.book_list == []

def test_add_book(lib_with_book):
    # тестирование добавления книги
    lib = lib_with_book

    assert len(lib.book_list) == 1


def test_remove_book(lib_with_book):
    # тестирование удаления несуществующей книги
    lib = lt.Library()

    with pytest.raises(lt.BookIndexError):
        lib.remove_book(0)

    # тестирование удаления существующей книги
    lib = lib_with_book
    book = lib.book_list[0]

    lib.remove_book(book.id)

    assert len(lib.book_list) == 0

def test_find_book(lib_with_book):
    # поиск книги с неправильной категорией
    lib = lt.Library()
    with pytest.raises(lt.FindKeyError):
        lib.find_book("автор", "Петр первый")

    # поиск книги которой нет
    lib = lib_with_book

    assert lib.find_book("author", "Пётр первый") == []

    # поиск книги которая есть
    book = lib.book_list[0]

    assert lib.find_book("author", "аузор") == [book]

def test_change_status(lib_with_book):
    # правильная смена статуса
    lib = lib_with_book
    book = lib.book_list[0]
    lib.change_status(book.id, "выдана")
    assert book.status == "выдана"

    # выбор несуществующего статуса
    with pytest.raises(ValueError):
        lib.change_status(book.id, "не выдана")

    # выбор того же статуса
    lib.change_status(book.id, "выдана")
    assert book.status == "выдана"

def test_read_from_file(file_with_lib):
    # проверяем чтение из несуществующего файла
    lib = lt.Library()
    with pytest.raises(FileNotFoundError):
        lib.read_from_file("notexist.txt")

    # проверяем чтение из файла с одной книгой
    lib.read_from_file(file_with_lib)
    assert len(lib.book_list) == 1

def test_write_to_file(lib_with_book):
    # проверяем записана ли информация о книге(6 строчек) в файл
    lib_with_book.write_to_file("written_data.txt")
    with open("written_data.txt", "r") as f:
        strs = f.readlines()
        assert len(strs) == 6