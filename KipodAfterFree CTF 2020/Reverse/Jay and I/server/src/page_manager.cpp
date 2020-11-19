//
// Created by GUY on 08/10/2020.
//

#include <page_manager.h>
#include <fstream>

#include "../include/page_manager.h"

PageManager::PageManager() {
    this->add_page("home", "home.html");
    this->add_page("login", "login.html");
    this->add_page("oops", "error.html");
    this->add_page("success", "success.html");
}

void PageManager::add_page(const std::string &name, const std::string &filename, const std::string &extra_dir, const std::string &content) {
    // Get path to html files
    fs::path html_page_dir{fs::current_path()};
    html_page_dir = html_page_dir.parent_path() / "res" / "pages";

    if (!extra_dir.empty())
        html_page_dir = html_page_dir / extra_dir;


    // Get home page html path
    fs::path page_path{html_page_dir / filename};

    if (!content.empty()) {
        std::ofstream tmp_file;
        tmp_file.open (page_path.string());
        tmp_file << content;
        tmp_file.close();
    }
    auto new_page = std::make_unique<Page *>(new Page(page_path));
    this->pages[name] = std::move(new_page);
}

Page *PageManager::get_page(const std::string &name) {
    return *this->pages[name];
}

