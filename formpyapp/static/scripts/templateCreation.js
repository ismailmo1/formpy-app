const imgForm = document.getElementById("uploadImgForm");

const container = document.getElementById("mainContainer");
// make spots public
let spots ={};

// image upload events
imgForm.addEventListener("submit", async (e) => {
  // prevent form post request
  e.preventDefault();
  console.log("sending form");
  // save image upload field to add as hidden field to new question definition form
  const photoUpload = document.querySelector("#photoUpload");
  hideForm();
  const spots = await findSpots(imgForm);
  addSpotCount(spots["num_spots"]);
  addAssignButton();
  addImage(spots["img"]);
  addAssignForm(spots["coords"], photoUpload);
});

// remove original image upload form to find spots 
function hideForm() {
  let formRow = document.getElementById("formRow");
  container.removeChild(formRow);
}

// ajax form post to find spots on template
async function findSpots(form) {
  let formData = new FormData(form);
  res = await fetch("/find-spots", { method: "POST", body: formData });
  spots = await res.json();
  return spots;
}

// add image with spots annotated
function addImage(imgData) {
  let imgContainer = document.createElement("img");
  imgContainer.id = "templateImg";
  imgContainer.classList.add("img-fluid");
  imgContainer.src = `data:image/png;base64,${imgData}`;
  container.appendChild(imgContainer);
}


function addSpotCount(numSpots) {
  let spotCounter = document.createElement("h3");
  spotCounter.classList.add("mb-2");
  spotCounter.innerHTML = `${numSpots} spots detected`;
  container.appendChild(spotCounter);
}

function addAssignButton() {
  let button = document.createElement("a");
  button.classList.add("btn", "btn-primary", "mb-2");
  button.setAttribute("href", "#assignqns");
  button.innerHTML = "Assign Questions";
  container.appendChild(button);
}

function addAssignForm(coords, photoUpload) {  
  // parent form element- contains all questiondivs
  let templateForm = document.createElement("form")
  templateForm.id = "templateDefForm"
  templateForm.setAttribute("method", "POST")
  templateForm.setAttribute("action", "/define-template")
  templateForm.setAttribute("name", "templateForm")
  templateForm.setAttribute("enctype", "multipart/form-data")
  
  let templateNameInput = createTemplateName();
  // hide orig image and submit as part of define template form
  photoUpload.hidden = true;
  // add coords as hidden input to define template form
  let coordsInput = document.createElement("input");
  coordsInput.setAttribute("type", "text");
  coordsInput.setAttribute("name", "coords");
  let coords_vals = [];
// add brackets around each coord (otherwise just a long string of comma sep vals)
  coords.forEach((coord)=>{
    coords_vals.push(`[${coord}]`)});
  coordsInput.value = coords_vals;
  coordsInput.hidden=true;
  templateForm.appendChild(coordsInput);

  templateForm.appendChild(photoUpload);
  templateForm.appendChild(templateNameInput);
  
  let submitBtn = document.createElement("button");
  submitBtn.classList.add("btn", "btn-success");
  submitBtn.innerHTML="Submit Template";
  templateForm.appendChild(submitBtn)
  // assign number of questions 
    let questionDiv = document.createElement("div");
    questionDiv.classList.add("row")
    questionDiv.id = "assignqns"
    questionDiv.innerHTML = "<h1 class='mt-5'>How many questions are on this template?</h1>"
    
    let questionCountInput = document.createElement("input")
    questionCountInput.classList.add("col-3")
    questionCountInput.setAttribute("type", "number")
    questionCountInput.setAttribute("min", "1")
    questionCountInput.setAttribute("max", coords.length)
    

    questionDiv.appendChild(questionCountInput)


    templateForm.insertBefore(questionDiv, submitBtn)
    container.appendChild(templateForm)
    
// add or remove questions when questionCount changes
    questionCountInput.addEventListener("input", function(e){
      let questionGroups = document.querySelectorAll(".questionGroup")
      let numQuestions = questionGroups.length
      if (parseInt(this.value)>numQuestions) {
        // add question
        // keep adding questions until input value met
        for(let i = numQuestions; this.value > i; i++){
          let questionGroup = createQuestionGroup(i+1);
          questionDiv.appendChild(questionGroup)
        }
        
      }else{
        // keep removing questions until input value met
        for(let i = numQuestions; this.value < i; i--){
          console.log(this.value, i)
          questionDiv.removeChild(questionGroups[i-1])
        }
      }
    })
    
}

