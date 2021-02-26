#!/usr/bin/env python3

import hashlib
import datetime
import string

def replace_pos(s,newstring,index):
    return(s[:index] + newstring + s[index + 1:])

def compute_commit(tree,parent,author,committer,message):
    cat_commit = "tree %s\nparent %s\nauthor %s\ncommitter %s\n\n%s\n" % (tree,parent,author,committer,message)
    full_commit = "commit %s\0%s" % (str(len(cat_commit)),cat_commit)
    hash_object = hashlib.sha1(full_commit.encode("utf-8"))
    return(hash_object.hexdigest())

def compute_tree(blob_hash):
    tree_string = "%s %s\0" % ("100644","flag.txt")
    tree_bytes = bytes.fromhex(blob_hash)
    debut = "tree %s\0" % str(len(tree_string.encode()+tree_bytes))
    hash_object = hashlib.sha1(debut.encode()+tree_string.encode()+tree_bytes)
    return(hash_object.hexdigest())

def compute_blob(blob_content):
    blob_string = "blob %s\0%s\n" % (str(len(blob_content)+1), blob_content)
    hash_object = hashlib.sha1(blob_string.encode("utf-8"))
    return(hash_object.hexdigest())

def compute_timestamp(str_date):
    date_time_obj = datetime.datetime.strptime(str_date, '%b %d %H:%M:%S %Y')
    timestamp = date_time_obj.replace(tzinfo=datetime.timezone.utc).timestamp()
    return(str(int(timestamp)))

commits = [
    "08e1f0dd3b9d710b1eea81f6b8f76c455f634e87",
    "c3e6c8ea777d50595a8b288cbbbd7a675c43b5df",
    "dca4ca5150b82e541e2f5c42d00493ba8d4aa84a",
    "cb18d2984f9e99e69044d18fd3786c2bf6425733",
    "d9af34e8a8ca6a24790d20262dafac71c3ddc980",
    "9dbf985598f5ef000ba2e8856c6bec12435f0ef8",
    "a6880ed0c8bb30263bd0a2a631eb9bf50dc72344",
    "6356e3d17ca6b7515c67cfe0a8712d1e8b57d713",
    "30240b427e09aa75f034527e91aaa1fbc1b243ee",
    "45ec9aba969782c72d18018126c2d9aeffde28b7",
    "59c9f723bff0952f6589157f3ef8e1858d01bfdc",
    "8a951bd3e56432dd689e83034c1ee7e21ae6ee56",
    "9b5ee533d17a9c0ff87d22bf0a433a621fbd55bf",
    "8984f8eac466cbf86a6aa6b0480be53a86d8108c",
    "6c35a04d1fdb8eedbbc9821b4c23b610bd3b4488",
    "a23b600c786b05623b765b4f0d7a3f52df63cdd5",
    "ff26e028a3faebd461c4cc0265d0f7b9ca049feb"
]
authors = [
    "Robert J. Lawful <boblaw@legal.committee>",
    "Pamela W. Mathews <pammy.emm@legal.committee>",
    "Christopher L. Hatch <crisscross.the.hatch@legal.committee>",
    "Peter G. Anderson <pepega@legal.committee>",
    "John J. Johnson <jojojo@legal.committee>",
    "Robert S. Storms <tempest@legal.committee>",
    "Robert J. Lawful <boblaw@legal.committee>",
    "Pamela W. Mathews <pammy.emm@legal.committee>",
    "Christopher L. Hatch <crisscross.the.hatch@legal.committee>",
    "Peter G. Anderson <pepega@legal.committee>",
    "John J. Johnson <jojojo@legal.committee>",
    "Robert S. Storms <tempest@legal.committee>",
    "Robert J. Lawful <boblaw@legal.committee>",
    "Pamela W. Mathews <pammy.emm@legal.committee>",
    "Christopher L. Hatch <crisscross.the.hatch@legal.committee>",
    "Peter G. Anderson <pepega@legal.committee>",
    "John J. Johnson <jojojo@legal.committee>"
]
dates = [
    'Mar 4 12:00:00 2020',
    'Mar 13 12:30:00 2020',
    'Mar 23 12:30:00 2020',
    'Apr 14 12:00:00 2020',
    'May 1 12:00:00 2020',
    'May 12 12:30:00 2020',
    'Jun 11 12:00:00 2020',
    'Jul 1 12:45:00 2020',
    'Jul 28 12:00:00 2020',
    'Aug 12 12:30:00 2020',
    'Aug 28 12:45:00 2020',
    'Sep 11 11:45:00 2020',
    'Oct 19 12:30:00 2020',
    'Oct 29 12:00:00 2020',
    'Nov 27 12:00:00 2020',
    'Dec 18 12:30:00 2020',
    'Jan 27 12:45:00 2021'
]
messages = [
    "Initial formation of the flag-deciding committee.",
    "Proceedings of the flag-deciding committee: 18",
    "Proceedings of the flag-deciding committee: 8, 31, 36",
    "Proceedings of the flag-deciding committee: 32, 33, 34",
    "Proceedings of the flag-deciding committee: 26, 27, 29",
    "Proceedings of the flag-deciding committee: 14, 15, 16",
    "Proceedings of the flag-deciding committee: 2, 5, 6",
    "Proceedings of the flag-deciding committee: 10, 11, 12",
    "Proceedings of the flag-deciding committee: 28, 30, 35",
    "Proceedings of the flag-deciding committee: 17, 24, 37",
    "Proceedings of the flag-deciding committee: 19, 20, 21",
    "Proceedings of the flag-deciding committee: 1, 3, 4",
    "Proceedings of the flag-deciding committee: 41, 42, 43",
    "Proceedings of the flag-deciding committee: 38, 39, 40",
    "Proceedings of the flag-deciding committee: 44, 45, 46",
    "Proceedings of the flag-deciding committee: 7, 9, 13",
    "Proceedings of the flag-deciding committee: 22, 23, 25"
]

