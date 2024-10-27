from fastapi import FastAPI, Body
app = FastAPI()

@app.get("/books")
async def get_books():
    return [{"title": "The Great Gatsby"}, {"title": "The Catcher in the Rye"}]

@app.get("/books/{book_value}")
async def get_books_dynamic(book_value: str):
    return {"title": book_value}

BOOKS = [
    {"category": "Fiction", "name": "The Great Gatsby"},
    {"category": "Science Fiction", "name": "Dune"},
    {"category": "Mystery", "name": "Harry Potter"},
    {"category": "Mystery", "name": "The Da Vinci Code"}
]

@app.get("/books/all/")
async def get_category_by_query_params():
    return BOOKS

@app.get("/books/")
async def get_category_by_query_params(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create/")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update/")
async def update_book(book_to_update=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('name').casefold() == book_to_update.get('name').casefold():
            BOOKS[i] = book_to_update


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('name').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break