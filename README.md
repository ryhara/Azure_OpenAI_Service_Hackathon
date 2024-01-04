# Penguins Team Project
このリポジトリは[Azure OpenAI Service　大学生向けハッカソン](https://hackathon2024xseedshub.peatix.com/)予選のためのリポジトリです。

This repository is for the qualifying round of the "Azure OpenAI Service for University Student Hackathon".

## Development Environment
- M1 MacBook Air / macOS Sonoma 14.2.1
- Python 3.9.6
- pip list
```
Package            Version
------------------ -------
astroid            3.0.2
blinker            1.7.0
click              8.1.7
dill               0.3.7
Flask              3.0.0
Flask-SQLAlchemy   3.1.1
importlib-metadata 7.0.1
isort              5.13.2
itsdangerous       2.1.2
Jinja2             3.1.2
MarkupSafe         2.1.3
mccabe             0.7.0
pip                21.2.4
platformdirs       4.1.0
pycodestyle        2.11.1
pylint             3.0.3
python-dotenv      1.0.0
setuptools         58.0.4
SQLAlchemy         2.0.25
tomli              2.0.1
tomlkit            0.12.3
typing_extensions  4.9.0
Werkzeug           3.0.1
zipp               3.17.0
```

## Usage

## Directory
```
.
├── .env.example
├── .gitignore
├── Makefile
├── README.md
├── flask_app
│   ├── __init__.py
│   ├── app.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── custom.js
│   ├── templates
│   │   ├── index.html
│   │   └── layout.html
│   └── views
│       └── sample.py
├── instance
│   └── config.py
├── pycodestyle
├── pylintrc
└── requirements.txt
```

## Reference
- [Azure OpenAI Service　大学生向けハッカソン](https://hackathon2024xseedshub.peatix.com/)
- [Flask チュートリアル 日本語](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/index.html)
- [【Flask】中規模な開発のディレクトリ構成を考える(qiita, github)](https://github.com/Koichi73/Flask-Template)
- [Flaskの基本をわかりやすくまとめる(qiita)](https://qiita.com/gold-kou/items/00e265aadc2112b0f56a)
- [【Python Flask & SQLAlchemy】(qiita)](https://qiita.com/Bashi50/items/e3459ca2a4661ce5dac6)