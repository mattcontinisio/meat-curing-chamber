eval $(egrep -v '^#' .env | xargs) miot-temperature-controller "$@"
