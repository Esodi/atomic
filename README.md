
---

# Atomic Competitions

Atomic Competitions is a web application that allows users to create, join, and manage competitions. Users can submit projects for competitions and view submissions if they are the competition creator.

## Features

- User authentication (signup, login, logout)
- Create and manage competitions
- Join competitions
- Submit projects for competitions
- View submissions for competitions (only for competition creators)
- Download project submissions

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Login
- Flask-Migrate
- Jinja2
- HTML/CSS

## Installation

### Prerequisites

- Python 3.6+
- Virtualenv

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/esodi/atomic.git
    cd atomic
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. **Run the application:**

    ```bash
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Configuration

The application configuration is stored in the `config.py` file. You can set the following configurations:

- `SQLALCHEMY_DATABASE_URI`: The database URI
- `SECRET_KEY`: The secret key for session management
- `ALLOWED_EXTENSIONS`: Allowed file extensions for project submissions

## Project Structure

```
atomic-competitions/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   └── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dash.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── submit_project.html
│   │   ├── view_submissions.html
│   │   └── competitions_list.html
│   └── static/
│       └── styles.css
│
├── migrations/
│
├── config.py
├── requirements.txt
└── run.py
```

## Usage

### User Authentication

- **Signup**: Users can sign up by providing a username, email, and password.
- **Login**: Users can log in using their username and password.
- **Logout**: Users can log out from their account.

### Competitions

- **Create Competition**: Authenticated users can create a new competition by providing a name, description, details, and fee.
- **Join Competition**: Authenticated users can join a competition.
- **Submit Project**: Users can submit a project for a competition they have joined. The submission includes a project description and a file.
- **View Submissions**: Competition creators can view all submissions for their competitions.
- **Download Submission**: Competition creators can download project submissions.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes ([`git commit -m 'Add some feature'`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fegao%2FDesktop%2Fatomic%2Fapp%2Froutes%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A228%2C%22character%22%3A27%7D%7D%5D%2C%225a981019-9583-4bb6-8406-703d3f09fabc%22%5D "Go to definition"))
5. Push to the branch (`git push origin feature-branch`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or suggestions, please open an issue or contact the project maintainer at [gershommethod02@gmail.com].

---
