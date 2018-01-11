#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sqlite3
import string


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.but1 = Button(root, text="Добавить",)
        self.but1.place(x=0, y=55, width=100)
        self.but1['command'] = self.new_word

        self.but2 = Button(root, text="Перевести")
        self.but2.place(x=100, y=55, width=100)
        self.but2['command'] = self.find_word

        self.but4 = Button(root, text="Закончить!")
        self.but4.place(x=25, y=180, width=150)
        self.but4['command'] = self.the_end_write_word

        self.but5 = Button(root, text="Отчистить всё...")
        self.but5.place(x=25, y=210, width=150)
        self.but5['command'] = self.remove_all

        
        self.but6 = Button(root, text="Обнулить слова")
        self.but6.place(x=25, y=280, width=150)
        self.but6['command'] = self.remove_new_words

        self.but6d1 = Button(root, text="Создать тест")
        self.but6d1.place(x=25, y=370, width=150)
        self.but6d1['command'] = self.make_test

        self.but6d2 = Button(root, text="Выбрать тест")
        self.but6d2.place(x=25, y=400, width=150)
        self.but6d2['command'] = self.find_test

        self.lab1 = Label(root, text="Слово для перевода:")
        self.lab1.place(x=10, y=5)

        self.lab2 = Label(root, text="Перевод:")
        self.lab2.place(x=10, y=90)

        self.lab3 = Label(root, text="Слова для изучения и повторения:")
        self.lab3.place(x=200, y=0)

        self.lab4 = Label(root, text="Введите название теста")
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

    def find_test(self):
        import findTest
        some = Tk()
        some.title("Выберите тест")
        some.geometry("160x115")
        pp = findTest.Application(some)
        some.mainloop()

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
        con = sqlite3.connect('words.db')
        cur = con.cursor()
        eng = False

        if len(word) != 0 and word[0] in string.ascii_lowercase:
            eng = True
        elif len(word) == 0:
            return 0

        sql = "SELECT * FROM words WHERE word LIKE '%"+word+"%'"
        try:
            cur.execute(sql)
        except sqlite3.DatabaseError as err:
            self.text3.delete(0.0, END)
            self.text3.insert(0.0, "Подходящих слов нет\n\n ПОРА БЫ ИХ ДОБАВИТЬ!!!")
            print("Ошибка: ", err)
        else:
            self.text3.delete(0.0, END)
            message = word.upper() + "------------------\n"
            text = "" 
            for id_t, name in cur:
                cur2 = con.cursor()
                sql = "SELECT * FROM translate WHERE word1='" + str(id_t) + "' OR word2='" + str(id_t) + "'"
                cur2.execute(sql)
                for id_t, word1, word2 in cur2:
                    cur3_1 = con.cursor()
                    cur3_2 = con.cursor()
                    sql1 = "SELECT word FROM words WHERE id='" + str(word1) + "'"
                    sql2 = "SELECT word FROM words WHERE id='" + str(word2) + "'"
                    cur3_1.execute(sql1)
                    cur3_2.execute(sql2)
                    word1 = cur3_1.fetchone()[0]
                    word2 = cur3_2.fetchone()[0]
                    
                    if word1[0] in string.ascii_lowercase:
                        if eng:
                            text = word1 + " - " + word2
                        else:
                            text = word2 + " - " + word1
                    else:
                        if eng:
                            text = word2 + " - " + word1
                        else:
                            text = word1 + " - " + word2 
                    message = message + text + "\n"

                    cur3_1.close()
                    cur3_2.close()
    
                cur2.close()
            cur.close()
            if text == "":
                message = message + "Подходящих слов нет\n\nПОРА БЫ ИХ ДОБАВИТЬ!!!"
                self.text3.insert(0.0, message)
                con.close()
                return 0
            self.text3.insert(0.0, message)
            con.close()

    def new_word(self):
        word1 = self.text1.get().lower().lstrip().rstrip()
        word2 = self.text2.get().lower().lstrip().rstrip()

        if len(word1) == 0 or len(word2) == 0:
            self.text2.insert(0.0, "Зполните все поля")
            return 0
        else:

            may_work = False
            word1_bool = False
            word2_bool = False

            con = sqlite3.connect('words.db')

            sql1 = "SELECT * FROM words WHERE word='"+word1+"'"
            sql2 = "SELECT * FROM words WHERE word='"+word2+"'"
            cur_1 = con.cursor()
            cur_2 = con.cursor()
            
            cur_1.execute(sql1)
            cur_2.execute(sql2)
            
            try:
                id_1 = cur_1.fetchone()[0]
                id_2 = cur_2.fetchone()[0]
            except:
                may_work = True
                cur_1.close()
                cur_2.close()
            else:
                cur_1.close()
                cur_2.close()

                cur_3 = con.cursor()
                sql = "SELECT * FROM translate WHERE (word1='"+str(id_1)+"' AND word2='"+str(id_2)+"') OR (word1='"+str(id_2)+"' AND word2='"+str(id_1)+"')"
                cur_3.execute(sql)
                try:
                    id_3 = cur_3.fetchone()[0]
                except:
                    cur_3.close()
                    may_work = True
                else:
                    self.text3.delete(0.0, END)
                    self.text3.insert(0.0, "Такой вид перевода уже имеется")
                    cur_3.close()
                    con.close()
                    return 0

            if may_work:
                #print("можем работать!")
                arr = [
                        (word1,),
                        (word2,)
                        ]
                sql = "INSERT INTO words(word) VALUES(?)"
                st = word1 + "-" + word2 + "\n"
                f = open('new_words.txt', 'a')
                f.write(st)
                f.close()
            
                con.close()
                con = sqlite3.connect('words.db')
                cur = con.cursor()
                cur.executemany(sql, arr)
                con.commit()
                cur.close()

                cur = con.cursor()
                sql = "SELECT id FROM words"
                cur.execute(sql)
                id_cr = 0
                id_pr = 0
                cnt = 0
                for id_t in cur:
                    cnt += 1
                cnt2 = 0 
                cur.execute(sql)
                for id_t in cur:
                    cnt2 += 1
                    if cnt - 1 == cnt2:
                        id_pr = id_t[0]
                    id_cr = id_t[0]

                sql = "INSERT INTO translate(word1, word2) VALUES(?,?)"
                idd = (id_pr, id_cr)
                cur.execute(sql, idd)
                con.commit()
                cur.close()
                con.close()
                
                self.text3.delete(0.0, END)
                self.text3.insert(0.0, "Перевод записан!")
            else:
                return 0




#основная часть
root = Tk()
root.title("Переводишко")
root.geometry("460x440")

app = Application(root)

root.mainloop()
