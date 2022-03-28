
# Formee- The terminal forms

Formee is a tool that provides an easy way to create, edit and manage all of your forms from the command line. It uses a powerful GraphQL API and strives to make the process of working with forms as easy and simple as possible.

![Formee Logo](/docs_assets/images/logo.svg)


## Installation

1. Install *formee* with pip

```bash
pip3 install formee
```

2. Use the Github repository

    ```bash
    git clone https://github.com/Arpan-206/formee.git
    cd formee
    ```

    - If you use poetry, then:
        ```bash
        poetry install
        ```
    - Otherwise, use pip
        ```bash
        pip3 install -r requirements.txt
        ```

## Usage

1. [Install the CLI.](#Installation)
2. Run the command
```bash
python3 -m formee
```
3. You're good to go.

## Project layout
This is the project file structure for reference.

    |-- LICENSE
    |-- README.md
    |-- docs
    |   |-- getting-started.md
    |   |-- index.md
    |   |-- installation.md
    |   `-- screenshots.md
    |-- docs_assets
    |   |-- images
    |   |   `-- favicon.ico
    |   |-- javascripts
    |   |   `-- config.js
    |   |-- stylesheets
    |   |   `-- pdf-export.css
    |   `-- theme
    |       `-- main.html
    |-- formee
    |   |-- __init__.py
    |   |-- __main__.py
    |   |-- auth
    |   |   |-- check.py
    |   |   |-- hasher.py
    |   |   |-- login.py
    |   |   |-- register.py
    |   |   |-- user_jwt.py
    |   |   |-- validate.py
    |   |   |-- visitor_jwt.py
    |   |   `-- visitor_settings.py
    |   `-- formTools
    |       |-- create.py
    |       |-- deploy.py
    |       |-- fill.py
    |       |-- read.py
    |       `-- validators.py
    |-- mkdocs.yml
    |-- pyproject.toml
    |-- requirements.txt
    `-- tests
        |-- __init__.py
        `-- test_formee.py


## License

[MIT](https://github.com/Arpan-206/formee/blob/main/LICENSE)



## Roadmap

- Add more type of fields

- Work on security

- Work on Auth

- Improve WebUI

- Improve runtime


## Authors

- [@Arpan-206](https://github.com/Arpan-206)


## Feedback

If you have any feedback, please reach out to us at arpan@hackersreboot.tech.


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.