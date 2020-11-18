# Horaido

Book Management System for literary salon Horaido

## Setting for local environment

`pipenv shell`

You have to set up follow environmetal valuables:

- APP_SETTINGS
ex) APP_SETTINGS = "config.DevelopmentConfig"

- DATABASE_URL
ex) DATABASE_URL='postgres://postgres:123456@localhost/horaido'

- MAIL_USERNAME
ex) MAIL_USERNAME = username@gmail.com

- MAIL_PASSWORD
ex) MAIL_PASSWORD = password

`flask run`

## Todo

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
