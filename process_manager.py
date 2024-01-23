import subprocess
import time
import os

def run_bot():
    running=True
    while running:
        bot_process = subprocess.Popen(['python', 'bot.py'])
        bot_process.wait()
        time.sleep(5)

os.system('cls')
while True:
    userInput = input(f'{__file__}> ').split(' ')

    if userInput[0] == 'start':
        run_bot()