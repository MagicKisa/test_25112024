import libtools as lt

lib = lt.Library()
lib.read_from_file("data.txt")


next_action = "next_action"
greetings = "greetings"
state = greetings

# конечный автомат
# при неправильном вводе данных пользователю даётся ещё попытка
# при правильном вводе данных автомат всё выполняет и переводит пользователя к следующему действию
while state != 6:
    # приветствие и меню
    if state == greetings:
        print("""Здравствуйте! 
                       Чтобы добавить книгу напишите 1,
                       Удаление книги - 2, Поиск книги - 3, 
                       Отобразить все книги - 4, Изменение статуса - 5,
                       Сохранить и завершить работу - 6""")
        state = next_action

    # Ввод следующего действия
    if state == next_action:
        try:
            print("Введите следующее действие(1-6): ")
            new_state = int(input())
            if 1 <= new_state <= 6:
                state = new_state
            else:
                print("Чуточку не то! Введите число от 1 до 6")
        except ValueError:
            print("Вы ввели не целое число, но я не сломался. Введите число от 1 до 6")

    # Добавление книги
    if state == 1:
        print("Введите название книги: ")
        title = input()
        print("Автора книги: ")
        author = input()
        print("Год издания книги: ")
        year = input()

        lib.add_book(title, author, year)
        print("Книга добавлена! Спасибо \n")
        state = next_action

    # Удаление книги
    if state == 2:
        print("Введите уникальный id книги для удаления: ")
        id = int(input())

        try:
            lib.remove_book(id)
            print("Книга удалена, спасибо!\n")
            state = next_action
        except lt.FindError:
            print("Книга с таким id не найдена, попробуйте ещё. ")

    # Поиск книги
    if state == 3:
        key = input("Введите категорию поиска(author, title, year): ")
        value = input("Введите автора, название или год(в зависимости от категории поиска): ")
        try:
            book_list = lib.find_book(key, value)

            print("Подходящие книги: ")
            for book in book_list:
                print(book)
            state = next_action

        except lt.FindKeyError:
            print("Книга с таким id не найдена, попробуйте ещё")

    # Вывод всех книг
    if state == 4:
        print(lib)
        state = next_action

    # Смена статуса у книги
    if state == 5:
        id = int(input("Введите id книги у которой хотите поменять статус: "))
        try:
            print("Введите новый статус (\"в наличии\", \"выдана\"): ")
            status = input()
            lib.change_status(id, status)
            print("Статус книги изменён. \n")

            state = next_action
        except ValueError:
            print("Вы ввели неправильный статус, попробуйте ещё")

print("Работа завершена, приходите ещё!")

# сохранение библиотеки
lib.write_to_file("data.txt")

