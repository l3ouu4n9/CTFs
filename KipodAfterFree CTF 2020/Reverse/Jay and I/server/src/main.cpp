#include <httplib.h>
#include <iomanip>
#include "../include/page_manager.h"
#include "../include/user_manager.h"
#include "../include/base64.h"

#define PORT 12345
#define MAX_USERS XXXXX // Add how many users you want

std::ostream &operator<<(std::ostream &os, const std::multimap <std::string, std::string> &mmap) {
    unsigned int max = mmap.size();
    unsigned int cur = 0;
    for (const auto &i : mmap) {
        os << i.first << "=" << i.second;
        if (cur < max - 1)
            os << "&";

        ++cur;
    }
    return os;
}

constexpr uintmax_t chunk_size = 1024;

int main(int argc, char *argv[]) {

    const auto user_manager {std::make_shared<UserManager*>(new UserManager(MAX_USERS))};

    const auto &page_manager{std::make_shared<PageManager*>(new PageManager)};

    httplib::Server svr;

    svr.Get("/login", [user_manager, page_manager](const httplib::Request &req, httplib::Response &res) {
        std::string username{req.get_param_value("username")};
        std::string password{req.get_param_value("password")};
        Page *show_page;

        if (username.empty() || password.empty()) {
            res.status = 400;
            res.set_content("empty parameters", "text/html");
        } else if (!(*user_manager)->login_user(username, password)) {
            res.status = 404;
            res.set_content("bad credentials", "text/html");
        } else {
            res.status = 200;
            show_page = (*page_manager)->get_page("login");
            res.set_content(show_page->get_content(), "text/html");
        }
    });


    svr.Get("/users", [user_manager](const httplib::Request &req, httplib::Response &res) {
        std::string username{req.get_param_value("username")};
        std::string password{req.get_param_value("password")};
        std::ostringstream users;
        Page *show_page;


        if (username.empty() || password.empty()) {
            res.status = 400;
            res.set_content("empty parameters", "text/html");
        } else if (!(*user_manager)->login_user(username, password)) {
            res.status = 404;
            res.set_content("bad credentials", "text/html");
        } else if (!(*user_manager)->is_admin(username)) {
            res.status = 401;
            res.set_content("you must be an admin to do this", "text/html");
        } else {
            res.status = 200;
            users = (*user_manager)->get_users(username);
            res.set_content(users.str(), "text/html");
        }
    });

    svr.Get("/recv_image", [user_manager, page_manager](const httplib::Request &req, httplib::Response &res) {

        std::string username{req.get_param_value("username")};
        std::string password{req.get_param_value("password")};

        Page *show_page;

        if (username.empty() || password.empty()) {
            res.status = 400;
            res.set_content("empty parameters", "text/html");
        } else if (!(*user_manager)->login_user(username, password)) {
            res.status = 404;
            res.set_content("bad credentials", "text/html");
        } else {
            res.status = 200;

            // Add new page
            const auto& base64_img_pair = (*user_manager)->get_from_alert_queue(username);
            if (base64_img_pair == nullptr)
            {
                res.status = 404;
                res.set_content("no new messages for you", "text/html");
                return;
            }

            res.set_chunked_content_provider( "text/plain", [base64_img_pair](size_t offset, httplib::DataSink &sink) {
                if (offset < base64_img_pair->second) {
                    const auto buffer = new char[chunk_size + 1]{};
                    auto read_count = std::fread(buffer, 1, chunk_size, base64_img_pair->first);
                    if (read_count != EOF)
                        sink.write(buffer, read_count);
                    free(buffer);
                } else {
                    // Delete temporary file, and close stream
                    std::fclose(base64_img_pair->first);
                    sink.done();
                }
                return true;
            });
        }
    });


    svr.Post("/send_image", [user_manager, page_manager](const httplib::Request &req, httplib::Response &res) {

        std::string username{req.get_file_value("username").content};
        std::string password{req.get_file_value("password").content};
        std::string target{req.get_file_value("target").content};
        std::string image{req.get_file_value("image").content};
        Page *show_page;

        if (username.empty() || password.empty() || target.empty()) {
            res.status = 400;
            res.set_content("empty parameters", "text/html");
        } else if (!(*user_manager)->login_user(username, password)) {
            res.status = 404;
            res.set_content("bad credentials", "text/html");
        } else if (!(*user_manager)->is_admin(username)) {
            res.status = 401;
            res.set_content("you must be an admin to do this", "text/html");
        } else if (!(*user_manager)->user_exists(target)) {
            res.status = 404;
            res.set_content("the target user doesn't exist", "text/html");
        } else {
			res.status = 200;
            show_page = (*page_manager)->get_page("success");
            // Add new page
            std::FILE* tmpf = std::tmpfile();
            image.append(":");
            image.append(username);
            std::fputs(image.c_str(), tmpf);
            std::rewind(tmpf);
            (*user_manager)->add_to_alert_queue(target, tmpf, image.length());

            res.set_content(show_page->get_content(), "text/html");
        }

    });

    svr.Get("/register", [user_manager, page_manager](const httplib::Request &req, httplib::Response &res) {
        std::string username{req.get_param_value("username")};
        std::string password{req.get_param_value("password")};
        std::string age{req.get_param_value("age")};
        std::string favorite_num{req.get_param_value("favorite_num")};

        Page *show_page;

        if (username.empty() || password.empty() || favorite_num.empty() || age.empty()) {
            res.status = 400;
            res.set_content("empty parameters", "text/html");
        } else if (!(*user_manager)->register_user(username, password, favorite_num, age)) {
            res.status = 403;
            res.set_content("user exists", "text/html");
        } else {
            res.status = 200;
            show_page = (*page_manager)->get_page("home");
            res.set_content(show_page->get_content(), "text/html");
        }
    });

    svr.Get(R"(.*)", [](const httplib::Request &req, httplib::Response &res) {
        res.status = 404;
        res.set_content("Invalid endpoint", "text/html");
    });

    svr.set_logger([](const httplib::Request &req, const httplib::Response &res) {
        auto _time = time(0);
        char* p = ctime(&_time);
        p[strlen(p) - 1] = '\0';

        std::cout << "[" <<  p << "] ";
        std::cout << "[" << req.remote_addr << "] " << req.method << " " << req.path;

        if (!req.params.empty())
            std::cout << "?" << req.params;

        std::cout << " -> " << res.status;
        if (res.status / 200 != 1) {
            std::cout << " RETURN " << res.body;
        }
        std::cout << std::endl;
    });

    std::cout << "The server is running on port: " << std::to_string(PORT) << std::endl;

    svr.listen("0.0.0.0", PORT);
    return 0;
}
