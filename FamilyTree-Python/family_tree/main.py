from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from Model.children import Children
from Model.first_couple import FirstCouple
from Model.spouse import Spouse
from database.database import get_db_connection
from service.children_service import add_children, get_children_details
from service.individuals_service import add_first_couple, get_family_tree_details, logger
from service.spouse_service import add_new_spouse, get_spouse_details, get_couple_details

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/individuals")
async def add_individual(individuals: FirstCouple, db: Session = Depends(get_db_connection)):
    logger.info("individual details: %s", individuals)
    add_first_couple(individuals, db)
    return {"message": "Couple added successfully"}

@app.post("/children")
async def add_child(children: Children, db: Session = Depends(get_db_connection)):
    logger.info("children details: %s", children)
    add_children(children, db)
    return {"message": "Child added successfully"}

@app.post("/spouse")
async def add_spouse(spouse: Spouse, db: Session = Depends(get_db_connection)):
    add_new_spouse(spouse, db)
    return {"message": "Spouse added successfully"}

@app.get("/children/{parent_id}")
async def get_children(parent_id: int, db: Session = Depends(get_db_connection)):
    return get_children_details(parent_id, db)

@app.get("/spouse/{spouse_id}")
async def get_spouse(spouse_id: int, db: Session = Depends(get_db_connection)):
    return get_spouse_details(spouse_id, db)

@app.get("/marriage/{individual_id}")
async def get_couple(individual_id: int, db: Session = Depends(get_db_connection)):
    return get_couple_details(individual_id, db)

@app.get("/family_tree/{last_name}")
async def get_family_tree(last_name: str, db: Session = Depends(get_db_connection)):
    return get_family_tree_details(last_name, db)
