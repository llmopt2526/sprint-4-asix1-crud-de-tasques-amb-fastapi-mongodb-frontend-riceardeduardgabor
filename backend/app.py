import os
from typing import Optional, List
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import AsyncMongoClient

# ------------------------------------------------------------------------ #
#                          Inicialització de l'aplicació                   #
# ------------------------------------------------------------------------ #
app = FastAPI(
    title="Gestor de Pel·lícules de Ricky",
    summary="API CRUD amb FastAPI i MongoDB Atlas",
)

# ------------------------------------------------------------------------ #
#                    Configuració de la connexió amb MongoDB               #
# ------------------------------------------------------------------------ #
MONGODB_URL = "mongodb+srv://riceardeduardgabor_db_user:bQrB2WEDUEmUyJBd@cluster1.m79fhot.mongodb.net/cine_db?retryWrites=true&w=majority&appName=Cluster1"

client = AsyncMongoClient(MONGODB_URL)
db = client.cine_db
movies_collection = db.get_collection("movies")

PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                             Definició dels models                        #
# ------------------------------------------------------------------------ #
class MovieModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(default="pendent de veure") # "pendent de veure" o "vista"
    puntuacio: int = Field(..., ge=1, le=5)
    genere: str = Field(...)
    usuari: str = Field(...) # Requerit per l'enunciat

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titol": "Inception",
                "descripcio": "Un lladre que roba secrets a través dels somnis",
                "estat": "pendent de veure",
                "puntuacio": 5,
                "genere": "Sci-Fi",
                "usuari": "Ricky"
            }
        },
    )

class UpdateMovieModel(BaseModel):
    """Model per a les actualitzacions (tots els camps opcionals)"""
    titol: Optional[str] = None
    descripcio: Optional[str] = None
    estat: Optional[str] = None
    puntuacio: Optional[int] = None
    genere: Optional[str] = None
    usuari: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

# ------------------------------------------------------------------------ #
#                          Endpoints (Rutes CRUD)                          #
# ------------------------------------------------------------------------ #

# 1. CREAR (POST)
@app.post("/movies", response_description="Afegir pel·lícula", status_code=status.HTTP_201_CREATED, response_model=MovieModel)
async def create_movie(movie: MovieModel = Body(...)):
    movie_dict = movie.model_dump(by_alias=True, exclude=["id"])
    new_movie = await movies_collection.insert_one(movie_dict)
    created_movie = await movies_collection.find_one({"_id": new_movie.inserted_id})
    return created_movie

# 2. LLISTAR (GET) - Amb filtre per gènere opcional
@app.get("/movies", response_description="Llistar pel·lícules", response_model=List[MovieModel])
async def list_movies(genere: Optional[str] = None):
    query = {}
    if genere:
        query["genere"] = genere
    movies = await movies_collection.find(query).to_list(100)
    return movies

# 3. ACTUALITZAR (PUT) - Requerit per l'enunciat
@app.put("/movies/{id}", response_description="Actualitzar pel·lícula", response_model=MovieModel)
async def update_movie(id: str, movie: UpdateMovieModel = Body(...)):
    update_data = {k: v for k, v in movie.model_dump().items() if v is not None}
    
    if len(update_data) >= 1:
        update_result = await movies_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if update_result.modified_count == 1:
            if (updated_movie := await movies_collection.find_one({"_id": ObjectId(id)})) is not None:
                return updated_movie

    if (existing_movie := await movies_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_movie

    raise HTTPException(status_code=404, detail=f"Pel·lícula {id} no trobada")

# 4. ELIMINAR (DELETE)
@app.delete("/movies/{id}", response_description="Eliminar pel·lícula")
async def delete_movie(id: str):
    delete_result = await movies_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Pel·lícula {id} no trobada")