# CS50 Web Programming with Python and JavaScript - Capstone

## LeadFlow

LeadFlow is a CRM (Customer Relationship Management) web application built with Django, JavaScript, HTML, and CSS. It was developed as the final Capstone project for CS50's Web Programming with Python and JavaScript course. The application allows a user to manage clients and the sales process through an interactive, Kanban-style pipeline in which deals are represented as draggable cards.

## 🗂️ Project Structure

The Django project contains the following key elements:

```
capstone/
├── crm/                          # Main Django application (CRM logic)
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_pipelinestage_is_final.py
│   │   └── 0003_remove_deal_tags_alter_activity_activity_type_and_more.py
│   ├── static/
│   │   └── crm/
│   │       ├── dashboard.js
│   │       ├── favicon.ico
│   │       ├── filters.js
│   │       ├── Inter.woff2
│   │       ├── JetBrainsMono-Regular.woff2
│   │       ├── logo.svg
│   │       ├── modal.js
│   │       ├── pipeline.js
│   │       ├── script.js
│   │       ├── SpaceGrotesk-Bold.woff2.js
│   │       ├── stage.js
│   │       └── styles.css
│   ├── templates/
│   │   └── crm/
│   │       ├── client_detail.html
│   │       ├── client_list.html
│   │       ├── dashboard.html
│   │       ├── layout.html
│   │       ├── login.html
│   │       ├── pipeline.html
│   │       ├── register.html
│   │       ├── stage_settings.html
│   │       └── task_list.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── crm_project/                   # Main project configuration
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

## Distinctiveness and Complexity

LeadFlow is a CRM system designed to manage customer relationships and the sales process. I believe this project fully satisfies the distinctiveness and complexity requirements of the course for several independent reasons.

First, LeadFlow is neither a social network nor an e-commerce site, so there is no risk of it being mistaken for Project 4 (Network) or Project 2 (Commerce). The application contains none of the elements typical of a social network, such as public profiles, posts, following other users, or likes. It also has no shopping cart, bidding mechanism, or any transactional features typical of e-commerce platforms. The entire logic of the application is built around business relationships between a single user (a salesperson) and that user's own clients and sales tasks — every logged-in user sees and manages only their own data, which is a fundamentally different data model from both a social network and an online marketplace.

Second, the complexity of the project stems from a multi-layered data structure and the number of models that work together. The application is built on six interrelated models: `Client`, `Deal`, `PipelineStage`, `Activity`, `Task`, and `Tag`. These models form a network of one-to-many and many-to-many relationships (for example, `Deal` has a `ForeignKey` to both `Client` and `PipelineStage`, a `ManyToMany` relationship to `Tag`, and is additionally linked to interaction history through `Activity` and to reminders through `Task`). Such a structure required careful query design (using `prefetch_related`, `annotate`, and `aggregate`) in order to avoid redundant database queries and to keep the pipeline view and the statistics dashboard performant.

Third, a key element of front-end complexity is a self-implemented **drag-and-drop mechanism** built on the native HTML5 Drag and Drop API, without relying on any third-party library. Dragging a card representing a deal from one pipeline column to another updates its stage and position in real time through an asynchronous `fetch()` request sent to a dedicated API endpoint (`/api/deals/<id>/move`), without reloading the page. This required writing logic to calculate a card's position relative to other elements within a column (the `getDragAfterElement` function), handling the `dragstart`, `dragover`, `dragleave`, and `drop` events, and keeping the visual state in sync with the database on the server side.

Fourth, since the native Drag and Drop API does not work reliably on touch devices, the application implements an **alternative navigation mechanism for mobile devices** — "◀" and "▶" buttons that let a user move a card between pipeline stages without dragging. This solution is driven by CSS media queries together with JavaScript logic that dynamically adds the appropriate buttons only when needed and updates their state (for example, disabling the "◀" button for the first column). This is a deliberate approach to the mobile-responsiveness requirement that goes beyond simply adjusting the CSS layout.

Fifth, the application includes a full user account system with data isolation — every salesperson has their own independent pipeline, their own clients, and their own sales stages, which they can freely configure (add new stages, change their order). Every view and API endpoint filters data by the `owner` field, which required consistently securing every single query against unauthorized access to another user's data — this is a significant element of both the complexity and the security of the application.

Finally, LeadFlow includes a statistics dashboard generated dynamically from aggregated database data (number of deals per stage, total pipeline value, number of overdue tasks), visualized with the Chart.js library. This required writing appropriate aggregation queries on the Django side (`Count`, `Sum` across relationships) as well as passing that data to the JavaScript layer in a format suitable for generating a chart.

I believe that, taken together, these elements — a multi-model data architecture, a hand-built drag-and-drop mechanism synchronized asynchronously with the backend, an alternative mobile interface, per-user data isolation, and a dynamic statistics dashboard — collectively exceed the level of complexity and originality of any single prior project in this course, and clearly distinguish LeadFlow from both Project 2 (Commerce) and Project 4 (Network).

## ✅ Features Overview

This section summarizes the core features implemented in the application.

### 🔑 User Authentication
- **Registration**: A new user creates an account, for which a default set of five pipeline stages is automatically generated.
- **Login/Logout**: Standard Django session-based authentication.
- Access to all CRM views requires the user to be logged in (`@login_required`).

### 📋 Sales Pipeline (Drag & Drop)
- Cards representing deals are arranged in columns corresponding to sales stages.
- Dragging a card between columns immediately updates its status in the database through an asynchronous request.
- Clicking a card opens a modal where the title, description, value, priority, and due date can be edited.
- Cards with an overdue due date are visually highlighted with a red border.

### 👥 Client Management
- A client list with search functionality by first name, last name, company, or email.
- A client detail page displays the full interaction history (calls, emails, meetings, notes) as well as all deals linked to that client.

### ✅ Tasks
- A separate task/reminder list, independent from the pipeline, where tasks can be marked as done without reloading the page.

### ⚙️ Pipeline Stage Configuration
- Users can add new sales stages themselves and set the order in which they are displayed.

### 📊 Statistics Dashboard
- A summary of the total number of deals, total pipeline value, number of closed deals, and number of overdue tasks.
- An interactive bar chart showing the distribution of deals across pipeline stages (Chart.js).

### 🛠️ Django Admin Interface
- Administrators can manage all clients, deals, activities, and tasks through the built-in Django admin panel.

## 📄 What's Contained in Each File

- **`crm/models.py`** — Model definitions: `Client`, `PipelineStage`, `Deal`, `Activity`, `Task`, and `Tag`, along with the relationships between them.
- **`crm/views.py`** — View logic (pipeline, clients, tasks, dashboard, authentication) as well as the API endpoints that handle `fetch()` requests coming from JavaScript (moving, creating, editing, and deleting deals).
- **`crm/forms.py`** — Django forms for clients, deals, tasks, pipeline stages, and activities, with querysets restricted to data belonging to the currently logged-in user.
- **`crm/admin.py`** — Django admin panel configuration for all models.
- **`crm/urls.py`** — URL routing, including a separate group of API endpoints under the `/api/` prefix.
- **`crm/templates/crm/`** — HTML templates: a shared layout with navigation, login/registration forms, the main pipeline view, client list and detail pages, the task list, stage settings, and the dashboard.
- **`crm/static/crm/css/styles.css`** — Application styling, including full responsiveness (media queries that switch the column-based pipeline view into a stacked mobile view with navigation buttons).
- **`crm/static/crm/js/pipeline.js`** — Drag-and-drop logic, the deal-editing modal, communication with the API via `fetch()`, and the mobile card-moving mechanism.
- **`crm/static/crm/js/dashboard.js`** — Initializes the Chart.js chart using data passed from the Django view.
- **`crm/static/crm/js/filters.js`** — Dynamic, debounced client search that does not require reloading the page.
- **`crm/static/crm/js/modal.js`** — Additional UX improvements for modals (resetting forms, preventing the edit modal from opening accidentally right after a drag-and-drop action).
- **`crm_project/settings.py`** — Project configuration, including registration of the `crm` app, static file paths, and the SQLite database.
- **`requirements.txt`** — List of Python dependencies required to run the project.

## 🚀 Running the Application

To run the application locally:

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up the database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

### Start the development server

```bash
python manage.py runserver
```

Then navigate to `http://127.0.0.1:8000`, register a new account (which will automatically create the default pipeline stages), and start using the application.

