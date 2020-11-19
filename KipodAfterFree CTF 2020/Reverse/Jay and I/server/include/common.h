//
// Created by GUY on 08/10/2020.
//
#include <experimental/filesystem>

#ifndef SERVER_COMMON_H
#define SERVER_COMMON_H

namespace fs = std::experimental::filesystem;

void read_file(fs::path

& fname,
char *out
);

std::uintmax_t get_file_size(fs::path

&fname);

#endif //SERVER_COMMON_H
