# Horaido

Book Management System for literary salon Horaido

## Setting for local environment

1. `pipenv shell`

You have to set up follow environmetal valuables:

- APP_SETTINGS
- DATABASE_URL
- MAIL_USERNAME
- MAIL_PASSWORD

For example, 
- APP_SETTINGS = "config.DevelopmentConfig"
- DATABASE_URL= "postgres://username:password@localhost/dbname"
- MAIL_USERNAME = "username@gmail.com"
- MAIL_PASSWORD = "password"

2. `flask run`

## ToDo

1. Implement filtering search
1. Modify UI in book detail page and display rental history
1. Modify UI in borrow, return, register and edit page
1. Coding exception handling
1. Modify the color
1. Implement account setting
1. Modify UI
1. Make automation test including Login/out, search/registry/borrow/return books.
1. Launch
1. Change to WTForm
1. Send email before due date if not returning the book yet
1. Add a function for searching books to register
1. Add a function to post reviews
