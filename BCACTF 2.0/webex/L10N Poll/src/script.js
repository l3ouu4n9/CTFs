async function localisePage() {
    const response = await fetch("/localisation-file");
    const strings = await response.json();
    ["question", "y", "n", "language"].forEach(key => {
        document.getElementById(key).innerText = strings[key];
    });
    document.querySelector("html").setAttribute("dir", strings.direction);
    document.body.style.display = "block";

    const languagesResponse = await fetch("/languages");
    const languages = await languagesResponse.json();
    const menu = document.getElementById("languages");
    languages.forEach(language => {
        const option = document.createElement("option");
        option.setAttribute("value", language.id);
        option.innerText = language.name;
        menu.appendChild(option);
    });
}

/**
 * @param {Array<number>} votes
 */
function populate(votes) {
    votes.forEach((val, idx) => {
        document.getElementById(`v${idx}`).innerText = val.toString();
    });
}

window.addEventListener("load", _ => {
    localisePage();
    document.getElementById("languages").addEventListener("change", e => {
        const menu = /** @type {HTMLSelectElement} */ (document.getElementById("languages"));
        if (menu.value !== "none") {
            const form = /** @type {HTMLFormElement} */ (document.getElementById("form"));
            form.submit();
        }
    });
    ["y", "n"].forEach(letter => {
        document.getElementById(letter).addEventListener("click", async e => {
            const response = await fetch(`/${letter}`, {method: "POST"});
            populate(await response.json());
            ["y", "n"].forEach(letter => {
                document.getElementById(letter).setAttribute("disabled", "true");
            });
        });
    });
});