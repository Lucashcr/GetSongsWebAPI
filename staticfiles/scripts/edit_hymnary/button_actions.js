function togglePopUp() {
    document.querySelector(".pop-up").toggleAttribute("hidden");
}

async function appendSong() {
    const song = await songs.then(data => data.find(song => song.id == song_select.value));
    console.log(song);
    if (document.getElementById(`song_${song.id}`)) {
        alert("Esta música já foi adicionada!");
        return;
    };

    const artist = await artists.then(data => data.find(artist => artist.id == song.artist));
    const category = await categories.then(data => data.find(category => category.id == song.category));

    let newSongElement = document.createElement("div");
    newSongElement.className = "song_item border border-secondary";
    newSongElement.draggable = true;

    newSongElement.innerHTML = `<div class="left">
            <h3 class="name">${song.name}</h3>
            <h4 class="artist">${artist.name}</h4>
        </div>
        <div class="right">
            <button class="btn-close close" id="close_${song.id}">&times;</button>
            <br>
            <h4 class="category">${category.name}</h4>
        </div>
        <input type="hidden" class=${song.id} value="${song.id}">`;

    newSongElement.addEventListener("dragstart", (e) => {
        e.target.classList.add("dragging");
    });
    newSongElement.addEventListener("dragend", (e) => {
        e.target.classList.remove("dragging");
    })

    const btn = document.getElementById(`close_${song.id}`)
    btn.addEventListener("click", (e) => {
        const id = e.target.id.replace('close_', '');
        songs_list.removeChild(document.getElementById(`song_${id}`));
    })

    songs_list.insertAdjacentElement("beforeend", newSongElement);
}

for (const btn of songs_list.getElementsByClassName('btn-close')) {
    btn.addEventListener("click", (e) => {
        const id = btn.id.replace('close_', '');
        songs_list.removeChild(document.getElementById(`song_${id}`));
    });
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
            'template': document.getElementById('template').value,
            'new_title': document.getElementById('new-title').value
        })
    }).then(response => response.json()).then(data => {
        alert(data.alert);
        if (data.status == 200) {
            window.location.replace(
                window.location.pathname.replace('/edit', '')
            );
        }
    });
}