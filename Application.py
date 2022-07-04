from tkinter import *
from tkinter import messagebox
import fishbot
from pynput import mouse, keyboard
import time
import pyscreenshot as ImageGrab
import spaceClicker
import os

number_of_clicks = 0
pointsArray = []
space = 0x39
delay = 0.1
one = 0x02
squareCreated = False
predicted = 0
isPlaying = False


class Application(Frame):
    def square(self):
        messagebox.showinfo("Zaznaczenie kwadratu",
                            "Aby przystąpić do łowienia\nZa pomocą środkowego przycisku myszy"
                            "\nZaznacz lewy górny róg dymku\nA potem prawy dolny\nNajlepiej aby to była sama cyferka")
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def fish(self):
        # if not squareCreated:
        #     messagebox.showinfo("Zaznacz kwadrat", "Najpierw zaznacz kwadrat")
        #     return
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        while isPlaying:
            global predicted
            predicted = 0
            while predicted == 0:
                im = ImageGrab.grab(bbox=(913, 207, 1019, 288))
                im.save("predict/testx.png")
                im.save("predict/test123.png")
                predicted = fishbot.test(model, "testx.png")
                os.remove("predict/testx.png")
                time.sleep(delay)
            do_fishing(predicted)
            time.sleep(8)
            spaceClicker.PressKey(one)
            time.sleep(delay)
            spaceClicker.ReleaseKey(one)
            time.sleep(delay)
            spaceClicker.PressKey(space)
            time.sleep(delay)
            spaceClicker.ReleaseKey(space)

    def pauseFishing(self):
        global isPlaying
        isPlaying = not isPlaying

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

        self.create_square = Button(self)
        self.create_square['text'] = "Zaznacz kwadrat"
        self.create_square['command'] = self.square

        self.create_square.pack({"side": "left"})

        self.start_fishing = Button(self)
        self.start_fishing['text'] = "Zacznij łowić"
        self.start_fishing['command'] = self.fish

        self.start_fishing.pack({"side": "left"})

        self.pause = Button(self)
        self.pause['text'] = "PAUSE"
        self.pause['command'] = self.pauseFishing

        self.pause.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        global model
        model = fishbot.loadModel()


def on_click(x, y, button, pressed):
    global number_of_clicks
    print(x, y)
    if pressed:
        if button == mouse.Button.middle:
            number_of_clicks += 1
            global pointsArray
            pointsArray.append(x)
            pointsArray.append(y)
            if number_of_clicks > 1:
                global squareCreated
                squareCreated = True
                return False


def on_press(key):
    if key == keyboard.Key.space:
        global isPlaying
        isPlaying = True
        return False


def do_fishing(predict):
    if predict == 1:

        clickSpace(1)
    if predict == 2:
        clickSpace(2)
    if predict == 3:
        clickSpace(3)
    if predict == 4:
        clickSpace(4)
    if predict == 5:
        clickSpace(5)


def clickSpace(times):
    for i in range(times):
        spaceClicker.PressKey(space)
        time.sleep(delay)
        spaceClicker.ReleaseKey(space)
        time.sleep(delay)


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
