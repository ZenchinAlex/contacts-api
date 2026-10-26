from fastapi import FastAPI,HTTPException

app = FastAPI()

contacts = [
    {"name": "Alex", "phone": "+373111"},
    {"name": "Bred", "phone": "+373222"},
    {"name": "Anna", "phone": "+373777"},
]

@app.get ("/contacts")
def get_contacts():
    return contacts

@app.get ("/contacts/{name}")
def find_contacts(name):
    matches = []
    for contact in contacts:
        if contact["name"] == name:
            matches.append(contact["phone"])
    if len(matches) == 0:
        raise HTTPException(status_code=404,detail="Контакт не найден")
    return matches