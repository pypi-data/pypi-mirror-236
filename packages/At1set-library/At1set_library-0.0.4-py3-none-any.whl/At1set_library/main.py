# Переменная __all__ определяет, какое пространство имен будет импортировано при конскрукции "from main.py import *"

__all__ = ["__init__", "help", "Scripts"]

import random as _random
import os as _os
from time import sleep as _sleep
import pyautogui as _m
from pyperclip import copy as _copy
from ctypes import windll

def __init__(): # Функция инициализации библиотеки
  print("\n[__init__.py INFO] ============ Библиотека At1set_library успешно импотрирована! ============\n")
  print("[__init__.py INFO] Месторасположение данной библиотеки:", fr"'{__spec__.origin}'", "\n")

def help(needFileReference=False):
  """
    Команда для вывода справки.

    По дефолту, справка выдается в консоль,
    однако если вам надо, можно создать файл
    справки. Для этого передайте в функцию True.
    Файл со справкой создастся в текущем каталоге
  """
  Reference = """\
  ******** Справка по библиотеке At1set_library ********
  
  В настоящий момент данная библиотека находится в очень
  раннем состоянии и доступен лишь 1 скрипт - Игра 'Камень, ножницы, бумага'
  Для ее вызова воспользуйтесь функцией zu_e_fa().\
"""
  
  if needFileReference:
    with open("help.txt", "w", encoding="UTF-8") as file:
      file.write(Reference)
  else:
    return print("\n", Reference, "\n")

