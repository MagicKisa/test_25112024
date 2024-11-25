import libtools as lt

lib = lt.Library()

state = -2

while state != 6:
    if state == -2:
        print("""Здравствуйте! Чтобы добавить книгу напишите 1,
                      Удаление книги - 2, Поиск книги - 3, 
                      Отобразить все книги - 4, Изменение статуса - 5,
                      Сохранить и завершить работу - 6""")
        state = -1

    if state == -1:
        try:
            print("Введите следующее действие(1-6): ")
            new_state = int(input())
            if 1 <= new_state <= 6:
                state = new_state
            else:
                print("Чуточку не то! Введите число от 1 до 6")
        except ValueError:
            print("Вы ввели не целое число, но я не сломался. Введите число от 1 до 6")

    if state == 1:
        print("Введите название книги: ")
        title = input()
        print("Автора книги: ")
        author = input()
        print("Год издания книги: ")
        year = input()

        lib.add_book(title, author, year)
        print("Книга добавлена! Спасибо \n")
        state = -1

    if state == 2:
        print("Введите уникальный id книги для удаления: ")
        id = int(input())

        try:
            lib.remove_book(id)
            print("Книга удалена, спасибо!\n")
            state = -1
        except lt.FindError:
            print("Книга с таким id не найдена, попробуйте ещё. ")

    if state == 3:
        key = input("Введите категорию поиска(author, title, year): ")
        value = input("Введите автора, название или год(в зависимости от категории поиска): ")
        try:
            book_list = lib.find_book(key, value)

            print("Подходящие книги: ")
            for book in book_list:
                print(book)
            state = -1

        except lt.FindKeyError:
            print("Книга с таким id не найдена, попробуйте ещё")

    if state == 4:
        print(lib)
        state = -1

    if state == 5:
        id = int(input("Введите id книги у которой хотите поменять статус: "))
        try:
            status = input("Введите новый статус (\"в наличии\", \"выдана\")")
            lib.change_status(id, status)
            print("Статус книги изменён. \n")

            state = -1
        except ValueError:
            print("Вы ввели неправильный статус, попробуйте ещё")

print("Работа завершена, приходите ещё!")
with open("data.txt", "w") as f:
    f.write(str(lib))

