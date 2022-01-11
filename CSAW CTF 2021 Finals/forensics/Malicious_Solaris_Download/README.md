
# Malicious_Solaris_Download
## Description:
Attached is a malicious firmware updater package (blackthorn_fw_updater.msi) for some of legacy Solaris equipment. The package contains an ELF file that sends and modifies IEC104 traffic.

From the network traffic observed in iec104.pcap, it looks like it's just polling the controller for certain fields periodically, but the firmware does have the ability to change values at some point.

Can you figure out what `IOA` it tries to change, and what `value` it sets it to?

 Note: flag format: `IOA`=`Value` inside of the standard `flag{___}` syntax, e.g. `flag{101=0xaabbccdd}`.

Author: CISA

