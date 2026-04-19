const API_URL = "http://127.0.0.1:8000/movies";

document.addEventListener("DOMContentLoaded", carregarDades);

async function carregarDades() {
    const resposta = await fetch(API_URL);
    const dades = await resposta.json();
    
    const llista = document.getElementById("movies-list");
    llista.innerHTML = "";

    dades.forEach(item => {
        const card = document.createElement("div");
        card.className = "movie-card";
        card.innerHTML = `
            <h3>${item.titol.toUpperCase()}</h3>
            <p>${item.descripcio}</p>
            <p>GENERE: ${item.genere} | NOTA: ${item.puntuacio}/5</p>
            <p>ESTAT: ${item.estat} | USUARI: ${item.usuari}</p>
            <button class="delete-btn" onclick="eliminarDada('${item._id || item.id}')">ELIMINAR REGISTRE</button>
        `;
        llista.appendChild(card);
    });
}

document.getElementById("movie-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const novaDada = {
        titol: document.getElementById("titol").value,
        descripcio: document.getElementById("descripcio").value,
        genere: document.getElementById("genere").value,
        puntuacio: parseInt(document.getElementById("puntuacio").value),
        estat: document.getElementById("estat").value,
        usuari: document.getElementById("usuari").value
    };

    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(novaDada)
    });

    e.target.reset();
    carregarDades();
});

async function eliminarDada(id) {
    if (confirm("Confirmar eliminacio definitiva?")) {
        await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        carregarDades();
    }
}