//
// Created by GUY on 08/10/2020.
//

#ifndef SERVER_USER_H
#define SERVER_USER_H

#include <string>
#include <ostream>
#include <cstring>


/* TODO: not quite sure what "structure packing" is, but I think
 *  I should add it someday.
 */
class User{
        private:
        unsigned char favorite_num;
        unsigned short age;

        // Returns whether the user is an admin
        unsigned char admin;
        char name[24];
        char password[24];

        private:
        void memset_strip_newline (const std::string& name);

        public:
        User(const std::string& _name, const std::string& _password, unsigned char _favorite_num, unsigned short _age, bool _admin);
        ~User() = default;

        public:
        inline bool is_admin() const {
            return this->admin == 1;
        }

        inline std::string get_name() const { return std::string(this->name); }
        inline std::string get_password() const { return std::string(this->password); }

        public:
        friend std::ostream& operator<<(std::ostream& out, User user);
};


#endif //SERVER_USER_H
