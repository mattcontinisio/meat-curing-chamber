package(default_visibility = ["//visibility:public"])

py_library(
    name = "metrics_lib",
    srcs = glob(["metrics/**/*.py"]),
)

py_binary(
    name = "metrics",
    srcs = glob(["metrics/**/*.py"]),
    main = "metrics.py",
    deps = ["//packages/config"],
)
