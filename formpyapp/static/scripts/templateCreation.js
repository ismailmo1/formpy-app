const form = document.getElementById("uploadImgForm");
const container = document.getElementById("mainContainer");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("sending form");
  showLoading();
  let spots = await findSpots(form);
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
    questionDiv = document.createElement("div");
    questionDiv.classList.add("row")
    questionDiv.id = "assignqns"
    questionDiv.innerHTML = "<h1 class='mt-5'>How many questions are on this template?</h1>"
    
    questionAssignments = document.createElement("input")
    questionAssignments.classList.add("col-3")
    questionAssignments.setAttribute("type", "number")
    questionAssignments.setAttribute("min", "1")
    questionAssignments.setAttribute("max", coords.length)
    
    questionForm = document.createElement("form")

    questionDiv.appendChild(questionAssignments)
    questionDiv.appendChild(questionForm)
    container.appendChild(questionDiv)
    


    questionAssignments.addEventListener("input", function(e){
      questionGroups = document.querySelectorAll(".questionGroup")
      if (parseInt(this.value)>questionGroups.length) {
        // add question
        console.log("adding")
        questionGroup=document.createElement("div")
        questionGroup.classList.add("questionGroup", "mt-4")
        questionGroup.innerHTML = `<h5>Question No. ${this.value}</h5>`
        
        answerGroup=document.createElement("div")
        answerGroup.classList.add("answerGroup","row")
        answerGroup.innerHTML = `<h6>Answer</h6>`
        
        answerVal = document.createElement("input")
        answerCoords = document.createElement("select")
        coords.forEach((coord)=>{
          answerCoord = document.createElement("option")
          answerCoord.setAttribute("value", coord)
          answerCoord.innerHTML = coord
          answerCoords.appendChild(answerCoord)
        })
        answerGroup.appendChild(answerVal)
        answerGroup.appendChild(answerCoords)

        questionGroup.appendChild(answerGroup)
        questionDiv.appendChild(questionGroup)
        
      }else{
        // remove question
        console.log("removing")
        questionDiv.removeChild(questionGroups[questionGroups.length-1])
      }
    })
    
}

questionGroup = document.createElement("div")
questionGroup.classList.add("questionGroup", "row")
//create answer inputs : value and location (x,y)
coordSelect = document.createElement("select")

