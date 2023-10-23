set(PROJECT_NAME sponge_pyplugin)
project(${PROJECT_NAME} LANGUAGES CXX CUDA)
cmake_minimum_required(VERSION 3.18)

set(SOURCES "")
set(INCLUDES "")
set(LIBRARIES "cuda")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE  ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

list(APPEND SOURCES main.cu common.cu common.cuh control.cu control.cuh MD_core/MD_core.cu MD_core/MD_core.cuh collective_variable/collective_variable.cu collective_variable/collective_variable.cuh)

find_package(CUDAToolkit REQUIRED)

add_definitions(-DNO_GLOBAL_CONTROLLER)
if (CUDAToolkit_VERSION VERSION_GREATER "11.0")
set(CMAKE_CUDA_ARCHITECTURES 70)
add_definitions(-DCUDA_ARCH_BIN=70)
set(CMAKE_CUDA_STANDARD 14)
else()
set(CMAKE_CUDA_ARCHITECTURES 50)
add_definitions(-DCUDA_ARCH_BIN=50)
set(CMAKE_CUDA_STANDARD 11)
endif()



add_library(${PROJECT_NAME} SHARED ${SOURCES})
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME ${PROJECT_NAME} PREFIX "" SUFFIX ".so")
set_target_properties(${PROJECT_NAME} PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
list(APPEND INCLUDES ${CUDA_INCLUDE_DIRS})
list(APPEND LIBRARIES ${CUDA_LIBRARIES})

find_package(Python3  REQUIRED COMPONENTS Development)
list(APPEND INCLUDES ${Python3_INCLUDE_DIRS})
list(APPEND LIBRARIES ${Python3_LIBRARIES})


include_directories(${INCLUDES})
target_link_libraries(${PROJECT_NAME} PUBLIC ${LIBRARIES})


