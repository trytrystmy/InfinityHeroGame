from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
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
    
    def sqlrun(sql):
        try:
            conn = sqlite3.connect('infinity_hero_game.db')
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            rows=c.fetchall()
            values=[]
            for element in rows:
                values.append(element)
            return values
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
            GlobalAction.sqlrun(heroes_table)
            GlobalAction.sqlrun(conf_table)
            GlobalAction.sqlrun(conf_value)
    def create_hero(name,maxhp=10,hp=10,maxmana=5,mana=5,lvl=1,exp=0,stre=1,dext=1,inte=1,luck=1,attack=10,magicattack=5,defense=0,magicdefense=0):
        create_character=''' INSERT INTO Heroes (Name,MaxHp,Hp,Maxmana,Mana,Level,Exp,Str,Dext,Int,Luck,Attack,MagicAttack,Defense,MagicDefense)
             VALUES ('{0}',{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14});'''.format(name,maxhp,hp,maxmana,mana,lvl,exp,stre,dext,inte,luck,attack,magicattack,defense,magicdefense)
        GlobalAction.sqlrun(create_character)
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
class InfoScreen(Screen):
    pass
class BeginScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
         
    def create_hero(self,name,validate):
        name=" ".join(name.split())
        if name=='':
            validate.text='Can not be empy!'
            validate.size_hint=(1,0.7)
        elif len(name)>15:
            validate.text='Too much letter max 15!'
            validate.size_hint=(1,0.7)
            self.ids.name.text=''
        else:
            GlobalAction.create_hero(name)
            conf_intro_true=''' UPDATE conf
   SET INTRO = 'True'
 WHERE id = 1;'''
            GlobalAction.sqlrun(conf_intro_true)
            sm.current='bohater'
            

               
class BohaterScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
        Menu(self)
        btn=Button(text=str('Hi!'))
        self.layout_r.add_widget(btn)
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')
sm = ScreenManager(transition=NoTransition())
class InfinityHeroApp(App):
      
    def build(self):
        check_intro='''SELECT INTRO
  FROM conf
 WHERE id = 1;
'''
        a=GlobalAction.sqlrun(check_intro)
        print(a[0])
        print(a)     
        if a[0]==True:
            print(True)
            sm.add_widget(InfoScreen(name='info'))
        else:
            print(False)
            sm.add_widget(BeginScreen(name='begin'))
        sm.add_widget(BohaterScreen(name='bohater'))
        
        GlobalAction()
        return sm
    def on_pre_leave(self):
        dbsql.conn.close()

InfinityHeroApp().run()