## 🧱 Static Assets

To collect static files before a production deployment:

```bash
python manage.py collectstatic
```

## 💡 Additional Information

- **Data isolation**: Every API endpoint and view filters data by `owner=request.user`, so users cannot access or modify data belonging to other accounts.
- **Error handling**: Forms validate user input, and API endpoints return appropriate HTTP status codes along with error messages in JSON format.
- **Extensibility**: The model structure was designed to make it easy to add future features, such as CSV data export, email notifications for upcoming deadlines, or integration with external mail APIs.
- **Mobile-first fallback**: Because the native Drag and Drop API is unreliable on touch devices, the application automatically switches to an alternative, button-based navigation interface on screens narrower than 768px.
- No generative AI was used in the implementation of the application itself; it was used only to assist in writing this README, in accordance with the course's academic honesty policy.

## 🎥 Demo
You can view a working version of the project here:
👉 https://search.realnormanik.workers.dev/

Video walkthrough of the specification:
🎥 [YouTube](https://youtu.be/D95OuOGGzyk)

## 📜 Certification

This project was submitted as part of the CS50’s Web Programming with Python and JavaScript course offered by Harvard University.
Upon successful completion, I was awarded a certificate, which is available here:

🎓 [View Certificate](https://certificates.cs50.io/6f5116d0-882d-4fc1-9dc6-0c96c5d4c7b1.pdf)