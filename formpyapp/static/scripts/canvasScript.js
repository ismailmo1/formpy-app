// create canvas with id of canvas element
// add options via object

const defineCanvas = new fabric.Canvas("defineCanvas");
const alignCanvas = new fabric.Canvas("alignCanvas");
const circleList = document.getElementById("circleList")
const defineNavBtn = document.getElementById("defineNavButton");
const alignNavBtn = document.getElementById("alignNavButton");
const saveNavBtn = document.getElementById("saveNavButton");
const imgForm = document.getElementById("uploadImgForm");
const imgFormUploadBtn = document.getElementById("uploadImgBtn");
const imgUploadInput = document.getElementById("photoUpload");
const uploadTab = document.getElementById("nav-upload");
const alignTab = document.getElementById("nav-align");
const alignBtn = document.getElementById("alignNavButton");
const uploadBtn = document.getElementById("uploadNavButton");
const activeBtnClassList = ["nav-link", "active"]
const inactiveBtnClassList = ["nav-link", "disabled"]
const activeTabClassList = ["tab-pane", "fade", "show", "active"]
const inactiveTabClassList = ["tab-pane", "fade"]
const answerPopup = document.getElementById("answerPopup")
const questionName = document.getElementById("questionName")
const multipleToggle = document.getElementById("multipleToggle")

let alignedImg = ''
let isTemplateDefined = false
let scaleFactor = 1
let boundingPts = []
const creationSteps = {
    UPLOAD: "upload",
    ALIGN: "align",
    DEFINE: "define",
    SAVE: "save"
}
// create template detection
imgForm ? creating = true : creating = false
// image upload events if on create template page creating template
if (creating) {
    // we are on the create template page
    imgFormUploadBtn.addEventListener("click", async (e) => {
        // prevent form post request
        e.preventDefault();
        // add image to canvas
        let preAlignImgSrc = URL.createObjectURL(imgUploadInput.files[0])
        prepareAlignTab(preAlignImgSrc);
        // save image upload field to add as hidden field to new question definition form
        boundingPts = await getBoundingPts(imgForm);
        let alignTab = new bootstrap.Tab(alignNavBtn);
        alignTab.show();
        addAlignSpots(boundingPts)
        deactivateTab(creationSteps.UPLOAD)
        activateTab(creationSteps.ALIGN)
    })
} else {
    // we are on the edit template page
};

function addAlignSpots(pts = []) {
    console.log("scaleFactor for spots:", scaleFactor);
    pts.forEach((pt) => {
        let radius = 10
        let x = scaleFactor * pt[0]
        let y = scaleFactor * pt[1]

        addCircle(alignCanvas, {
            top: y,
            left: x,
            radius: radius,
            fill: 'rgba(255,0,0, 0.5)'
        })
    }
    )
}

function scaleAlignSpots(canvas, scaleFactor) {
    canvas._objects.map((obj) => {
        let { top, left, radius } = obj
        scaledTop = (top * scaleFactor) - radius
        scaledLeft = (left * scaleFactor) - radius
        obj.top = scaledTop
        obj.left = scaledLeft

    })

}



// ajax form post to find bounding box in template
async function getBoundingPts(form) {
    let formData = new FormData(form);
    res = await fetch("/upload-template", { method: "POST", body: formData });
    let { img, pts } = await res.json();
    return img, pts;
}

function prepareAlignTab(img) {
    alignNavBtn.addEventListener("shown.bs.tab", () => {
        prepareCanvas(alignCanvas, img)

    })
}


function prepareDefineTab(img) {
    defineNavBtn.addEventListener("shown.bs.tab", () => {
        prepareCanvas(defineCanvas, img)

    })
}

function getStepEl(creationStep) {
    let tabId = `nav-${creationStep}`
    let buttonId = `${creationStep}NavButton`
    let badgeId = `${creationStep}NavBadge`
    const tab = document.getElementById(tabId)
    const button = document.getElementById(buttonId)
    const badge = document.getElementById(badgeId)

    return { "tab": tab, "button": button, "badge": badge }
}

