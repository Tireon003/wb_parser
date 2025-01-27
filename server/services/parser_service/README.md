Create .env file and paste the following (change smth if you need):
```text
PARSER_SERVICE_HOST="0.0.0.0"
PARSER_SERVICE_PORT=5001

PATH_TO_CREDENTIALS="path-to-your-google-api-credentials"
GOOGLE_SHEET_NAME="WB Cards"

LOG_LEVEL="INFO"
LOG_FORMAT="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)-7s - %(message)s"

WB_URL="https://www.wildberries.ru"

SELENIUM_HOST="selenium_server"  // do not touch
SELENIUM_PORT=4444
USER_AGENT="user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
```