# Cooking servese "Foodgram"
## _Delicious food without any gram of rubbish_

### Powered by

[![N|Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![N|Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
[![N|DRF](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![N|PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)  
[![N|HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://html.spec.whatwg.org/multipage/)
[![N|CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://www.w3.org/Style/CSS/)
[![N|JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.ecma-international.org/publications-and-standards/standards/ecma-262/)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)  
[![N|Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![N|Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org)

## Description
Application for publishing recipes. Users can follow authors, create a list of favorites and create a shopping list. The project runs in Docker containers. Web server - Nginx.

## Installation

Feel free to install and explore this project.  
If you want to get deep into code, you should clone repo. Run this command:
```sh
git clone git@github.com:ImreTot/foodgram-project-react.git
```
We recommend you to run frontend and nginx into docker containers. 
In this case execute next command. Be sure you are in dir `/infra`:
```shell
docker compose up
```
However, you can run only backend by django server.
At first, create in `backend/` directory virtual environment. 
>We use `Python3.11`
```shell
python3.11 -m venv .venv
```
Then install requirements:
```shell
pip install -r requirements.txt
```
Another option is to run whole project using only docker features.
In that case you need only `docker-compose.production.yml`. 
Don't forget about creating `.env` file in the same directory.
Here is the variables list:

- DJANGO_SECRET_KEY
- DJANGO_ALLOWED_HOSTS
- CSRF_TRUSTED_ORIGINS
- DEBUG
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- DB_HOST
- DB_PORT

## API
In the project root in the folder `docs` there is documentation with a detailed description of all endpoints. Also you can import api specification in Postman or another API platform for building and using APIs.

## Development plans
- add indexes for models
- optimize queries

## About me

I'm Roman Kiyashko, python developer from south russian city.
Also, I'm a journalist. 
Technology, science, education, music and extreme sports - these are the four foundations of my productive work.  
You can contact with me by one of this ways:
- Telegram: https://t.me/MDPaul
- Email - kiiashko.r@gmail.com
- Facebook - https://www.facebook.com/kiiashko.r/

## License

MIT

**Free Software, Hell Yeah!**
