#!/usr/bin/env node

var URL = require('url').URL;

function findVariants(targetChar) {
    let targetHost = 'test' + targetChar + '.com';
    for (i = 32; i <= 65535; ++i) {
        let candidateChar = String.fromCharCode(i);
        let input = 'http://test' + candidateChar + '.com';
        try {
            let url = new URL(input);
            if (url.hostname === targetHost) {
                charSet[targetChar].push(candidateChar);
                console.log(targetChar, ':', i, candidateChar);
            }
        }
        catch(e) {
        }
    }
}


if(process.argv[2] === undefined){
    console.log('Usage: node url_unicode.js [url]');
    process.exit(1);
}

let domain = process.argv[2];
domain = domain.replace('//','');

var charSet = {}
let domainSet = new Set(domain);
for (c of domainSet) {
    charSet[c] = new Array();
    findVariants(c)
}

// Create Example URL
example_url = new Array();
for(var i = 0; i < domain.length; ++i){
    if(domain.charAt(i) == ':'){
        example_url.push(':');
    } else {
        charArray = charSet[domain.charAt(i)];
        example_url.push(charArray[0]);
        charArray.shift();
    }
}

console.log('Example URL: ', example_url.join(''));