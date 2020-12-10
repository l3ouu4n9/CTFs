let submit_btn = document.getElementById('signUpSubmit');
let pwd = document.getElementById('passwordInput');
let div = document.getElementById('resultDiv');

var valid_pwd_regex = /^[a-z0-9]+$/;
 
submit_btn.addEventListener('click', function(){ 
    if (pwd.value.match(valid_pwd_regex) && pwd.value.length <= 14 && pwd.value.length >= 9) {
        div.innerHTML = "That password is valid!\nWe're not taking new members at the moment, but we'll get back to you.";
    } else {
	   div.innerHTML = "Invalid password!";
    }
});