document.addEventListener('DOMContentLoaded', function() {
    const expenseRadio = document.getElementById('expense');
    const incomeRadio = document.getElementById('income');
    const categories = document.getElementById('categories');
    const expenseOptions = document.getElementById('expenseOptions');
    const incomeOptions = document.getElementById('incomeOptions');

    function updateCategories(optionsSelect) {
        categories.innerHTML = '';
        for (let option of optionsSelect.options) {
            categories.appendChild(option.cloneNode(true));
        }
    }

    expenseRadio.addEventListener('change', function() {
        if (expenseRadio.checked) {
            updateCategories(expenseOptions);
        }
    });

    incomeRadio.addEventListener('change', function() {
        if (incomeRadio.checked) {
            updateCategories(incomeOptions);
        }
    });
});