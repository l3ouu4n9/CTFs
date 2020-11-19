//
// Created by GUY on 08/10/2020.
//
#include <memory>
#include <vector>
#include <map>
#include <queue>
#include "user.h"


#ifndef SERVER_USER_MANAGER_H
#define SERVER_USER_MANAGER_H

class UserManager{
private:
    std::vector < std::unique_ptr < User * >> users;
    std::map <std::string , std::queue<std::pair<FILE*, uintmax_t>*>*> alerts;

private:
    void initialize();

public:
    UserManager(size_t user_length): users{} {
        users.reserve(user_length);
        this->initialize();
    }
    ~UserManager() = default;

public:
    bool add_user(const std::string& name, const std::string& password, unsigned char favorite_num, unsigned short age, bool admin);

    [[maybe_unused]] void print_users();

public:
    bool remove_user(const std::string& name, const std::string& password);
    bool login_user(const std::string& name, const std::string& password);
    bool register_user(std::string name, const std::string& password, const std::string &favorite_num, const std::string& age);

public:
    void add_to_alert_queue(const std::string& target, FILE* tmpf, uintmax_t file_length);
    std::pair<FILE*, uintmax_t>* get_from_alert_queue(const std::string& target) {
        if (this->alerts.find(target) == this->alerts.end())
            return nullptr;
        auto alert_queue = this->alerts[target];
        if (alert_queue->empty())
            return nullptr;
        auto first = alert_queue->front();
        alert_queue->pop();
        return first;
    }
public:
    bool is_admin(const std::string& name);
    bool user_exists(const std::string& name);

public:
    std::ostringstream get_users(const std::string &username);

};


#endif //SERVER_USER_MANAGER_H
