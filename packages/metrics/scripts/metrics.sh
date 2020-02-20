eval $(egrep -v '^#' .env | xargs) miot-metrics "$@"
