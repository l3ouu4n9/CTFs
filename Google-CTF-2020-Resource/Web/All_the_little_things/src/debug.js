// Extend user object
function load_debug(user) {
    let debug;
    try {
        debug = JSON.parse(window.name);
    } catch (e) {
        return;
    }

    if (debug instanceof Object) {
        Object.assign(user, debug);
    }

    if(user.verbose){
        console.log(user);
    }

    if(user.showAll){
        document.querySelectorAll('*').forEach(e=>e.classList.add('display-block'));
    }

    if(user.keepDebug){
        document.querySelectorAll('a').forEach(e=>e.href=append_debug(e.href));
    }else{
        document.querySelectorAll('a').forEach(e=>e.href=remove_debug(e.href));
    }

    window.onerror = e =>alert(e);
}

function append_debug(u){
    const url = new URL(u);
    url.searchParams.append('__debug__', 1);
    return url.href;
}

function remove_debug(u){
    const url = new URL(u);
    url.searchParams.delete('__debug__');
    return url.href;
}