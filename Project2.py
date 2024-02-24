import pickle
import os


class Book:
    def __init__(self, title, publisher, isbn_10, isbn_13, edition=None, year=None, month=None, language=None,
                 NumberOfCopies=1):
        self.title = title
        self.publisher = publisher
        self.isbn_10 = isbn_10
        self.isbn_13 = isbn_13
        self.edition = edition
        self.year = year
        self.month = month
        self.language = language
        self.archived = False
        self.NumberOfCopies = NumberOfCopies

    def display_Information(self):
        print(f"Title: {self.title}")
        print(f"Publisher: {self.publisher}")
        print(f"ISBN-10: {self.isbn_10}")
        print(f"ISBN-13: {self.isbn_13}")
        if self.edition:
            print(f"Edition: {self.edition}")
        if self.year:
            print(f"Year: {self.year}")
        if self.month:
            print(f"Month: {self.month}")
        if self.language:
            print(f"Language: {self.language}")
        print(f"Number of Copies: {self.NumberOfCopies}")


class BookCover(Book):
    def __init__(self, title, publisher, isbn_10, isbn_13, num_pages, edition=None, year=None, month=None,
                 language=None, NumberOfCopies=1):
        super().__init__(title, publisher, isbn_10, isbn_13, edition, year, month, language, NumberOfCopies)
        self.num_pages = num_pages

    def display_Information(self):
        super().display_Information()
        print(f"Type: Hardcover")
        print(f"The Pages Number: {self.num_pages}")


class PaperBook(Book):
    def __init__(self, title, publisher, isbn_10, isbn_13, num_pages, edition=None, year=None, month=None,
                 language=None, NumberOfCopies=1):
        super().__init__(title, publisher, isbn_10, isbn_13, edition, year, month, language, NumberOfCopies)
        self.num_pages = num_pages

    def display_Information(self):
        super().display_Information()
        print(f"Type: Paperback")
        print(f"The Pages Number: {self.num_pages}")


