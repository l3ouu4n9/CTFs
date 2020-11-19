//
// Created by GUY on 08/10/2020.
//

#include "../include/page.h"
#include <fstream>
#include <iostream>


Page::Page(fs::path &fname) {
    std::uintmax_t file_size{get_file_size(fname)};
    this->content_len = file_size;
    this->content = std::make_unique<char *>(new char[file_size + 1]());
    read_file(fname, *this->content);
}
