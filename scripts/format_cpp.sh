#!/bin/bash

clang-format --version

find ./packages -regex '.*\.\(cpp\|hpp\|cc\|cxx\)' -exec clang-format -style=file -i {} \;
