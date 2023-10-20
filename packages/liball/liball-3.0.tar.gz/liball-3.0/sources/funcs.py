# from buble import *
import time
import os

def aperimeter(a, b = None):
    if b != None:
        try:
            return (a+b)*2
        except:
            return "FATAL ERROR"
    else:
        try:
            return a*4
        except:
            return "FATAL ERROR"

def asquare(a, b = None):
    if b != "pass":
        try:
            return a*b
        except:
            return "FATAL ERROR"
    else:
        try:
            return a*a
        except:
            return "FATAL ERROR"

"""^^^^ Площадь и Периметр ^^^^"""

def atime(timef, typef = 'sec'):
    try:
        if typef == 'sec':
            return eval(time.sleep(timef))
        elif typef == 'mlsec':
            return eval(time.sleep(timef/1000))
    except:
        return "FATAL ERROR time construction or library construction"

def apause():
    try:
        return eval(os.system('pause'))
    except:
        return "FATAL ERROR pause construction or library construction"

def adownload(proceng = 101, shag = 0.1, pause = False, language = 'ru'):
    if language == 'ru':
        s='|'
        for i in range(proceng):
            time.sleep(shag)
            print('\r','Загруска: ',i*s,str(i),'%',end='')
        print ('')
        if pause == True:
            os.system('pause')
    elif language == 'en':
        s='|'
        for i in range(proceng):
            time.sleep(shag)
            print('\r','Download: ',i*s,str(i),'%',end='')
        print ('')
        if pause == True:
            os.system('pause')

"""^^^^ пауза, задержка и загрузка ^^^^"""


def register(count=1, language='ru', downloadf=True):
    array_login = []
    array_password = []
    array_reg = []
    if language == 'ru':
        for i in range(count):
            login = str(input('Введите логин: '))
            password = str(input('Введите пароль: '))
            array_login.append(login)
            array_password.append(password)
        if downloadf == True:
            adownload()
        print('Регитрация успешно завершена.')
    elif language == 'en':
        for i in range(count):
            login = str(input('Enter the login: '))
            password = str(input('Enter the password: '))
            array_login.append(login)
            array_password.append(password)
        if downloadf == True:
            adownload(language='en')
        print('Registration completed successfully.')

    array_reg.append(array_login)
    array_reg.append(array_password)
    return array_reg


def login(logins, count=1, language='ru', downloadf=True):
    array_login = logins[0]
    array_password = logins[1]

    array_loginf = []
    array_passwordf = []
    array_logins = []
    if language == 'ru':
        for i in range(count):
            login = str(input('Введите логин: '))
            password = str(input('Введите пароль: '))
            if login in array_login:
                passwordf = array_password[array_login.index(login)]
                if passwordf == password:
                    array_loginf.append(login)
                    array_passwordf.append(password)
                    print('Вход успешно завершен.')
                    print()
                else:
                    array_loginf.append('False')
                    array_passwordf.append('False')
                    print('Неправельный логин или пароль.')
                    print()
            else:
                array_loginf.append('False')
                array_passwordf.append('False')
                print('Неправельный логин или пароль.')
                print()

        array_logins.append(array_loginf)
        array_logins.append(array_passwordf)
        if downloadf == True:
            adownload()
        return array_logins

"""Вход и регистрация"""


"""
def bif(condition, action, elaction = 'False', elifcondition = 'False', elifaction = 'False'): #if else elif action - дейтвие, condition - условие
    try:
        if eval(str(condition)):
            return eval(str(action))
        elif eval(str(elifcondition)):
            return eval(str(elifaction))
        else:
            return eval(str(elaction))
    except:
        return "FATAL ERROR if construction or library construction"
def bwhile(condition, action): #while action - дейтвие, condition - условие
    try:
        while eval(str(condition)):
            eval(str(action))
    except:
        return "FATAL ERROR while construction or library construction"
def bfor(condition, action, rangef): #for action - дейтвие, condition - условие
    try:
        #return "for"
        for condition in eval(str(rangef)): #eval(str(condition)):
            eval(str(action))
    except:
        return "FATAL ERROR for construction or library construction"

Old library - buble
"""