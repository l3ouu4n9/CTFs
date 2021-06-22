"use strict";

const placeholders = [
    "Write something...",
    "Type something...",
    "Wow it's an inviting textarea",
    "I have an idea for what you should write! https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "uwu"
];

/**
 * @type {string | undefined}
 */
let publishID;

/**
 * @param {string} id 
 */
function updateDetails(id) {
    publishID = id;
    document.getElementById("outdated").style.display = "none";
    document.getElementById("id").innerText = id;
    document.getElementById("preview").setAttribute("href", "/page/" + encodeURIComponent(id));
    document.getElementById("submit-text").innerText = "You seem to be a good writer. Submit your page for a chance to win a flag!";
    document.getElementById("publish-details").classList.add("submitted");
}

async function publish() {
    const button = /** @type {HTMLButtonElement} */ (document.getElementById("publish"));
    button.disabled = true;
    document.getElementById("publish-details").classList.remove("submitted");
    publishID = undefined;
    document.getElementById("outdated").style.display = "none";

    const title = /** @type {HTMLInputElement} */ (document.getElementById("title"));
    const content = /** @type {HTMLTextAreaElement} */ (document.getElementById("content"));

    const response = await fetch("/publish", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            title: title.value,
            content: content.value
        })
    });
    const json = await response.json();

    button.disabled = false;
    if (json.id) {
        button.innerText = "Publish";
        updateDetails(json.id);
    } else {
        console.error("An error occurred. Please contact BCACTF staff.");
        button.innerText = "Error! Retry?";
    }
}

async function submit() {
    const button = /** @type {HTMLButtonElement} */ (document.getElementById("submit"));
    button.disabled = true;

    const text = document.getElementById("submit-text");
    text.innerText = "Submitting...";

    const response = await fetch("/visit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: publishID
        })
    });
    const json = await response.json();

    button.disabled = false;
    if (json.visited) {
        text.innerText = "Your submission has been viewed!";
    } else {
        text.innerText = "An error occurred.";
    }
}

window.addEventListener("DOMContentLoaded", _ => {
    const placeholder = placeholders[Math.floor(Math.random() * placeholders.length)];
    /** @type {HTMLTextAreaElement} */ (document.getElementById("content")).setAttribute("placeholder", placeholder);

    document.getElementById("publish").addEventListener("click", _ => {
        publish();
    });

    document.getElementById("submit").addEventListener("click", _ => {
        submit();
    });

    document.getElementById("content").addEventListener("change", _ => {
        if (publishID) {
            document.getElementById("outdated").style.display = "block";
        }
    });
});