// Check that the license is signed.
extern "C" bool CheckLicenseSignature(uint8_t* license_buf, int len)
{
	if (len < 16)
	{
		return false;
	}
	
	// Obviously, Z3, angr, KLEE, etc. won't solve this cryptosystem.
	uint8_t signature[16];
	GetKeySignature(&license_buf[0], signature);

	uint8_t hash[32];
	SHA256_CTX ctx;
	sha256_init(&ctx);
	sha256_update(&ctx, license_buf + 16, len - 16);
	sha256_final(&ctx, hash);

	return !memcmp(signature, hash, 16);
}
