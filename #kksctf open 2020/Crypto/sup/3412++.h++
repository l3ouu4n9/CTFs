#pragma once

#include <cstdlib>
#include <cstdint>
#include <vector>

namespace kks3412 {

    /* Init multiplication table and other constants */
    int lib_init (void);

    /* Free memory after use */
    void lib_fin (void);

    /* Set encryption key */
    void set_key (const uint8_t* key);

    /* Delete encryption key */
    void del_key (void);

    /* Encrypt 128-bit block of data */
    void encrypt_block (uint8_t* data);

    /* Decrypt 128-bit block of data */
    void decrypt_block (uint8_t* data);

}