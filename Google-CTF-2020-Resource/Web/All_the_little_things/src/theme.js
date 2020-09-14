function set_dark_theme(obj) {
    const theme_url = "/static/styles/bootstrap_dark.css";
    document.querySelector('#bootstrap-link').href = theme_url;
    localStorage['theme'] = theme_url;
}

function set_light_theme(obj) {
    theme_url = "/static/styles/bootstrap.css";
    document.querySelector('#bootstrap-link').href = theme_url;
    localStorage['theme'] = theme_url;
}

function update_theme() {
    const theme = document[USERNAME].theme;
    const s = document.createElement('script');
    s.src = `/theme?cb=${theme.cb}`;
    document.head.appendChild(s);
}

document.querySelector('#bootstrap-link').href = localStorage['theme'];