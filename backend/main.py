import os
from typing import Optional, List
from fastapi import FastAPI, Body, HTTPException, status
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import AsyncMongoClient

# ------------------------------------------------------------------------ #
#                          Inicialització                                  #
# ------------------------------------------------------------------------ #
app = FastAPI(
    title="Gestor de Pel·lícules de Ricky",
    summary="API CRUD amb FastAPI i MongoDB Atlas"
)

# CONNEXIÓ A MONGODB ATLAS (Substitueix LA_TEVA_CONTRASENYA)
MONGODB_URL = "mongodb+srv://riceardeduardgabor_db_user:bQrB2WEDUEmUyJBd@cluster1.m79fhot.mongodb.net/cine_db?retryWrites=true&w=majority&appName=Cluster1"

client = AsyncMongoClient(MONGODB_URL)
db = client.cine_db
movies_collection = db.get_collection("movies")

# Helper per convertir els IDs de MongoDB a strings
PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                            Model de la Pel·lícula                        #
# ------------------------------------------------------------------------ #
class MovieModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(default="pendent de veure")
    puntuacio: int = Field(..., ge=1, le=5)
    genere: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titol": "Inception",
                "descripcio": "Un lladre que roba secrets a través dels somnis",
                "estat": "vista",
                "puntuacio": 5,
                "genere": "Sci-Fi"
            }
        },
    )

# ------------------------------------------------------------------------ #
#                            Endpoints (Rutes)                             #
# ------------------------------------------------------------------------ #

# 1. CREAR una pel·lícula (POST)
@app.post("/movies", response_description="Afegir pel·lícula", status_code=status.HTTP_201_CREATED, response_model=MovieModel)
async def create_movie(movie: MovieModel = Body(...)):
    movie_dict = movie.model_dump(by_alias=True, exclude=["id"])
    new_movie = await movies_collection.insert_one(movie_dict)
    created_movie = await movies_collection.find_one({"_id": new_movie.inserted_id})
    return created_movie

# 2. LLISTAR totes les pel·lícules (GET)
@app.get("/movies", response_description="Llistar pel·lícules", response_model=List[MovieModel])
async def list_movies():
    movies = await movies_collection.find().to_list(100)
    return movies

# 3. ESBORRAR una pel·lícula per ID (DELETE)
@app.delete("/movies/{id}", response_description="Eliminar pel·lícula")
async def delete_movie(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no vàlid")
    
    delete_result = await movies_collection.delete_one({"_id": ObjectId(id)})
    
    if delete_result.deleted_count == 1:
        return {"missatge": "Pel·lícula eliminada correctament"}
    
    raise HTTPException(status_code=404, detail=f"Pel·lícula amb ID {id} no trobada")

# Ruta de benvinguda
@app.get("/")
async def read_root():
    return {"missatge": "Benvingut al teu Gestor de Pel·lícules, Ricky!"}