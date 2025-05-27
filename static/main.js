document.addEventListener('DOMContentLoaded', function() {
    loadTheme()
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

function toggleTheme() {
    const body = document.body;
    const themeToggle = document.querySelector('.theme-toggle');
    
    if (body.getAttribute('data-theme') === 'light') {
        body.removeAttribute('data-theme');
        themeToggle.textContent = '🌙';
        localStorage.setItem('theme', 'dark');
    } else {
        body.setAttribute('data-theme', 'light');
        themeToggle.textContent = '☀️';
        localStorage.setItem('theme', 'light');
    }
}

// Load saved theme
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const themeToggle = document.querySelector('.theme-toggle');
    
    if (savedTheme === 'light') {
        document.body.setAttribute('data-theme', 'light');
        themeToggle.textContent = '☀️';
    } else {
        themeToggle.textContent = '🌙';
    }
}

// Show notification
function showNotification(message, isSuccess = true) {
    const notification = document.getElementById('notification');
    const messageElement = notification.querySelector('.notification-message');
    const iconElement = notification.querySelector('.notification-icon');
    
    messageElement.textContent = message;
    iconElement.textContent = isSuccess ? '✓' : '✗';
    
    if (isSuccess) {
        notification.classList.remove('error');
    } else {
        notification.classList.add('error');
    }
    
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}