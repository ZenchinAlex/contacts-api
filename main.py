import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Contact(BaseModel):
    name: str
    phone: str


def load_contacts(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_contacts(contacts, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


contacts = load_contacts("contacts.json")


@app.get("/contacts")
def get_contacts():
    return contacts

@app.get("/contacts/{name}")
def find_contacts(name):
    matches = []
    for contact in contacts:
        if contact["name"] == name:
            matches.append(contact["phone"])
    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Контакт не найден")
    return matches


@app.post("/contacts")
def add_contact(contact: Contact):
    for existing in contacts:
        if existing["name"] == contact.name and existing["phone"] == contact.phone:
            raise HTTPException(status_code=409, detail="Такой контакт уже есть")
    contacts.append({"name": contact.name, "phone": contact.phone})
    save_contacts(contacts, "contacts.json")
    return {"message": "Контакт добавлен"}