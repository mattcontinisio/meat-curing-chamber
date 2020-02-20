package(default_visibility = ["//visibility:public"])

py_library(
    name = "csv_writer_lib",
    srcs = glob(["csv_writer/**/*.py"]),
)

py_binary(
    name = "csv_writer",
    srcs = glob(["csv_writer/**/*.py"]),
    main = "csv_writer.py",
    deps = ["//packages/config"],
)
