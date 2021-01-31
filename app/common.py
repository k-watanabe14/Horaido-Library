from flask import flash

def display_errors(items):
    for field, errors in items():
        for error in errors:
            flash(error)