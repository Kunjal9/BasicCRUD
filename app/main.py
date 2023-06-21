import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String, Text, create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# SQLAlchemy specific code
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# html_str = """<!DOCTYPE html>
# <html>
#   <head>
#     <title>Contact Form</title>
#   </head>
#   <body>
#     <h1>Contact Us</h1>
#     <form method="post" action="/contact">
#       <label for="name">Name:</label>
#       <input type="text" id="name" name="name" required><br>
#       <label for="email">Email:</label>
#       <input type="email" id="email" name="email" required><br>
#       <label for="message">Message:</label><br>
#       <textarea id="message" name="message" rows="4" required></textarea><br>
#       <input type="submit" value="Submit">
#     </form>
#   </body>
# </html>

# """

# Base = declarative_base()

app = FastAPI()


class ContactForm(Base):
    __tablename__ = "contact_form"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    message = Column(Text)


Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
@app.get("/")
async def show_contact_form(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.post("/contact")
async def contact_form(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    email = form_data.get("email")
    message = form_data.get("message")
    
    db = SessionLocal()
    contact = ContactForm(name=name, email=email, message=message)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    db.close()
    return {"message": "Form submitted successfully"}

# @app.get("/users/{user_id}")
# def read_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @app.get("/users/")
# def read_users():
#     db = SessionLocal()
#     users = db.query(User).all()
#     return users


# @app.put("/users/{user_id}")
# def update_user(user_id: int, name: str, email: str):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.name = name
#     user.email = email
#     db.commit()
#     db.refresh(user)
#     return user


# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return {"message": "User deleted successfully"}
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
if __name__ == "__main__":
    main()
