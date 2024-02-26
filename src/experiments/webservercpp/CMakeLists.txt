cmake_minimum_required(VERSION 3.9)
project(webserver LANGUAGES CXX)

# Optionally, set CMAKE_PREFIX_PATH if Boost is not in a standard location
# set(CMAKE_PREFIX_PATH "/path/to/boost_1_71_0")

# Ensure C++14 is used
set(CMAKE_CXX_STANDARD 14)

# Find Boost 1.71 and the filesystem component
find_package(Boost 1.71.0 COMPONENTS filesystem REQUIRED)

# Add the executable
add_executable(webserver server.cpp)

# Link Boost libraries
target_link_libraries(webserver Boost::filesystem)
