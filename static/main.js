const expenseRadio = document.getElementById('expense');
const incomeRadio = document.getElementById('income');
expenseRadio.addEventListener('change',() => {
    if(expenseRadio.checked){
        document.getElementById('incomeCategories').style.display = "none"
        document.getElementById('expenseCategories').style.display = "inline"
    }
})
incomeRadio.addEventListener('change',() => {
    if(incomeRadio.checked){
        document.getElementById('incomeCategories').style.display = "inline"
        document.getElementById('expenseCategories').style.display = "none"
    }
})