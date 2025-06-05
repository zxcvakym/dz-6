from typing import List, Dict, Union, Optional, Annotated

from pydantic import BaseModel, field_validator, Field, EmailStr, HttpUrl, field_validator

class BookModel(BaseModel):
    index: int = Field(..., description="Запис індексу")
    name: str = Field(..., description="Назва книги")
    author: str = Field(..., description="Автор")
    date_year: Optional[int] = Field(None, description="Рік видання книги")
    total_count: Optional[int] = Field(None, description="Доступна кількість ")


class BookModelResponse(BaseModel):
    index: int = Field(..., description="Запис індексу")
    name: str = Field(..., description="Назва книги")
    author: str = Field(..., description="Автор")
    date_year: Optional[int] = Field(None, description="Рік видання книги")
    total_count: Optional[int] = Field(None, description="Доступна кількість ")
    
    
class UserModel(BaseModel):
    name: Annotated[str, Field(default="Alex", examples=["Alex", "Alex12"], description="Ім'я користувача", min_length=2)]
    login: Annotated[str, Field(..., description="Логін", min_length=2)]
    password: Annotated[str, Field(..., examples=["1Yo&69"], description="Пароль", min_length=6)]
    email: EmailStr = Field(...)
    phone_number: Annotated[str, Field(..., example=["+380 (69) 357 42 89"], description="Номер телефону.", min_length=12)]
    

    @field_validator("password")
    def check_pass(cls, value: str):
        if value == "1Yo&69":
            raise ValueError("Ти що голова брати приклад у пароль?")
        
        if any([value.isdigit(), value.isalpha()]):
            raise ValueError("У паролі має бути одна літера або цифра.")
        
        is_upper = False
        is_lower = False
        for char in value:
            if not is_upper and char.isupper():
                is_upper = True
            if not is_lower and char.islower():
                is_lower = True
            if all([is_lower, is_upper]):
                break
        else:
            raise ValueError("У паролі має бути одна маленька та велика літера.")
        return value
    
    
    @field_validator("phone_number")
    def check_phone_num(cls, value: str):
        if value == "+380 (99) 39 38 570":
            raise ValueError("Приклад не можна брати як номер телефону.")
    
        if any(char.isalpha() for char in value):
            raise ValueError("В номеру телефону немає бути букв. ")
        return value