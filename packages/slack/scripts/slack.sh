eval $(egrep -v '^#' .env | xargs) miot-slack "$@"
