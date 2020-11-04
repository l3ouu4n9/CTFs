import random

def checkPassword(password):
    if(len(password) != 43):
      return False
    if(password[26] == 'r' and 
      password[33] == 't' and 
      password[32] == '3' and 
      password[16] == '3' and 
      password[4] == 'F' and 
      password[21] == 'r' and 
      password[38] == '1' and 
      password[18] == 'c' and 
      password[22] == '@' and 
      password[31] == 'g' and 
      password[7] == 'u' and 
      password[0] == 'C' and 
      password[6] == 'p' and 
      password[39] == '3' and 
      password[3] == 'T' and 
      password[25] == '3' and 
      password[29] == 't' and 
      password[42] == '}' and 
      password[12] == 'g' and 
      password[23] == 'c' and 
      password[30] == '0' and 
      password[40] == '3' and 
      password[28] == '_' and 
      password[20] == '@' and 
      password[27] == '$' and 
      password[17] == '_' and 
      password[35] == '3' and 
      password[8] == '7' and 
      password[24] == 't' and 
      password[41] == '7' and 
      password[13] == '_' and 
      password[5] == '{' and 
      password[2] == 'C' and 
      password[11] == 'n' and 
      password[9] == '7' and 
      password[15] == 'h' and 
      password[34] == 'h' and 
      password[1] == 'Y' and 
      password[10] == '1' and 
      password[37] == '_' and 
      password[14] == 't' and 
      password[36] == 'r' and 
      password[19] == 'h'):
      return True
    return False

password = input("Enter password: ")
if(checkPassword(password)):
  print("PASSWORD ACCEPTED\n")
else:
  print("PASSWORD DENIED\n")



