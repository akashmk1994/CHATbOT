import datetime
import pyjokes
import pyttsx3
import time as t
import pywhatkit
import speech_recognition as sr
import wikipedia
import winsound
import Legiondata
import re

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
tasks = []


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source, timeout=20)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'legion' in command:
                command = command.replace('legion', '')
                print(command)
        return command
    except Exception as e:
        print(e)
        talk('Unable to Recognize your voice...')


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        talk("Good Morning !")

    elif 12 <= hour < 18:
        talk("Good Afternoon !")

    else:
        talk("Good Evening !")

    assname = "Legion"
    talk("I am your Assistant")
    talk(assname)


def add_command(task_name, date):
    Legiondata.add_ent(task_name, date)


def delete_ent(task_name):
    Legiondata.delete_ent(task_name)


def view_command():
    for row in Legiondata.view_ent():
        tasks.append(row)
    return tasks


def run_app():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk(info)
    elif 'what is' in command:
        thing = command.replace('what is', '')
        info = wikipedia.summary(thing, 1)
        talk(info)
    elif 'how are you' in command:
        talk("I am fine, Thank you")
        talk("How are you?")
    elif 'fine' in command or "good" in command:
        talk("It's good to know that your fine")
    elif "change your name" in command:
        talk("What would you like to call me, Sir ")
        assname = take_command()
        talk("Thanks for naming me" + assname)
    elif 'bye' in command:
        talk("Thanks for giving me your time")
        exit()
    elif 'alarm' in command:
        alarm = command.replace('alarm for', '')
        alarm = str(alarm.strip())
        regex = '[0-9]+[\:]+[0-9]'
        if not re.search(regex, alarm):
            length_alarm = int(len(alarm))
            talk('Setting alarm for' + alarm)
            if length_alarm > 3:
                alarm = alarm.replace(alarm[0:2], alarm[0:2] + ':')
            else:
                alarm = alarm.replace(alarm[0:1], alarm[0:1] + ':')
        else:
            talk('Setting alarm for' + alarm)
        while True:
            t.sleep(1)
            current_time = datetime.datetime.now()
            now = current_time.strftime("%H:%M")
            date = current_time.strftime("%d/%m/%Y")
            if now == alarm:
                talk('Its time to Wake up' + alarm)
                winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
                break
    elif 'add task for today' in command:
        task_name = command.replace('add task for today', '')
        date = t.strftime("%d/%m/%Y")
        add_command(str(task_name), str(date))
        talk('Task added as reminder')
    elif 'remind me the task for today' in command:
        exiting_tasks = view_command()
        for tas in exiting_tasks:
            talk(tas)
        if not exiting_tasks:
            talk('There are no tasks')
    elif 'remove the task' in command:
        remove_task = command.replace('remove the task', '')
        delete_ent(str(remove_task))
        talk('Removed task' + remove_task)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        take_command()


wishMe()
while True:
    run_app()
