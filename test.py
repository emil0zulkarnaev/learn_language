#!/usr/bin/python3
#-*- coding:utf-8 -*-

from tkinter import *
from tkinter import ttk
import random

class Application(Toplevel):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.mr_master = master
        self.title("Потестируемся))")
        self.geometry("400x240")
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.create_words_list()

        self.ind_word = 0

        self.lab1 = Label(self, text="Выберите верный перевод слова:")
        self.lab1.place(x=10, y=10)

        self.lab2 = Label(self, text=self.list_first_words[0].capitalize())
        self.lab2.place(x=10, y=30)
        self.lab2.config(font=10)

        self.var = IntVar()
        self.radiobuttons = []
        crd = 60
        value = 1
        k = 0
        some_list = self.random_some()
        rnd_int = random.randint(0, 3)
        some_list.insert(rnd_int, self.list_second_words[0])

        print(self.list_first_words)
        print(self.list_second_words)
        self.right_variant = rnd_int
        print(some_list[self.right_variant])
        print(self.right_variant, rnd_int)
        for i in range(4):
            self.radiobuttons.append(Radiobutton(self, variable=self.var, value=value, text=some_list[k],
                                                 command=self.create_radio_button))
            k += 1
            self.radiobuttons[len(self.radiobuttons)-1].place(x=10, y=crd)
            crd += 30
            value += 1

        self.button1 = Button(self, text="Дальше")
        self.button1.place(x=30, y=190, width=150)
        self.button1['command'] = self.next_question

    def next_question(self):
        if self.ind_word < len(self.list_first_words) - 1:
            self.ind_word += 1

            self.lab2.config(text=self.list_first_words[self.ind_word].capitalize())

            k = 0
            some_list = self.random_some()
            rnd_int = random.randint(0, 3)
            some_list.insert(rnd_int, self.list_second_words[self.ind_word])
            self.right_variant = rnd_int
            for i in range(4):
                self.radiobuttons[i].config(text=some_list[k])
                k += 1
        else:
            self.destroy()


    def create_radio_button(self):
        ind_variant = int(self.var.get()) - 1
        # print(ind_variant, self.right_variant)
        if self.right_variant == ind_variant:
            self.lab2.config(text=self.list_first_words[self.ind_word].capitalize() + "   !!!Верно!!!")
        else:
            self.lab2.config(text=self.list_first_words[self.ind_word].capitalize() + "   ...Не верно =(")

    def create_words_list(self):
        f = open('ftest.txt', 'r')
        f_text = f.read().replace("\n", "")
        f.close()

        try:
            f = open("./tests/" + f_text + ".txt", 'r')
        except:
            self.destroy()
        else:
            f_text = f.read() + "\n"
            f.close()

        self.list_first_words = []
        self.list_second_words = []
        s = ""
        for i in f_text:
            if i == "-" and s != "":
                self.list_first_words.append(s)
                s = ""
                continue
            elif i == "\n" and s != "":
                self.list_second_words.append(s)
                s = ""
                continue

            s = s + i
    def random_some(self):
        help_list = [x for x in self.list_second_words]
        help_list.remove(self.list_second_words[self.ind_word])
        #help_list.remove(self.list_first_words[self.ind_word])
        list_ch = []
        if len(help_list) != 0:
            for i in range(3):
                rnd_int = random.randint(0, len(help_list)-1)
                list_ch.append(help_list[rnd_int])
                help_list.remove(help_list[rnd_int])

        return list_ch


def main():
    some = Tk()
    some.title("Hello")
    some.geometry("400x240")

    app = Application(some)

    some.mainloop()

if __name__ == "__main__":
    main()