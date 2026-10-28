
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Contact(BaseModel):
    name: str
    phone: str


def init_db():
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT
        )
    """)
    connection.commit()
    connection.close()

init_db()


@app.get("/contacts")
def get_contacts():
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name, phone FROM contacts")
    rows = cursor.fetchall()
    connection.close()

    result = []
    for row in rows:
        result.append({"name": row[0], "phone": row[1]})
    return result

@app.get("/contacts/{name}")
def find_contacts(name):
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()
    cursor.execute("SELECT phone FROM contacts WHERE name = ?", (name,))
    rows = cursor.fetchall()
    connection.close()

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="Контакт не найден")

    matches = []
    for row in rows:
        matches.append(row[0])
    return matches


@app.post("/contacts")
def add_contact(contact: Contact):
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM contacts WHERE name = ? AND phone = ?",
        (contact.name, contact.phone),
    )
    if cursor.fetchone() is not None:
        connection.close()
        raise HTTPException(status_code=409, detail="Такой контакт уже есть")

    cursor.execute(
        "INSERT INTO contacts (name, phone) VALUES (?, ?)",
        (contact.name, contact.phone),
    )
    connection.commit()
    connection.close()
    return {"message": "Контакт добавлен"}