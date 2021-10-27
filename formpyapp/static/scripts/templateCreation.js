const imgForm = document.getElementById("uploadImgForm");

const container = document.getElementById("mainContainer");
// make spots public
let spots ={};

// image upload events if img uploaded
if(imgForm){
  // we are on the create template page
imgForm.addEventListener("submit", async (e) => {
  // prevent form post request
  e.preventDefault();
  // save image upload field to add as hidden field to new question definition form
  const photoUpload = document.querySelector("#photoUpload");
  hideForm();
  const spots = await findSpots(imgForm);
  addSpotCount(spots["num_spots"]);
  addAssignButton();
  addImage(spots["img"]);
  addAssignForm(spots["coords"], photoUpload);
})}else{
  // we are on the edit template page
  spots["coords"] = [];
  options = document.querySelector("select").querySelectorAll("option");
  [...options].map((opt)=>{spots["coords"].push(opt.value)})
  // need to assign event listeners to existing elements
  // find existing question number input
  let questionCountInput = document.querySelector("#questionCountInput")
  // add new badge when question created
  questionCountInput.addEventListener("input", (e)=>{questionCountEvent(e,badge=true)})
  // loop through all answers group add answer btns and assign event listeners
  let ansBtns = document.querySelectorAll(".addAnsBtn")
  ansBtns.forEach(btn=>{
    // add badge to ansBtnEvent
    btn.addEventListener("click", (e)=>{ansBtnEvent(e, badge=true)});
})
};

// remove original image upload form to find spots 
function hideForm() {
  let formRow = document.getElementById("formRow");
  container.removeChild(formRow);
}

// ajax form post to find spots on template
async function findSpots(form) {
  let formData = new FormData(form);
  console.log(formData)
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
  // add csrf token
  let csrfInput = document.createElement("input")
  csrfInput.type = "hidden"
  csrfInput.name = "csrf_token" 
  csrfInput.value= csrf_token

  let templateNameInput = createTemplateName();
  //add toggle to set template public/private
  let templatePublicToggle = createPublicToggle();
  // hide orig image but keep in form to submit part of define template form
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
  
  templateForm.appendChild(csrfInput);
  templateForm.appendChild(photoUpload);
  templateForm.appendChild(templateNameInput);
  templateForm.appendChild(templatePublicToggle);


  
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
    questionCountInput.id= 'questionCountInput'

    

    questionDiv.appendChild(questionCountInput)


    templateForm.insertBefore(questionDiv, submitBtn)
    container.appendChild(templateForm)
    
// add or remove questions when questionCount changes
    questionCountInput.addEventListener("input", questionCountEvent)
    
}

function createPublicToggle(){
    // create toggle switch for multple qns
    let publicToggleDiv = document.createElement("span")
    publicToggleDiv.classList.add("col-2","form-check","form-switch")
    let publicToggle = document.createElement("input")
    publicToggle.setAttribute("type", "checkbox")
    publicToggle.value ="True"
    // keep naming convention consistent with other form fields for easy parsing
    // i.e. delimit with - for qn-ans-inputType
    let publicToggleName = `public`
    publicToggle.name = publicToggleName
    publicToggle.id = publicToggleName
    publicToggle.classList.add("form-check-input")
    publicToggle.checked=true;
    let toggleLabel = document.createElement("label")
    toggleLabel.innerHTML = "Public"
    toggleLabel.setAttribute("for", publicToggleName)
    toggleLabel.classList.add("form-check-label")
    publicToggleDiv.appendChild(toggleLabel);
    publicToggleDiv.appendChild(publicToggle);
  
  return publicToggleDiv    
}

function questionCountEvent(e, badge){
  let questionGroups = document.querySelectorAll(".questionGroup")
  let numQuestions = questionGroups.length
  let questionDiv = document.querySelector("#assignqns")
  let qnCountinput = e.target.value
  if (parseInt(qnCountinput)>numQuestions) {
    // add question
    // keep adding questions until input value met
    for(let i = numQuestions; qnCountinput > i; i++){
      let questionGroup = createQuestionGroup(i+1, badge);
      questionDiv.appendChild(questionGroup)
    }
    
  }else{
    // keep removing questions until input value met
    for(let i = numQuestions; qnCountinput < i; i--){
      console.log(qnCountinput, i)
      questionDiv.removeChild(questionGroups[i-1])
    }
  }
}

function createAnswerGroup(coords, questionId, badge=false){
  let questionGroup = document.querySelector(`#${questionId}`);
  let ansNum = questionGroup.querySelectorAll(".answerGroup").length+1;
  let answerGroup=document.createElement("div");

  answerGroup.classList.add("answerGroup","row", "my-2");
  answerGroup.innerHTML = `<h6>Answer${ansNum}</h6>`;
  // add new indicator if badge is true i.e. on edit template to differentiate new/old ans
  if(badge){
    answerGroup.innerHTML = `<h6>Answer${ansNum}  <span class='mx-2 badge bg-success rounded-pill'>New</span></h6>`;
  }
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

function createQuestionGroup(questionNum, badge=false){
 
  let questionGroup=document.createElement("div");
  let questionGroupId = `question${questionNum}`
  questionGroup.classList.add("questionGroup", "mt-4");
  questionGroup.innerHTML = `<h5>Question No. ${questionNum}</h5>`;
  if(badge){
    questionGroup.innerHTML = `<h5>Question No. ${questionNum}  <span class='mx-2 badge bg-success rounded-pill'>New</span></h5>`;
  }
  questionGroup.id = questionGroupId
  
  // create toggle switch for multple qns
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
  addAnsBtn.classList.add("btn", "btn-primary", "col-3", "addAnsBtn");  
  addAnsBtn.addEventListener("click", ansBtnEvent)

  questionGroup.appendChild(addAnsBtn);
  return questionGroup;
}

function ansBtnEvent(e, badge){
  e.preventDefault();
  // create answer group with sequential naming convention i.e. question1-answer1/2/3...
  answerGroup = createAnswerGroup(spots["coords"], e.target.parentElement.id, badge=badge);
  let currQuestionGroup = e.target.parentElement;
  currQuestionGroup.appendChild(answerGroup);  
};

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