function createAnswerGroup(coords, questionId){
  let questionGroup = document.querySelector(`#${questionId}`);
  let ansNum = questionGroup.querySelectorAll(".answerGroup").length+1;
  let answerGroup=document.createElement("div");

  answerGroup.classList.add("answerGroup","row", "my-2");
  answerGroup.innerHTML = `<h6>Answer${ansNum}</h6>`;
  
  let answerVal = document.createElement("input");
  answerVal.classList.add("col-3");
  answerVal.name = `${questionId}-answer${ansNum}-value`
  let answerCoordSelect = document.createElement("select");
  answerCoordSelect.name = `${questionId}-answer${ansNum}-index`
  
  // wrapper for answer coord select
  let answerCoordDiv = document.createElement("div");
  answerCoordDiv.classList.add("col-2");

  // add all coords to dropdown 
  coords.forEach((coord)=>{
    let answerCoord = document.createElement("option")
    answerCoord.setAttribute("value", coord)
    answerCoord.innerHTML = `${coords.indexOf(coord)}: ${coord}`
    answerCoordSelect.appendChild(answerCoord)
  })
  answerCoordDiv.appendChild(answerCoordSelect)
  answerGroup.appendChild(answerCoordDiv)
  answerGroup.appendChild(answerVal)
  return answerGroup  
}

function createQuestionGroup(questionNum){
 
  let questionGroup=document.createElement("div");
  let questionGroupId = `question${questionNum}`
  questionGroup.classList.add("questionGroup", "mt-4");
  questionGroup.innerHTML = `<h5>Question No. ${questionNum}</h5>`;
  questionGroup.id = questionGroupId
  
  // create toggle swtich for multple qns
  let multipleFlagSwitchDiv = document.createElement("div")
  multipleFlagSwitchDiv.classList.add("form-check","form-switch")
  let multipleFlagSwitch = document.createElement("input")
  multipleFlagSwitch.setAttribute("type", "checkbox")
  multipleFlagSwitch.value ="True"
  // keep naming convention consistent with other form fields for easy parsing
  // i.e. delimit with - for qn-ans-inputType
  let multipleFlagSwitchName = `question${questionNum}-answerAll-multipleFlag`
  multipleFlagSwitch.name = multipleFlagSwitchName
  multipleFlagSwitch.id = multipleFlagSwitchName
  multipleFlagSwitch.classList.add("form-check-input")
  let switchLabel = document.createElement("label")
  switchLabel.innerHTML = "Multiple Answers"
  switchLabel.setAttribute("for", multipleFlagSwitchName)
  switchLabel.classList.add("form-check-label")
  multipleFlagSwitchDiv.appendChild(switchLabel);
  multipleFlagSwitchDiv.appendChild(multipleFlagSwitch);

  questionGroup.appendChild(multipleFlagSwitchDiv);

  // create add answer button
  let addAnsBtn = document.createElement("button");
  addAnsBtn.innerHTML = "Add Answer";
  addAnsBtn.classList.add("btn", "btn-primary", "col-3");  
  addAnsBtn.addEventListener("click", (e)=>{
    e.preventDefault();
    // create answer group with sequential naming convention i.e. question1-answer1/2/3...
    answerGroup = createAnswerGroup(spots["coords"], questionGroupId);
    let currQuestionGroup = e.target.parentElement;
    currQuestionGroup.appendChild(answerGroup);  
  })

  questionGroup.appendChild(addAnsBtn);
  return questionGroup;
}

function createTemplateName(){
  let questionNameDiv = document.createElement("div");
  questionNameDiv.classList.add("row")
  questionNameDiv.id = "questionName"
  questionNameDiv.innerHTML = "<h3 class='mt-5'>Give your template a name:</h1>"
  
  let questionNameInput = document.createElement("input")
  questionNameInput.classList.add("col-3")
  questionNameInput.name="templateName"
  questionNameDiv.appendChild(questionNameInput)

  return questionNameDiv;

}