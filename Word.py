#-*- coding:utf-8 -*-

import sqlite3
import Log

path = "./words.db"
logFile = Log.Log('logs', './')

class Word:
    def __init__(self, word='russian', translate='english'):
        self.word = ""
        self.translate = ""
        self.cf = {
        '_word': word,
        '_translate': translate
        }

    def set(self, word, translate):
        conn = sqlite3.connect(path)
        cf = {
        '_word': word,
        '_translate': translate
        }
        _id = {}

        for i in self.cf:
            _str = "SELECT id FROM "+self.cf[i]+" WHERE word='"+cf[i]+"'"
            #_id.append(None)
            cursor = conn.cursor()
            cursor.execute(_str)
            
            _idDb = cursor.fetchone()
            if not _idDb:
                _str = "INSERT INTO "+self.cf[i]+" (word) VALUES ('"+cf[i]+"')"
                cursor.execute(_str)
                conn.commit()
                
                _cursor = conn.execute("SELECT MAX(id) FROM "+self.cf[i])

                try:
                    _id[self.cf[i]]= _cursor.fetchone()[0]
                except:
                    _id[self.cf[i]]= 0
            else:
                _id[self.cf[i]]= str(_idDb[0])
                    
        _sqlM = []
        _sqlM.append("SELECT * FROM translation WHERE russian='"+str(_id[self.cf['_word']])+"' AND english='"+str(_id[self.cf['_translate']])+"'")
        _sqlM.append("SELECT * FROM translation WHERE russian='"+str(_id[self.cf['_translate']])+"' AND english='"+str(_id[self.cf['_word']])+"'")

        stop = False
        for i in _sqlM:
            cursor = conn.cursor()
            cursor.execute(i)
            if len(cursor.fetchall()) != 0:
                stop = True
                break

        if not stop:
            #_id = [_id[0], _id[1]] if self.cf['_word'] == 'russian' else [_id[1], _id[0]]
            _sql = "INSERT INTO translation ("+self.cf['_word']+","+self.cf['_translate']+") VALUES ('"+str(_id[self.cf['_word']])+"','"+str(_id[self.cf['_translate']])+"')"
            print(_sql)
            cursor = conn.cursor()
            cursor.execute(_sql)
            conn.commit()
            return 0
        
        else:
            logFile.write('Такой перевод уже существует '+word+":"+translate)
            return -1

    def _translate(self, word):
        conn = sqlite3.connect(path)

        _sqlM = []
        _sqlM.append("SELECT id FROM russian WHERE word='"+word+"'")
        _sqlM.append("SELECT id FROM english WHERE word='"+word+"'")

        result = None
        number = 0
        for i in _sqlM:
            number += 1
            cursor = conn.cursor()
            cursor.execute(i)

            _result = cursor.fetchone()            
            if _result:
                result = _result[0]
                break
            
        if result:
            columns = ['english', 'russian'] if number == 1 else ['russian', 'english']  #выбор идёт наоборот            
            _sql = "SELECT "+columns[0]+" FROM translation WHERE "+columns[1]+"='"+str(result)+"'"

            cursor = conn.cursor()
            cursor.execute(_sql)

            _id = cursor.fetchall()
            result = word.upper()+":\n"
            for i in _id:
                _sql = "SELECT word FROM "+columns[0]+" WHERE id='"+str(i[0])+"'"
                _result = cursor.execute(_sql).fetchone()[0]
                
                result = result + " => " + _result + "\n"

            return result
        else:
            return result
        

    def save(self):
        pass
