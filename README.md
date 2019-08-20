# card10 - nickname
Nickname app for the card10 badge #cccamp2019

## Features
- Simple and advanced mode
- customizable colors
- automatic day/night mode

# Simple
0. Boot into USB storage mode
1. Install the app
2. Put a file called nickname.txt on your card10
3. Write your nickname into the file (max 11 chars)
4. Boot into normal mode
5. Start the nickname.py app

# Advanced
For more advanced nickname fun
0. Boot into USB storage mode
1. Install the app
2. Put a file called nickname.json on your card10
3. Put the following JSON into the file and update it to your needs
```json
{
  "nickname": "nick",
  "subtitle": "sub",
  "background": [33,66,99],
  "fg_color": [0,0,255],
  "bg_color": [0,255,0],
  "fg_sub_color": [255,0,0],
  "bg_sub_color": [0,255,0],

  "background_night": [33,66,99],
  "fg_color_night": [0,0,255],
  "bg_color_night": [0,255,0],
  "fg_sub_color_night": [255,0,0],
  "bg_sub_color_night": [0,255,0]
}
```
4. Boot into normal mode
5. Start the nickname.py app