const API_URL = "http://127.0.0.1:8000/movies";

document.addEventListener('DOMContentLoaded', loadMovies);

async function loadMovies() {
    const res = await fetch(API_URL);
    const movies = await res.json();
    const tableBody = document.getElementById('moviesTableBody');
    tableBody.innerHTML = '';
    movies.forEach(m => {
        tableBody.innerHTML += `
            <tr>
                <td><strong>${m.titol}</strong><br><small>${m.genere}</small></td>
                <td>⭐ ${m.puntuacio}/5</td>
                <td><button class="button button-outline" onclick="deleteMovie('${m._id}')">🗑️ Borrar</button></td>
            </tr>`;
    });
}

document.getElementById('movieForm').onsubmit = async (e) => {
    e.preventDefault();
    const movie = {
        titol: document.getElementById('titol').value,
        descripcio: document.getElementById('descripcio').value,
        genere: document.getElementById('genere').value,
        puntuacio: parseInt(document.getElementById('puntuacio').value),
        estat: "pendent de veure",
        usuari: "Ricky"
    };
    await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(movie)
    });
    e.target.reset();
    loadMovies();
};

async function deleteMovie(id) {
    if(confirm('Segur?')) {
        await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        loadMovies();
    }
}