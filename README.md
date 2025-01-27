# wb_parser
A fullstack application to parse cards from Wildberries to Google Tables by article number.

The application consists of:
1. Client (telegram bot)
2. Gateway API
3. The parsing service
4. Logging service

### Project Stack:
- Flask (WSGI based framework for building API)
- Aiogram (User's Tg bot)
- Selenium (with Selenium standalone server, for WB scrapping)
- RabbitMQ (using aiormq)
- Pygsheets (for interaction with Google Sheets)

### How to run

1. Clone repository
```shell
git clone https://github.com/Tireon003/wb_parser.git
```
2. Browse to project directory
3. Create .env file in the root. It should contain the following:
```text
API_GATEWAY_PORT=5000

RMQ_USER="guest"
RMQ_PASS="guest"

SELENIUM_HOST="selenium_server" // do not touch
SELENIUM_PORT=4444
```
4. Configure other parts of application (client, parser service, logger service). Instuctions placed inside each of them root dir.
5. Run application:
```shell
docker-compose up -d --build
```