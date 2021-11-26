const saveAsBtn = document.querySelector("#saveCopy");
const editForm = document.querySelector("#templateDefForm");

prepareCanvas(defineCanvas, `data:image/jpeg;base64, ${imgData}`)

template.questions.map((qn) => {
    qn.answers.map((ans) => {
        let { x_coordinate, y_coordinate } = ans.coordinates
        console.log(x_coordinate, y_coordinate);
        addCircle(defineCanvas, { top: y_coordinate, left: x_coordinate })
    })
})