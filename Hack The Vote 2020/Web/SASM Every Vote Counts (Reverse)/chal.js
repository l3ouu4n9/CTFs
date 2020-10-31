// Flags A and B can be gotten separately 

module.add_import(0, function() {
  // Flag 1 does not need admin
    fetch(
      '/flagA',
      {
        method: 'POST',
        body: decodeURI(location.hash.slice(1))
      } 
    )
    .then(x=>x.text())
    .then(x=>alert(x));
});
module.init();

function is_buffer_view(arr) {
  if (!(arr.buffer instanceof ArrayBuffer))
    return false;
}

function str_to_byte_arr(s) {
  return s.split('').map((x,y)=>s.charCodeAt(y)).concat([0]);
}

window.addEventListener('message', function(ev) {
  let data = ev.data;
    console.log("GOT",data)
  if (data.type == 'set_success_text') {

    let buffer = data.buffer;
    if (typeof(buffer) === 'string') {
      copy_string(str_to_byte_arr(buffer), buffer.length + 1);

    // Simple array buffer, access it as uint8
    } else if (buffer instanceof ArrayBuffer) {
      let acc = new Uint8Array(buffer);
      copy_string(acc, acc.length);

    // Simple typed array case (already uint8)
    } else if (buffer instanceof Uint8Array) {
      copy_string(buffer, buffer.length);

    // Any other typed array
    } else if (ArrayBuffer.isView(buffer)) {
      // Get the total size of the array (uint32 -> 4 uint8)
      let total_len = buffer.length * buffer.BYTES_PER_ELEMENT;
      
      // Make sure to get the offset correct for the underly buffer
      let acc = new Uint8Array(buffer.buffer, buffer.byte_offset);
      copy_string(acc, total_len);
    } else {
      throw("Invalid buffer sent");
    }
  }
  if (data.type == 'vote') {
    module.vote(data.vote);
  }
});

function copy_string(arr, len) {
  let max = module.get_max_length();
  if (len > max || len < 0) {
    throw("Input data too long");
  }
  module.io_buffer.set(arr);
  module.set_success_text(len);
}

iframe = document.createElement('iframe');
iframe.sandbox = 'allow-scripts'
if (location.hash.length < 2) {
  let html = `
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css">
  <script>
  top.postMessage({
    type:'set_success_text',
    // Thanks for voting!
    buffer:new Uint8Array([84,104,97,110,107,115,32,102,111,114,32,118,111,116,105,110,103,33,0])
  },'*');
  function vote() {
    let v = {};
    for(let r of document.forms[0].vote_opt) {
      if (r.checked)
        v.option = r.value;
      r.checked = false;
    }
    if (v.option === undefined)
      return false;
    top.postMessage({
      type: 'vote',
      vote: v,
    },'*');
    return false;
  }
  </script>
</head>
<body>
  <section class="section">
  <div class="container">
    <h1 class="title">Select Your Vote</h1>
    <form>
      <div class="control">
        <label class="radio">
          <input type="radio" name="vote_opt" value="GW">
          George Washington
        </label>
      </div>
      <div class="control">
        <label class="radio">
          <input type="radio" name="vote_opt" value="AL">
          Abe Lincoln
        </label>
      </div>
      <div class="control mt-3">
        <button onclick="return window.vote()" class="button is-fullwidth is-primary">Vote!</button>
      </div>
    </form>
  </div>

  </section>
</body>

</html>`
  location.hash = encodeURIComponent(JSON.stringify({html:html}));
  iframe.src = 'data:text/html,'+html
    document.body.appendChild(iframe);

}
let input = JSON.parse(decodeURIComponent(location.hash.slice(1)));

if (input.html)
{
  iframe.src = 'data:text/html,' + input.html;
  document.body.appendChild(iframe);
} else {
  module.vote(input);
}

// Flag B is at /flagB for the admin