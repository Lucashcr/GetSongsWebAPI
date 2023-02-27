function togglePopUp() {
    document.querySelector(".pop-up").toggleAttribute("hidden");
}

function appendSong() {
    let song = songs.find(song => song.id == song_select.value);

    let newSongElement = document.createElement("tr");
    newSongElement.classList.add("song_item");
    newSongElement.draggable = true;

    let category = document.createElement("td");
    category.innerText = categories.find(cat => song.category == cat.id).name;
    newSongElement.appendChild(category);
    let songname = document.createElement("td");
    songname.innerText = song.name;
    newSongElement.appendChild(songname);
    let artist = document.createElement("td");
    artist.innerText = artists.find(art => song.artist == art.id).name;
    newSongElement.appendChild(artist);
    let song_id_input = document.createElement("input");
    song_id_input.type = "hidden";
    song_id_input.classList.add("song_id");
    song_id_input.value = song.id;
    newSongElement.appendChild(song_id_input)

    songs_list.insertAdjacentElement("beforeend", newSongElement);
    togglePopUp();
}

function removeSong() {
    songs_list.removeChild(songs_list.lastElementChild);
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}

function saveHymnary() {
    let songs_id = Array.from(songs_list.querySelectorAll('.song_id'))
        .map(song_id => parseInt(song_id.value));
    console.log(songs_id);

    const csrftoken = getCookie('csrftoken');

    fetch(window.location.pathname.replace('edit', 'save'), {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'songs_id': songs_id,
            'print_category': document.getElementById('print-category').checked,
            'template': document.getElementById('template').value
        })
    }).then(response => { return response.json() }).then(
        data => alert(data.result)
    );
}