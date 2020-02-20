eval $(egrep -v '^#' .env | xargs) miot-humidity-controller "$@"
