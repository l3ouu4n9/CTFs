var _0x3150=["","\x6C\x65\x6E\x67\x74\x68","\x6D\x61\x78","\x63\x68\x61\x72\x41\x74","\x63\x68\x61\x72\x43\x6F\x64\x65\x41\x74","\x66\x72\x6F\x6D\x43\x68\x61\x72\x43\x6F\x64\x65","\x73\x68\x61\x6B\x74\x69"];

function merge(_0xd4c8x2, _0xd4c8x3) {
    for (var _0xd4c8x4 = 0, _0xd4c8x5 = '', _0xd4c8x6 = Math['max'](_0xd4c8x2['length'], _0xd4c8x3['length']); _0xd4c8x4 < _0xd4c8x6; _0xd4c8x4++) {
        _0xd4c8x5 += _0xd4c8x2['charAt'](_0xd4c8x4) || '';
        _0xd4c8x5 += _0xd4c8x3['charAt'](_0xd4c8x4) || ''
    };
    return _0xd4c8x5
}

function encryptXor(_0xd4c8x8) {
    var _0xd4c8x9 = '';
    for (var _0xd4c8x4 = 0, _0xd4c8xa = 1; _0xd4c8x4 < _0xd4c8x8['length']; _0xd4c8x4++, _0xd4c8xa++) {
        if (_0xd4c8xa == _0xd4c8x8['length']) {
            _0xd4c8xa = 0
        };
        _0xd4c8x9 += String['fromCharCode'](_0xd4c8x8['charCodeAt'](_0xd4c8x4) ^ _0xd4c8x8['charCodeAt'](_0xd4c8xa))
    };
    return _0xd4c8x9
}
/*
if (usr['length'] == 5) {
    magic = btoa(encryptXor(merge('shakti', usr)))
}
*/
console.log(Buffer.from(encryptXor(merge('shakti', 'aaaaa'))).toString('base64'));

// EgkJAAAKChUVCBo=
// login with
// username aaaaa
// password EgkJAAAKChUVCBo=
// shaktictf{901d_und3r_7h3_r41n60w_768ef91!!!}