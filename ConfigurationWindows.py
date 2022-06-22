from tkinter import Label, Button, messagebox, Entry, Tk

import pyglet
import Position

citiesIdPositionGlobal = {}
counterMeasuresIdPositionGlobal = {}
enemyMissileMaxNumber = []


class ConfigurationWindowsClass(object):
    def __init__(self, width, height, PosInferiorLimitX, PosInferiorLimitY, PosSuperiorLimitX, PosSuperiorLimitY):
        self.window = Tk()
        self.window.geometry(f'{width}x{height}')
        self.window.configure(background='grey')
        self.window.resizable(False, True)
        self.enemyMissileNumberEntry = Entry(self.window, bg='white')
        self.cityNumberEntry = Entry(self.window, bg='white')
        self.counterMeasuresNumberEntry = Entry(self.window, bg='white')
        self.citiesIdPosEntries = {}
        self.counterMeasuresIdPosEntries = {}
        self.PosInferiorLimitX = PosInferiorLimitX
        self.PosInferiorLimitY = PosInferiorLimitY
        self.PosInferiorLimitZ = 0
        self.PosSuperiorLimitX = PosSuperiorLimitX
        self.PosSuperiorLimitY = PosSuperiorLimitY
        self.PosSuperiorLimitZ = 50
        pyglet.font.add_file('./fonts/digital-7.ttf')

    def clear_frame(self):
        for widgets in self.window.winfo_children():
            widgets.destroy()

    def generateLabel(self, text, x, y):
        label = Label(self.window, text=text, background='grey', relief="groove")
        label.place(x=x, y=y, width=65)
        label.config(font=("digital-7", 10))

    def generatePosEntries(self, x, y, id, type):
        entryX = Entry(self.window, bg='white')
        entryX.place(x=x, y=y, width=30)

        entryY = Entry(self.window, bg='white')
        entryY.place(x=x + 40, y=y, width=30)

        entryZ = Entry(self.window, bg='white')
        entryZ.place(x=x + 80, y=y, width=30)

        if type == "city":
            self.citiesIdPosEntries[id] = [entryX, entryY, entryZ]
        else:
            self.counterMeasuresIdPosEntries[id] = [entryX, entryY, entryZ]

    def numberEntriesNotEmpty(self):
        return len(self.cityNumberEntry.get()) != 0 \
               and len(self.counterMeasuresNumberEntry.get()) != 0 \
               and len(self.enemyMissileNumberEntry.get()) != 0

    def numberEntriesAreInteger(self):
        cityNumber = self.cityNumberEntry.get()
        MissileNumber = self.enemyMissileNumberEntry.get()
        counterMeasureNumber = self.counterMeasuresNumberEntry.get()
        return cityNumber.isnumeric() and MissileNumber.isnumeric() and counterMeasureNumber.isnumeric()

    def cityPositionIsNotEmpty(self, id):
        return len(self.citiesIdPosEntries[id][0].get()) != 0 \
               and len(self.citiesIdPosEntries[id][1].get()) \
               and len(self.citiesIdPosEntries[id][2].get())

    def cityPositionsAreInteger(self, id):
        cityPositionX = self.citiesIdPosEntries[id][0].get()
        cityPositionY = self.citiesIdPosEntries[id][1].get()
        cityPositionZ = self.citiesIdPosEntries[id][2].get()
        return cityPositionX.isnumeric() and cityPositionY.isnumeric() and cityPositionZ.isnumeric()

    def cityPositionAreInRange(self, id):
        cityPositionX = int(self.citiesIdPosEntries[id][0].get())
        cityPositionY = int(self.citiesIdPosEntries[id][1].get())
        cityPositionZ = int(self.citiesIdPosEntries[id][2].get())
        return (self.PosInferiorLimitX <= cityPositionX <= self.PosSuperiorLimitX) \
               and (self.PosInferiorLimitY <= cityPositionY <= self.PosSuperiorLimitY) \
               and (self.PosInferiorLimitZ <= cityPositionZ <= self.PosSuperiorLimitZ)

    def counterMeasuresPositionIsNotEmpty(self, id):
        return len(self.counterMeasuresIdPosEntries[id][0].get()) != 0 \
               and len(self.counterMeasuresIdPosEntries[id][1].get()) \
               and len(self.counterMeasuresIdPosEntries[id][2].get())

    def counterMeasuresPositionsAreInteger(self, id):
        counterMeasurePositionX = self.counterMeasuresIdPosEntries[id][0].get()
        counterMeasurePositionY = self.counterMeasuresIdPosEntries[id][1].get()
        counterMeasurePositionZ = self.counterMeasuresIdPosEntries[id][2].get()
        return counterMeasurePositionX.isnumeric() and counterMeasurePositionY.isnumeric() and counterMeasurePositionZ.isnumeric()

    def counterMeasuresPositionAreInRange(self, id):
        counterMeasurePositionX = int(self.counterMeasuresIdPosEntries[id][0].get())
        counterMeasurePositionY = int(self.counterMeasuresIdPosEntries[id][1].get())
        counterMeasurePositionZ = int(self.counterMeasuresIdPosEntries[id][2].get())
        return (self.PosInferiorLimitX <= counterMeasurePositionX <= self.PosSuperiorLimitX) \
               and (self.PosInferiorLimitY <= counterMeasurePositionY <= self.PosSuperiorLimitY) \
               and (self.PosInferiorLimitZ <= counterMeasurePositionZ <= self.PosSuperiorLimitZ)

    def safePositions(self):
        global citiesIdPositionGlobal
        global counterMeasuresIdPositionGlobal
        citiesIdPositionGlobal.clear()
        counterMeasuresIdPositionGlobal.clear()
        couldFinishTheProgram = True
        for id in self.citiesIdPosEntries:
            if self.cityPositionIsNotEmpty(id):
                if self.cityPositionsAreInteger(id):
                    if self.cityPositionAreInRange(id):
                        position = Position.positionClass(int(self.citiesIdPosEntries[id][0].get()),
                                                          int(self.citiesIdPosEntries[id][1].get()),
                                                          int(self.citiesIdPosEntries[id][2].get()))
                        citiesIdPositionGlobal[id] = position
                    else:
                        couldFinishTheProgram = False
                        messagebox.showerror(message=f"You must insert an integer that is contain in the position limit, fix the city {id} positions")
                else:
                    couldFinishTheProgram = False
                    messagebox.showerror(message=f"Only integers are allowed, fix the city {id} positions")
            else:
                couldFinishTheProgram = False
                messagebox.showerror(message=f"You must fill all the position of the city {id}")

        for id in self.counterMeasuresIdPosEntries:
            if self.counterMeasuresPositionIsNotEmpty(id):
                if self.counterMeasuresPositionsAreInteger(id):
                    if self.counterMeasuresPositionAreInRange(id):
                        position = Position.positionClass(int(self.counterMeasuresIdPosEntries[id][0].get()),
                                                          int(self.counterMeasuresIdPosEntries[id][1].get()),
                                                          int(self.counterMeasuresIdPosEntries[id][2].get()))
                        counterMeasuresIdPositionGlobal[id] = position
                    else:
                        couldFinishTheProgram = False
                        messagebox.showerror(message=f"You must insert an integer that is contain in the position limit, fix the counterMeasure {id} positions")
                else:
                    couldFinishTheProgram = False
                    messagebox.showerror(message=f"Only integers are allowed, fix the counterMeasure {id} positions")
            else:
                couldFinishTheProgram = False
                messagebox.showerror(message=f"You must fill all the position of the counterMeasure {id}")

        if couldFinishTheProgram:
            self.close_window()

    def generatePositionBoxes(self):
        global enemyMissileMaxNumber
        if self.numberEntriesNotEmpty():
            if self.numberEntriesAreInteger():
                enemyMissileMaxNumber.append(int(self.enemyMissileNumberEntry.get()))
                cityNumber = int(self.cityNumberEntry.get())
                counterMeasureNumber = int(self.counterMeasuresNumberEntry.get())

                self.clear_frame()

                y = 10
                self.setLegend(f"Limit X [{self.PosInferiorLimitX}, {self.PosSuperiorLimitX}]", 10, y)
                self.setLegend(f"Limit Y [{self.PosInferiorLimitY}, {self.PosSuperiorLimitY}]", 140, y)
                self.setLegend(f"Limit Z [{self.PosInferiorLimitZ}, {self.PosSuperiorLimitZ}]", 270, y)

                yCities = y + 30
                for i in range(cityNumber):
                    self.generateLabel(f"city {i}", 10, yCities)
                    self.generatePosEntries(80, yCities, i, "city")
                    yCities += 30

                yCounterMeasures = y + 30
                for i in range(counterMeasureNumber):
                    self.generateLabel(f"CMeasure {i}", 200, yCounterMeasures)
                    self.generatePosEntries(270, yCounterMeasures, i, "counterMeasure")
                    yCounterMeasures += 30

                y = yCounterMeasures if yCounterMeasures > yCities else yCities
                self.setReadyButtonForPositionEntries(y)
            else:
                messagebox.showerror(message="Only intergers are allowed")
        else:
            messagebox.showerror(message="You must fill all the entries")

    def setHeading(self, text):
        label = Label(self.window, text=text, background='grey')
        label.config(font=("digital-7", 20))
        label.pack()

    def setFieldTitles(self):
        labelEnemyMissileNumber = Label(self.window, text="Max Number of Enemy Missiles in the screen",
                                        bg='grey', relief="groove")
        labelEnemyMissileNumber.place(x=10, y=40, height=30)
        labelEnemyMissileNumber.config(font=("digital-7"))

        labelCityNumber = Label(self.window, text="Number of cities in the map",
                                bg='grey', relief="groove")
        labelCityNumber.place(x=10, y=80, height=30)
        labelCityNumber.config(font=("digital-7"))

        labelCounterMeasuresNumber = Label(self.window, text="Number of CounterMeasure Systems in the map",
                                           bg='grey', relief="groove")
        labelCounterMeasuresNumber.place(x=10, y=120, height=30)
        labelCounterMeasuresNumber.config(font=("digital-7"))

    def setEntryBoxes(self):
        self.enemyMissileNumberEntry.place(x=350, y=40, width=40, height=30)

        self.cityNumberEntry.place(x=350, y=80, width=40, height=30)

        self.counterMeasuresNumberEntry.place(x=350, y=120, width=40, height=30)

    def setReadyButtonForNumberEntries(self):
        generationBoxButton = Button(self.window, text="Ready", bg='grey', command=self.generatePositionBoxes)
        generationBoxButton.place(x=170, y=170, width=60)
        generationBoxButton.config(font=("digital-7"))

    def setReadyButtonForPositionEntries(self, y):
        generationBoxButton = Button(self.window, text="Ready", bg='grey', command=self.safePositions)
        generationBoxButton.place(x=170, y=y, width=60)
        generationBoxButton.config(font=("digital-7"))

    def setLegend(self, text, x, y):
        label = Label(self.window, text=text, background='grey')
        label.config(font=("digital-7", 15))
        label.place(x=x, y=y)

    def close_window(self):
        self.window.destroy()

    def launchInterface(self):
        self.setHeading("Simulation Setup")
        self.setFieldTitles()
        self.setEntryBoxes()
        self.setReadyButtonForNumberEntries()
        self.window.mainloop()


