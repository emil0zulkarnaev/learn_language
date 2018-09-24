#!/usr/bin/python3
#-*- coding:utf-8 -*-

from tkinter import *
from tkinter import ttk
import string
from Word import Word
from international import Languages

ABV_english = string.ascii_lowercase
ABV_russian = ['а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)

        self.preparation()

        self.grid()
        self.create_widgets()
        self.grid()

        self.Language = ['Eng', 'Rus']
        self.nLanguage = 0
        self.doInternational()

    def preparation(self):
        import os
        lst = os.listdir('./')
        if 'tests' not in lst:
            os.makedirs('./tests')
            
        ### Make SQLite3 db
        if 'words.db' not in lst:
            import sqlite3
            conn = sqlite3.connect('words.db')
            
            _strM = []
            _strM.append("""
CREATE TABLE english (
    id   INTEGER PRIMARY KEY AUTOINCREMENT
                 UNIQUE
                 NOT NULL,
    word TEXT    UNIQUE
                 NOT NULL
);
""")
            _strM.append("""
CREATE TABLE russian (
    id   INTEGER PRIMARY KEY AUTOINCREMENT
                 UNIQUE
                 NOT NULL,
    word TEXT    UNIQUE
                 NOT NULL
);
""")
            _strM.append("""
CREATE TABLE translation (
    id      INTEGER PRIMARY KEY AUTOINCREMENT
                    UNIQUE
                    NOT NULL,
    russian INTEGER NOT NULL,
    english INTEGER NOT NULL
);
""")
            for i in _strM:
                cursor = conn.cursor()
                cursor.execute(i)
                conn.commit
            conn.close()
    
    def create_widgets(self):
        self.but1 = Button(root)
        self.but1.place(x=0, y=55, width=100)
        self.but1['command'] = self.new_word

        self.but2 = Button(root)
        self.but2.place(x=100, y=55, width=100)
        self.but2['command'] = self.find_word

        self.but4 = Button(root)
        self.but4.place(x=25, y=180, width=150)
        self.but4['command'] = self.the_end_write_word

        self.but5 = Button(root)
        self.but5.place(x=25, y=210, width=150)
        self.but5['command'] = self.remove_all

        
        self.but6 = Button(root)
        self.but6.place(x=25, y=280, width=150)
        self.but6['command'] = self.remove_new_words

        self.but6d1 = Button(root)
        self.but6d1.place(x=25, y=370, width=150)
        self.but6d1['command'] = self.make_test

        self.but6d2 = Button(root)
        self.but6d2.place(x=25, y=400, width=150)
        self.but6d2['command'] = self.find_test

        self.butInternational = Button(root)
        self.butInternational.place(x=400, y=400, width=50)
        self.butInternational['command'] = self.doInternational

        self.labInternational = Label(root, text="Чтобы сменить язык, нажмите =>")
        self.labInternational.place(x=200, y=400)

        self.lab1 = Label(root)
        self.lab1.place(x=10, y=5)

        self.lab2 = Label(root)
        self.lab2.place(x=10, y=90)

        self.lab3 = Label(root)
        self.lab3.place(x=200, y=0)

        self.lab4 = Label(root)
        self.lab4.place(x=10, y=320)

        self.text1 = Entry(root)
        self.text1.place(x=5, y=25, width=190, height=25)

        self.text2 = Entry(root)
        self.text2.place(x=5, y=110,width=190, height=25)

        self.text3 = Text(root)
        self.text3.place(x=200, y=20, width=245, height=350)

        self.text4 = Entry(root)
        self.text4.place(x=5, y=340, width=190, height=25)

        self.scrollbar = Scrollbar(root)
        self.scrollbar.place(x=445, y=150) 
        self.scrollbar['command'] = self.text3.yview        #привязка скроллбара к текстовому полю
        self.text3['yscrollcommand'] = self.scrollbar.set   #привязка текстового поля к скроллбару

    def doInternational(self):
        lang = self.Language[self.nLanguage]
        self.butInternational['text'] = lang
        
        lg = Languages[lang]
        for i in lg:
            try:
                self.__dict__[i]['text']= lg[i]
            except:
                pass
                #print('Не вышло для ', lg[i])

        ind = self.Language.index(lang)
        self.nLanguage = ind+1 if self.nLanguage < len(self.Language)-1 else 0
            

    def find_test(self):
        import findTest
        pp = findTest.Application(self, self.nLanguage-1)

    def make_test(self):
        name_test = self.text4.get().lower().lstrip().rstrip()
        if (len(name_test) == 0):
            message = "Вы не ввели название теста"
            self.text3.delete(0.0, END)
            self.text3.insert(0.0, message)
        else:
            try:
                f = open("./tests/" + name_test + ".txt", 'r')
            except:
                f = open("./tests/" + name_test + ".txt", 'w')
                f2 = open("new_words.txt", 'r')

                f2_text = f2.read()
                f2.close()

                f.write(f2_text)
                f.close()

                message = "Тест создан"
                self.text3.delete(0.0, END)
                self.text3.insert(0.0, message)

            else:
                message = "Тест с таким называнием уже существует"
                self.text3.delete(0.0, END)
                self.text3.insert(0.0, message)

    def remove_new_words(self):
        f = open('new_words.txt', 'w')
        f.write('')
        f.close()

        self.text3.delete(0.0, END)
        self.text3.insert(0.0, "Лист добавленных слов обнулён")

    def remove_all(self):
        self.text1.delete(0, END)
        self.text2.delete(0, END)
        self.text3.delete(0.0, END)

    def the_end_write_word(self):
        f = open('new_words.txt', 'r')
        text = f.read()
        message = """ЭТИ СЛОВА НУЖНО ВЫУЧИТЬ!-----
/////////////////////////////
""" + text
        f.close()
        
        self.text3.delete(0.0, END)
        self.text3.insert(0.0, message)


    def find_word(self):
        word = self.text1.get().lower().lstrip().rstrip()

        _word = Word()
        result = _word._translate(word)

        if result:
            self.text3.insert(0.0, result)
        else:
            message = "Подходящих слов нет\n\nПОРА БЫ ИХ ДОБАВИТЬ!!!"
            self.text3.insert(0.0, message)

    def new_word(self):
        word1 = self.text1.get().lower().lstrip().rstrip()
        word2 = self.text2.get().lower().lstrip().rstrip()

        if len(word1) == 0 or len(word2) == 0:
            self.text2.insert(0.0, "Зполните все поля")
            return 0
        elif (word1[0] in ABV_english and word2[0] in ABV_english) or (word1[0] in ABV_russian and word2[0] in ABV_russian):
            self.text3.delete(0.0, END)
            self.text3.insert(0.0, "Так ниизяяя, подумайте дважды")
        else:
            languages = ['russian', 'english'] if word1[0] in ABV_russian else ['english', 'russian']
            
            word = Word(word=languages[0], translate=languages[1])
            result = word.set(word1, word2)

            if result == -1:
                self.text3.delete(0.0, END)
                self.text3.insert(0.0, "Такой вид перевода уже имеется")
            else:
                file = open('new_words.txt', 'a')
                file.write(word1+'-'+word2+'\n')
                file.close()
                
                self.text3.delete(0.0, END)
                self.text3.insert(0.0, "Перевод записан!")




#основная часть
root = Tk()
root.title("Переводишко")
root.geometry("460x440")

app = Application(root)

root.mainloop()
