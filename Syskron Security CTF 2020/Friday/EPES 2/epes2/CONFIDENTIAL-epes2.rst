============
[CONFIDENTIAL] EPES2
============

***************
Purpose of the document
***************
This document describes the Enhanced PLC Encryption Standard 2 (EPES2), © 2020 BB Industry a.s.

***************
Company-wide standards for crypto
***************
* The Information Security Policy of BB Industry a.s. applies. Especially, the "Working Instruction: Deployment of cryptographic algorithms" needs to be considered.
* For EPES2, key derivation according to RFC 7914 is used. The LibrePLC crypto module uses the defaults for better security: N=16384, r=8, p=1, dkLen=64.
* The LibrePLC crypto module supports the Advanced Encryption Standard (AES; ISO/IEC 18033-3) for encryption. The keys are generated using RFC 6238. Valid key sizes are 128 or 192 bits.
* The LibrePLC crypto module uses MessagePack for data exchange on port 62011/udp.

***************
Device setup
***************
* On each PLC, the LibrePLC crypto module is configured in the file "libreplc-config.json." During the first setup, the BB service sets the device ID and the PLC's private key.
* For every other PLC on the production line that needs to communicate with the PLC, the corresponding private key is set in "libreplc-config-shared-keys.json." The last two digits are omitted.
* Each PLC must be synchronized. For this, the LibrePLC crypto module uses IEEE 1588-2019. IEEE 1588-2019 is set up in the "ptp-config.json."
* The network configuration file "if-config.json" maps device IDs onto IP addresses. 

***************
Communication process
***************

A. Start of connection stream
===============
1. The initiator (in the following "PLC1") sends a handshake (SYN) to the destination device (in the following "PLC2"). The handshake includes the protocol (epes), the protocol version (e.g., 2), the protocol message (here "SYN"), a random salt for RFC 7914, the HMAC size for RFC 6238, the AES key size, a random IV for AES, and the mode of operation of AES.
2. PLC2 answers with "ACK" if it can process messages. If message processing isn't available, PLC2 answers with "RST."
3. PLC1 receives the message. If "ACK" is received, PLC1 and PLC2 proceed to key derivation. If "RST" is received, PLC1 terminates the connection.

B. Key derivation (shared secret)
===============
1. After sending "ACK", PLC2 starts to derive the shared key. PLC1 starts the key derivation after receiving "ACK."
2. Each device looks up the corresponding key of the other PLC in "libreplc-config-shared-keys.json." If no key is configured, the communication is aborted for security reasons.
3. Each device concatenates its own secret key and the other device's secret key and uses this as the input for RFC 7914. The secret key of the device with the lower device ID comes first. Example: B000 and B001 derive the shared key. B000 < B001. This means the shared key is KDF(B000B001).

C. Encrypted message exchange
===============
1. For each message, the sender uses RFC 6238 to generate an ephemeral key. The input is the shared secret (see B). The output is an 8-digit key. The HMAC size for RFC 6238 is defined in the handshake (see A).
2. The sender uses the ephemeral key (UTF-8) and the AES parameters (see A) to encrypt the message. For AES-128, the ephemeral key is stretched by duplication, resulting in a 16-digit key. For AES-192, the key is stretched to 24 digits.
3. The sender sends the encrypted message and the epoch timestamp for validation.
4. The receiver checks the epoch timestamp. If it deviates more than 5 seconds from the receiver's current time, the communication is aborted. If the deviation is less than 5 seconds, the receiver conducts the same steps to decrypt the message.

D. End of connection stream
===============
1. After transmitting all data, PLC1 sends a "CLO" message to PLC2.
2. PLC2 answers with "CLO."
3. Both PLCs end the connection.
