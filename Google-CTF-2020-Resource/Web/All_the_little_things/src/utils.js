// make sure that variable is undefined
function is_undefined(x) {
    return typeof x === "undefined" && x == undefined
}

window.addEventListener('DOMContentLoaded', ()=>{
    fetch('/me').then(e => e.json()).then(make_user_object);
})