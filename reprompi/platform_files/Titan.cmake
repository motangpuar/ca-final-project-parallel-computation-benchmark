
SET(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS)
SET(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS)

SET(CMAKE_C_COMPILER cc)
SET(CMAKE_CXX_COMPILER CC)
SET(CMAKE_C_FLAGS "-O3 -std=c99 -DZF_LOG_OPTIMIZE_SIZE -D_POSIX_C_SOURCE=199309L")
SET(CMAKE_CXX_FLAGS "-O3 -std=c++11")

#set(ENABLE_RDTSCP ON)
#set(FREQUENCY_MHZ "2200")

SET(BUILD_SHARED_LIBS 0)

message(STATUS "Using Cray compilers: ${CMAKE_C_COMPILER}")
