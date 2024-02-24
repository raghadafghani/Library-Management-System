# Library-Management-System
This repository contains the project for the ENCS3130 Linux Laboratory course, part of the Department of Electrical & Computer Engineering at Birzeit University. The project is focused on developing a Library Management System (LMS) using Python.

# Project Description
The Library Management System (LMS) provides various functionalities to effectively manage a library's collection. The following features are implemented in the system:

Add New Book: Allows the user to add new books to the library collection. The user needs to provide a file containing the book information in a specific format. The LMS displays the book information on the screen and sets the number of copies to 1 for each new book. If a book already exists, the user can choose to replace the existing record or add another copy.

Load Books from File: Reads a file containing book information, parses the data, and handles any file-related errors.

Search Books: Enables users to search for books in the library collection using various parameters. The search results are displayed on the screen, and users can also save the results in a text file named "search_result.txt".

Edit Book Information: Allows users to edit the details of existing books. Users can provide the file name or ISBN number to update the book's information. The LMS confirms the changes with the user before saving the modified data. The edited book is added as a new entry in addition to the books in the file.

Archive Books: Allows users to move rarely used books to an archive by entering the ISBNs of the desired books and confirming the action. The user can specify the number of copies to be archived if multiple copies exist in the LMS.

Delete Books: Enables users to delete books from the LMS. Only archived books can be deleted, and the LMS prompts the user for confirmation. If the book is successfully deleted, a confirmation message is displayed. If the book is not found in the archive, a "Book not found" message is printed.

Generate Reports: Provides various reports about the books available in the LMS. The reports include information such as the total number of books, the number of different books, the number of archived books, the number of books newer than a specific year, book distribution by publisher, and book distribution by year.

Exit and Save to File: Terminates the LMS and saves all book data to a file named "lms.txt".

