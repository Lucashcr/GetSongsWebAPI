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
    newSongElement.classList.add("song_item border border-secondary");
    newSongElement.draggable = true;

    newSongElement.innerHTML = `<div>
            <h3 class="name">${song.name}</h3>
            <h4 class="artist">${artist.name}</h4>
        </div>
        <h4 class="category">${category.name}</h4>
        <input type="hidden" class=${song.id} value="{{item.song.id}}">`;
    // songs.then(data => {
    //     let song = data.find(song => song.id == song_select.value);

    //     let newSongElement = document.createElement("div");
    //     newSongElement.classList.add("song_item border border-secondary");
    //     newSongElement.draggable = true;

    //     newSongElement.innerHTML = `<div>
    //             <h3 class="name">${song.name}</h3>
    //             <h4 class="artist">${song.artist}</h4>
    //         </div>
    //         <h4 class="category">${song.category}</h4>
    //         <input type="hidden" class=${song.id} value="{{item.song.id}}">`;
    //     let category = document.createElement("td");
    //     categories.then(data => {
    //         category.innerText = data.find(cat => song.category == cat.id).name;
    //         newSongElement.appendChild(category);
    //         let songname = document.createElement("td");
    //         songname.innerText = song.name;
    //         newSongElement.appendChild(songname);
    //         let artist = document.createElement("td");
    //         artists.then(data => {
    //             artist.innerText = data.find(art => song.artist == art.id).name;
    //             newSongElement.appendChild(artist);
    //             let song_id_input = document.createElement("input");
    //             song_id_input.type = "hidden";
    //             song_id_input.classList.add("song_id");
    //             song_id_input.value = song.id;
    //             newSongElement.appendChild(song_id_input)

    //             songs_list.insertAdjacentElement("beforeend", newSongElement);
    //         })
    //     })
    // })
}

// function removeSong() {
//     songs_list.removeChild(songs_list.lastElementChild);
// }


function removeSong(id) {
    console.log(id);
    songs_list.removeChild(document.getElementById(`song_${id}`));
}

for (const btn of songs_list.getElementsByClassName('btn-close')) {
    btn.addEventListener("click", (e) => {
        removeSong(btn.id.replace('close_', ''))
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