# Personal Finance App

![Personal Finance App Screenshot](Images/Light%20Mode.png)

> **Track your expenses and incomes with a modern, responsive, and easy-to-use web application.**

---

## ✨ Overview

The **Personal Finance App** is a web-based application designed to help users manage their finances by tracking expenses and incomes. With a clean UI, dark/light theme toggle, and powerful filtering, you can easily monitor your financial health and keep your spending in check.

- [Personal Finance](Personal-Finance-App.onrender.com)

---

## 🚀 Features

- **Add Transactions:** Log both expenses and incomes with categories, amounts, and descriptions.
- **Current Balance:** Instantly see your up-to-date balance.
- **Transaction History:** View all your past transactions in a scrollable, filterable list.
- **Filter & Search:** Filter transactions by type, category, or date.
- **Delete Transactions:** Remove unwanted entries with a single click.
- **Responsive Design:** Works beautifully on desktop and mobile.
- **Dark/Light Theme:** Toggle between dark and light modes for comfortable viewing.

---

## 🛠️ Technologies Used

- **Python 3**: Core programming language.
- **Flask**: Lightweight web framework for backend and routing.
- **SQLite**: Embedded database for storing transactions.
- **HTML5 & Jinja2**: For templating and dynamic content rendering.
- **CSS3**: Custom, modern, and responsive styling.
- **JavaScript**: For dynamic UI interactions (category switching, theme toggle).
- **Bootstrap Icons/Emojis**: For a visually appealing interface.

---

## 📁 Project Structure

```
.
├── db.py                # Database logic (CRUD, filtering, etc.)
├── finance.db           # SQLite database file
├── main.py              # Flask application (routes, logic)
├── static/
│   ├── main.js          # JavaScript for UI interactivity
│   └── style.css        # Custom CSS styles
├── templates/
│   └── index.html       # Main HTML template (Jinja2)
└── README.md            # Project documentation
```

---

## 📝 How It Works

### 1. **Database Layer ([db.py](db.py))**

- Handles all database operations using SQLite.
- Functions for creating tables, adding, deleting, fetching, and filtering transactions.
- Calculates the current balance based on all entries.

### 2. **Backend ([main.py](main.py))**

- Built with Flask.
- Handles routes:
  - `/` : Home page, add transactions, show history.
  - `/filter` : Filter transactions by type, category, or date.
  - `/delete/<id>` : Delete a transaction.
- Passes data to the frontend using Jinja2 templates.

### 3. **Frontend ([templates/index.html](templates/index.html))**

- Responsive layout with two main sections:
  - **Left:** Add new transactions, view balance.
  - **Right:** Transaction history, filters.
- Uses Jinja2 for dynamic content (categories, history, etc.).

### 4. **Styling ([static/style.css](static/style.css))**

- Modern, clean, and responsive design.
- Dark and light themes with smooth transitions.
- Custom scrollbars, buttons, and form elements.

### 5. **Interactivity ([static/main.js](static/main.js))**

- Dynamic category selection based on transaction type.
- Filter options update automatically.
- Theme toggle with local storage persistence.

---

## 🖥️ Screenshots


| Dark Theme | Light Theme |
|:----------:|:-----------:|
| ![Dark](Images/Dark%20Mode.png) | ![Light](Images/Light%20Mode.png) |

---

## ⚙️ Getting Started

### 1. **Clone the Repository**

```sh
git clone https://github.com/Thunderer9506/Personal-Finance-App.git
cd personal-finance-app
```

### 2. **Set Up Virtual Environment**

```sh
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. **Install Dependencies**

```sh
pip install flask
```

### 4. **Initialize the Database**

- The database is created automatically on first run.
- To manually create the table, you can uncomment and run `createTable()` in [db.py](db.py).

### 5. **Run the Application**

```sh
python main.py
```

- Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## 🧩 Customization

- **Categories:** Edit `expenseCategory` and `incomeCategory` in [main.py](main.py) to add/remove categories.
- **Styling:** Modify [static/style.css](static/style.css) for custom themes or layouts.
- **Database:** Extend [db.py](db.py) for more advanced analytics or export features.

---

## 📝 Credits

- Built with [Flask](https://flask.palletsprojects.com/) and [SQLitecloud](https://www.sqlitecloud.org/).
- UI inspired by modern finance dashboards.

---


> **Made with ❤️ for personal finance management.**
