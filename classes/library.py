import sqlite3


class Library:
    def __init__(self, db_path):
        # Инициализация объекта библиотеки с указанием пути к базе данных
        self.db_path = db_path
        # Создание таблиц при инициализации объекта
        self.create_tables()

    def create_tables(self):
        """Метод для создания таблиц books и genres в базе данных, если они не существуют."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            # Создание таблицы books с полями title, author, description, genre
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                title TEXT,
                                author TEXT,
                                description TEXT,
                                genre TEXT
                            )''')

            # Создание таблицы genres с полями id (первичный ключ) и name
            cursor.execute('''CREATE TABLE IF NOT EXISTS genres (
                                id INTEGER PRIMARY KEY,
                                name TEXT
                            )''')
            connection.commit()

            # Проверяем, есть ли уже жанры в базе данных
            cursor.execute("SELECT COUNT(*) FROM genres")
            count = cursor.fetchone()[0]
            if count == 0:
                # Если нет, то добавляем стандартные жанры
                cursor.executemany("INSERT INTO genres (name) VALUES (?)", [("Фантастика",), ("Роман",), ("Поэзия",)])
                connection.commit()

    def add_book(self, book):
        """Метод для добавления книги в базу данных."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            # Вставка данных о книге в таблицу books
            cursor.execute("INSERT INTO books (title, author, description, genre) VALUES (?, ?, ?, ?)",
                           (book.title, book.author, book.description, book.genre))

    def search_books(self, keyword):
        """Метод для поиска книг по ключевому слову."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            # Поиск книг по названию или автору, содержащих заданное ключевое слово
            cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                           ('%' + keyword + '%', '%' + keyword + '%'))
            return cursor.fetchall()

    def display_books(self):
        """Метод для отображения списка книг."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT title, author FROM books")
            books = cursor.fetchall()
            match bool(books):
                # Если есть книги в базе данных
                case True:
                    print("Список книг в библиотеке:")
                    for idx, book in enumerate(books, start=1):
                        print(f'№{idx}. Название книги: "{book[0]}"; Автор: {book[1]}')

                    # Предоставляем выбор действия пользователю
                    choice = input("\n1. Просмотреть подробную информацию о книге\n"
                                   "2. Вывести книги с определенным жанром\n3. Выход в главное меню\n"
                                   "Выберите действие: ")
                    match choice:
                        # Просмотр подробной информации о книге
                        case "1":
                            book_choice = int(input("Введите номер книги для просмотра подробной информации: "))
                            if 1 <= book_choice <= len(books):
                                selected_book = books[book_choice - 1]
                                self.display_book_details(selected_book)
                            else:
                                print("Некорректный номер книги. Попробуйте снова.")
                        # Вывод книг по заданному жанру
                        case "2":
                            self.display_books_by_genre_prompt()
                        # Возвращаемся в главное меню
                        case "3":
                            return
                        # Некорректный ввод
                        case _:
                            print("Некорректный ввод! Попробуйте снова.")
                # Если нет книг в базе данных
                case False:
                    print("В библиотеке нет книг.")

    def display_book_details(self, selected_book):
        """Метод для отображения подробной информации о книге."""
        title, author = selected_book[0], selected_book[1]
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT description, genre FROM books WHERE title=? AND author=?",
                (title, author)
            )
            book_info = cursor.fetchone()
            if book_info:
                description, genre = book_info
                print("\nИнформация о книге:")
                print(f"Название: {title}")
                print(f"Автор: {author}")
                print(f"Описание: {description}")
                print(f"Жанр: {genre}\n")
            else:
                print("Информация о книге не найдена.")

    def display_books_by_genre_prompt(self):
        """Метод для отображения списка книг определенного жанра (по запросу пользователя)."""
        genre = input("Введите жанр книги для отображения: ")
        self.display_books_by_genre(genre)

    def display_books_by_genre(self, genre):
        """Метод для отображения списка книг определенного жанра."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT title, author FROM books WHERE genre=?", (genre,))
            genre_books = cursor.fetchall()
            if genre_books:
                print(f"\nКниги жанра '{genre}':")
                for book in genre_books:
                    print(f'Книга: "{book[0]}"; Жанр: "{book[1]}"')
            else:
                print(f"Нет книг жанра '{genre}' в библиотеке.")

    def get_existing_genres(self):
        """Метод для получения списка существующих жанров
            существующих жанров из базы данных."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM genres")
            genres = cursor.fetchall()
            return [genre[0] for genre in genres]

    def prompt_genre(self):
        """Метод для запроса у пользователя выбора жанра."""
        genres = self.get_existing_genres()
        print("Существующие жанры:")
        for idx, genre in enumerate(genres, start=1):
            print(f"{idx}. {genre}")
        print(f"{len(genres) + 1}. Ввести свой жанр")

        while True:
            choice = input("Выберите жанр книги: ")
            if choice.isdigit() and 1 <= int(choice) <= len(genres) + 1:
                if int(choice) == len(genres) + 1:
                    new_genre = input("Введите свой жанр: ")
                    return new_genre
                else:
                    return genres[int(choice) - 1]
            else:
                print("Некорректный ввод. Попробуйте снова.")

    def remove_book(self):
        """Метод для удаления книги из библиотеки."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            if books:
                print("Список книг в библиотеке:")
                for idx, book in enumerate(books, start=1):
                    print(f'№{idx}. Название книги: "{book[0]}"; Автор: {book[1]}')
                try:
                    book_number = int(input("Введите номер книги для удаления: "))
                    selected_book = books[book_number - 1][0]
                    author = books[book_number - 1][1]
                    # Удаление книги из таблицы books
                    cursor.execute("DELETE FROM books WHERE title=? AND author=?", (selected_book, author,))
                    print("Книга удалена.")
                except IndexError:
                    print("Некорректный номер книги.")
            else:
                print("В библиотеке нет книг.")
