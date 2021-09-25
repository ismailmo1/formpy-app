const form = document.getElementById("uploadImgForm");
const container = document.getElementById("mainContainer");
// make spots public
let spots ={};

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("sending form");
  showLoading();
  spots = await findSpots(form);
  addSpotCount(spots["num_spots"]);
  addAssignButton();
  addImage(spots["img"]);
  addAssignForm(spots["coords"]);
});

function showLoading() {
  let formRow = document.getElementById("formRow");
  container.removeChild(formRow);
}

async function findSpots(form) {
  let formData = new FormData(form);
  res = await fetch("/find-spots", { method: "POST", body: formData });
  spots = await res.json();
  return spots;
}

function addImage(imgData) {
  let imgContainer = document.createElement("img");
  imgContainer.id = "templateImg";
  imgContainer.classList.add("img-fluid");
  imgContainer.src = `data:image/png;base64,${imgData}`;
  container.appendChild(imgContainer);
}

function addSpotCount(numSpots) {
  spotCounter = document.createElement("h3");
  spotCounter.classList.add("mb-2");
  spotCounter.innerHTML = `${numSpots} spots detected`;
  container.appendChild(spotCounter);
}

function addAssignButton() {
  button = document.createElement("a");
  button.classList.add("btn", "btn-primary", "mb-2");
  button.setAttribute("href", "#assignqns");
  button.innerHTML = "Assign Questions";
  container.appendChild(button);
}

function addAssignForm(coords) {
  // parent form element- contains all questiondivs
  let questionForm = document.createElement("form")
  questionForm.id = "templateDefForm"
  questionForm.setAttribute("method", "POST")
  questionForm.setAttribute("action", "/define-template")
  questionForm.setAttribute("name", "templateForm")

  let submitBtn = document.createElement("button");
  submitBtn.classList.add("btn", "btn-success");
  submitBtn.innerHTML="Submit Template";
  questionForm.appendChild(submitBtn)
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
    questionForm.insertBefore(questionDiv, submitBtn)
    container.appendChild(questionForm)
    
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

function createAnswerGroup(coords){
  let answerGroup=document.createElement("div");
  answerGroup.classList.add("answerGroup","row", "my-2");
  answerGroup.innerHTML = `<h6>Answer</h6>`;
  
  let answerVal = document.createElement("input");
  answerVal.classList.add("col-3");
  let answerCoordSelect = document.createElement("select");
  
  // wrapper for answer coord select
  let answerCoordDiv = document.createElement("div");
  answerCoordDiv.classList.add("col-2");

  coords.forEach((coord)=>{
    let answerCoord = document.createElement("option")
    answerCoord.setAttribute("value", coord)
    answerCoord.innerHTML = coord
    answerCoordSelect.appendChild(answerCoord)
  })
  answerCoordDiv.appendChild(answerCoordSelect)
  answerGroup.appendChild(answerCoordDiv)
  answerGroup.appendChild(answerVal)
  return answerGroup  
}

function createQuestionGroup(questionNum){
 
  let questionGroup=document.createElement("div");
  questionGroup.classList.add("questionGroup", "mt-4");
  questionGroup.innerHTML = `<h5>Question No. ${questionNum}</h5>`;
  
  // create add answer button
  let addAnsBtn = document.createElement("button");
  addAnsBtn.innerHTML = "Add Answer";
  addAnsBtn.classList.add("btn", "btn-primary");
  addAnsBtn.addEventListener("click", (e)=>{
    e.preventDefault();
    answerGroup = createAnswerGroup(spots["coords"]);
    let currQuestionGroup = e.target.parentElement;
    currQuestionGroup.appendChild(answerGroup);  
  })

  questionGroup.appendChild(addAnsBtn);
  return questionGroup;
}