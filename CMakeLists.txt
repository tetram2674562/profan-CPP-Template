cmake_minimum_required(VERSION 3.20)
project(TEMPLATE C CXX)

set(PROFANLIB_DIR "${CMAKE_SOURCE_DIR}/3rdParty/profanOS")
set(PROFANOS_DIR "${CMAKE_SOURCE_DIR}/profanOS")

# Download all dependencies from profan and install them.
file(MAKE_DIRECTORY ${PROFANLIB_DIR}/libc/headers)
# Libc
if (NOT EXISTS "${PROFANLIB_DIR}/libs/libc.a")
    # file(DOWNLOAD https://github.com/elydre/libatron/releases/download/latest/libc.so ${CMAKE_SOURCE_DIR}/3rdParty/profanOS/libc.so)
    file(DOWNLOAD https://github.com/elydre/libatron/releases/download/latest/libc.a ${PROFANLIB_DIR}/libc/libs/libc.a)

    # Profan Headers
    file(DOWNLOAD https://github.com/elydre/libatron/releases/download/latest/profanOS_headers.tar.gz ${PROFANLIB_DIR}/libc/profanOS_headers.tar.gz)
    file(ARCHIVE_EXTRACT
            INPUT ${PROFANLIB_DIR}/libc/profanOS_headers.tar.gz
            DESTINATION ${PROFANLIB_DIR}/libc/headers
    )
endif ()

# libpthread
file(DOWNLOAD https://github.com/elydre/libatron/releases/download/latest/libpthread.a ${PROFANLIB_DIR}/libstdcpp/libs/libpthread.a)
# libgcc (invalid for now)
# file(DOWNLOAD https://github.com/elydre/libatron/releases/download/latest/libgcc.a ${PROFANLIB_DIR}/libstdcpp/libs/libgcc.a)

# Compiler with flags
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 98)
# Exception not working yet D:
set(CMAKE_C_FLAGS "-m32 -march=i686 -ffreestanding -fno-exceptions -fno-gnu-tm -nostdinc -nostdlib -Wundef -Wall -Wextra -D__profanOS__ -Werror -fno-stack-protector")
set(CMAKE_CXX_FLAGS "-m32 -march=i686 -ffreestanding -fno-exceptions -fno-gnu-tm -nostdinc -nostdlib -Wundef -Wall -Wextra -D__profanOS__ -Werror -fno-stack-protector -fno-threadsafe-statics -fno-unwind-tables -fno-asynchronous-unwind-tables -fno-use-cxa-atexit")
set(CMAKE_EXE_LINKER_FLAGS "-Wl,-melf_i386 -nostdlib")
# Grab all the sources files !
file(GLOB_RECURSE SOURCES ${CMAKE_SOURCE_DIR}/src/**)
# Creation of the executable
add_executable(main ${PROFANOS_DIR}/tools/entry_elf.c ${SOURCES})

# Include profan system libs
target_include_directories(main PRIVATE ${PROFANLIB_DIR}/libc/headers)  # libc
target_include_directories(main PRIVATE ${PROFANLIB_DIR}/libstdcpp/headers) # libstdc++
target_include_directories(main PRIVATE ${PROFANLIB_DIR}/libstdcpp/headers/i686-bsd) # libstdc++
# Include our headers
target_include_directories(main PRIVATE ${CMAKE_SOURCE_DIR}/include)

# Use profanOS elf link script
target_link_options(main PRIVATE
        "-Wl,-T${PROFANOS_DIR}/tools/link_elf.ld"
)

# link with static profan libc
# https://stackoverflow.com/questions/45135/why-does-the-order-in-which-libraries-are-linked-sometimes-cause-errors-in-gcc/409470#409470
# Linking them in the correct order
target_link_libraries(main PRIVATE
        -Wl,--start-group
        ${PROFANLIB_DIR}/libstdcpp/libs/libstdc++.a
        ${PROFANLIB_DIR}/libc/libs/libc.a
        ${PROFANLIB_DIR}/libstdcpp/libs/libpthread.a
        ${PROFANLIB_DIR}/libstdcpp/libs/libgcc.a
        -Wl,--end-group
)


# Addons

set(THIRDPARTY_DIR ${CMAKE_SOURCE_DIR}/3rdParty)

file(GLOB LIB_DIRS
        RELATIVE ${THIRDPARTY_DIR}
        ${THIRDPARTY_DIR}/*
)
foreach (lib ${LIB_DIRS})
    if (lib STREQUAL "profanOS")
        continue()
    endif ()
    set(LIB_PATH "${THIRDPARTY_DIR}/${lib}")
    if (IS_DIRECTORY "${LIB_PATH}")
        if (EXISTS "${LIB_PATH}/headers")
            target_include_directories(main PRIVATE "${LIB_PATH}/headers")
        endif ()
        file(GLOB LIB_FILES "${LIB_PATH}/*.a" "${LIB_PATH}/*.so")
        if (LIB_FILES)
            target_link_libraries(main PRIVATE ${LIB_FILES})
        endif ()
    endif ()
endforeach ()