bruteforce = [
    [],
    [18],
    [8,31,36],
    [32,33,34],
    [26,27,29],
    [14,15,16],
    [2,5,6],
    [10,11,12],
    [28,30,35],
    [17,24,37],
    [19,20,21],
    [1,3,4],
    [41,42,43],
    [38,39,40],
    [44,45,46],
    [7,9,13],
    [22,23,25]
]
flag = "union{*****************_****************************}"

for i in range(2, len(messages)):
    timestamp = compute_timestamp(dates[i])
    authors_i = "%s %s +0000" % (authors[i],timestamp)
    # git config user.name git config user.email
    committer_i = "Flag-deciding Committee <committee@legal.committee> %s +0000" % timestamp
    message_i = messages[i]
    parent_i = commits[i-1]
    expected_commit_hash = commits[i]
    for s1 in string.printable:
        for s2 in string.printable:
            for s3 in string.printable:
                try_content = replace_pos(flag, s1, bruteforce[i][0]+5)
                try_content = replace_pos(try_content, s2, bruteforce[i][1]+5)
                try_content = replace_pos(try_content, s3, bruteforce[i][2]+5)
                blob_content = compute_blob(try_content)
                tree = compute_tree(blob_content)
                computed_hash=compute_commit(tree,parent_i,authors_i,committer_i,message_i)
                if (computed_hash == expected_commit_hash):
                    flag = try_content
                    print(flag)
                    continue

"""
union{*******3*********_************r****d**********}
union{*******3*********_************rm1n*d**********}
union{*******3*********_*******_d*t*rm1n*d**********}
union{*******3*****1de*_*******_d*t*rm1n*d**********}
union{*0**1t*3*****1de*_*******_d*t*rm1n*d**********}
union{*0**1t*3*_d3*1de*_*******_d*t*rm1n*d**********}
union{*0**1t*3*_d3*1de*_*******_d3t3rm1n3d**********}
union{*0**1t*3*_d3*1deD_*****H*_d3t3rm1n3d_*********}
union{*0**1t*3*_d3*1deD_bu7**H*_d3t3rm1n3d_*********}
union{c0mm1t*3*_d3*1deD_bu7**H*_d3t3rm1n3d_*********}
union{c0mm1t*3*_d3*1deD_bu7**H*_d3t3rm1n3d_***c26***}
union{c0mm1t*3*_d3*1deD_bu7**H*_d3t3rm1n3d_6a7c26***}
union{c0mm1t*3*_d3*1deD_bu7**H*_d3t3rm1n3d_6a7c2619a}
union{c0mm1tt33_d3c1deD_bu7**H*_d3t3rm1n3d_6a7c2619a}
union{c0mm1tt33_d3c1deD_bu7_SHA_d3t3rm1n3d_6a7c2619a}
"""