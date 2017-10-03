from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import sqlite3
from sqlite3 import Error
import os.path
from kivy.uix.widget import Widget

#from win32api import GetSystemMetrics
#print "Width =", GetSystemMetrics(0)
#print "Height =", GetSystemMetrics(1)
class GlobalAction:
    
    def sqlddl(conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
        except Error as e:
            pass
    def __init__(self):
        if os.path.exists('infinity_hero_game.db')==True:
            try:  
                conn = sqlite3.connect('infinity_hero_game.db')
            except Error as e:
                pass
        else:
            heroes_table = """ CREATE TABLE Heroes (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    Name         TEXT    NOT NULL
                         UNIQUE,
    MaxHp        INT     NOT NULL,
    Hp           INT     NOT NULL,
    MaxMana      INT     NOT NULL,
    Mana         INT     NOT NULL,
    Level        INT     NOT NULL,
    Exp          INT     NOT NULL,
    Str          INT     NOT NULL,
    Dext         INT     NOT NULL,
    Int          INT     NOT NULL,
    Luck         INT     NOT NULL,
    Attack       INT     NOT NULL,
    MagicAttack  INT     NOT NULL,
    Defense      INT     NOT NULL,
    MagicDefense INT     NOT NULL
); """
            conf_table= """ CREATE TABLE conf (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    INTRO BOOLEAN NOT NULL             
);"""
            conf_value=''' INSERT INTO conf (INTRO)
                 VALUES ('False');'''
            conn = sqlite3.connect('infinity_hero_game.db')
            GlobalAction.sqlddl(conn, heroes_table)
            GlobalAction.sqlddl(conn, conf_table)
            GlobalAction.sqlddl(conn, conf_value)
    
def Menu(self):
    #Hero, city, map, adventure
    left_buttons=[(Button,'Hero'),(Button,'City'),(Button,'Map'),(Button,'Adventure')]
    layout = BoxLayout(orientation='horizontal',padding=20,spacing=5)
    self.layout_l = GridLayout(cols=1,size_hint=(0.2,1))
    self.layout_r = BoxLayout(orientation='horizontal',size_hint=(0.8,1))
    layout.add_widget(self.layout_l)
    layout.add_widget(self.layout_r)
    for num in left_buttons:
        wid_t=num[0]
        wid_te=num[1]
        btn=wid_t(text=wid_te,font_size='15dp')
        btn.texture_update()
        self.layout_l.add_widget(btn)
    
    self.add_widget(layout)
class IntroWidget(Widget):
    pass
class StatsWidget(Widget):
    pass
class BeginScreen(Screen): 
    def __init__(self,**kwargs):
        super().__init__()
        if 1==1:
            print(self.ids) 
        else:
            pass
            #pokaz statystyki, nazwa level, czas gry
    
class BohaterScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
        Menu(self)
        btn=Button(text=str('Hi!'))
        self.layout_r.add_widget(btn)
        
class InfinityHeroApp(App):   
    from kivy.config import Config
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '400')
    def build(self):
        sm = ScreenManager()
        sm.add_widget(BeginScreen(name='intro'))
        sm.add_widget(BohaterScreen(name='bohater'))
        GlobalAction()
        return sm
    def on_pre_leave(self):
        dbsql.conn.close()
    def create_hero(self,name):
        print(name)
        
    

InfinityHeroApp().run()
