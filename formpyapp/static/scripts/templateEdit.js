const saveAsBtn = document.getElementById("saveCopy");
const editForm = document.getElementById("templateDefForm");
const updateBtn = document.getElementById("defineCanvasUpdate")

// override variables in canvasScript
alignedImg = `data:image/jpeg;base64, ${imgData}`
defineUrl = "/define-template/copy"

prepareCanvas(defineCanvas, alignedImg);
activateTab(creationSteps.DEFINE)
templateName.value = template.name;
publicToggle.checked = template.public;

template.questions.map((qn, idx) => {
    // question 1 already initialised on load so only add additional questions
    (idx > 0) && addQuestion();
    qn.answers.map((ans) => {
        let { x_coordinate, y_coordinate } = ans.coordinates
        addCircle(defineCanvas, {
            top: y_coordinate,
            left: x_coordinate,
            question: qn.question_value,
            value: ans.value
        })
    })
})

updateBtn.addEventListener("click", async () => {
    defineUrl = `/update-template/${templateId}`
    let res = await defineTemplate(update = true)
    console.log(res);
})