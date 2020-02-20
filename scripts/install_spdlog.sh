git clone https://github.com/gabime/spdlog.git
cd spdlog
git checkout v1.5.0
mkdir build
cd build
cmake -DSPDLOG_BUILD_EXAMPLE=OFF -DSPDLOG_BUILD_TESTS=OFF ..
make -j
sudo make install
sudo ldconfig