function activateTab(creationStep) {
    const { tab, button, badge } = getStepEl(creationStep)
    button.classList.remove("disabled")
    button.classList.add("active")
    tab.classList.add("show", "active")
    badge.classList.remove("bg-secondary")
    badge.classList.add("bg-warning", "text-dark")

}

function deactivateTab(creationStep) {
    const { tab, button, badge } = getStepEl(creationStep)
    button.classList.add("disabled")
    badge.classList.remove("bg-warning", "text-dark")
    badge.classList.add("bg-success")
}



let currentQuestion = 0
// list of questions to initialise obj when submitting spot data
let questions = {}
let questionMultiple = {}
let questionNumbers = []
let questionNames = {}

// hold alignpts data
let alignPts = []

window.addEventListener("resize", resizeCanvas)

// ajax form post to align template image
async function alignImg(alignPts, imgForm) {
    alignImgForm = new FormData(imgForm)
    alignImgForm.append("pts", JSON.stringify(alignPts))
    alignImgForm.append("scale", JSON.stringify(scaleFactor))
    res = await fetch("/align-template", { method: "POST", body: alignImgForm });
    let { img } = await res.json();
    return img;
}

function setCurrentQuestion(qnNumber) {
    // globally set current question  
    currentQuestion = qnNumber
    const badge = document.createElement("span")
    badge.classList.add("position-absolute", "top-0", "start-100", "translate-middle",
        "badge", "rounded-pill", "bg-danger")
    badge.innerText = qnNumber
}


function addImageToCanvas(canvas, imgData) {
    const bgImage = new fabric.Image.fromURL(imgData, (img) => {

        // get image aspect ratio to decide if scale to height or width
        imgAR = img.width / img.height
        if (imgAR >= 1) {
            // scale image width to canvas
            scaleFactor = canvas.width / img.width

        } else {
            // // scale image height to canvas
            scaleFactor = canvas.height / img.height
        }
        img.set({ scaleY: scaleFactor, scaleX: scaleFactor })

        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas))
        console.log("img scaleFactor", scaleFactor);
        // move alignment circles
        scaleAlignSpots(canvas, scaleFactor)
    })


}
function prepareCanvas(canvas, imgData) {
    let canvasContainer = document.getElementById(`${canvas.lowerCanvasEl.id}Div`)
    let w = canvasContainer.offsetWidth
    resizeCanvas(canvas, imgData);
    addCanvasEventListeners(canvas)
}


// exportBtn.addEventListener('click', resizeCanvas, false);

function resizeCanvas(canvas, imgData) {
    let canvasName = canvas.lowerCanvasEl.id
    let canvasControls = document.getElementById(`${canvasName}Controls`)
    let canvasContainer = document.getElementById(`${canvas.lowerCanvasEl.id}Div`)
    canvas.setHeight(canvasContainer.offsetWidth * 0.6);
    canvas.setWidth(canvasContainer.offsetWidth);
    let newTop = canvasContainer.offsetTop + (canvasContainer.offsetHeight / 2) - (canvasControls.offsetHeight / 2)
    canvasControls.setAttribute("style", `left:${canvasContainer.offsetLeft}px;top:${newTop}px`)
    if (canvasName == "defineCanvas") {
        let qnControl = document.getElementById("defineCanvasQnControls")
        console.log(qnControl);
        qnControl.setAttribute("style", `left:${canvasContainer.offsetLeft + (canvasContainer.offsetWidth / 2) - qnControl.width}px;top:${canvasContainer.offsetTop + 5}px`)
    }
    addImageToCanvas(canvas, imgData);

    canvas.renderAll();
}


