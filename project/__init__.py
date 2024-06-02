"""
Welcome to the documentation for the Social scraping API!

This project is written in Python, with the
[Flask](https://flask.palletsprojects.com/) web framework. This documentation
is generated automatically from the
the APIFairy Flask extension. linkedin

## Introduction

This project is a Flask API that retrieves recent activity (latest 20-30 posts) from a LinkedIn user by their LinkedIn ID and fetches the engagement data (likers) of each post, including their IDs, names, and titles.

## Configuration

If you are running this service yourself while developing
there are a number of environment variables that you can set to configure its
behavior. The variables can be defined directly in the environment or in a
`.env` file in the project directory. The following table lists all the
environment variables that are currently used:

- LINKEDIN_EMAIL=your_linkedin_email@example.com
- LINKEDIN_PASSWORD=your_linkedin_password
- BROWSER=your_browser(edge, chrome, firefox, default=edge)


## Errors

All errors returned by this API use the following JSON structure:

```json
{
    "code": <numeric error code>,
    "message": <short error message>,
    "description": <longer error description>,
}
```

In the case of schema validation errors, an `errors` property is also returned,
containing a detailed list of validation errors found in the submitted request:

```json
{
    "code": <error code>,
    "message": <error message>,
    "description": <error description>,
    "errors": [ <error details>, ... ]
}
```
"""

from .app import create_app, ma
