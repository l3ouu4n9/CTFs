
# Reasonable_Security_Ahead
## Description:
<div class="challenge-description">We have infiltrated the shadowy organization and set up a tunnel to their secret mainframe (<span style="color:red">nc chal.b01lers.com 25002</span>). Unfortunately, any server output is encrypted via plain RSA. All is not lost, however, because a trusted insider can provide temporary access to their test server (<span style="color:red">nc chal.b01lers.com 25001</span>). The test server has an additional feature that allows for toggling encryption on and off through a modified output function
<div class="bbcode_code">
<div class="bbcode_code_head">Code:</div>
<div class="bbcode_code_body" style="white-space:pre">   def output(self, msg):
       if self.debug: print(msg)
       else:          normal_encrypted_output(msg)</div>
</div>
Your mission, should you accept it, is to leverage the given access and extract the secret data from the mainframe within the next 48 hours. Time is critical, so manage resources wisely. This message will self-destruct in 5.. 4.. 3.. 2.. 1..<br/>
<br/>
<i>by dm</i></div>

