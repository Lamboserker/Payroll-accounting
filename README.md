
# Payroll Accounting System

## Overview
The Payroll Accounting System is a comprehensive solution designed to manage and streamline payroll processes. It allows for employee data management, payroll calculation, and report generation. The system ensures compliance with tax regulations and automates the payroll process, making it efficient and error-free.

## Features
- **Employee Management:** Add, update, and delete employee records.
- **Payroll Calculation:** Automatic calculation of employee salaries, taxes, deductions, and bonuses.
- **Tax Compliance:** Tax tables for various regions to ensure up-to-date compliance.
- **User Management:** Admins and roots can create users, update profiles, and manage roles.
- **JWT Authentication:** Secure login and token-based authentication.
- **PDF Document Management:** Watches for incoming PDF files and processes them.

## Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** React.js, Tailwind CSS
- **Database:** MongoDB
- **Authentication:** JWT (JSON Web Tokens)
- **PDF Watcher:** Python script for handling incoming PDF files

### Install dependencies
Navigate to the project directory and install the dependencies.

For the backend:
```bash
cd server
pip install -r requirements.txt
```

For the frontend:
```bash
cd client
npm install
```

### Set up environment variables
Create a `.env` file in the backend root directory with the following variables:

```plaintext
DB_URI=mongodb://localhost:27017/payroll
JWT_SECRET_KEY=your-secret-key
```

### Run the project
To start the backend:
```bash
cd server
uvicorn main:app --reload
```

To start the frontend:
```bash
cd client
npm run dev
```

## API Endpoints

### Auth Routes
- **POST /auth/login**: Logs in and returns a JWT token.
- **POST /auth/register**: Registers a new user (admin or root required for creating admin roles).
- **GET /auth/me**: Returns the current authenticated user's data.

### User Routes (Protected)
- **GET /protected/users**: Returns all users (only accessible by admin and root).
- **GET /protected/users/{user_id}**: Retrieves user information by user ID.
- **PUT /protected/profile**: Allows a user to update their profile.

### PDF Routes
- **POST /pdf/upload**: Uploads a PDF for processing.
- **GET /pdf/status**: Returns the current status of the PDF watcher.

## Running PDF Watcher
The backend runs a `pdf_watcher.py` script in the background to handle and process PDF documents.

## Usage
- **Login:** Use the login page to authenticate with your credentials.
- **Dashboard:** Access the payroll dashboard to view and manage employee payroll data.
- **Generate Reports:** Use the report section to generate monthly or yearly payroll reports.

## Contributing
We welcome contributions! If you'd like to contribute, please fork the repository, create a feature branch, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any questions or issues, feel free to reach out via email or open an issue on the GitHub repository.

---

> **Note:** Ensure all sensitive data such as API keys, passwords, and private information are never exposed in the source code. Always use `.env` files for such configurations.
