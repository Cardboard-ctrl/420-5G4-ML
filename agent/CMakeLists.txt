cmake_minimum_required(VERSION 3.21)
project(bibliotheque LANGUAGES CXX)

# Specifie qu'on veut la version C++17 du langage
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED YES)
set(CMAKE_CXX_EXTENSIONS NO)

# Bibliotheque du coeur, partagee entre l'application et le module Python
add_library(biblio_core STATIC
    book.cpp
    user.cpp
    library.cpp
    filemanager.cpp
)
target_include_directories(biblio_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
set_target_properties(biblio_core PROPERTIES POSITION_INDEPENDENT_CODE ON)
# flag pour tous les warnings possible
target_compile_options(biblio_core PRIVATE -Wall -Wextra -Wpedantic)

# Application en ligne de commande
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE biblio_core)
target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic)

# Module Python (pybind11)
option(BUILD_PYTHON_BINDINGS "Construire le module Python bibliotheque_py" ON)
if(BUILD_PYTHON_BINDINGS)
    find_package(pybind11 CONFIG REQUIRED)
    pybind11_add_module(bibliotheque_py bindings/bindings.cpp)
    target_link_libraries(bibliotheque_py PRIVATE biblio_core)
    target_compile_options(bibliotheque_py PRIVATE -Wall -Wextra -Wpedantic)
    set_target_properties(bibliotheque_py PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
    )
endif()
