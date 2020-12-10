with open("8_of_hearts.enc", "rb") as input:
    with open("8_of_hearts.png","ab") as output:
        while 1:
            byte_s = input.read(1)
            if not byte_s:
                break
            output.write(bytes([byte_s[0] ^ 0x41]))