package(default_visibility = ["//visibility:public"])

py_library(
    name = "rf433",
    srcs = glob(["rf433/**/*.py"]),
)

py_binary(
    name = "humidity_controller_main",
    srcs = glob(["rf433/**/*.py"]),
    main = "humidity_controller.py",
)

py_binary(
    name = "temperature_controller_main",
    srcs = glob(["rf433/**/*.py"]),
    main = "temperature_controller.py",
)
