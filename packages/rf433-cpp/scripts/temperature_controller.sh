eval $(egrep -v '^#' .env | xargs) ./_build_release_gcc_make/packages/rf433-cpp/temperature_controller "$@"
