const form = document.querySelector("form");
const container = document.querySelector("#main-content>.container")

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("sending form");
    showLoading();
    let spots = await findSpots(form);
    addImage(spots["img"])

})

function showLoading() {
    container.removeChild(form)
}

async function findSpots(form) {
    let formData = new FormData(form);
    res = await fetch("/find-spots", { method: "POST", body: formData })
    spots = await res.json()
    return spots
}

function addImage(imgData) {
    let imgContainer = document.createElement("img")
    imgContainer.classList.add("img-fluid")
    imgContainer.src = `data:image/png;base64,${imgData}`
    container.appendChild(imgContainer)
}
