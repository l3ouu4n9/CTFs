
# Tar_Inspector
## Description:
My friend linked me this cool site. He said 
it's super secure so there's no way you could 
blindly break in.

[http://web2.utctf.live:8123/](http://web2.utctf.live:8123/)

_by mattyp_

Hint due to popular request:
```
# creates a secured version of the filename
def secure_filename(filename):
    # strip extension and any sneaky path traversal stuff
    filename = filename[:-4]
    filename = os.path.basename(filename)
    # escape shell metacharacters
    filename = re.sub("(!|\$|#|&|\"|\'|\(|\)|\||<|>|`|\\\|;)", r"\\\1", filename)
    filename = re.sub("\n", "", filename)
    # add extension
    filename += '__'+hex(randrange(10000000))[2:]+'.tar'
    return filename
```

