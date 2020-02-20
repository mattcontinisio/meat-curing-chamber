eval $(egrep -v '^#' .env | xargs) miot-csv-writer "$@"
