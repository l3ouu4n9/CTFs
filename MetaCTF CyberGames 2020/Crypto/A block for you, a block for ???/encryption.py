import math

rounds = 16

# Blocks should be 64 bits and passwords 32 bits
def EncryptBlock(block, password):
    global rounds
    
    b64 = int(block.hex(), 16)
    password = int(password.hex(), 16) * 0x8D1B4035

    mask64 = (1 << 64) - 1
    mask32 = (1 << 32) - 1
    
    # Split the block into left and right halves
    left = b64 >> 32
    right = b64 & mask32
    
    for i in range(0, rounds):
        # Encrypt left half
        left = ((left << 19) | (left >> 13)) & mask32
        left ^= password >> 32
        left ^= right
        
        # Switch left and right
        tmp = right
        right = left
        left = tmp
        
        # Cycle password
        password = (password * 3 + 0x5812CE48F3A68B09) & mask64

    b64 = (left << 32) | right

    return (b64 & mask64).to_bytes(int(math.log2(b64) / 8 + 1), 'big')

def DecryptBlock(block, password):
    global rounds
    
    b64 = int(block.hex(), 16)
    pws = [int(password.hex(), 16) * 0x8D1B4035]

    mask64 = (1 << 64) - 1
    mask32 = (1 << 32) - 1
    
    # Precompute passwords
    for i in range(1, rounds):
        pws += [(pws[i - 1] * 3 + 0x5812CE48F3A68B09) & mask64]
    
    # Split the block into left and right halves
    left = b64 >> 32
    right = b64 & mask32
              
    for i in range(0, rounds):
        # Switch left and right
        tmp = right
        right = left
        left = tmp
        
        # Decrypt left half
        left ^= right
        left ^= pws[rounds - 1 - i] >> 32
        left = ((left >> 19) | (left << 13)) & mask32

    b64 = (left << 32) | right

    return (b64 & mask64).to_bytes(int(math.log2(b64) / 8 + 1), 'big')

def Encrypt(plaintext, password):
    
    # round up so nothing gets cut off
    block_count = int(math.ceil(float(len(plaintext) + 8) / 8))

    # Pad so that we don't cause errors
    plaintext += b'\x41' * (block_count * 8 - len(plaintext))
    
    ciphertext = b''
    
    # Encrypt each block
    for i in range(0, len(plaintext), 8):
        ciphertext += EncryptBlock(plaintext[i : i + 8], password)

    return ciphertext

def Decrypt(ciphertext, password):

    # No need for any rounding since we're guaranteed the ciphertext comes in
    # blocks of 8 bytes
    block_count = int(len(ciphertext) / 8)

    plaintext = b''

    # Decrypt each block
    for i in range(0, len(ciphertext), 8):
        plaintext += DecryptBlock(ciphertext[i : i + 8], password)

    return plaintext
