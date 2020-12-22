function addnote(filename){
    let div = document.createElement("div")
    let a = document.createElement("a");
    a.innerText = filename;
    a.href = `/note/${filename}`;
    div.appendChild(a);
    notes.appendChild(div);
}   

fetch("/flag",{"method":"POST","headers":{"X-I-Want":"flag"}}).then((r)=>{
    r.json().then((r)=>{
        flag.innerHTML = `FLAG: ${r.data}`;
    });
});

fetch("/notes_list.json").then((r)=>{
    r.json().then((r)=>{
        r.forEach(addnote);
    });
});