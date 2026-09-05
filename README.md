# CS50W: Web Programming with Python and JavaScript - Projects

This repository contains my solutions to the projects from **[CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/)**, Harvard University's course on modern web development, taught by Brian Yu.

Over the course of this class, I moved from building a static front-end for Google Search through to designing and shipping full-stack Django applications with asynchronous JavaScript front-ends - along the way exploring HTML/CSS, Django models and views, REST-like APIs consumed via `fetch`, user authentication, and the design of an original web application of my own.

## 📚 About the Course

CS50W is entirely focused on the design and implementation of web applications: how to structure the front-end with HTML, CSS, and JavaScript; how to build the back-end with Python and the Django framework, including models, views, templates, migrations, and the Django admin; how to make applications dynamic and responsive using asynchronous JavaScript (`fetch`, event listeners, DOM manipulation) instead of full-page reloads; and how to design, scope, and document an original project from scratch. The course does not map lectures one-to-one onto projects, so several projects assume familiarity with material from later lectures before they can reasonably be attempted.

The course is organized around seven projects of increasing scope - from a static front-end, to a database-backed encyclopedia, an auction site, an email client, a social network, and finally a capstone project of one's own design.

## 🗂️ Repository Structure

Each folder in this repository corresponds to one project, and includes its own `README.md` describing the specific requirements, my implementation, and what I learned from it in more detail.

| Project           | Topic                        | Description                                                                                                                                  |
|--------------------|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Project 0 | Search       | `search` - a static front-end for Google Search, Google Image Search, and Google Advanced Search, built with plain HTML and CSS and GET forms |
| Project 1 | Wiki         | `wiki` - a Wikipedia-like encyclopedia built with Django, storing entries as Markdown files and rendering them as HTML, with search, entry creation, editing, and a random-page feature |
| Project 2 | Commerce     | `commerce` - an eBay-like auction site built with Django, supporting listings, bidding, watchlists, comments, categories, and a Django admin interface |
| Project 3 | Mail         | `mail` - a single-page email client built on a pre-supplied Django/API back-end, implemented entirely in JavaScript (`inbox.js`) to send mail, browse mailboxes, view, archive, and reply to messages using `fetch` |
| Project 4 | Network      | `network` - a Threads/Twitter-like social network built with Django and JavaScript, supporting posts, likes, following, pagination, and in-place post editing without a page reload |
| Capstone  | Final Project | `capstone` - an original full-stack web application of my own design, built with Django and JavaScript, distinct in purpose and complexity from the other projects in the course |

## 🎯 What I Learned

Working through CS50W gave me a solid, practical foundation in full-stack web development:

- **Front-end fundamentals** - structuring pages with semantic HTML, styling them with CSS, and submitting data to a server using HTML forms and GET/POST parameters.
- **Django fundamentals** - defining models to represent application data, writing views and URL configurations, rendering data with the Django template language, and running migrations to keep the database schema in sync with the models.
- **User authentication** - implementing registration, login, logout, and access control (e.g. via the `@login_required` decorator) so that users can only view or modify data they're permitted to.
- **Relational design in practice** - modeling real application domains (auction listings and bids, posts and followers, emails and mailboxes) as related Django models, including self-referencing relationships like a user following other users.
- **Asynchronous JavaScript** - using `fetch` to call an API without reloading the page, updating the DOM in place (e.g. editing a post, liking a post, marking an email as read), and attaching event listeners to dynamically created elements.
- **Designing and consuming an API** - reading API documentation to understand request/response shapes, and issuing GET, POST, and PUT requests with JSON payloads to read and update server-side data.
- **Pagination and performance-minded UI** - using Django's `Paginator` on the back-end and Bootstrap's pagination components on the front-end to avoid loading unbounded amounts of data at once.
- **Mobile responsiveness** - designing layouts that adapt cleanly across screen sizes, a hard requirement for the capstone project.
- **Project scoping and documentation** - taking a project from a written specification (or, for the capstone, from a blank page) to a working application, and writing a README that clearly documents distinctiveness, complexity, file structure, and how to run the application.
- **Security-mindedness** - understanding why routes are protected against unauthorized edits (e.g. ensuring a user can never edit another user's post or another user's auction listing via any route), and why CSRF protection matters for POST/PUT requests in a real-world project.

More than any single framework feature or line of JavaScript, this course shaped how I think about building for the web: separating concerns between front-end and back-end, treating the browser as a thin, dynamic client of a well-designed API, and always asking not just "does this feature work?" but "is it secure, responsive, and usable by someone other than me?"

## 🎓 Certificate

Upon completing the course, I was awarded the official CS50W certificate from Harvard University (HarvardX):

**[View my CS50W Certificate](https://certificates.cs50.io/6f5116d0-882d-4fc1-9dc6-0c96c5d4c7b1)**

## 🔗 Course Information

- Course homepage: [https://cs50.harvard.edu/web/](https://cs50.harvard.edu/web/)
- Instructor: Brian Yu
- Institution: Harvard University

---

*Each subfolder in this repository contains a dedicated README with a detailed breakdown of that specific project, my implementation, and the concepts it reinforced.*