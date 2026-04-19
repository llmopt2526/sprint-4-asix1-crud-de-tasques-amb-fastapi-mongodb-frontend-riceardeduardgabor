# SPRINT 4: GESTIÓ DE PEL·LÍCULES
**Desenvolupador:** Riceard Gabor  
**Projecte:** Aplicació CRUD (Crear, Llegir, Actualitzar, Esborrar)  

---

## 1. Descripció del Projecte
Aquest projecte consisteix en un sistema per gestionar una llista personal de pel·lícules. L'objectiu ha estat connectar una interfície web (**Frontend**) amb un servidor de dades (**Backend**) i una base de dades al núvol.

## 2. Estructura del Sistema
El projecte s'ha organitzat seguint l'estructura simple demanada per l'enunciat:

* **`backend/app.py`**: Conté tota la lògica del servidor, la connexió a la base de dades i els models de dades.
* **`backend/requirements.txt`**: Llista de dependències de Python.
* **`frontend/`**: Conté la interfície d'usuari (HTML, CSS minimalista i JavaScript).
* **`tests/`**: Inclou el fitxer de proves realitzades amb Postman (`Postman_API_tests.json`).

---

## 3. Procés de Desenvolupament

### Pas 1: Configuració del Backend
He utilitzat **FastAPI** per crear el servidor. He definit un model de dades per a les pel·lícules que inclou: títol, descripció, gènere, puntuació (1-5), estat (pendent/vista) i l'usuari responsable.

### Pas 2: Base de Dades
He connectat el sistema a **MongoDB Atlas**. Per fer-ho, he utilitzat la llibreria **PyMongo Async**, que permet guardar i recuperar la informació de forma eficient sense bloquejar el servidor.

### Pas 3: Creació de l'API (Endpoints)
He programat les quatre operacions bàsiques del CRUD:
* **GET**: Per llistar totes les pel·lícules.
* **POST**: Per afegir noves entrades des del formulari.
* **PUT**: Per modificar l'estat o dades d'una pel·lícula existent.
* **DELETE**: Per eliminar registres del sistema.

### Pas 4: Interfície Frontend
He creat una web amb un disseny **minimalista en blanc i negre**. He utilitzat **JavaScript (Fetch)** per fer que la web es comuniqui en temps real amb el Backend sense haver de recarregar la pàgina.

### Pas 5: Verificació i Tests
He validat que tots els punts d'accés (endpoints) funcionen correctament utilitzant **Postman**, exportant els resultats a la carpeta de tests com demanava l'enunciat.

---

## 4. Com executar el projecte
1. Activar el servidor:
   ```bash
   python -m uvicorn backend.app:app --reload