import speech_recognition as sr
import pyttsx3 as pts
import pywhatkit as pwk
import webbrowser as web
import wikipedia as wiki
import pyautogui as pg
import time
from openai_helper import ask_computer

#hand = h.HandLandmarks()
#mail = ["mail to", "mail", "send mail", "send mail to", "a", "to", "send"]
whats = ["send message", "message", "dm",
         "direct message", "share", "to", "whatsapp"]
list_of_replacements = ["search", "search for", "search about", "find about", "find",
                        "find for", "play", "is", "on youtube", "in youtube", "youtube", "tell me", "tell", "open", "in", "video", "for", "about", "results", "on google", "in google", "what is", "information", "details", "give info", "give information", "find information", "info"]
receipient = {"mother": "+919999999999", "myself": "+919999999999"}
groupid = {"friends": "//add grp link//",
           "project": "//add grp link//"}
draw_list = ["don't", "do not", "stop", "remove"]
selfie_sig = False

listener = sr.Recognizer()
engine = pts.init()
engine. setProperty("rate", 178)  # rate of speech
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)
engine.say("what can I do for you")
engine.runAndWait()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=0.5)
            print("listening")
            voice = listener.listen(source)
            # show_all : for full response
            command = listener.recognize_google(voice)
    except sr.RequestError:
        talk("API unavailable")
        exit()
    except sr.UnknownValueError:
        talk("Unable to recognize speech")
        return ''
    return command


def processCommand():
    command = listen().lower()
    print(command)
    for i in whats:
        if i in command:
            msgTo(command)
            return
    else:
        query(command)
        return

    '''if ("take a selfie") in command:
        hand.selfie()
    elif ("draw") in command:
        for i in draw_list:
            if i in command:
                hand.drawOnImage(False)
        else:
            hand.drawOnImage(True)'''


def query(command):
    if ("youtube" or "video" or "play") in command:
        # print(pwk.playonyt(command, True))
        for i in list_of_replacements:
            command = command.replace(i, '').strip()
        if command == '':
            talk("opening youtube")
            web.open(f"https://www.youtube.com")
        else:
            talk("opening"+command+"in youtube")
            web.open(f"https://www.youtube.com/results?q={command}")
    elif ("what" or "information") in command:
        for i in list_of_replacements:
            command = command.replace(i, '').strip()
        data = wiki.summary(command)
        suggestions = wiki.search(command, 10, True)
        talk("info about"+command)
        print(suggestions)
        talk(data)
    elif ("search" or "google") in command:
        for i in list_of_replacements:
            command = command.replace(i, '').strip()
        talk("searching"+command)
        web.open(f"https://www.google.com/search?q={command}")
    else:
        res = ask_computer(command)
        talk(res)


def msgTo(command):
    if ("web" or "open") in command:
        res = pwk.open_web()
        if res:
            talk("opened")
        else:
            talk("can't open")
    elif "group" in command:
        talk("who's the receipient")
        rec = ''
        while(rec == ''):
            talk("please repeat it again")
            id = listen()
            if id not in groupid.keys():
                talk("id not found")
                return
            rec = groupid[id]
        talk("what's the message")
        msg = ''
        while(msg == ''):
            talk("please repeat it again")
            msg = listen()
        pwk.sendwhatmsg_to_group_instantly(rec, msg, 7)
    elif "message" in command:
        talk("who's the receipient")
        rec = ''
        rec = receipient[listen()]
        while(rec == ''):
            talk("please repeat it again")
            id = listen()
            if id not in groupid.keys():
                talk("id not found")
                return
            rec = receipient[listen()]
        talk("what's the message")
        msg = ''
        while(True):
            msg = listen()
            if msg == '':
                break
            talk("please repeat it again")
        pwk.sendwhatmsg_instantly(rec, msg, 4)

        time.sleep(5)
        pg.press("enter")
    else:
        talk("command couldn't be processed")


while(True):
    processCommand()
