# CS50 Project 3 - Mail

This project is a single-page email client developed using Django and vanilla JavaScript as part of the CS50 Web Programming with Python and JavaScript course. It replicates core email functionalities, including sending, receiving, viewing, archiving, and replying to emails in a dynamic, interactive interface.

## 🗂️ Project Structure

The Django project contains the following key elements:

```
mail/
├── mail/                # Django app for all functionality
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_email_id_alter_user_id.py
│   ├── static/          # JavaScript and CSS for client-side interactivity
│   │   └── mail/
│   │       ├── centra-no2-bold.woff2
│   │       ├── favicon.ico
│   │       ├── logo.svg
│   │       ├── script.js
│   │       ├── styles.css
│   │       ├── register.webp
│   │       ├── yahoo-sans-bold.woff2
│   │       ├── yahoo-sans-cr4-vf.woff2
│   │       ├── yahoo-sans-light.woff2
│   │       ├── yahoo-sans-semibold.woff2
│   │       └── 
│   ├── templates/       # HTML templates
│   │   └── mail/
│   │       ├── index.html
│   │       ├── layout.html
│   │       ├── login.html
│   │       └── register.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # Email model
│   ├── tests.py
│   ├── urls.py
│   └── views.py             # API endpoints and page rendering
├── project3/                # Main project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .gitignore
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt
```

## ✅ Features Overview

This section summarizes the core features implemented in the application.

### 🔑 User Authentication
  
  - **Register/Login/Logout**: Users can create an account, log in, and securely log out.
  - Logged-in users can access their personalized email data.

### ✉️ Compose Email

  - Users can write new emails by specifying:
    - Recipients
    - Subject
    - Message body
  - Sent emails are saved in the database and accessible through the "Sent" mailbox.
  - Emails are not delivered to real email servers (internal system only).

### 📬 Mailboxes

  - Users can navigate between Inbox, Sent, and Archive.
  - Each mailbox displays a list of relevant emails showing:
    - Sender or recipient
    - Subject
    - Timestamp

### 🔍 View Email

  - Clicking on an email opens a detailed view with:
    - Sender
    - Recipients
    - Subject
    - Timestamp
    - Body
  - Emails are marked as read once opened.

### 📁 Archive / Unarchive Emails

  - Emails can be archived or unarchived with one click:
    - Archive emails from Inbox
    - Unarchive from Archive view

### 🔁 Reply to Emails

  - Users can reply to received emails.
  - The reply form auto-fills:
    - Recipient
    - Formatted subject (`Re:`prefix)
    - Original message as quoted text

### 📱 Responsive Design

  - The interface is responsive and works smoothly across various screen sizes and devices.

### ⚙️ Technical Notes

  - **JavaScript + AJAX**: Frontend interactions use JavaScript and `fetch` to make asynchronous calls to Django's REST API, enabling seamless updates without page reloads.
  - **Error Handling**: The UI handles cases such as missing recipients or server errors with user-friendly feedback.
  - **Extensibility**: Modular code allows easy extension, such as support for threading or message search.

## 🚀 Running the Application

To run the app locally:

### Install dependencies

```bash
pip install -r requirements.txt
```

### Database setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start development server

```bash
python manage.py runserver
```

## 🧱 Static Assets

To collect and build static assets:

```bash
python manage.py collectstatic
```

## 🎥 Demo
You can view a working version of the project here:
👉 https://search.realnormanik.workers.dev/

Video walkthrough of the specification:
🎥 [YouTube](https://youtu.be/scyvx77RVhU)

## 📜 Certification
This project was submitted as part of the CS50’s Web Programming with Python and JavaScript course offered by Harvard University.
Upon successful completion, I was awarded a certificate, which is available here:

🎓 [View Certificate](https://certificates.cs50.io/6f5116d0-882d-4fc1-9dc6-0c96c5d4c7b1.pdf)
