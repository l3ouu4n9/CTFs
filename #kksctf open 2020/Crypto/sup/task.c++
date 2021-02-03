#include "3412++.h++"
#include <sstream>
#include <iostream>
#include <cassert>
#include <cstring>
#include <iomanip>

// reversed byte order, see gost3412
std::vector<uint8_t> hex_to_vector (const char* inp)
{
    std::vector<uint8_t> out;
    char temp[3];
    for (int i = 0; (inp[i] != 0 && inp[i+1] != 0); i += 2)
    {
        temp[0] = inp[i];
        temp[1] = inp[i+1];
        temp[2] = 0;
        out.insert(out.begin(), strtol(temp, NULL, 16));
    }
    return out;
}

std::string hex_vector (const std::vector<uint8_t> a) {
    auto ai = a.begin();
    std::stringstream ss;
    for (; ai != a.end(); ++ai)
    {
        ss << std::setw(2) << std::setfill('0') << std::hex << (int)*ai;
    }
    return ss.str();
}

int main (void)
{
    kks3412::lib_init();

    const char* hexflag = "REDACTED";
    assert(strlen(hexflag) == 64);

    kks3412::set_key(hex_to_vector(hexflag).data());

    std::vector<uint8_t> data = hex_to_vector("cabbccddeeff00112233445566778899aababbccddeeff00112233445566778899aabbccddeeff00112233445566778899");

    std::cout << hex_vector(data) << std::endl;
    kks3412::encrypt_block(data.data());
    kks3412::encrypt_block(data.data()+16);
    kks3412::encrypt_block(data.data()+32);

    std::cout << hex_vector(data) << std::endl;
    kks3412::decrypt_block(data.data());
    kks3412::decrypt_block(data.data()+16);
    kks3412::encrypt_block(data.data()+32);

    std::cout << hex_vector(data) << std::endl;

    kks3412::lib_fin();
    return 0;
}
