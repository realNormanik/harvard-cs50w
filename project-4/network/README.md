# CS50 Project 4 - Network

This project is a basic social networking platform—similar to X/Twitter—built as part of CS50’s Web Programming with Python and JavaScript course. The app allows users to post messages, follow others, and interact with posts. It combines Django on the backend with a dynamic JavaScript frontend and responsive design using HTML and CSS.

## 🗂️ Project Structure

The Django project contains the following key elements:

```
cs50-network/
├── network/                # Django app for tweet, likes and posts
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_tweet.py
│   │   ├── 0003_like_follow.py
│   │   ├── 0004_alter_follow_following.py
│   │   ├── 0005_rename_following_follow_followed_by.py
│   │   ├── 0006_alter_follow_followed_by.py
│   │   ├── 0007_remove_follow_followed_by_alter_follow_user_and_more.py
│   │   ├── 0008_remove_like_likedby_like_likedby.py
│   │   ├── 0009_tweet_like_delete_like.py
│   │   ├── 0010_alter_follow_user.py
│   │   ├── 0011_user_profile_picture.py
│   │   ├── 0012_tweet_tweetimage_alter_user_profile_picture.py
│   │   └── 0013_alter_follow_id_alter_tweet_id_alter_user_id.py
│   ├── static/
│   │   └── network/
│   │       ├── chirp-bold.woff2
│   │       ├── chirp-extended-heavy.woff2
│   │       ├── chirp-medium.woff2
│   │       ├── chirp-regular.woff2
│   │       ├── default-profile-picture.webp
│   │       ├── favicon.ico
│   │       ├── logo.svg
│   │       ├── script.js
│   │       └── styles.css
│   ├── templates/
│   │   └── network/
│   │       ├── popup/
│   │       │   ├── edit.html
│   │       │   ├── login.html
│   │       │   └── post.html
│   │       ├── allPosts.html
│   │       ├── following.html
│   │       ├── index.html
│   │       ├── layout.html
│   │       ├── login.html
│   │       ├── profile.html
│   │       ├── register.html
│   │       └── tweet.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── projekt4/                # Main project configuration
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

### 🔐 User Authentication

  - Users can register, log in, and log out.
  - The interface and navigation adapt based on authentication status.

### 📝 New Post

  - Signed-in users can compose new posts (text only).
  - Posts are saved to the database and rendered dynamically on the site.

### 📰 All Posts

  - The homepage displays posts from all users in reverse chronological order.
  - Each post includes:
    - Author username (linked to their profile)
    - Content
    - Timestamp
    - Like count
  - Paginated view (10 posts per page).

### 👤 User Profiles

  - Clicking a username opens the profile page:
    - Displays all the user’s posts
    - Shows follower and following counts
    - Allows logged-in users to follow or unfollow

### 🧾 Following Feed

  - Signed-in users can view a feed showing posts from users they follow.
  - Feed is paginated similarly to the "All Posts" page.

### ✏️ Edit Post

  - Users can edit their own posts.
  - Editing is handled asynchronously with JavaScript (no page reload).

### ❤️ Like/Unlike Posts

  - Users can like or unlike any post.
  - Like counts update instantly via AJAX.

### ⚙️ Technical Notes

  - **JavaScript + Fetch API**: AJAX is used to handle likes, editing, and dynamic content updates.
  - **Pagination**: All post views are paginated with "Previous" and "Next" buttons.
  - **Error Handling**: Forms and interactions are validated, and appropriate feedback is provided to users.
  - **Extensibility**: The structure supports easy future enhancements, such as adding comments or media.

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
🎥 https://youtu.be/tdkpOleV3NY

## 📜 Certification
This project was submitted as part of the CS50’s Web Programming with Python and JavaScript course offered by Harvard University.
Upon successful completion, I was awarded a certificate, which is available here:

🎓 [View Certificate](https://certificates.cs50.io/6f5116d0-882d-4fc1-9dc6-0c96c5d4c7b1.pdf)
