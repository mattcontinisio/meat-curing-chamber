package(default_visibility = ["//visibility:public"])

py_library(
    name = "slack_lib",
    srcs = glob(["slack/**/*.py"]),
)

py_binary(
    name = "slack",
    srcs = glob(["slack/**/*.py"]),
    main = "slack.py",
    deps = ["//packages/config"],
)
