const saveAsBtn = document.querySelector("#saveCopy");
const editForm = document.querySelector("#templateDefForm");

saveAsBtn.addEventListener("click", (e)=>{
    e.preventDefault()
    editForm.action = '/define-template/copy'
    let currTemplateId = document.createElement("input")
    currTemplateId.name = 'currTempId'
    currTemplateId.value = tempId
    currTemplateId.hidden = true
    editForm.appendChild(currTemplateId)
    editForm.submit()
    
})