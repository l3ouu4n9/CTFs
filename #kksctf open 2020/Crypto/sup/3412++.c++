#include "3412++.h++"

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1

namespace kks3412 {

static const uint8_t gost_pi[256] =
{
    252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77,
    233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193,
    249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79,
    5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31,
    235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204,
    181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135,
    21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177,
    50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87,
    223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3,
    224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74,
    167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65,
    173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59,
    7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137,
    225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97,
    32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82,
    89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182
};

static const uint8_t gost_inv_pi[256] =
{
    165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158, 57, 85, 126, 82, 145,
    100, 3, 87, 90, 28, 96, 7, 24, 33, 114, 168, 209, 41, 198, 164, 63,
    224, 39, 141, 12, 130, 234, 174, 180, 154, 99, 73, 229, 66, 228, 21, 183,
    200, 6, 112, 157, 65, 117, 25, 201, 170, 252, 77, 191, 42, 115, 132, 213,
    195, 175, 43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212, 15, 156, 47,
    155, 67, 239, 217, 121, 182, 83, 127, 193, 240, 35, 231, 37, 94, 181, 30,
    162, 223, 166, 254, 172, 34, 249, 226, 74, 188, 53, 202, 238, 120, 5, 107,
    81, 225, 89, 163, 242, 113, 86, 17, 106, 137, 148, 101, 140, 187, 119, 60,
    123, 40, 171, 210, 49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46, 54,
    219, 105, 179, 20, 149, 190, 98, 161, 59, 22, 102, 233, 92, 108, 109, 173,
    55, 97, 75, 185, 227, 186, 241, 160, 133, 131, 218, 71, 197, 176, 51, 250,
    150, 111, 110, 194, 246, 80, 255, 93, 169, 142, 23, 27, 151, 125, 236, 88,
    247, 31, 251, 124, 9, 13, 122, 103, 69, 135, 220, 232, 79, 29, 78, 4,
    235, 248, 243, 62, 61, 189, 138, 136, 221, 205, 11, 19, 152, 2, 147, 128,
    144, 208, 36, 52, 203, 237, 244, 206, 153, 16, 68, 64, 146, 58, 1, 38,
    18, 26, 72, 104, 245, 129, 139, 199, 214, 32, 10, 8, 0, 76, 215, 116
};

static const uint8_t gost_lvec[16] =
{
    0x94, 0x20, 0x85, 0x10, 0xc2, 0xc0, 0x1, 0xfb, 0x1, 0xc0, 0xc2, 0x10, 0x85, 0x20, 0x94
};

static uint8_t k[10][16];
static uint8_t gf256_mul_table[256][256];

static bool is_init = false;
static bool is_key_set = false;

// https://github.com/mjosaarinen/kuznechik/blob/master/kuznechik_8bit.c
static uint8_t mul_gf256 (uint8_t x, uint8_t y)
{
    uint8_t z;

    z = 0;
    while (y) {
        if (y & 1)
            z ^= x;
        x = (x << 1) ^ (x & 0x80 ? 0xC3 : 0x00);
        y >>= 1;
    }

    return z;
}

static void do_x (const uint8_t* iv, const uint8_t* ki, uint8_t* ov)
{
    for (int i = 0; i < 16; i++)
    {
        ov[i] = iv[i]^ki[i];
    }
}

static void do_s (const uint8_t* iv, uint8_t* ov)
{
    return;
    for (int i = 0; i < 16; i++)
    {
       ov[i] = gost_pi[iv[i]];
    }
}

static void do_inv_s (const uint8_t* iv, uint8_t* ov)
{
    return;
    for (int i = 0; i < 16; i++)
    {
        ov[i] = gost_inv_pi[iv[i]];
    }
}

static void do_r (const uint8_t* iv, uint8_t* ov)
{
    if (!is_init) return;
    uint8_t x = iv[0];
    for (int idx = 1; idx < 16; idx++)
    {
        x ^= gf256_mul_table[iv[idx]][gost_lvec[idx-1]];
        ov[idx-1] = iv[idx];
    }
    ov[15] = x;
}

static void do_inv_r (const uint8_t* iv, uint8_t* ov)
{
    if (!is_init) return;
    uint8_t x = iv[15];
    for (int idx = 14; idx >= 0; idx--)
    {
        x ^= gf256_mul_table[iv[idx]][gost_lvec[idx]];
        ov[idx+1] = iv[idx];
    }
    ov[0] = x;
}

static void do_l (const uint8_t* iv, uint8_t* ov)
{
    std::copy(iv, iv+16, ov);
    for (int round = 0; round < 16; round++) do_r(ov, ov);
}

static void do_inv_l (const uint8_t* iv, uint8_t* ov)
{
    std::copy(iv, iv+16, ov);
    for (int round = 0; round < 16; round++) do_inv_r(ov, ov);
}

static void do_f (uint8_t idx, uint8_t* a1, uint8_t* a0)
{
    uint8_t temp[16] = {0};
    uint8_t ci[16] = {0};
    ci[0] = idx;

    do_l(ci, ci);  // Generate iteration constant (Ci)

    do_x(a1, ci, temp);  // temp = a1^ci
    do_s(temp, temp);  // temp = s(temp)
    do_l(temp, temp);  // temp = l(temp)
    do_x(a0, temp, temp);  // temp ^= a0

    std::copy(a1, a1+16, a0);
    std::copy(temp, temp+16, a1);
}

static void split_key (const uint8_t* key, uint8_t* k1, uint8_t* k2)
{
    std::copy(key+16, key+32, k1);
    std::copy(key, key+16, k2);
}

int lib_init (void)
{
    if (is_init) return EXIT_FAILURE;

    // Fill multiplication table
    for (int i = 0; i < 256; i++)
    {
        for (int j = 0; j < 256; j++)
        {
            gf256_mul_table[i][j] = mul_gf256(i, j);
        }
    }

    kks3412::del_key(); // make sure that key is zeroed

    is_init = true;
    return EXIT_SUCCESS;
}

void lib_fin (void)
{
    if (!is_init) return;
    if (is_key_set) kks3412::del_key();

    is_init = false;
}

void set_key (const uint8_t* key)
{
    if (is_key_set) return;

    uint8_t k1[16];
    uint8_t k2[16];

    split_key(key, k1, k2);

    for (int i = 0; i <= 32; i++)
    {
        if ((i & 7) == 0)
        {
            std::copy(k1, k1+16, k[i >> 2]);
            std::copy(k2, k2+16, k[(i >> 2) + 1]);
        }
        do_f(i+1, k1, k2);
    }

    is_key_set = true;
}

void del_key (void)
{
    for (int i = 0; i < 10; ++i)
    {
        for (int j = 0; j < 16; ++j)
        {
            k[i][j] = 0x00;
        }
    }

    is_key_set = false;
}

void encrypt_block (uint8_t* data)
{
    if (!(is_key_set && is_init)) return;

    for (int i = 0; i < 9; i++)
    {
        do_x(data, k[i], data);
        do_s(data, data);
        do_l(data, data);
    }
    do_x(data, k[9], data);
}

void decrypt_block (uint8_t *data)
{
    if (!is_key_set || !is_init) return;

    do_x(data, k[9], data);
    for (int i = 8; i >= 0; i--)
    {
        do_inv_l(data, data);
        do_inv_s(data, data);
        do_x(data, k[i], data);
    }
}

} /* namespace kks3412 */
