from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Dict

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    rating: float
    review: str
    published_date: int
    def __init__(self, id, title, author, rating, review,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating
        self.review = review
        self.published_date = published_date

class BookRequest(BaseModel):
    id: int=Field(default=None)
    title: str=Field()
    author: str=Field()
    rating: float=Field()
    review: str=Field()
    published_date: int=Field()
    class Config:
        schema_extra={
            'example':{
                'title':'name of the book',
                'author':'name of the author',
                'rating':4.7,
                'review':'review of the book',
                'published_date':2012
            }
        }



books = [
    Book(1, "The Big Sleep", "Raymond Chandler", 4.5, "A detective story so tangled, you'll need a map and a magnifying glass.",published_date=2025),
    Book(2, "The Maltese Falcon", "Dashiell Hammett", 4.3, "A bird worth more than its weight in trouble.",published_date=2025),
    Book(3, "Farewell, My Lovely", "Raymond Chandler", 4.2, "A tale of love, loss, and a lot of bruises.",published_date=2012),
    Book(4, "The Postman Always Rings Twice", "James M. Cain", 4.1, "When the postman rings, someone ends up dead.",published_date=2012),
    Book(5, "Double Indemnity", "James M. Cain", 4.4, "Insurance fraud never looked so good... or so deadly.",published_date=2022),
    Book(6, "The Long Goodbye", "Raymond Chandler", 4.6, "A goodbye that stretches out like a bad hangover.",published_date=2022)
    ]

@app.get("/")
def root():
    return {"message": "WELCOME TO THE BOOKS"}

@app.get("/books")
def get_books():
    return books

@app.post('/create_book')
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    books.append(book_id(new_book))


@app.get('/books/published')
def get_book_published_date(published_date: int):
    books_published = []
    for book in books:
        if book.published_date == published_date:
            books_published.append(book)
    return books_published

@app.get("/books/{id}")
def get_book(id: int):
    for book in books:
        if book.id == id:
            return book

def book_id(book: Book):
    if len(books) > 0:
        book.id = books[-1].id + 1
    else:
        book.id = book.id + 1

    return book

@app.put('/books/update')
def update_book(book: BookRequest):
    for i in range(len(books)):
        if books[i].id == book.id:
            updated_book = Book(**book.dict())
            books[i] = updated_book


@app.delete('/books/{id}')
def delete_book(id: int):
    for i in range(len(books)):
        if books[i].id == id:
            books.pop(i)
            break

@app.get('/books/published')
def get_book_published_date(published_date: int):
    books_published = []
    for book in books:
        if book.published_date == published_date:
            books_published.append(book)
    return books_published