class User {
    #username; #theme; #img
    constructor(username, img, theme) {
        this.#username = username
        this.#theme = theme
        this.#img = img
    }
    get username() {
        return this.#username
    }

    get img() {
        return this.#img
    }

    get theme() {
        return this.#theme
    }

    toString() {
        return `user_${this.#username}`
    }
}

function make_user_object(obj) {

    const user = new User(obj.username, obj.img, obj.theme);
    window.load_debug?.(user);

    // make sure to not override anything
    if (!is_undefined(document[user.toString()])) {
        return false;
    }
    document.getElementById('profile-picture').src=user.img;
    window.USERNAME = user.toString();
    document[window.USERNAME] = user;
    update_theme();
}