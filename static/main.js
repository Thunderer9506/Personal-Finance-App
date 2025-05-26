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

    // Filter type/category dynamic update
    const filterType = document.getElementById('filterType');
    const filterCategories = document.getElementById('filterCategories');
    const filterExpenseOptions = document.getElementById('filterExpenseOptions');
    const filterIncomeOptions = document.getElementById('filterIncomeOptions');

    function updateFilterCategories(optionsSelect) {
        filterCategories.innerHTML = '';
        for (let option of optionsSelect.options) {
            filterCategories.appendChild(option.cloneNode(true));
        }
    }

    filterType.addEventListener('change', function() {
        if (filterType.value === "Expense") {
            updateFilterCategories(filterExpenseOptions);
        } else if (filterType.value === "Income") {
            updateFilterCategories(filterIncomeOptions);
        }
    });

    // Initialize filter categories on page load
    if (filterType.value === "Expense") {
        updateFilterCategories(filterExpenseOptions);
    } else if (filterType.value === "Income") {
        updateFilterCategories(filterIncomeOptions);
    }
});