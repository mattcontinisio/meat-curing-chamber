eval $(egrep -v '^#' .env | xargs) miot-dht "$@"
