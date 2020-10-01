# EZ Bake Oven
Do you like baking? Don't leave the oven on for too long! 

## Writeup
1. When I click for cooking the Magic Cookies, I saw a new cookie
```
in_oven : eyJyZWNpcGUiOiAiTWFnaWMgQ29va2llcyIsICJ0aW1lIjogIjA5LzI2LzIwMjAsIDE0OjAxOjA0In0=
```

2. Base64 decode
```
{"recipe": "Magic Cookies", "time": "09/26/2020, 14:01:04"}
```

3. The time is the time I clicked `Cook`, Encode the following and paste it to the cookie so that the server thought I have cooked it for 7200 minutes. Problem solved.
```
{"recipe": "Magic Cookies", "time": "09/21/2020, 14:01:04"}
```