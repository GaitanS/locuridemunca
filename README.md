# JoburiPentruRomani - Job Board Platform

## Description

JoburiPentruRomani is a web application built with Django, designed to connect employers with potential candidates, focusing particularly on technical, operational, and specialized roles within Romania. It provides features for job posting, searching, filtering, user registration (job seekers and companies), and subscription plans for companies.

## Key Features

*   **User Roles:** Separate registration and dashboard experiences for Job Seekers and Companies.
*   **Job Listings:** Companies can post jobs; users can browse, search, and filter job listings.
*   **Job Categories:** Jobs are organized by categories.
*   **Company Profiles:** Companies have profiles (details managed via admin for now).
*   **Job Seeker Profiles:** Job seekers have profiles (details managed via admin for now).
*   **Subscription Plans:** Multiple subscription tiers for companies with varying features (managed via admin).
*   **Email Verification:** User accounts require email verification upon signup.
*   **Password Reset:** Standard password reset functionality via email.
*   **Django Admin:** Customized admin interface for managing users, jobs, categories, and plans.

## Technology Stack

*   **Backend:** Python, Django
*   **Frontend:** HTML, Tailwind CSS (via CDN), Font Awesome (via CDN), minimal JavaScript
*   **Database:** SQLite (default development database)
*   **Key Python Packages:**
    *   Django
    *   Pillow (for image handling like logos)
    *   *Many others listed in `requirements.txt`*

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Database Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (for Admin Access):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an admin username and password. Make sure the user is active (it should be by default now, but if login fails, check the `is_active` flag).

6.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the Application:**
    *   Main Site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    *   Admin Interface: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
