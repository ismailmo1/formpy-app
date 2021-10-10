let readBtn = document.querySelector("#readFormBtn");
let formsUploadFrm = document.querySelector("form");
let container = document.querySelector("#mainContainer")

readBtn.addEventListener("click", async (e)=>{
    e.preventDefault();
    forms = new FormData(formsUploadFrm);
    res = await fetch("/read", { method: "POST", body: forms });
    markedImgs = await res.json();
    markedImgs['imgs'].forEach(imgData=>{
        let img = document.createElement("img")
        img.classList.add("img-fluid");
        img.src = `data:image/png;base64,${imgData}`;
        container.appendChild(img)
    })
    console.log(markedImgs['answers'])
})