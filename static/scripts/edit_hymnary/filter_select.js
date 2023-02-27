// function getRequestFromAPI(model, id = "") {
//     const xhr = new XMLHttpRequest();
//     xhr.open("GET", `https://${window.location.hostname}/api/${model}/${id}`, false);
//     xhr.send();
//     return JSON.parse(xhr.response);
// }

// async function getRequestFromAPI(model, id = "") {
//     const response = await fetch(`/api/${model}/${id}`);
//     var jsonData = await response.json();
//     return jsonData;
// };

// let categories = getRequestFromAPI("category");
// let artists = getRequestFromAPI("artist");
// let songs = getRequestFromAPI("song");

// let categories = fetch(`https://${window.location.hostname}/api/category`).then(response => { return response.json() });
let categories;
fetch(`https://${window.location.hostname}/api/category`)
    .then(response => { categories = response.json() });
let artists;
fetch(`https://${window.location.hostname}/api/artist`)
    .then(response => { artists = response.json() });
let songs;
fetch(`https://${window.location.hostname}/api/song`)
    .then(response => { songs = response.json() });

let category_select = document.getElementById('select-category');
let song_select = document.getElementById('select-song');

let song_preview = document.getElementById('song-preview')

category_select.addEventListener("change", (e) => {
    song_select.innerHTML = "";
    song_select.appendChild(new Option("---"));
    songs.then(data => {
        data
            .filter(song => song.category == e.target.value)
            .forEach(element => {
                artists.then(data => {
                    let artist_name = data.find(artist => artist.id == element.artist).name;
                    song_select.appendChild(new Option(`${element.name} - ${artist_name}`, element.id));
                })
            });
    })
})

song_select.addEventListener("change", (e) => {
    let song = getRequestFromAPI('song', e.target.value);
    song_preview.setAttribute('src', song.preview_url);
    song_preview.hidden = false;
})