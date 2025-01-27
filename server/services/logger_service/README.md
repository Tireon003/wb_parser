Create .env file and paste the following (change smth if you need):
```text
RMQ_USER="guest"
RMQ_PASS="guest"
RMQ_HOST="rmq_broker" // do not touch
RMQ_PROTOCOL="amqp"

LOGGER_QUEUE_NAME="logger"

LOG_LEVEL="INFO"
LOG_FORMAT="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)-7s - %(message)s"
```