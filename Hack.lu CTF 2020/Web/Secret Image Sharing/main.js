// Event handler

addform.onsubmit = async (e) => {
    e.preventDefault()
    await addApi(text.value)
    let items = await getApi()
    displayAll(items)
    text.value = ''
}

searchform.onsubmit = async (e) => {
    e.preventDefault()
    displayAll(await searchApi(search.value))
}

uploadForm.onchange = async (e) => {
    // todo: add description
    await uploadApi(file1.files[0], '')
    let items = await getApi()
    await displayAll(items)
}

window.onload = async () => {
    let items = await getApi()
    await displayAll(items)
    if(location.hash.slice(1)){
        autoload(location.hash.slice(1))
    }
}

// API Calls

const addApi = async (text) => {
    await wrapFetch('/api/add', {
        method: 'POST',
        credentials: 'include',
        body: `text=${text}`,
        headers: {
            'Content-type': 'application/x-www-form-urlencoded',
        }
    })
}

const getApi = async () => {
    // no need for error handling so we use normal fetch
    return await fetch('/api/get', {
        method: 'GET',
        credentials: 'include',
    }).then(x => x.json())
}

const deleteApi = async (text) => {
    await wrapFetch(`/api/delete/${text}`, {
        method: 'DELETE',
        credentials: 'include',
    })
}

const searchApi = async (search) => {
    return await wrapFetch(`/api/search/${encodeURIComponent(search)}`, {
        method: 'POST',
        credentials: 'include',
    })
}

const imageApi = async (text) => {
    return await wrapFetch(`/api/image/${text}`, {
        method: 'GET',
        credentials: 'include',
    })
}

const uploadApi = async (file, description) => {
    let formData = new FormData()
    formData.append('file1', file)
    formData.append('description', description)
    return await wrapFetch(uploadForm.action, {
        method: 'PUT',
        credentials: 'include',
        body: formData
    })
}


const wrapFetch = (url, options) => {
    return fetch(url, options)
    .then(x => x.json())
    .then((j) => {
        console.log(j)
        j.error ? msg(j.error) : msg('')
        return j
    })
}

// Display functions

const displayAll = async (items) => {
    list.innerHTML = ''
    for(let {text} of items){
        displayItem(text)  
    }
}

const displayItem = (text) => {
    let li = document.createElement('li')
    li.classList.add('list-group-item')
    let span1 = document.createElement('span')

    span1.innerText = text
    span1.classList.add('clickable')
    span1.onclick = () => displayImage(text, li)
    li.appendChild(span1)

    let span2 = document.createElement('span')
    span2.innerText = 'x'
    span2.classList.add('float-right','clickable')
    span2.onclick = () => deleteItem(text)
    li.appendChild(span2)

    list.appendChild(li)
}

const msg = (m) => {
    msgbox.style.display = (m) ? "block" : "none"
    msgbox.innerHTML = m
}

const displayImage = async (text, ele) => {
    // hide
    if(ele.childElementCount === 3){
        location.hash = ''
        ele.lastChild.remove()
    }
    //show
    else{
        location.hash = text
        let {path} = await imageApi(text)
        if(path){
            let img = document.createElement('img')
            img.classList.add('rounded', 'mx-auto', 'd-block')
            img.src = path
            ele.appendChild(img)
        }
        else{
            let button = document.createElement('button')

            button.classList.add('btn','btn-primary','mx-auto', 'd-block')
            button.innerText = 'Upload Image'
            button.onclick = () => openUpload(text)
            ele.appendChild(button)
        }
    }

}

// utils

const autoload = (text) => {
    for (let li of list.children){
        if(li.firstElementChild.innerText === text){
            displayImage(text, li)
        }
    }
}

const openUpload = (text) => {
    uploadForm.action = `/api/image/${text}`
    file1.click()
}

const deleteItem = async (text) => {
    await deleteApi(text)
    let items = await getApi()
    displayAll(items)
}
