from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import sqlite3
from sqlite3 import Error
import os.path
from kivy.uix.widget import Widget
swords_name=['Stormbringer','Endbringer','Lightbringer','Vengeful Crusader']
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
            heroes_table = """ CREATE TABLE heroes (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    Name         TEXT    NOT NULL
                         UNIQUE,
    MaxHp        INT     NOT NULL,
    Hp           INT     NOT NULL,
    MaxMana      INT     NOT NULL,
    Mana         INT     NOT NULL,
    Level        INT     NOT NULL,
    Gold         INT     NOT NULL,
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
            items_table= '''CREATE TABLE items (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         CHAR,
    place        CHAR,
    type         CHAR    NOT NULL,
    color        CHAR,
    morehp       INT,
    moremp       INT,
    morestr      INT,
    moredext     INT,
    moreint      INT,
    moreluck     INT,
    moreattack   INT,
    moremattack  INT,
    moredefense  INT,
    moremdefense INT,
    bckimage     CHAR,
    info         CHAR
);'''
            eq_table='''CREATE TABLE eq (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    id_button    CHAR,
    id_item      INT REFERENCES items (id));'''
            heroes_eq_table='''CREATE TABLE heroes_eq (
    id       INTEGER PRIMARY KEY,
    place    CHAR    NOT NULL
                     UNIQUE,
    idofitem INT     REFERENCES items (id) 
);'''
            sword_test='''INSERT INTO items (name,type,moreattack,bckimage)
                VALUES ('Kaczucha','sword',5,'items/sword/sword_1.png');

'''
            GlobalAction.sqlrun(heroes_table)
            GlobalAction.sqlrun(conf_table)
            GlobalAction.sqlrun(conf_value)
            GlobalAction.sqlrun(items_table)
            GlobalAction.sqlrun(eq_table)
            GlobalAction.sqlrun(heroes_eq_table)
            GlobalAction.sqlrun(sword_test)
    def create_hero(name,maxhp=10,hp=10,maxmana=5,mana=5,lvl=1,exp=0,stre=1,dext=1,inte=1,luck=1,attack=10,magicattack=5,defense=0,magicdefense=0):
        create_character=''' INSERT INTO Heroes (Name,MaxHp,Hp,Maxmana,Mana,Level,Gold,Str,Dext,Int,Luck,Attack,MagicAttack,Defense,MagicDefense)
             VALUES ('{0}',{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14});'''.format(name,maxhp,hp,maxmana,mana,lvl,exp,stre,dext,inte,luck,attack,magicattack,defense,magicdefense)
        GlobalAction.sqlrun(create_character)       
class NewGameScreen(Screen):
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
            sm.current='hero'
            
class HeroScreen(Screen): 
    def __init__(self,**kwargs):
        super().__init__()
    def on_pre_enter(self):
        select_character='''SELECT *
  FROM Heroes
'''
        leng_eq=1
        while leng_eq<31:
            
            select_eq_items=''' SELECT *
  FROM eq
  WHERE id={}'''.format(leng_eq)
            
            b=GlobalAction.sqlrun(select_eq_items)
            try:
                if not b:
                    id_btn='eq_'+str(leng_eq)
                    self.ids[id_btn].background_normal='items/default/default.png'
                    self.ids[id_btn].background_down='items/default/default.png'
                else:
                    id_btn=b[0][1]
                    id_item=b[0][2]
                    select_item_properte=''' SELECT *
  FROM items
  WHERE id={}'''.format(id_item)
                    c=GlobalAction.sqlrun(select_item_properte)
                    self.ids[id_btn].background_normal=c[0][15]
                    self.ids[id_btn].background_down=c[0][15]
                    self.ids[id_btn].bind(on_press=lambda x:self.item_popup())
            except IndexError:
                pass
                
            leng_eq+=1
            
        a=GlobalAction.sqlrun(select_character)
        self.ids.gold.text='Gold '+str(a[0][7])
        self.ids.hp.text='Hp '+str(a[0][2])+'/'+str(a[0][3])
        self.ids.mana.text='Mana '+str(a[0][4])+'/'+str(a[0][5])
        self.ids.attack.text='Attack '+str(a[0][12])
        self.ids.mattack.text='Magic Attack '+str(a[0][13])
        self.ids.defense.text='Defense '+str(a[0][14])
        self.ids.mdefense.text='Magic Defense '+str(a[0][15])
        self.ids.lvl.text='Lvl '+str(a[0][6])
        self.ids.stre.text='Str '+str(a[0][8])
        self.ids.dext.text='Dext '+str(a[0][9])
        self.ids.inte.text='Int '+str(a[0][10])
        self.ids.luck.text='Luck '+str(a[0][11])
    def on_leave(self):
        pass
    def item_popup(*arg):
        box=BoxLayout(orientation='vertical')
        box.add_widget(Button(text='Info'))
        box.add_widget(Button(text='Equipment'))
        popup = Popup(title='"Weapon name"',
        content=box,
        separator_height='0',
        size_hint=(None, None), size=(200, 150))
        popup.open()

    
class CityScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()

class MapScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
        
class AdventureScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')
sm = ScreenManager(transition=NoTransition())
class InfinityHeroApp(App):
    def change_ss(self,name):
        sm.current=name
    def build(self):
        GlobalAction()
        check_intro='''SELECT INTRO
  FROM conf
 WHERE id = 1;
'''
        a=GlobalAction.sqlrun(check_intro)
        if a[0][0]=='False':
            sm.add_widget(NewGameScreen(name='newgame'))
        else:
            pass
        sm.add_widget(HeroScreen(name='hero'))
        sm.add_widget(CityScreen(name='city'))
        sm.add_widget(MapScreen(name='map'))
        sm.add_widget(AdventureScreen(name='adventure'))
        return sm
    def on_pre_leave(self):
        dbsql.conn.close()
InfinityHeroApp().run()   
