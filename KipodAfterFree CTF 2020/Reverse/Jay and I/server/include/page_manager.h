//
// Created by GUY on 08/10/2020.
//
#include "page.h"
#include <memory>
#include <map>

#ifndef SERVER_PAGE_MANAGER_H
#define SERVER_PAGE_MANAGER_H


class PageManager {
private:
    std::map<std::string, std::unique_ptr<Page*>> pages;
        public:
        PageManager();
        ~PageManager() = default;

/*
 * Page functions
 */
        public:
        void add_page(const std::string& name, const std::string& filename, const std::string &extra_dir="", const std::string &content="");
        public:
        Page* get_page(const std::string& name);
};


#endif //SERVER_PAGE_MANAGER_H