class Library:
    def __init__(self):
        self.books = []

    def AddBook(self, book):
        self.books.append(book)
        print("The Book Added successfully.")

    def LoadBook(self, FileName):
        try:
            with open(FileName, 'r') as file:
                lines = file.readlines()
                Book_Information = {}
                for line in lines:
                    if line.strip() == "":
                        if Book_Information:
                            self.Creat_Update_Book(Book_Information)
                            Book_Information = {}
                    else:
                        separator = ":" if ":" in line else " : "
                        key, value = line.strip().split(separator, 1)
                        Book_Information[key.strip()] = value.strip()
                if Book_Information:
                    self.Creat_Update_Book(Book_Information)
        except FileNotFoundError:
            print("The File not found.")
        except Exception as e:
            print(f"Error occurred while loading books from file: {str(e)}")

    def Creat_Update_Book(self, Book_Information):
        isbn_13 = Book_Information.get("ISBN-13")
        ExistBook = self.get_book_by_isbn(isbn_13)
        if ExistBook:
            print(f"Book with ISBN-13 {isbn_13} already exists in the LMS.")
            choice = input("Do you want to Replace or Add a new copy? (Replace/Add): ")
            if choice.lower() == "Replace":
                self.ReplaceBook(ExistBook, Book_Information)
            else:
                self.AddCopy(ExistBook, Book_Information)
        else:
            self.CreatBook(Book_Information)

    def get_book_by_isbn(self, isbn_13):
        for book in self.books:
            if book.isbn_13 == isbn_13:
                return book
        return None

    def ReplaceBook(self, ExistBook, Book_Information):
        # Update the book attributes with new information
        ExistBook.title = Book_Information.get("Title")
        ExistBook.publisher = Book_Information.get("Publisher")
        ExistBook.isbn_10 = Book_Information.get("ISBN-10")
        ExistBook.isbn_13 = Book_Information.get("ISBN-13")
        ExistBook.num_pages = Book_Information.get("Hardcover") or Book_Information.get("Paperback")
        ExistBook.edition = Book_Information.get("Edition")
        ExistBook.year = Book_Information.get("Year")
        ExistBook.month = Book_Information.get("Month")
        ExistBook.language = Book_Information.get("Language")
        NumberOfCopies = int(Book_Information.get("Number of Copies", 1))
        ExistBook.NumberOfCopies = NumberOfCopies
        print("Book Replaced successfully.")
        self.display_Book_Information(ExistBook)

    def AddCopy(self, ExistBook, Book_Information):
        NumberOfCopies = int(Book_Information.get("Number of Copies", 1))
        ExistBook.NumberOfCopies += NumberOfCopies
        print("New copy Added successfully.")
        self.display_Book_Information(ExistBook)

    def CreatBook(self, Book_Information):
        title = Book_Information.get("Title")
        publisher = Book_Information.get("Publisher")
        isbn_10 = Book_Information.get("ISBN-10")
        isbn_13 = Book_Information.get("ISBN-13")
        num_pages = Book_Information.get("Hardcover") or Book_Information.get("Paperback")
        edition = Book_Information.get("Edition")
        year = Book_Information.get("Year")
        month = Book_Information.get("Month")
        language = Book_Information.get("Language")
        NumberOfCopies = int(Book_Information.get("Number of Copies", 1))
        if num_pages:
            book_type = BookCover if "Hardcover" in Book_Information else PaperBook
            book = book_type(title, publisher, isbn_10, isbn_13, num_pages, edition, year, month, language,
                             NumberOfCopies)
        else:
            book = Book(title, publisher, isbn_10, isbn_13, edition, year, month, language, NumberOfCopies)
        self.AddBook(book)
        self.display_Book_Information(book)

    def display_Book_Information(self, book):
        print("Book Information:")
        book.display_Information()

    def SearchBook(self, SearchParams):
        SearchResults = []
        for book in self.books:
            match = True
            for key, value in SearchParams.items():
                if getattr(book, key.lower(), None) != value:
                    match = False
                    break
            if match:
                SearchResults.append(book)
        return SearchResults

    def SearchBookAndPrint(self, SearchParams):
        SearchResults = self.SearchBook(SearchParams)
        if SearchResults:
            for index, book in enumerate(SearchResults, start=1):
                print(f"\nSearch Result {index}:")
                self.display_Book_Information(book)
                print("-------------------")
        else:
            print("No matching books found.")

    def SearchBookAndGet(self, SearchParams):
        SearchResults = self.SearchBook(SearchParams)
        return SearchResults

    def StoreSearchInfo(self, SearchResults, FileName):
        try:
            with open(FileName, 'w') as file:
                file.write("Search Results:\n\n")
                for book in SearchResults:
                    file.write(f"Title: {book.title}\n")
                    file.write(f"Publisher: {book.publisher}\n")
                    file.write(f"ISBN-10: {book.isbn_10}\n")
                    file.write(f"ISBN-13: {book.isbn_13}\n")
                    if isinstance(book, BookCover):
                        file.write(f"Type: Hardcover\n")
                        file.write(f"Number of Pages: {book.num_pages}\n")
                    elif isinstance(book, PaperBook):
                        file.write(f"Type: Paperback\n")
                        file.write(f"Number of Pages: {book.num_pages}\n")
                    if book.edition:
                        file.write(f"Edition: {book.edition}\n")
                    if book.year:
                        file.write(f"Year: {book.year}\n")
                    if book.month:
                        file.write(f"Month: {book.month}\n")
                    if book.language:
                        file.write(f"Language: {book.language}\n")
                    file.write("-------------------\n")
            print(f"Search results stored in file: {FileName}")
        except Exception as e:
            print(f"Error occurred while storing the search results: {str(e)}")

    def EditBook(self, title, NewInfo):
        books = self.SearchBook({"title": title})
        if books:
            if len(books) == 1:
                book = books[0]
                for key, value in NewInfo.items():
                    setattr(book, key.lower(), value)
                print("Book information updated successfully.")
            else:
                print("Multiple books with the same title found. Please provide more specific information.")
        else:
            print("Book not found.")

    def ArchiveBook(self, title):
        books = self.SearchBook({"title": title})
        if books:
            if len(books) == 1:
                book = books[0]
                confirm = input(f"Do you want to archive the book '{book.title}'? (yes/no): ")
                if confirm.lower() == "yes":
                    NumberOfCopies = int(input(f"How many copies of '{book.title}' do you want to archive? "))
                    if NumberOfCopies > book.NumberOfCopies:
                        print(f"Error: '{book.title}' has only {book.NumberOfCopies} copies available.")
                    else:
                        book.NumberOfCopies -= NumberOfCopies
                        print(f"{NumberOfCopies} copies of '{book.title}' archived successfully.")
            else:
                print("Multiple books with the same title found:")
                for i, book in enumerate(books):
                    print(f"{i + 1}. {book.title}")
                book_numbers = [str(i) for i in range(1, len(books) + 1)]
                book_choice = input("Please choose the book number(s) you want to archive (separated by commas): ")
                chosen_books = []
                for choice in book_choice.split(","):
                    if choice.strip() in book_numbers:
                        chosen_books.append(books[int(choice.strip()) - 1])
                if chosen_books:
                    for book in chosen_books:
                        NumberOfCopies = int(input(f"How many copies of '{book.title}' do you want to archive? "))
                        if NumberOfCopies > book.NumberOfCopies:
                            print(f"Error: '{book.title}' has only {book.NumberOfCopies} copies available.")
                        else:
                            book.NumberOfCopies -= NumberOfCopies
                            print(f"{NumberOfCopies} copies of '{book.title}' archived successfully.")
                else:
                    print("Invalid book number(s) entered.")
        else:
            print("Book not found.")

    def RemoveBook(self, title):
        books = self.SearchBook({"title": title})
        if books:
            for book in books:
                if book.archived:
                    self.books.remove(book)
                    print("Book removed successfully.")
                else:
                    print("Only archived books can be removed from the LMS.")
        else:
            print("Book not found.")

    def SaveInformations(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.books, file)

    def GenerateReports(self):
        print("Books available in the library:")
        for book in self.books:
            book.display_Information()
            print("-------------------")

    def PrintReports(self):
        print("Library Report:")
        print("-------------------")
        print("1. Total number of books in the LMS:", len(self.books))

        UniqurBooks = set(self.books)
        print("2. Total number of different books offered in the LMS:", len(UniqurBooks))

        ArchivedBooks = [book for book in self.books if book.archived]
        print("3. Total number of books archived in the LMS:", len(ArchivedBooks))

        year = input("Enter the year to check the number of books newer than that: ")

        try:
            year = int(year)
            NewerBooks = [book for book in self.books if book.year and int(book.year) > year]
            print("4. Total number of books newer than", year, ":", len(NewerBooks))
        except ValueError:
            print("Invalid year input. Please enter a valid year.")

        print("5. Book distribution by publisher:")
        CountOfPublisher = {}
        for book in self.books:
            publisher = book.publisher
            CountOfPublisher[publisher] = CountOfPublisher.get(publisher, 0) + 1
        for publisher, count in CountOfPublisher.items():
            print(f"{publisher}: {count}")

        print("6. Book distribution by year:")
        CountOfYears = {}
        for book in self.books:
            year = book.year
            CountOfYears[year] = CountOfYears.get(year, 0) + 1
        for year, count in CountOfYears.items():
            print(f"{year}: {count}")

    def SaveBooks(self, FileName):
        try:
            with open(FileName, 'w') as file:
                for book in self.books:
                    file.write(f"Title: {book.title}\n")
                    file.write(f"Publisher: {book.publisher}\n")
                    file.write(f"ISBN-10: {book.isbn_10}\n")
                    file.write(f"ISBN-13: {book.isbn_13}\n")
                    if isinstance(book, BookCover):
                        file.write(f"Type: Hardcover\n")
                        file.write(f"Number of Pages: {book.num_pages}\n")
                    elif isinstance(book, PaperBook):
                        file.write(f"Type: Paperback\n")
                        file.write(f"Number of Pages: {book.num_pages}\n")
                    if book.edition:
                        file.write(f"Edition: {book.edition}\n")
                    if book.year:
                        file.write(f"Year: {book.year}\n")
                    if book.month:
                        file.write(f"Month: {book.month}\n")
                    if book.language:
                        file.write(f"Language: {book.language}\n")
                    file.write("-------------------\n")
            print(f"Books' data saved to file: {FileName}")
        except Exception as e:
            print(f"Error occurred while saving books' data: {str(e)}")

    def menu(self):

        while True:
            print("Library Management System")
            print("-------------------")
            print("1. Add new book")
            print("2. Load books from file")
            print("3. Search for a book")
            print("4. Edit book information")
            print("5. Archive a book")
            print("6. Remove a book")
            print("7. Show the books")
            print("8. Generating reports about the books available in the LMS.")
            print("9. Terminate LMS")

            choice = input("Enter your choice: ")

            if choice == "1":
                title = input("Enter the title of the book: ")
                publisher = input("Enter the publisher of the book: ")
                isbn_10 = input("Enter the ISBN-10 of the book: ")
                isbn_13 = input("Enter the ISBN-13 of the book: ")
                edition = input("Enter the edition of the book (press enter to skip): ")
                year = input("Enter the year of the book (press enter to skip): ")
                month = input("Enter the month of the book (press enter to skip): ")
                language = input("Enter the language of the book (press enter to skip): ")
                book_type = input("Enter the book type (Hardcover/Paperback): ")
                if book_type.lower() == "hardcover":
                    num_pages = input("Enter the number of pages: ")
                    book = BookCover(title, publisher, isbn_10, isbn_13, num_pages, edition, year, month, language)
                elif book_type.lower() == "paperback":
                    num_pages = input("Enter the number of pages: ")
                    book = PaperBook(title, publisher, isbn_10, isbn_13, num_pages, edition, year, month, language)
                else:
                    book = Book(title, publisher, isbn_10, isbn_13, edition, year, month, language)
                self.AddBook(book)

            elif choice == "2":
                FileName = input("Enter the file name: ")
                self.LoadBook(FileName)


            # Inside the menu method, after the "3. Search for a book" option

            # Inside the menu method, after the "3. Search for a book" option

            elif choice == "3":

                SearchParams = {}

                print("Enter search parameters (press enter to skip):")

                title = input("Title: ")

                if title:
                    SearchParams["title"] = title

                publisher = input("Publisher: ")

                if publisher:
                    SearchParams["publisher"] = publisher

                isbn_10 = input("ISBN-10: ")

                if isbn_10:
                    SearchParams["isbn_10"] = isbn_10

                isbn_13 = input("ISBN-13: ")

                if isbn_13:
                    SearchParams["isbn_13"] = isbn_13

                edition = input("Edition: ")

                if edition:
                    SearchParams["edition"] = edition

                year = input("Year: ")

                if year:
                    SearchParams["year"] = year

                month = input("Month: ")

                if month:
                    SearchParams["month"] = month

                language = input("Language: ")

                if language:
                    SearchParams["language"] = language

                SearchResults = self.SearchBookAndGet(SearchParams)

                self.SearchBookAndPrint(SearchParams)

                save_option = input("Do you want to save the search results? (yes/no): ")

                if save_option.lower() == "yes" and SearchResults:

                    FileName = input("Enter the file name to store the search results: ")

                    self.StoreSearchInfo(SearchResults, FileName)

                else:

                    print("No matching books found.")




            elif choice == "4":

                search_title = input("Enter the title of the book to edit: ")

                SearchParams = {"title": search_title}

                SearchResults = self.SearchBookAndGet(SearchParams)

                if SearchResults:

                    print("Matching books:")

                    for index, book in enumerate(SearchResults, start=1):
                        print(f"{index}. {book.title}")

                    book_choice = input("Enter the number corresponding to the book you want to edit: ")

                    if book_choice.isdigit() and 1 <= int(book_choice) <= len(SearchResults):

                        book_index = int(book_choice) - 1

                        book = SearchResults[book_index]

                        print("Selected book:")

                        book.display_Information()

                        print("-------------------")

                        confirm = input("Do you want to edit this book? (yes/no): ")

                        if confirm.lower() == "yes":

                            NewInfo = {}

                            print("Enter the new information (press enter to skip):")

                            NewTitel = input("Title: ")

                            if NewTitel:
                                NewInfo["title"] = NewTitel

                            NewPublisher = input("Publisher: ")

                            if NewPublisher:
                                NewInfo["publisher"] = NewPublisher

                            NewIsbn10 = input("ISBN-10: ")

                            if NewIsbn10:
                                NewInfo["isbn_10"] = NewIsbn10

                            NewIsbn13 = input("ISBN-13: ")

                            if NewIsbn13:
                                NewInfo["isbn_13"] = NewIsbn13

                            NewEdition = input("Edition: ")

                            if NewEdition:
                                NewInfo["edition"] = NewEdition

                            NewYear = input("Year: ")

                            if NewYear:
                                NewInfo["year"] = NewYear

                            NewMonth = input("Month: ")

                            if NewMonth:
                                NewInfo["month"] = NewMonth

                            NewLanguage = input("Language: ")

                            if NewLanguage:
                                NewInfo["language"] = NewLanguage

                            self.EditBook(book.title, NewInfo)

                    else:

                        print("Invalid book choice.")

                else:

                    print("No matching books found.")



            elif choice == "5":
                title = input("Enter the title of the book to archive: ")
                self.ArchiveBook(title)


            elif choice == "6":

                title = input("Enter the title of the book to remove: ")

                self.RemoveBook(title)


            elif choice == "7":

                self.GenerateReports()


            elif choice == "8":

                self.PrintReports()

                print("Thank you for using the Library Management System.")
                break


            elif choice == "9":
                FileName = input("Enter the file name to save the books' data: ")
                self.SaveBooks(FileName)
                print("LMS terminated. Books' data saved to file.")
                break



            else:
                print("Invalid choice. Please try again.")


lms = Library()
lms.menu()

