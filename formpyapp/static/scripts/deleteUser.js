const deleteRadios = document.querySelectorAll('input[type="radio"')
const deleteBtn = document.querySelector("#deleteUserBtn")
deleteRadios.forEach(radio=>{
    radio.addEventListener("click", (e)=>{
        if(radio.value ==='none'){
            deleteBtn.value = 'Delete Account'
        }else{
            deleteBtn.value = 'Delete Account and Templates'
        }
    })})