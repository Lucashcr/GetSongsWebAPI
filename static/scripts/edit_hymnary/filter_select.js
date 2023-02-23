function getRequestFromAPI(model, id = "") {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", `https://${window.location.hostname}/api/${model}/${id}`, false);
    xhr.send();
    return JSON.parse(xhr.response);
}

// async function getRequestFromAPI(model, id="") {
//     const response = await fetch(`/api/${model}/${id}`);
//     var jsonData = await response.json();
//     return jsonData;
// };

let categories = getRequestFromAPI("category");
let artists = getRequestFromAPI("artist");
let songs = getRequestFromAPI("song");

let category_select = document.getElementById('select-category');
let song_select = document.getElementById('select-song');

let song_preview = document.getElementById('song-preview')

category_select.addEventListener("change", (e) => {
    song_select.innerHTML = "";
    song_select.appendChild(new Option("---"));
    songs
        .filter(song => song.category == e.target.value)
        .forEach(element => {
            let artist_name = artists.find(artist => artist.id == element.artist).name;
            song_select.appendChild(new Option(`${element.name} - ${artist_name}`, element.id));
        });
})

song_select.addEventListener("change", (e) => {
    let song = getRequestFromAPI('song', e.target.value);
    song_preview.setAttribute('src', song.preview_url);
    song_preview.hidden = false;
})