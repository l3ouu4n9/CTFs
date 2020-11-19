//
// Created by GUY on 08/10/2020.
//

#include <iostream>
#include <fstream>
#include "../include/common.h"

void read_file(fs::path &fname, char *out) {
    std::fstream page_file{fname.c_str()};
    std::uintmax_t file_size;

    if (!page_file) {
        std::ostringstream error_stream;
        error_stream << "Could not open handle to page: " << fname.string() << std::endl;
        throw fs::filesystem_error{error_stream.str(), std::make_error_code(std::errc::bad_file_descriptor)};
    }

    file_size = get_file_size(fname);

    page_file.read(out, file_size);

    page_file.close();
}

std::uintmax_t get_file_size(fs::path &fname) {
    std::error_code error_code;
    std::uintmax_t file_size;

    file_size = fs::file_size(fname, error_code);

    if (error_code.value() != 0) {
        std::ostringstream error_stream;
        error_stream << "Could not get page size: " << fname << std::endl;
        throw fs::filesystem_error{error_stream.str(), error_code};
    }

    return file_size;
}
