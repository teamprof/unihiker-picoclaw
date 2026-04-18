# Dashboard of running PicoClaw on UNIHIKER M10

## Introduction 
This project leverages the UNIHIKER GUI library to implement a graphical dashboard for PicoClaw, running on the UNIHIKER M10 SBC.
Before starting, **ensure that PicoClaw is properly set up** and running on the UNIHIKER M10. For detailed instructions, please refer to [Running PicoClaw on UNIHIKER M10](https://community.dfrobot.com/makelog-318617.html)

[![License: GPL v3](https://img.shields.io/badge/License-GPL_v3-blue.svg)](https://github.com/teamprof/pico-audio-ml/blob/main/LICENSE)  
<a href="https://www.buymeacoffee.com/teamprof" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 38px !important;width: 128px !important;" ></a>


## Software setup
Run the following commands to clone the project repository and install the required libraries.
```
git clone https://github.com/teamprof/unihiker-picoclaw.git
cd unihiker-picoclaw/dashboard
pip install -r requirements.txt
```

## Run dashboard app
- Ensure that the PicoClaw binary file is located at "/root/picoclaw/picoclaw", or update "config.py" to set the correct path
```
PATH_PICOCLAW = "/root/picoclaw/picoclaw"
```
- Launch the dashboard by executing the following command.
```
python main.py
```
If everything goes smoothly, you should see the following screen.  
[![screen-start](./assets/screen-start.png)](https://github.com/teamprof/unihiker-picoclaw/blob/main/assets/screen-start.png)  
PicoClaw is now successfully running on your UNIHIKER M10.


### Stop PicoClaw
Stop PicoClaw by click the stop icon [![icon-stop](./dashboard/assets/stop.png)](https://github.com/teamprof/unihiker-picoclaw/blob/main/dashboard/assets/stop.png)
or press the Button A  
The following screen shows PicoClaw is stopped.   
[![screen-stop](./assets/screen-stop.png)](https://github.com/teamprof/unihiker-picoclaw/blob/main/assets/screen-stop.png)


### Start PicoClaw
Start PicoClaw by click the start icon [![icon-start](./dashboard/assets/start.png)](https://github.com/teamprof/unihiker-picoclaw/blob/main/dashboard/assets/start.png)
or press the Button A 

### Test 
- Send the message "what is your name" on Telegram.
- Wait to receive the response.  
[![picoclaw-tg](./assets/picoclaw-tg.jpg)](https://github.com/teamprof/unihiker-picoclaw/blob/main/assets/picoclaw-tg.jpg)  


### Exit dashboard app
click the exit icon 
[![icon-exit](./dashboard/assets/exit.png)](https://github.com/teamprof/unihiker-picoclaw/blob/main/dashboard/assets/exit.png)
or press the Button B to exit the dashboard

### Video demo
Video demo is available on [video demo](https://youtube.com/shorts/2kDmuJmmUu4)  
[![video](./assets/video.jpg)](https://youtube.com/shorts/2kDmuJmmUu4)  



## License
- The project is licensed under GNU GENERAL PUBLIC LICENSE Version 3
---

## Copyright
- Copyright 2026 teamprof.net@gmail.com. All rights reserved.

