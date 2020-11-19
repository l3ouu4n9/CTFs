//
// Created by GUY on 08/10/2020.
//

#include <iostream>
#include <experimental/filesystem>
#include "../include/user_manager.h"
#include "../include/common.h"
#include <boost/algorithm/string.hpp>

bool UserManager::add_user(const std::string &name, const std::string &password, unsigned char favorite_num, unsigned short age, bool admin) {
    if (users.capacity() <= users.size())
        return false;
    try {
        users.insert(users.begin(), std::make_unique<User *>(new User{name, password, favorite_num, age, admin}));
    } catch (const std::exception& e) {
        return false;
    }
    return true;
}

[[maybe_unused]] void UserManager::print_users() {
    for (auto &e : users) {
        if (e == nullptr)
            continue;
        auto user = static_cast<User *>(*e);
        std::cout << *user << std::endl;
    }
}

void UserManager::initialize() {
    namespace fs = std::experimental::filesystem;

    auto cur_dir{fs::current_path()};
    auto users_path = cur_dir.parent_path() / "res" / "users" / "users.txt";

    std::uintmax_t file_size{get_file_size(users_path)};

    auto users_content = new char[file_size + 1]{};
    read_file(users_path, users_content);

    std::vector <std::string> split_lines;

    boost::split(split_lines, users_content, boost::is_any_of("\n"));

    for (auto &line : split_lines) {
        std::vector <std::string> split_commas;
        boost::split(split_commas, line, boost::is_any_of(","));

        if (split_commas.size() != 5) {
            std::ostringstream error_stream;
            error_stream << "Not enough columns in users.txt: " << line << std::endl;
            throw std::out_of_range{error_stream.str()};
        }
        auto age = static_cast<unsigned short>(std::stoi(split_commas[3]));
        auto favorite_num = static_cast<unsigned char>(std::stoi(split_commas[2]));
        this->add_user(split_commas[0], split_commas[1], favorite_num, age,
                       boost::algorithm::to_lower_copy(split_commas[4]) == "true");
    }
}

bool UserManager::remove_user(const std::string &name, const std::string &password) {
    for (auto i = this->users.begin(); i < this->users.end(); ++i) {
        User *user = **i;
        if (user == nullptr)
            continue;

        if (user->get_name() == name) {
            if (user->get_password() == password) {
                this->users.erase(i);
                return true;
            }

            return false;
        }
    }

    return false;
}

bool UserManager::login_user(const std::string &name, const std::string &password) {
    for (auto &cur : this->users) {
        auto user = static_cast<User *>(*cur);
        if (user->get_name() == name) {
            return user->get_password() == password;
        }
    }
    // Couldn't find user
    return false;
}

bool UserManager::register_user(std::string name, const std::string &password, const std::string &favorite_num, const std::string &age) {
    for (auto &cur : this->users) {
        auto user = static_cast<User *>(*cur);

        if (user->get_name() == name) {
            // Found user. Can't register again
            return false;
        }
    }

    auto _favorite_num = static_cast<unsigned short>(std::stoi(age));
    auto _age = static_cast<unsigned short>(std::stoi(age));

    this->add_user(name, password, _favorite_num, _age, false);
    return true;
}

bool UserManager::is_admin(const std::string &name) {
    for (auto &cur : this->users) {
        auto user = static_cast<User *>(*cur);
        if (user->get_name() == name) {
            return user->is_admin();
        }
    }
    // Couldn't find user
    return false;
}

std::ostringstream UserManager::get_users(const std::string &username) {
    std::ostringstream out;
    unsigned int max = this->users.size();
    unsigned int cur_index = 0;

    for (auto &cur : this->users) {
        auto user = static_cast<User *>(*cur);
        std::string name = user->get_name();
		
		// Add user to name list
		out << name;
		if (cur_index < max - 1)
			out << ",";

        ++cur_index;
    }

    return out;
}

bool UserManager::user_exists(const std::string& name) {
    for (auto &cur : this->users) {
        auto user = static_cast<User *>(*cur);

        if (user->get_name() == name) {
			// Found user
            return true;
		}
    }
    return false;
}

void UserManager::add_to_alert_queue(const std::string &target, FILE *tmpf, uintmax_t file_length) {
    auto target_user = this->alerts.find(target);
    if (target_user == this->alerts.end()) {
        // Create user alert queue
        auto alert_queue = new std::queue<std::pair<FILE *, uintmax_t> *>();
        this->alerts[target] = static_cast<std::queue<std::pair<FILE *, uintmax_t> *> *>(alert_queue);
    }

    this->alerts[target]->push(new std::pair(tmpf, file_length));
}