function addCanvasEventListeners(canvas) {
    let deleteAns = document.getElementById("deletePopup")
    let saveAns = document.getElementById("submitPopup")

    let canvasName = canvas.lowerCanvasEl.id
    let submitAlignBtn = document.getElementById(`alignCanvasSubmit`)
    let submitDefineBtn = document.getElementById(`defineCanvasSubmit`)
    let zoomInBtn = document.getElementById(`${canvasName}ZoomIn`)
    let zoomOutBtn = document.getElementById(`${canvasName}ZoomOut`)
    let panModeBtn = document.getElementById(`${canvasName}PanMode`)
    if (canvasName == "defineCanvas" | canvasName == "editCanvas") {
        const addCircleBtn = document.getElementById("addCircle");
        const addQn = document.getElementById("addQn");
        addCircleBtn.addEventListener("click", () => {
            circle = addCircle(canvas)
            circle.question = currentQuestion
            // questions[currentQuestion].push(circle)
        })
        // add new question to list 
        addQn.addEventListener("click", addQuestion)

    }
    if (canvasName == "alignCanvas") {

        submitAlignBtn.addEventListener("click", async (e) => {
            console.log("sending align");
            alignCanvas._objects.forEach(pt => {
                let { left, top } = pt
                alignPts.push([left, top])
            })

            alignedImg = await alignImg(alignPts, imgForm)
            alignedImg = `data:image/jpeg;base64, ${alignedImg}`
            prepareDefineTab(alignedImg);

            let defineTab = new bootstrap.Tab(defineNavBtn);
            defineTab.show();

            deactivateTab(creationSteps.ALIGN)
            activateTab(creationSteps.DEFINE)

        })
    }

    submitDefineBtn.addEventListener("click", async (e) => {
        console.log(e, "sending template", isTemplateDefined);
        if (!isTemplateDefined) {
            isTemplateDefined = true
            submitDefineBtn.classList.add("disabled")
            const publicToggle = document.getElementById("publicToggle")
            const templateName = document.getElementById("templateName")
            // defineData = {}
            // // create empty array for each question
            // questionNumbers.forEach((qn) => {
            //     defineData[qn] = []
            // })
            questions['public'] = publicToggle.checked;
            questions['templateName'] = templateName.value
            questions['uploadedImg'] = alignedImg
            defineCanvas._objects.map((obj) => {
                let { top, left, question, value } = obj
                // defineData[question].push({ top, left, value })
                ansCoords = Math.round(left) + ',' + Math.round(top)
                ansVal = value
                answer = { 'answer_coords': ansCoords, "answer_val": ansVal }
                questions[question]['answers'].push(answer)

            })
            let res = await fetch("/define-template/new", {
                method: "POST",
                headers: {
                    'X-CSRF-Token': csrf_token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(questions)
            });
            let template = await res.json();
            console.log(template);

            // add logic to enable save tab and redirect to view page?
            let saveTab = new bootstrap.Tab(saveNavBtn);
            saveTab.show();
            deactivateTab(creationSteps.DEFINE)
            activateTab(creationSteps.SAVE)
        }
    })

    saveAns.addEventListener("click", () => {
        const ansVal = document.getElementById("answerValue")
        canvas.getActiveObject().value = ansVal.value
    })
    deleteAns.addEventListener("click", (e) => {
        console.log("deleting:", e.target);
        canvas.remove(canvas.getActiveObject())
        answerPopup.hidden = true
    })

    panModeBtn.status = false
    panModeBtn.addEventListener("click", (e) => {
        if (!panModeBtn.status) {
            panModeBtn.classList.toggle("panModeOn")
            panModeBtn.classList.remove("btn-dark")
            panModeBtn.classList.add("btn-warning")
            panModeBtn.status = true;
            canvas.isSelection = false
        } else {
            panModeBtn.classList.toggle("panModeOn")
            panModeBtn.classList.add("btn-dark")
            panModeBtn.classList.remove("btn-warning")
            panModeBtn.status = false;
            canvas.isSelection = true

        }
    }
    )

    canvas.on('mouse:down', function (opt) {
        let evt = opt.e;
        if (panModeBtn.status) {
            this.isDragging = true;
            this.selection = false;
            this.lastPosX = evt.clientX;
            this.lastPosY = evt.clientY;
        }
        if (opt.target == null) {
            answerPopup.hidden = true;
        }
    });

    canvas.on('mouse:move', function (opt) {
        if (this.isDragging) {
            let e = opt.e;
            let vpt = this.viewportTransform;
            // move viewport by amount moved since last move      
            vpt[4] += e.clientX - this.lastPosX;
            vpt[5] += e.clientY - this.lastPosY;
            this.requestRenderAll();
            this.lastPosX = e.clientX;
            this.lastPosY = e.clientY;
        }
    });
    canvas.on('mouse:up', function (opt) {
        // on mouse up we want to recalculate new interaction
        // for all objects, so we call setViewportTransform
        this.setViewportTransform(this.viewportTransform);
        this.isDragging = false;
        this.selection = true;
    });



    // add zoom in/out func
    zoomOutBtn.addEventListener("click", () => {
        canvas.setZoom(canvas.getZoom() * 0.9)
    })

    zoomInBtn.addEventListener("click", () => {
        canvas.setZoom(canvas.getZoom() * 1.1)
    })

}

function addCircle(canvas, {
    radius = 10,
    top = 200,
    left = 200,
    strokeWidth = 3,
    stroke = 'rgba(255,0,0, 0.5)',
    fill = 'rgba(0,0,0, 0.5)',
} = {}) {
    opts = {
        radius: radius,
        top: top,
        left: left,
        strokeWidth: strokeWidth,
        stroke: stroke,
        fill: fill
    }
    const circle = new fabric.Circle(opts);
    canvas.add(circle);
    circle.value = `ans${canvas._objects.length}`
    circle.hasControls = false;
    circle.on("selected", (e) => {
        console.log(e.target, circle);
        showPopup(circle, canvas)
    })
    circle.on("moving", () => {
        answerPopup.hidden = true;
    })
    return circle
}

function addQuestion() {
    let canvasControlsList = document.getElementById("defineCanvasControlsList")
    let newQn = document.createElement("li")
    let link = document.createElement("a")
    link.setAttribute("href", '#')
    let span = document.createElement("span")
    span.classList.add("badge", "bg-secondary", "m-1", "questionSelect")
    link.appendChild(span)
    newQn.appendChild(link)
    span.innerText = canvasControlsList.childElementCount

    newQn.addEventListener("click", () => {
        activateQn(newQn)
    })

    canvasControlsList.appendChild(newQn)
    questionNumbers.push(newQn.innerText)
    // instantiate question_id obj in questions obj 
    questions[newQn.innerText] = {}
    questions[newQn.innerText]['multiple'] = true
    questions[newQn.innerText]['answers'] = []

    return newQn
}

function activateQn(questionNum) {
    let qnControl = document.getElementById("defineCanvasQnControls")
    let canvasControlsList = document.getElementById("defineCanvasControlsList")

    canvasControlsList.querySelectorAll(".bg-danger").forEach(span => {
        span.classList.add("bg-secondary")
        span.classList.remove("bg-danger")
    })
    questionNum.querySelector("span").classList.toggle("bg-danger")
    questionNum.querySelector("span").classList.toggle("bg-secondary")
    setCurrentQuestion(questionNum.innerText)
    multipleToggle.checked = questions[questionNum.innerText]['multiple']
    qnControl.getElementsByClassName("btn")[0].innerText = `Currently defining Question ${currentQuestion}`
    questionName.value = questionNames[questionNum.innerText]
}

function showPopup(circle, canvas) {
    // move popup;
    answerPopup.hidden = false
    const { top, left, question, value, width, strokeWidth } = circle
    const ansVal = document.getElementById("answerValue")
    const qnNum = document.getElementById("questionPopup")
    qnNum.innerText = `Question ${question}`
    answerPopup.style.left = (2 + width + strokeWidth + left + canvas._offset.left) + 'px'
    answerPopup.style.top = (top + canvas._offset.top) + 'px'
    ansVal.value = value
}

multipleToggle.addEventListener("change", setMultipleFlag)
questionName.addEventListener("change", setQuestionName)

function setMultipleFlag() {
    questions[currentQuestion]['multiple'] = multipleToggle.checked;
}
function setQuestionName() {
    questionNames[currentQuestion] = questionName.value;
}


activateQn(addQuestion())