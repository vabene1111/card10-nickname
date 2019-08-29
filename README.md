# card10 - nickname
Nickname app for the card10 badge #cccamp2019

## Features
- Simple and advanced mode
- battery indicator (needs to be tested for voltage thresholds)
- customizable colors
- turon on/off led (hold button for a few seconds right=off/left=on)
- automatic day/night mode


# Install
The nickname app should come pre-installed with your device. In order to install or update it manually follow these steps:

Boot your Card10 into USB-Storage mode (hold down right while pressing power).

There are plan to simplify installing of apps using various tools. Right now you need to either
download the module from the hatchery and put it in the `apps` in a folder called `card10_nickname` including an `__init__.py` with the code and a 
`metadata.json` which you can get somewhere from the hatchery.

The second option is to simply take the `nickname.py` and drop it in the `apps` directory.

# Configure
## Simple
1. Boot into USB storage mode
2. Put a file called nickname.txt on your card10
3. Write your nickname into the file (max 11 chars)
4. Boot into normal mode
5. Start the nickname.py app

## Advanced
For more advanced nickname fun replace `nickname.txt` with a `nickname.json` with the following configuration

```json
{
  "nickname": "card10",
  "subtitle": "cccamp2019",

  "background": [255,255,255],
  "fg_color": [153,186,0],
  "bg_color": [255,255,255],
  "fg_sub_color": [111,135,0],
  "bg_sub_color": [255,255,255],

  "background_night": [53,53,53],
  "fg_color_night": [153,186,0],
  "bg_color_night": [53,53,53],
  "fg_sub_color_night": [111,135,0],
  "bg_sub_color_night": [53,53,53],
  
  "battery": false,
  "battery_color_good": [0,255,0],
  "battery_color_ok": [255,215,0],
  "battery_color_bad": [255,0,0]
}
```
Nice to know:
- You can leave out every value except for the `nickname`, this will use the default settings
- If you leave out the text background the default background is taken
- If you use `#time` as `subtitle` the current time will be displayed
  **Note** This is currently WIP since you cannot eaisly set the system time.

