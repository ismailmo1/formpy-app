const saveAsBtn = document.querySelector("#saveCopy");
const editForm = document.querySelector("#templateDefForm");

// override variables in canvasScript
alignedImg = `data:image/jpeg;base64, ${imgData}`
defineUrl = "/define-template/copy"

// add current template id to save old image name in copied template
questions['currTempId'] = templateId


prepareCanvas(defineCanvas, alignedImg);
activateTab(creationSteps.DEFINE)
templateName.value = template.name;
publicToggle.checked = template.public;

template.questions.map((qn, idx) => {
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
