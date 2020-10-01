# Swipe
Whoops, I accidentally right-swiped on something I didn't mean to. Now I have this weird file?

## Description
There is a file `swipe` on the server, and it contains gibberish.

## Writeup
1. From `xxd swipe`, I got `b0VIM` at the beginning, which means it is a vim swap file.
2. I write the output of `cat swipe | base64` to a file `swipe_b64`, and `cat swipe_b64 | base64 -D > .swipe.swp`
3. I recovered it with `vim -r .swipe.swp`, and `:wq`, it automatically saved to `/tmp/swipe/flag.png`.
4. Do `foremost /tmp/swipe/flag.png`, and I got a QR code, which leads to flag.