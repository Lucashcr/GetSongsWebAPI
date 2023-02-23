const songs_list = document.getElementById("songs_list");

document.addEventListener("dragstart", (e) => {
    e.target.classList.add("dragging");
});

document.addEventListener("dragend", (e) => {
    e.target.classList.remove("dragging");
});

songs_list.addEventListener("dragover", (e) => {
    const dragging = document.querySelector(".dragging");
    const applyAfter = getNewPosition(songs_list, e.clientY);

    if (applyAfter) {
        applyAfter.insertAdjacentElement("afterend", dragging);
    } else {
        songs_list.prepend(dragging);
    }
});

function getNewPosition(songs_list, posY) {
    const items = songs_list.querySelectorAll(".song_item:not(.dragging)");
    let result;

    for (let refer_item of items) {
        const box = refer_item.getBoundingClientRect();
        const boxCenterY = box.y + box.height / 2;

        if (posY >= boxCenterY) result = refer_item;
    }

    return result;
}