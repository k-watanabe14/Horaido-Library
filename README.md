# houraidou

Book Management System for literary salon Houraidou

## Setting for local environment

`pipenv shell`

`export APP_SETTINGS="config.DevelopmentConfig"`

`export DATABASE_URL='postgres://username:password@localhost/db_name'`

ex.) `export DATABASE_URL='postgres://postgres:123456@localhost/houraidou'`

`flask run`

## Todo

1. Implement filtering search
1. Add book image itself into DB
1. Send email before due date if not returning the book yet
1. Modify UI in book detail page and display rental history
1. Modify UI in borrow, return, register and edit page
1. Coding exception handling
1. Modify the color
1. Implement account setting
1. Modify UI
1. Launch
1. Change to WTForm
