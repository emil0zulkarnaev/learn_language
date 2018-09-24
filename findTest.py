#!/usr/bin/python3
#-*- coding:utf-8 -*-

from tkinter import *
from tkinter import ttk
from international import Languages

class Application(Toplevel):
    def __init__(self, master, language=0):
        super(Application, self).__init__(master)
        self.mr_master = master
        self.title("Выберите тест")
        self.geometry("160x115")
        self.grid()
        self.create_widgets()

        self.Language = ['Eng', 'Rus']
        self.nLanguage = language
        self.doInternational()

    def create_widgets(self):
        self.list_test = self.make_list_test()
        self.combobox = ttk.Combobox(self, values=self.list_test, height=3, state="readonly")
        if (len(self.list_test) != 0):
            self.combobox.set(self.list_test[0])
        else:
            self.combobox.set("none")
        self.combobox.place(x=5, y=5, width=150)

        self.button = Button(self, text="Выбрать")
        self.button.place(x=5, y=50, width=150)
        self.button['command'] = self.pick_test

        self.button2 = Button(self, text="Отмена")
        self.button2.place(x=5, y=80, width=150)
        self.button2['command'] = self.on_closing

    def doInternational(self):
        lang = self.Language[self.nLanguage]
        
        lg = Languages[lang]
        for i in lg:
            try:
                self.__dict__[i]['text']= lg[i]
            except:
                pass
                #print('Не вышло для ', lg[i])

    def on_closing(self):
        print('close findTest')
        self.mr_master._findTest = False
        self.destroy()

    def pick_test(self):
        ind_of_test = self.combobox.current()
        if len(self.list_test)-1>=ind_of_test:
            f = open('ftest.txt', 'w')
            f.write(self.list_test[ind_of_test])
            f.close()

            import test
            pp = test.Application(self.mr_master, self.nLanguage)
            self.mr_master.test = True

        else:
            self.destroy()

    def make_list_test(self):
        import os

        list_test = [x.replace(".txt", "") for x in os.listdir('./tests/')]

        return list_test

def main():
    some = Tk()
    some.title("Hello")
    some.geometry("160x115")

    app = Application(some)

    some.mainloop()

if __name__ == "__main__":
    main()
