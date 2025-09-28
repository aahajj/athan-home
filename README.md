# Athan @ Home

If you live in a place where you cannot hear the athan, you’re probably relying on an app (such as Mawaqit) on your phone to know the prayer times. While these apps generally work perfectly fine, I’ve had an issue with not being able to hear my phone when the athan goes off for Fajr.I tried using another device, such as my iPad, where I don’t enable DND-mode at night. However, I noticed that the athan often doesn’t play until the end. Setting an alarm was a working solution but since it is static, it is not a long term solution.
I also realized that I don’t just want to hear the athan from my phone I want a source that blasts it louder and clearer. At first, I thought about buying a smart home speaker. But since I don’t want a device that’s always listening to me, I decided to build something of my own instead.

#### What do you need?
1. Raspberry Pi (or anything semilar)
2. Speakers

The Idea is to run the python script on the Raspberry Pi that fetches the athan times everyday and plays athan from a local file.

#### how to install?
To install and run everything for this project as simply as possible, you can use the following command on your device:

```bash
git clone https://github.com/aahajj/athan-home.git
cd athan-home
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt
python3 main.py 
```

The command will:
1. Download the project,
2. Install all required dependencies,
3. And start the program.

If you want to start the program in the background you will need to add & at the end of the command. ``python3 main.py &``

Make sure you have Git, Python3 and pip3 installed before running the command. 