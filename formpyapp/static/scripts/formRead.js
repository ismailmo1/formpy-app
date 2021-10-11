let readBtn = document.querySelector("#readFormBtn");
let formsUploadFrm = document.querySelector("form");
let container = document.querySelector("#mainContainer")
let imageModal = document.querySelector("#formImgModal")
let modalTitle = document.querySelector(".modal-title")
let modalBody = document.querySelector(".modal-body")
let formResults

// read button ajax call to read uploaded forms
readBtn.addEventListener("click", async (e)=>{
    e.preventDefault();
    forms = new FormData(formsUploadFrm);
    res = await fetch("/read", { method: "POST", body: forms });
    formResults = await res.json();

    // add hidden images to modal
    formResults['imgs'].forEach((imgData, i) =>{
        let img = document.createElement("img");
        // match image number to form num in table
        img.id = `form${i+1}Img`;
        img.hidden=true;
        img.classList.add("img-fluid");
        img.src = `data:image/png;base64,${imgData}`;
        modalBody.appendChild(img);
    })
    
    // add csv download button
    let csvDlBtn = document.createElement("a")
    csvDlBtn.classList.add("btn", "btn-success")
    csvDlBtn.addEventListener("click", (e)=>{download_table_as_csv("formResultsTable")})
    csvDlBtn.innerText = "Export as CSV"
    container.appendChild(csvDlBtn);
    
    // add results table
    let resultsTable = createResultsTable(formResults['answers']);
    container.appendChild(resultsTable);
})

imageModal.addEventListener("show.bs.modal", (e)=>{
    // Button that triggered the modal
  let button = e.relatedTarget
  // Extract info from data-bs-* attributes
  let form_num = button.getAttribute('data-bs-form-num')
  populateImageModal(form_num)
})

function createResultsTable(forms){
    // populate table headings with question_ids and loop through each form to add rows with values
    let tableDiv = document.createElement("div");
    let formResultsTable = document.createElement("table");
    let tableHeader = document.createElement("thead");
    let tableBody = document.createElement("tbody")
    // first header col is form name/enumeration
    let tableHdrRow = document.createElement("tr");
    let formHeaderCol = document.createElement("th");
    formHeaderCol.innerHTML = "Form # "
    tableHdrRow.appendChild(formHeaderCol);
    // second header col = img link
    let imgHeaderCol = document.createElement("th");
    imgHeaderCol.innerHTML = "Image"
    tableHdrRow.appendChild(imgHeaderCol);
    
    
    // create header col for each question id
    let firstForm = forms[0]
    Object.keys(firstForm).forEach(qn=>{
        let headerCol = document.createElement("th");
        headerCol.innerHTML = qn
        tableHdrRow.appendChild(headerCol)
    })
    // add header
    tableHeader.appendChild(tableHdrRow);    
    formResultsTable.appendChild(tableHeader)
    // iterate through form's questions

    let form_num = 0
    forms.forEach(form=>{
        form_num +=1
        addResultsRow(form, tableBody, form_num)
    })
    formResultsTable.appendChild(tableBody)
    tableDiv.classList.add("table-responsive")
    formResultsTable.classList.add("table")
    formResultsTable.id = "formResultsTable"
    
    
    tableDiv.appendChild(formResultsTable);
    return tableDiv
}

function addResultsRow(formResult, tableBody, form_num){
    // parse each form and return table row (tr)
    let tableRow = document.createElement("tr");
    // first col for form number 
    let formNumCol = document.createElement("td");
    formNumCol.innerText = form_num;
    tableRow.appendChild(formNumCol);

    // second col for image modal
    let imgCol = document.createElement("td")
    let modalBtn = document.createElement("button");
    modalBtn.classList.add("btn", "btn-link");
    modalBtn.innerHTML = "<i class='far fa-image'></i>";
    modalBtn.setAttribute("data-bs-toggle", "modal")
    modalBtn.setAttribute("data-bs-target", "#formImgModal")
    modalBtn.setAttribute("data-bs-form-num", form_num)

    modalBtn.setAttribute("type", "button")
    imgCol.appendChild(modalBtn);
    
    tableRow.appendChild(imgCol);

    // add column for each question in form
    Object.keys(formResult).forEach(qn=>{
        let tableCol = document.createElement("td");
        tableCol.innerText = formResult[qn]
        tableRow.appendChild(tableCol)
    })

    tableBody.appendChild(tableRow)
}

function populateImageModal(form_num){

    let formImg = document.querySelector(`#form${form_num}Img`);
    formImg.hidden=false;
    modalTitle.innerText = `Image for form #${form_num}`;
    // modalBody.innerHTML+= formResults["answers"]
    // TODO add table with detailed stats for form: answer filled % etc
}