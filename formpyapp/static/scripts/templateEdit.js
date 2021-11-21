const saveAsBtn = document.querySelector("#saveCopy");
const editForm = document.querySelector("#templateDefForm");
const editCanvas = new fabric.Canvas("defineCanvas");

prepareCanvas(editCanvas, `data:image/jpeg;base64, ${imgData}`)
