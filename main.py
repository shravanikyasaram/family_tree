from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Model.children import Children
from Model.first_couple import FirstCouple
from Model.spouse import Spouse
from database.database import get_db_connection
from service.children_service import add_children, get_children_details
from service.individuals_service import add_first_couple
from service.spouse_service import add_new_spouse, get_spouse_details, get_couple_details

app = FastAPI()

@app.get("/")
async def hello():
    return "Hello World!"

@app.post("/individuals")
async def add_individual(individuals: FirstCouple, db: Session = Depends(get_db_connection)):
    add_first_couple(individuals, db)
    return {"message": "Couple added successfully"}

@app.post("/children")
async def add_child(children: Children, db: Session = Depends(get_db_connection)):
    add_children(children, db)
    return {"message": "Child added successfully"}

@app.post("/spouse")
async def add_spouse(spouse: Spouse, db: Session = Depends(get_db_connection)):
    add_new_spouse(spouse, db)
    return {"message": "Spouse added successfully"}

@app.get("/children/{parent_id}")
async def get_individual(parent_id, db: Session = Depends(get_db_connection)):
    return get_children_details(parent_id, db)

@app.get("/spouse/{spouse_id}")
async def get_spouse(spouse_id, db: Session = Depends(get_db_connection)):
    return get_spouse_details(spouse_id, db)

@app.get("/marriage/{id}")
async def get_couple(couple_id, db: Session = Depends(get_db_connection)):
    return get_couple_details(couple_id, db)