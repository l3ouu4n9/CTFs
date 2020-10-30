(async () => {
    const urlParams = new URLSearchParams(location.search)
    let src = urlParams.get('src') ? urlParams.get('src') : 'sandbox.html'
    // make sure its up
    try{
        await fetch(src, {mode: 'no-cors', cache: 'no-cache'})
    }
    catch(e){
        console.log('noooo hecking')
        return
    }
    litterbox.src = src   
})()