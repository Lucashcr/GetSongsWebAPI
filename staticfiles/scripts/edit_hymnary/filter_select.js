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
    songs.then(data => {
        let song = data.find(song => song.id == e.target.value);
        song_preview.setAttribute('src', song.preview_url);
        song_preview.hidden = false;
    })
})