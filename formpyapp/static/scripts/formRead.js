let readBtn = document.querySelector("#readFormBtn");
let formsUploadFrm = document.querySelector("form");
let container = document.querySelector("#mainContainer")

readBtn.addEventListener("click", async (e)=>{
    e.preventDefault();
    forms = new FormData(formsUploadFrm);
    res = await fetch("/read", { method: "POST", body: forms });
    markedImgs = await res.json();
    markedImgs['imgs'].forEach(imgData=>{
        let img = document.createElement("img")
        img.classList.add("img-fluid");
        img.src = `data:image/png;base64,${imgData}`;
        container.appendChild(img)
    })
    let resultsTable = createResultsTable(markedImgs['answers'])

    container.appendChild(resultsTable)
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

    
    
    tableDiv.appendChild(formResultsTable);
    return tableDiv
}

function addResultsRow(formResult, tableBody, form_num){
    // parse each form and return table row (tr)
    let tableRow = document.createElement("tr");
    // add in row for form number
 
    let tableCol = document.createElement("td");
    tableCol.innerText = form_num
    tableRow.appendChild(tableCol)

    Object.keys(formResult).forEach(qn=>{
        let tableCol = document.createElement("td");
        tableCol.innerText = formResult[qn]
        tableRow.appendChild(tableCol)
    })
    tableBody.appendChild(tableRow)
}