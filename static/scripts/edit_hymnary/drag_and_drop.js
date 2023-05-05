const songs_list = document.getElementById("songs_list");
const song_items = document.getElementsByClassName("song_item");

for (const song_item of song_items) {
    song_item.addEventListener("dragstart", (e) => {
        e.target.classList.add("dragging");
    });
    song_item.addEventListener("dragend", (e) => {
        e.target.classList.remove("dragging");
    })
};

songs_list.addEventListener("dragover", (e) => {
    const dragging = document.querySelector(".dragging");
    const applyAfter = getNewPosition(e.clientY);

    console.log(applyAfter);

    if (applyAfter) {
        applyAfter.insertAdjacentElement("afterend", dragging);
    } else {
        songs_list.prepend(dragging);
    }
});

function getNewPosition(posY) {
    const items = songs_list.querySelectorAll(".song_item:not(.dragging)");
    let result;

    console.log("posY: ", posY)
    for (let refer_item of items) {
        const box = refer_item.getBoundingClientRect();

        if (posY >= box.top) {
            result = refer_item
        };
    }

    return result;
}