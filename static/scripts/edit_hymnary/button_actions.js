function togglePopUp() {
    document.querySelector(".pop-up").toggleAttribute("hidden");
}

function removeSong(targetID) {
    songs_list.removeChild(
        document.getElementById(
            targetID.replace('close', 'song')
        )
    );
}

async function appendSong() {
    const song = await songs.then(data => data.find(song => song.id == song_select.value));
    if (document.getElementById(`song_${song.id}`)) {
        alert("Esta música já foi adicionada!");
        return;
    };

    const artist = await artists.then(data => data.find(artist => artist.id == song.artist));
    const category = await categories.then(data => data.find(category => category.id == song.category));

    let newSongElement = document.createElement("div");
    newSongElement.id = `song_${song.id}`;
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
        <input type="hidden" class="song_id" value="${song.id}">`;

    newSongElement = songs_list.insertAdjacentElement("beforeend", newSongElement);
    newSongElement.addEventListener("dragstart", (e) => {
        e.target.classList.add("dragging");
    });
    newSongElement.addEventListener("dragend", (e) => {
        e.target.classList.remove("dragging");
    })
    newSongElement.children[1].children[0].addEventListener("click", (e) => {
        removeSong(e.target.id);
    });
}

for (const btn of songs_list.getElementsByClassName('btn-close')) {
    btn.addEventListener("click", (e) => { removeSong(e.target.id); })
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

async function saveHymnary(showAlert = false) {
    let songs_id = Array.from(songs_list.querySelectorAll('.song_id'))
        .map(song_id => parseInt(song_id.value));

    await fetch(window.location.pathname.replace('edit', 'save'), {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            'songs_id': songs_id,
            'print_category': document.getElementById('print-category').checked,
            'template': document.getElementById('template').value,
            'new_title': document.getElementById('new-title').value
        })
    })
        .then(response => response.json())
        .then(data => {
            if (showAlert) {
                alert(data.alert);
                showAlert = false;
            }

            if (data.status != 200) {
                if (showAlert)
                    alert(data.alert);

                console.log(data);
            }

        });
}

async function viewHymnary() {
    await saveHymnary();
    window.open(window.location.pathname.replace('edit', 'export'), '_blank');
}

async function exportHymnary() {
    await saveHymnary();
    window.open(window.location.pathname.replace('edit', 'export?as_attachment=1'), '_blank');
}