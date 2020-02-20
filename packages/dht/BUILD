package(default_visibility = ["//visibility:public"])

py_library(
    name = "dht_lib",
    srcs = glob(["dht/**/*.py"]),
)

py_binary(
    name = "dht",
    srcs = glob(["dht/**/*.py"]),
    main = "dht.py",
    deps = ["//packages/config"],
)
