# DataCose Full Stack Challenge

The goal of this challenge if to create a Nuxt frontend with a FastAPI backend matching the objectives down below.

To bootstrap this project, we've used a basic [Nuxt 2](https://nuxtjs.org/) and [FastAPI](https://fastapi.tiangolo.com/lo/) template. There is a Dockerfile available in case you want to work with Docker during development, but this is not a requirement.

The usage of the following packages is mandatory:
- Nuxt
    - BootstrapVue
    - [VueTreeselect](https://vue-treeselect.js.org/) (you need to install this yourself)
- FastAPI
    - Pydantic
    - SQLAlchemy (you need to install this yourself)

To store your data you can either use a sqllite database file, or use a local Postgres database (preferred).

If you choose to use a Postgres database, please provide a seed-file with some dummy data and a migration file to setup the database schema.

In case you use sqllite, provide the database file.

## Objectives

Create a username/password protected app that authenticates API requests using Bearer tokens (not session tokens). Store the user credentials in your database and allow us to sign in using the frontend (please provide the credentials for one user, no need to create functionality to create users). All pages, except for the login page, should be inaccessible when not signed in.

### Data schema

The portal will be used to manage data about authors and their books. An author can have zero or more books, a book always has an author. An author just has a required name field. Books have a required name field, and a required page numbers field.


### Pages
In the portal, there should be two pages (+ a login page). Make sure a user can navigate to both pages using a nav-bar layout.

#### Authors
On this page, render a paginated table of authors with the following columns:
- Name
- Number of books (this is calculated based on the books)

On top of this page, add an input field that is used to search for authors. Next to it, create a button that opens a modal to add a new author. When clicked on a table row, show a modal to edit the author. Make sure any changes can be saved to the database.

The modal to add/edit an author should a name field (of the author) + a table with the books of the authors (name + number of pages). A user should be able to add, edit or delete a book.

#### Books
On this page, render a paginated table of books with the following columns:
- Name
- Author name
- Number of pages

On top of this page, add an input field that is used to search for books. Next to it, create a button that opens a modal to add a new book. When clicked on a table row, show a modal to edit the book. Make sure any changes can be saved to the database.

The modal to add/edit a book should have three fields:
- Name
- Number of pages
- Author (should be a searchable treeselect with authors)

## Notes
The usage of the provided template is mandatory. Submissions not written in this template, will not be reviewed. Writing tests is not mandatory, but doing so will give you bonus points. Please fork this repository and provide us a link to a public GitHub repository.



## SETUP INSTRUCTIONS

# BACKEND API SETUP
- Cd into the src/api folder
- create a .env file and use the contect of the .env.example file
- update the values of the env to suit your local postgres credentials
- Make any other custom change to the env
- Create the postgres db
- Create and Activate a virtual enviroment for the python dependencies
- Run `pip install -r requirements.txt` to install the dependencies in the requirement.txt
- Run alembic uprade head to apply existing migrations
- Run `python3 initial_data.py` to populate Database with initial seed data
- Run  `uvicorn main:app --reload` to start the server
- The server should be running on `http://localhost:8000/`

# FRONTEND SETUP
- cd into src/dashboard folder
- Run  `npm run dev` to start the server
- The client should be running on `http://localhost:3000`


login details
- username : `testuser`
- password `testpassword`


# Screenshots

<img width="663" alt="Screenshot 2023-07-01 at 22 15 54" src="https://github.com/tonyguesswho/developer-full-stack-challenge/assets/19865565/79723b78-c55a-4a3b-8fe9-cf6541b25542">
<img width="748" alt="Screenshot 2023-07-01 at 22 15 44" src="https://github.com/tonyguesswho/developer-full-stack-challenge/assets/19865565/e8c30306-7fe3-4516-9f48-6c74b67ec5c4">
<img width="1501" alt="Screenshot 2023-07-01 at 22 14 26" src="https://github.com/tonyguesswho/developer-full-stack-challenge/assets/19865565/65946022-8e2e-4367-bb1f-82cdde42c5ec">