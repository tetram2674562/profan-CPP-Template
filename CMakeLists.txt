cmake_minimum_required(VERSION 3.20)
project(PongPong C CXX)

set(PROFANLIB_DIR "${CMAKE_SOURCE_DIR}/3rdParty/profanOS")
set(PROFANOS_DIR "${CMAKE_SOURCE_DIR}/profanOS")

# Download all dependencies from profan and install them.
file(MAKE_DIRECTORY ${PROFANLIB_DIR}/headers)
# Libc
if(NOT EXISTS "${PROFANLIB_DIR}/libs/libc.a")
    # file(DOWNLOAD https://github.com/elydre/libatron/releases/download/latest/libc.so ${CMAKE_SOURCE_DIR}/3rdParty/profanOS/libc.so)
    file(DOWNLOAD https://github.com/elydre/libatron/releases/download/latest/libc.a ${PROFANLIB_DIR}/libs/libc.a)

    # Profan Headers
    file(DOWNLOAD https://github.com/elydre/libatron/releases/download/latest/profanOS_headers.tar.gz ${PROFANLIB_DIR}/profanOS_headers.tar.gz)
    file(ARCHIVE_EXTRACT
            INPUT ${PROFANLIB_DIR}/profanOS_headers.tar.gz
            DESTINATION ${PROFANLIB_DIR}/headers
    )
endif()


# Compiler with flags
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 98)
set(CMAKE_C_FLAGS "-m32 -march=i686 -ffreestanding -fno-exceptions -fno-stack-protector -nostdinc -nostdlib -Wundef -Wall -Wextra -D__profanOS__ -Werror")
set(CMAKE_CXX_FLAGS "-m32 -march=i686 -ffreestanding -fno-exceptions -fno-stack-protector -nostdinc -nostdlib -Wundef -Wall -Wextra -D__profanOS__ -Werror -fno-rtti")
set(CMAKE_EXE_LINKER_FLAGS "-Wl,-melf_i386 -nostdlib")
# Grab all the sources files !
file(GLOB_RECURSE SOURCES ${CMAKE_SOURCE_DIR}/src/**)
# Creation of the executable
add_executable(main ${PROFANOS_DIR}/tools/entry_elf.c ${SOURCES})

# Include profan system libs
target_include_directories(main PRIVATE ${PROFANLIB_DIR}/headers)
# Include our headers
target_include_directories(main PRIVATE ${CMAKE_SOURCE_DIR}/include)
# Use profanOS elf link script
target_link_options(main PRIVATE
        "-Wl,-T${PROFANOS_DIR}/tools/link_elf.ld"
)
# link with static profan libc
target_link_libraries(main PRIVATE ${PROFANLIB_DIR}/libs/libc.a)