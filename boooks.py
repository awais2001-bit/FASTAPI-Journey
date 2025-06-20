from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'Title':'Title one', 'Author':'Author one', 'Category':'Science'},
    {'Title':'Title two', 'Author':'Author two', 'Category':'Computer'},
    {'Title':'Title three', 'Author':'Author three', 'Category':'Maths'},
    {'Title':'Title four', 'Author':'Author four', 'Category':'Maths'},
    {'Title':'Title five', 'Author':'Author five', 'Category':'Science'},
    {'Title':'Title six', 'Author':'Author five', 'Category':'English'},
    {'Title':'Title seven', 'Author':'Author five', 'Category':'English'}
]

#simple api endpoint
@app.get("/books")  # Add this
async def read_all_books():
    return BOOKS

@app.get("/books/byauthor/{Author}")
async def read_book_by_author(Author: str):
    books_by_author = []
    for book in BOOKS:
        if book.get('Author').casefold() == Author.casefold():
            books_by_author.append(book)
    return books_by_author

#path parameter function
@app.get("/books/{book_title}")  # Add this
async def read_book(book_title):
    for book in BOOKS:
        if book['Title'].casefold() == book_title.casefold():
            return book

#query parameter function
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

#both query and path parameters
@app.get("/books/{book_author}/")
async def read_category_by_author(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Author').casefold() == book_author.casefold() and \
                book.get('Category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

