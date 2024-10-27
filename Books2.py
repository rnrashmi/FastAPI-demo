from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID not needed', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A story about the American Dream",
                "rating": 3
            }
        }
    }


            

BOOKS = [
    Book(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 'A story about the American Dream', 3),
    Book(2, 'Dune', 'Frank Herbert', 'A science fiction masterpiece', 5),
    Book(3, 'Harry Potter', 'J.K. Rowling', 'A story about a young wizard', 2),
    Book(4, 'The Da Vinci Code', 'Dan Brown', 'A mystery thriller', 1),
    Book(5, 'The Catcher in the Rye', 'J.D. Salinger', 'A story about a young boy in New York', 4),
    Book(6, 'The Alchemist', 'Paulo Coelho', 'A story about a young shepherd in Spain', 5),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book_request=Body()):
    BOOKS.append(book_request)

@app.post("/create-books", status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    book.id=1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

@app.get("/books/")
async def read_book_by_rating(book_rating: int=Query(gt=0, lt=5)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status=400, detail='Item not found')

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break