class Scripts():
  """
    Класс, который содержит в себе все
    прикольненькие скрипты, которые описаны
    в библиотеке. :)

  """
  def __init__(self) -> None:
    pass

  @staticmethod  
  def zu_e_fa():
    """
    Игра 'Камень, ножницы, бумага'
    """

    variables = ["камень", "ножницы", "бумага"]
    ai_score = 0
    score = 0

    print("Игра началась!")
    game_rooles = """
    Правила игры

    В начале игры вы вводите либо цифру:
    1 - Камень
    2 - Ножницы
    3 - Бумага

    Или просто слово целиком

    Камень побеждает ножницы, ножницы побеждают бумагу,
    бумага побеждает камень, все очень просто.

    После ввода, компьютер случайно выбирает 1 из 3х вариантов,
    после чего, либо он, либо вы выигрываете и зарабатываете +1
    балл \n
  """
    print(game_rooles)
    while True:
      print(f"\nТекущий счет: {score} {ai_score} \n")
      inp = input("Введите ваш выбор: ").strip().lower()
      isTextInput = False
      try:
        inp = int(inp)
        if inp > 3 or inp < 1:
          print("\nВы превысили возможный набор вариантов, возможно вы ошиблись, перезапускаю попытку...")
          _sleep(1)
          continue
      except:
        if inp == "exit()":
          print("\nВы завершили игру!")
          return _sleep(1)

        if inp in variables:
          inp = variables.index(inp)+1
        else:
          print("\nЭй, вы не играете по правилам! Для выхода, введите команду exit()")
          _sleep(1)
          continue
        isTextInput = True
      
      _sleep(0.5)
      if not isTextInput:
        print(f"\nВы выбрали {variables[inp-1].capitalize()}!")
      ai_decision = _random.randint(1, 3)
      print(f"\nКомпьютер выбирает", end="")
      print(f"{'.'}", end="")
      _sleep(0.5)
      print(f"{'.'}", end="")
      _sleep(0.5)
      print(f"{'.'}", end="")
      _sleep(0.5)
        
      print(f" {variables[ai_decision-1].capitalize()}! \n")
      _sleep(1)
      
      if ai_decision == inp:
        print("Ничья! Следующий раунд...")
        _sleep(1)
        continue

      isWin = False
      match inp:
        case 1:
          if ai_decision == 2:
            isWin = True
        case 2:
          if ai_decision == 3:
            isWin = True
        case 3:
          if ai_decision == 1:
            isWin = True
        case _:
          pass
      if isWin:
        print("Победа! вы заработали 1 очко")
        score += 1
      else:
        ai_score += 1
        print("Проигрыш! Компьютер зарабатывает 1 очко")

  @staticmethod
  def hehe_script():
    screenWidth, screenHeight = _m.size()
    _sleep(1)
    _m.moveTo(1, screenHeight, duration=0.1)
    _m.rightClick()
    _m.moveRel(100, -50, duration=0.1)
    x, y = _m.position()
    _m.moveRel(335, -45, duration=0.1)
    _sleep(1)
    _m.moveRel(0, -20, duration=0.1)
    _sleep(1)
    
    for i in range(3):
      _sleep(0.5)
      _m.press("esc")


    # hahaha
    _m.hotkey("win", "r")
    _m.press(["c", "m", "d"])
    _m.press("enter")
    for i in range(10):
      _m.press(["h", "a"])
    _m.press("enter")

    # dir
    _sleep(1)
    _m.press(["d", "i", "r"])
    _m.press("enter")
    _sleep(1)

    # exit
    _m.press(["e", "x", "i", "t"])
    _m.hotkey("shift", "9")
    _m.hotkey("shift", "0")
    _sleep(1)
    _m.press("enter")
    
    _sleep(1)
    _m.moveTo(1, screenHeight, duration=0.1)
    _m.rightClick()
    _m.moveRel(100, -50, duration=0.1)
    x, y = _m.position()
    _m.moveRel(335, -45, duration=0.1)
    _sleep(1)
    _m.moveRel(0, -20, duration=0.1)
    _sleep(1)
    _m.leftClick()

  @staticmethod
  def write_a_calc_script(speed=0.1, _isLayoutEn=True):

    """Спойлерить не хорошо,
    но по названию понятно, что сейчас
    будет происходить.
    
    Чтобы скрипт сработал правильно, переключите
    свою раскладку на ENG ДО начала работы скрипта."""
    
    if speed < 0.1: return print("Переменная {speed} не может принимать значение < 0.1!")
    _sleep(1)
    print("Для корректной работы скрипта необходимо сделать пару вещей.")
    _sleep(1)
    print("Вам необходимо ввести любой символ в консоль (\"no\" завершит скрипт, если вы запустили его по ошибке), после того запуститься таймер до начала работы скрипта.")
    _sleep(1)
    print("До истечения таймера, кликните курсором мыши на пустое место в файле программы/текущем файле .py")
    print("ОБЯЗАТЕЛЬНО ПЕРЕКЛЮЧИТЕ РАСКЛАДКУ КЛАВИАТУРЫ НА ENG!")
    message = input("Готовы? : ")
    if message == "no": return None
    _sleep(2)
    print("5")
    _sleep(1)
    print("4")
    _sleep(1)
    print("3")
    _sleep(1)
    print("2")
    _sleep(1)
    print("1")
    _sleep(2)
    print("Поехали!")

    for i in range(3):                
      _m.press("enter")

    _sleep(1)
    string = """def calculator():
result = 0
err_message = \""""
    _m.write(string, interval=speed)
    _copy("Похоже, вы ошиблись при вводе. Пожалуйста проверьте правильность вводимых вами данных!")
    _m.hotkey("ctrl", "v")
    _m.write("\"", interval=speed)
    
    string = """

try:
a = float(input(\""""
    _m.write(string, interval=speed)

    _copy("Введите число a: ")
    _m.hotkey("ctrl", "v")
    string = "\"))"
    _m.write(string, interval=speed)

    string = """
x = float(input(\""""
    _m.write(string, interval=speed)

    _copy("Введите число b: ")
    _m.hotkey("ctrl", "v")
    string = "\"))"
    _m.write(string, interval=speed)

    string = """
operation_type = int(input(\""""
    _m.write(string, interval=speed)

    _copy("Введите тип операции (цифру): \\n1) +\\n2) -\\n3) *\\n4) /\\n\\n")
    _m.hotkey("ctrl", "v")
    string = "\"))"
    _m.write(string, interval=speed)

    string = """
except:
return print(err_message)
"""
    _m.write(string, interval=speed)

    _m.press("enter", interval=speed)

    string = """match operation_type:
case 1:
result = a + x

"""

    _m.write(string, interval=speed)
    string = """\bcase 2:
result = a - x

"""
    _m.write(string, interval=speed)
    string = """\bcase 3:
result = a * x

"""
    _m.write(string, interval=speed)
    string = """\bcase 4:
result = a / x

"""
    _m.write(string, interval=speed)
    string = """\bcase _:
return print(err_message)
"""
    _m.write(string, interval=speed)

    string = """
\breturn print(result)
"""
    _m.write(string, interval=speed)

    string = """

calculator()"""
    _m.write(string, interval=speed)

    print("Готово! P.S. Не забудьте закомментировать строку с вызовом данного скрипта, если хотите протестировать работоспособность написанного калькулятора!")