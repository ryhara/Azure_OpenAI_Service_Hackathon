# Penguins Team Project
このリポジトリは[Azure OpenAI Service　大学生向けハッカソン](https://hackathon2024xseedshub.peatix.com/)予選のためのリポジトリです。

This repository is for the qualifying round of the "Azure OpenAI Service for University Student Hackathon".

## Overview


## Development Environment
- M1 MacBook Air / macOS Sonoma 14.2.1
- Docker version 24.0.6, build ed223bc
- Python 3.9.6
- pip list
```
Package            Version
------------------ -------

```

## Usage
1. At project root
	- Dockerを起動します
	- Start Docker(Docker Desktop)

2. make env
	- cp .env.example .env
```
$ make env
```
3. .env setting
	- .envファイルにAPI_KEYとSECRET_KEYを設定する。
	- Set API_KEY and SECRET_KEY in the .env file.

4. make all
	- docker compose -f ./docker-compose.yml build --no-cache
	- docker compose -f ./docker-compose.yml up -d
```
$ make all
```
5. access to
	- http://localhost:5001


## Reference
- [Azure OpenAI Service　大学生向けハッカソン](https://hackathon2024xseedshub.peatix.com/)
- [Azure OpenAI Service 公式ドキュメント](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/)
- [Flask チュートリアル 日本語](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/index.html)
- [【Flask】中規模な開発のディレクトリ構成を考える(qiita, github)](https://github.com/Koichi73/Flask-Template)
- [Flaskの基本をわかりやすくまとめる(qiita)](https://qiita.com/gold-kou/items/00e265aadc2112b0f56a)
- [【Python Flask & SQLAlchemy】(qiita)](https://qiita.com/Bashi50/items/e3459ca2a4661ce5dac6)