Coding:
- elastic usage - Predefined text that we  can use for creating a course (keywords in Elastic can identify text)
- async request support

Business:
- add separate endpoint for topics - done
- data base integration to store courses
- multi-language support - done
- admin panel to work with prompts
- analyzing job skill sets and building courses based on cluster analysis
- інтерактивна частина (спілкування з чатом), побудувати навчальне середовище на основі компетенції в рамках спеціалізації

docker run --name svitoch_postgres -e POSTGRES_PASSWORD=123 -v /Users/artemkakun/Projects/home/svitoch/postgres_data:/var/lib/postgresql/data -p 5432:5432 -d postgres