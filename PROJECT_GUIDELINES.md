# Project Documentation

This documentation provides best practices and guidelines for the Medical AI Assistant project. All documentation and code comments should be written in English to ensure consistency and accessibility for all contributors.

## Best Practices

- **Language:** Use English for all code, comments, documentation, and commit messages.
- **Structure:** Organize code into logical modules and folders (e.g., `backend/`, `frontend/`).
- **Virtual Environments:** Always use a virtual environment for Python dependencies. Do not install packages globally.
- **Requirements:** List all Python dependencies in `requirements.txt` and keep it updated.
- **Version Control:** Use `.gitignore` to exclude environment files, compiled code, and sensitive data.
- **API Design:** Follow RESTful principles for API endpoints. Use clear, descriptive names and HTTP methods.
- **Documentation:** Maintain up-to-date `README.md` files in the root and main subfolders. Add docstrings to all functions and classes.
- **Testing:** Write tests for critical functionality. Use a `tests/` folder if needed.
- **Security:** Never commit secrets or credentials. Use environment variables and `.env` files for sensitive data.
- **Code Style:** Follow PEP8 for Python code. Use linters and formatters (e.g., `black`, `flake8`).

## Getting Started

1. Clone the repository.
2. Create and activate a virtual environment in the `backend/` folder.
3. Install dependencies: `pip install -r requirements.txt`
4. Run the FastAPI server: `python -m uvicorn main:app --reload`
5. Access the API docs at `http://127.0.0.1:8000/docs`

## Contribution Guidelines

- Open issues for bugs or feature requests.
- Fork the repository and create pull requests for changes.
- Write clear commit messages in English.
- Review and test your code before submitting.

---

For any questions, please refer to this documentation or open an issue in the repository.
