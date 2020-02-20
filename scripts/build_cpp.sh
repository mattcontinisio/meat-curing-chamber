#!/bin/bash

usage="usage: build_cpp.sh [release|debug|san|coverage|tidy] [gcc|clang] [make|ninja]"
build_type=$1
compiler=$2
make_or_ninja=$3

if  [ "$compiler" = "gcc" ]
then
    export CC=/usr/bin/gcc
    export CXX=/usr/bin/g++
elif [ "$compiler" = "clang" ]
then
    export CC=/usr/bin/clang
    export CXX=/usr/bin/clang++
else
    echo $usage
    exit
fi

if  [ "$make_or_ninja" = "make" ]
then
    cmake_generator="Unix Makefiles"
elif [ "$make_or_ninja" = "ninja" ]
then
    cmake_generator="Ninja"
else
    echo $usage
    exit
fi

build_dir="_build_"$build_type"_"$compiler"_"$make_or_ninja
rm -rf $build_dir
mkdir $build_dir
cd $build_dir

if  [ "$build_type" = "release" ]
then

    cmake -DCMAKE_BUILD_TYPE=Release -G "$cmake_generator" ..
    $make_or_ninja
    cd ..
elif [ "$build_type" = "debug" ]
then
    cmake -DCMAKE_BUILD_TYPE=Debug -G "$cmake_generator" ..
    $make_or_ninja
    cd ..
elif [ "$build_type" = "san" ]
then
    cmake -DCMAKE_BUILD_TYPE=Debug -DSANITIZE_ADDRESS=On -G "$cmake_generator" ..
    $make_or_ninja
    cd ..
elif [ "$build_type" = "coverage" ]
then
    cmake -DCMAKE_BUILD_TYPE=Debug -DWITH_COVERAGE=ON -G "$cmake_generator" ..
    $make_or_ninja
    $make_or_ninja test_coverage
    cd ..
elif [ "$build_type" = "tidy" ]
then
    CXX_FLAGS="-Werror -Wcast-align -Wfloat-equal -Wimplicit-atomic-properties -Wmissing-declarations -Woverlength-strings -Wshadow -Wstrict-selector-match -Wundeclared-selector -Wunreachable-code -std=c++11" cmake -DCLANG_TIDY_FIX=ON -G "$cmake_generator" ..
    $make_or_ninja
    cd ..
else
    echo $usage
    cd ..
    rm -rf $build_dir
fi
