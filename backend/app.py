import os
from typing import Optional, List
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import AsyncMongoClient

# ------------------------------------------------------------------------ #
#                          1. Inicialitzacio de l'API                      #
# ------------------------------------------------------------------------ #
app = FastAPI(
    title="API Cine Riceard",
    summary="Sistema de gestio de dades per al projecte Sprint 4",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------ #
#                 2. Configuracio de la connexio amb MongoDB               #
# ------------------------------------------------------------------------ #
MONGO_URL = "mongodb+srv://riceardeduardgabor_db_user:bQrB2WEDUEmUyJBd@cluster1.m79fhot.mongodb.net/cine_db?retryWrites=true&w=majority"
client = AsyncMongoClient(MONGO_URL)
db = client.cine_db
movie_collection = db.get_collection("movies")

PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                          3. Definicio dels models                        #
# ------------------------------------------------------------------------ #
class MovieModel(BaseModel):
    """ Model de dades per a la gestio de pel·licules """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(...)          # pendent de veure / vista
    puntuacio: int = Field(..., ge=1, le=5)
    genere: str = Field(...)
    usuari: str = Field(...)         # Riceard

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

# ------------------------------------------------------------------------ #
#                          4. Rutes de l'API (CRUD)                        #
# ------------------------------------------------------------------------ #

@app.get("/movies", response_model=List[MovieModel])
async def llistar_pelicules():
    """ Jo llisto tots els registres de la base de dades """
    return await movie_collection.find().to_list(1000)

@app.post("/movies", status_code=status.HTTP_201_CREATED, response_model=MovieModel)
async def crear_pelicula(movie: MovieModel = Body(...)):
    """ Jo creo un nou registre a la col·leccio """
    new_movie = await movie_collection.insert_one(
        movie.model_dump(by_alias=True, exclude=["id"])
    )
    return await movie_collection.find_one({"_id": new_movie.inserted_id})

@app.put("/movies/{id}", response_model=MovieModel)
async def actualitzar_pelicula(id: str, movie: MovieModel = Body(...)):
    """ Jo modifico un registre existent """
    update_data = movie.model_dump(by_alias=True, exclude=["id"])
    resultat = await movie_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True
    )
    if resultat:
        return resultat
    raise HTTPException(status_code=404, detail="Registre no trobat")

@app.delete("/movies/{id}")
async def eliminar_pelicula(id: str):
    """ Jo elimino un registre de forma permanent """
    resultat = await movie_collection.delete_one({"_id": ObjectId(id)})
    if resultat.deleted_count == 1:
        return {"missatge": "Registre eliminat correctament"}
    raise HTTPException(status_code=404, detail="Error en eliminar")