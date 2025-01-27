Create .env file and paste the following (change smth if you need):
```text
API_GATEWAY_PORT=5000
API_GATEWAY_HOST="0.0.0.0"

PARSER_SERVICE_PROTOCOL="http"
PARSER_SERVICE_HOST="parser_service" // do not touch
PARSER_SERVICE_PORT=5001

RMQ_USER="guest"
RMQ_PASS="guest"
RMQ_HOST="rmq_broker"  // do not touch
RMQ_PROTOCOL="amqp"

LOGGER_QUEUE_NAME="logger"

LOG_LEVEL="INFO"
LOG_FORMAT="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)-7s - %(message)s"
```