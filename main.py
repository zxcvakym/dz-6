from typing import List, Dict, Union, Optional, Annotated

from fastapi import FastAPI, HTTPException, status, Query, Path
from fastapi.responses import JSONResponse
from data_actions import get_db, save_db
from models import BookModel, BookModelResponse, UserModel
import uvicorn


app = FastAPI()
users_save = []

@app.get("/books/", response_model=List[BookModelResponse], status_code=status.HTTP_202_ACCEPTED)
async def get_books():
    return get_db()


@app.get("/books/{index}/", response_model=Optional[BookModelResponse], status_code=status.HTTP_202_ACCEPTED)
async def get_book(index: int):
    book = next((book for book in get_db() if book.get("index") == index), None)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Книгу з id {index} не найдено")
    return book


@app.post("/books/", status_code=status.HTTP_201_CREATED)
async def add_book(book_model: BookModel):
    db = get_db()
    db.append(book_model.model_dump())
    save_db(db)
    return JSONResponse("Нова книга додена.")


@app.post("/users/", status_code=status.HTTP_201_CREATED)
def add_user(user: UserModel): 
    users_save.append(user.model_dump())
    return JSONResponse("Нового користувача додано.")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)