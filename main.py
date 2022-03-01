from PyQt5.QtWidgets import QMainWindow,QFileDialog,QStackedWidget,QListWidgetItem,QTextEdit,QListWidget ,QApplication ,QWidget, QLabel , QPushButton , QToolButton , QPushButton ,QScrollArea , QLineEdit, QFrame,QMenuBar,QDial,QGroupBox,QFormLayout
from PyQt5 import uic
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5 import QtGui
import mysql.connector as msqc
import pygame
from pygame import mixer
from PIL import Image
import sys 
db = msqc.connect(host = "localhost", username = "root", password = " " , database ="graphic_player",)
cur = db.cursor(buffered=True)
mixer.init()
class win(QMainWindow):
    def __init__(self,playlist_name=""):
        super(win, self).__init__()
        uic.loadUi('player.ui',self)
        self.lst_song = self.findChild(QScrollArea,"songs")
        self.vol_dial = self.findChild(QDial , "vol_dial")
        self.vol_lbl = self.findChild(QLabel , "vol")
        self.create = self.findChild(QPushButton , "create_playlist")
        self.playplaylist = self.findChild(QPushButton , "play_playlist")
        self.refresh = self.findChild(QPushButton , "refresh")
        self.current_playlist = self.findChild(QLabel , "current_playlist")
        self.current_thumbnail = self.findChild(QLabel , "current_thumbnail")
        self.current_song_name = self.findChild(QLabel , "current_song_name")
        self.pause = self.findChild(QPushButton , "pause")
        self.next = self.findChild(QPushButton , "next")
        self.play = self.findChild(QPushButton , "play")
        self.play_that_song = self.findChild(QPushButton , "play_that_song")
        self.song_number_in_playlist = self.findChild(QLineEdit , "song_number_in_playlist")
        self.previous = self.findChild(QPushButton , "previous")
        ##################################################################################
        self.play_that_song.clicked.connect(lambda :PLAY_SONG())
        self.play.clicked.connect(lambda :PLAY())
        self.previous.clicked.connect(lambda : PREVIOUS())
        self.create.clicked.connect(lambda : create_play())
        self.playplaylist.clicked.connect(lambda : play_list())
        self.next.clicked.connect(lambda : NEXT())
        self.vol_dial.valueChanged.connect(lambda : set_vol())
        self.refresh.clicked.connect(lambda : REFRESH())
        self.pause.clicked.connect(lambda : PAUSE())
        ####################################################################################
        self.current_playlist.setText(f"Current Playlist:\n {playlist_name}")
        self.current_song_name.setText(f"Current Song :- None")
        global name_of_playlist;name_of_playlist = playlist_name
        global pse,song_current; pse = 1;song_current =""
        global song_no , name_songs ,thumbnails;song_no = 0
        name_songs = []
        thumbnails = []
        list_song =[]
        def REFRESH():
            global song_no , name_songs ,thumbnails,list_song
            song_no = 0
            name_songs = []
            thumbnails = []
            list_song =[]
            self.current_playlist.setText(f"Current Playlist:\n \n{name_of_playlist.capitalize()}")
            query = f"SELECT music_name , music_thumbnail FROM {name_of_playlist}"

            try:
                mixer.music.stop()
                cur.execute(query)
                a = cur.fetchall()
                thumbnail = []
                nm_songs = []
                formlayout = QFormLayout()
                groupbox = QGroupBox()
                groupbox.setStyleSheet("border-radius:10px")
                try:
                    x = 1
                    for songs in a:
                        name_songs.append(songs[0])  
                        thumbnails.append(songs[1]) 
                    for detail in range(len(name_songs)):
                        label_1 = QLabel(f"  {x}. {name_songs[detail]}")
                        x +=1
                        label_1.setFont(QFont('Bahnschrift SemiBold', 12))
                        label = QLabel()
                        pixmap = QPixmap(f"{thumbnails[detail]}")
                        pixmap = pixmap.scaled(70, 55)
                        label.setPixmap(pixmap)
                        label_1.setStyleSheet("color: #fff")
                        thumbnail.append(label_1)
                        nm_songs.append(label)
                        formlayout.addRow(nm_songs[detail],thumbnail[detail])
                except :
                    self.current_song_name.setText(f"Current Song :- None")
                    pixmap = QPixmap("E:\Python Practice\GUI PyQt5\ICONS FOR APP\image-filled-square-button")
                self.current_thumbnail.setPixmap(pixmap)
                groupbox.setLayout(formlayout)
                self.lst_song.setWidget(groupbox)
                self.current_song_name.setText(f"Current Song :- {name_songs[0]}")
                pixmap = QPixmap(f"{thumbnails[0]}")
                self.current_thumbnail.setPixmap(pixmap)
                query = f"SELECT music_location FROM {name_of_playlist}"
                cur.execute(query)
                a = cur.fetchall()
                song_no = 0
                list_song = a    
                song_current = a[0][0]
                 
                # mixer.music.load(f"{music}")
                # mixer.music.play()
            except:
                pass
        def PLAY_SONG():
            no = self.song_number_in_playlist.text()
            try:
                if (len(no)!=0):
                    try:
                        global song_no , list_song , thumbnails ,name_songs
                        song_no = int(no)-1
                        # print(f"{list_song[song_no][0]}",f"{thumbnails[song_no]}",f"Current Song :- {name_songs[song_no]}")
                        mixer.music.load(f"{list_song[song_no][0]}")
                        mixer.music.play()
                        pixmap = QPixmap(f"{thumbnails[song_no]}")
                        self.current_thumbnail.setPixmap(pixmap)
                        self.current_song_name.setText(f"Current Song :- {name_songs[song_no]}")
                    except:
                        pass
            except:
                pass
        def PLAY():
            try:
                global song_no , list_song 
                # print(f"{list_song[song_no][0]}",f"{thumbnails[song_no]}",f"Current Song :- {name_songs[song_no]}")
                mixer.music.load(f"{list_song[song_no][0]}")
                mixer.music.play()
            except:
                pass
        def PAUSE():
            global pse 
            if (pse==1):   
                mixer.music.pause()
                pse = 0 
            else:
                mixer.music.unpause()
                pse = 1 
                # print(f"{list_song} list ")
        def NEXT():
            try:
                global song_no , list_song , thumbnails ,name_songs,pse  
                pse = 1    
                song_no = song_no +1
                # print(f"{list_song[song_no][0]}",f"{thumbnails[song_no]}",f"Current Song :- {name_songs[song_no]}")
                mixer.music.load(f"{list_song[song_no][0]}")
                mixer.music.play()
                pixmap = QPixmap(f"{thumbnails[song_no]}")
                self.current_thumbnail.setPixmap(pixmap)
                self.current_song_name.setText(f"Current Song :- {name_songs[song_no]}")
            except:
                pass
        def PREVIOUS():
            try:
                global song_no , list_song , thumbnails ,name_songs,pse 
                pse = 1 
                song_no = song_no -1
                # print(f"{list_song[song_no][0]}",f"{thumbnails[song_no]}",f"Current Song :- {name_songs[song_no]}")
                mixer.music.load(f"{list_song[song_no][0]}")
                mixer.music.play()
                pixmap = QPixmap(f"{thumbnails[song_no]}")
                self.current_thumbnail.setPixmap(pixmap)
                self.current_song_name.setText(f"Current Song :- {name_songs[song_no]}")
            except:
                pass
        def play_list():
            win_main.setCurrentIndex(win_main.currentIndex()+2)
        def create_play():
            win_main.setCurrentIndex(win_main.currentIndex()+1)
        def set_vol():
            self.val = self.vol_dial.value()
            pygame.mixer.music.set_volume((self.val)/100)
            self.vol_lbl.setText(f'Vol : {self.val}')        
class create(win):
    def __init__(self):
        super(create, self).__init__()
        uic.loadUi("create_card.ui",self)
        ######################################################################################
        self.back = self.findChild(QPushButton , "back")
        self.make = self.findChild(QPushButton , "make_playlist")
        self.name = self.findChild(QPushButton , "set_name")
        self.name_set = self.findChild(QLineEdit , "name")
        self.lbl_name = self.findChild(QLabel , "lbl_name")
        self.thumbnail_playlist = self.findChild(QLabel , "thumbnail_playlist")
        self.select_image = self.findChild(QPushButton , "select_image")
        self.set_thumbnail = self.findChild(QPushButton , "set_thumbnail")
        self.thumbnail_loc = self.findChild(QLineEdit , "thumbnail_loc")
        ########################################################################
        self.name.clicked.connect(lambda : create_name())
        self.back.clicked.connect(lambda : prev_win())
        self.make.clicked.connect(lambda : make_list())
        self.select_image.clicked.connect(lambda : sel_image())
        ######################################################################################
        file_loc = ""
        def sel_image():
            file = QFileDialog.getOpenFileName(self,"Open image","E:\\","png (*.png);;jpeg (*.jpg)")
            global file_loc
            file_loc = file[0]
            if len(file_loc)==0:
                pass 
            else:
                pixmap = QPixmap(file[0])
                self.thumbnail_playlist.setPixmap(pixmap)
                self.thumbnail_loc.setText(file[0])
        def create_name():
            if (len(self.name_set.text())==0):
                pass
            else:
                nam = self.name_set.text()
                self.lbl_name.setText(nam)
            
        def make_list():
            if (len(self.name_set.text())==0 or len(self.thumbnail_loc.text())==0):
                pass
            else :       
                query = f"CREATE TABLE {self.name_set.text()}(music_name VARCHAR(225) , music_location VARCHAR(225) , music_thumbnail VARCHAR(225))"
                
                print(query)
                try :
                    cur.execute(query)
                    db.commit()
                    query = f"INSERT INTO playlist_info values ('{self.name_set.text().lower()}' , '{self.thumbnail_loc.text()}') "
                    try :
                        cur.execute(query)
                        db.commit()
                        win_main.setCurrentIndex(win_main.currentIndex()+1)
                        win_play().REFRESH()
                    except :
                        cur.rollback()
                        print("Error occured")
                except :
                    print("Already Exist")
                # self.name_set.text()
        def prev_win():
            self.thumbnail_loc.setText("")
            win_main.setWindowTitle("Music Player")
            win_main.setCurrentIndex(win_main.currentIndex()-1)
 

class win_play(win):
    def __init__(self):
        super(win_play, self).__init__()
        uic.loadUi("Playlist.ui",self)
         
        self.search = self.findChild(QPushButton , "search_playlist")
        self.back = self.findChild(QPushButton , "back")
        self.fram = self.findChild(QFrame , "frame")
        self.scroll = self.findChild(QScrollArea, "scrollArea")
        self.srch_name = self.findChild(QLineEdit, "srch_name")
        self.refresh_page = self.findChild(QPushButton , "refresh_page")
        ########################################################
        self.refresh_page.clicked.connect(lambda : REFRESH())
        self.back.clicked.connect(lambda : prev_win())
        self.search.clicked.connect(lambda :srch())        
        ########################################################
        def srch():
            txt = self.srch_name.text()
            txt = txt.lower()
            qty = f"SELECT * from playlist_info WHERE Name_of_playlist ='{txt}'"
            cur.execute(qty)
            a = cur.fetchall()  
            string = f"('{txt}',)"
            for list_name in a: # Need to imporve search algo
                if(txt==list_name[0]):
                    win_main.setWindowTitle(f"{txt}")
                    win_main.addWidget(play(list_name[0],list_name[1]))
                    win_main.setCurrentIndex(win_main.currentIndex()+1)
                    break
        # def default_playlist():
        #     formlayout = QFormLayout()
        #     groupbox = QGroupBox()
        #     thumbnail = []
        #     nm_songs = []
        #     sc = []
        #     thumbnails_playlist = []
        #     name_playlist= []
        #     query = f"SELECT * FROM playlist_info;"
        #     cur.execute(query)
        #     detail = cur.fetchall()
        #     for songs in detail:
        #             name_playlist.append(songs[0])  
        #             thumbnails_playlist.append(songs[1]) 
        #     for details in range(len(name_playlist)):
        #         scr = QScrollArea()
        #         scr.setStyleSheet("background:'black';border-radius:10px ")
        #         name_songs = []
        #         thumbnails_song = []
        #         query = f"SELECT music_name , music_thumbnail FROM {name_playlist[details]}"
        #         try:
        #             cur.execute(query)
        #             a = cur.fetchall()
        #             thumbnail_img = []
        #             songs_nm = []
        #             formlayouts = QFormLayout()
        #             groupboxs = QGroupBox()
        #             groupboxs.setStyleSheet("border-radius:10px")
        #             try:
        #                 x = 1
        #                 for songs in a:
        #                     name_songs.append(songs[0])  
        #                     thumbnails_song.append(songs[1]) 
        #                 for items in range(len(name_songs)):
        #                     label_1 = QLabel(f"  {x}. {name_songs[items]}")
        #                     x +=1
        #                     label_1.setFont(QFont('Bahnschrift SemiBold', 12))
        #                     label = QLabel()
        #                     pixmap = QPixmap(f"{thumbnails_song[items]}")
        #                     pixmap = pixmap.scaled(65, 50)
        #                     label.setPixmap(pixmap)
        #                     label_1.setStyleSheet("color: #fff")
        #                     thumbnail_img.append(label_1)
        #                     songs_nm.append(label)
        #                     formlayouts.addRow(songs_nm[items], thumbnail_img[items])
        #                 groupboxs.setLayout(formlayouts)
        #                 scr.setWidget(groupboxs)
        #                 scr.setMinimumHeight(150)  
        #                 scr.setMinimumWidth(150)
        #             except :
        #                 print("Error 1")
        #         except :
        #             print("Error")
        #         lbl= QLabel(f"{name_playlist[details].capitalize()}")
        #         lbl.setStyleSheet('''color:#fff;font: 63 12pt "Bahnschrift SemiBold";border-radius:10px''')
        #         # lbl.setGeometry(20,20,50,50)
        #         lbl_1 = QLabel()
        #         pixmap = QPixmap(f"{thumbnails_playlist[details]}")
        #         pixmap= pixmap.scaled(191,161)
        #         lbl_1.setStyleSheet("border-radius: 15px")
        #         lbl_1.setPixmap(pixmap)
        #         sc.append(scr)
        #         nm_songs.append(lbl)
        #         thumbnail.append(lbl_1)
        #         formlayout.addRow(thumbnail[details],nm_songs[details])
        #         # formlayout.addRow()
        #         formlayout.addRow(sc[details])
        #     groupbox.setLayout(formlayout)
        #     self.scroll.setWidget(groupbox)
        # default_playlist()
        def REFRESH():
            print("wr")
            formlayout = QFormLayout()
            groupbox = QGroupBox()
            thumbnail = []
            nm_songs = []
            sc = []
            thumbnails_playlist = []
            name_playlist= []
            query = f"SELECT * FROM playlist_info;"
            cur.execute(query)
            detail = cur.fetchall()
            for songs in detail:
                    name_playlist.append(songs[0])  
                    thumbnails_playlist.append(songs[1]) 
            for details in range(len(name_playlist)):
                scr = QScrollArea()
                scr.setStyleSheet("background:'black';border-radius:10px ")
                name_songs = []
                thumbnails_song = []
                query = f"SELECT music_name , music_thumbnail FROM {name_playlist[details]}"
                try:
                    cur.execute(query)
                    a = cur.fetchall()
                    thumbnail_img = []
                    songs_nm = []
                    formlayouts = QFormLayout()
                    groupboxs = QGroupBox()
                    groupboxs.setStyleSheet("border-radius:10px")
                    try:
                        x = 1
                        for songs in a:
                            name_songs.append(songs[0])  
                            thumbnails_song.append(songs[1]) 
                        for items in range(len(name_songs)):
                            label_1 = QLabel(f"  {x}. {name_songs[items]}")
                            x +=1
                            label_1.setFont(QFont('Bahnschrift SemiBold', 12))
                            label = QLabel()
                            pixmap = QPixmap(f"{thumbnails_song[items]}")
                            pixmap = pixmap.scaled(65, 50)
                            label.setPixmap(pixmap)
                            label_1.setStyleSheet("color: #fff")
                            thumbnail_img.append(label_1)
                            songs_nm.append(label)
                            formlayouts.addRow(songs_nm[items], thumbnail_img[items])
                        groupboxs.setLayout(formlayouts)
                        scr.setWidget(groupboxs)
                        scr.setMinimumHeight(150)  
                        scr.setMinimumWidth(150)
                    except :
                        print("Error 1")
                except :
                    print("Error")
                lbl= QLabel(f"{name_playlist[details].capitalize()}")
                lbl.setStyleSheet('''color:#fff;font: 63 12pt "Bahnschrift SemiBold";border-radius:10px''')
                # lbl.setGeometry(20,20,50,50)
                lbl_1 = QLabel()
                pixmap = QPixmap(f"{thumbnails_playlist[details]}")
                pixmap= pixmap.scaled(191,161)
                lbl_1.setStyleSheet("border-radius: 15px")
                lbl_1.setPixmap(pixmap)
                sc.append(scr)
                nm_songs.append(lbl)
                thumbnail.append(lbl_1)
                formlayout.addRow(thumbnail[details],nm_songs[details])
                # formlayout.addRow()
                formlayout.addRow(sc[details])
            groupbox.setLayout(formlayout)
            self.scroll.setWidget(groupbox)
        REFRESH()
        def prev_win():
            win_main.setCurrentIndex(0)
            
class play(QMainWindow):
    def __init__(self,nam,loc):
        super(play, self).__init__()
        uic.loadUi("addsong.ui",self)
        self.back = self.findChild(QPushButton , "back")
        self.thumbnail_list = self.findChild(QLabel , "thumbnail_list")
        self.list_name = self.findChild(QLabel , "list_name")
        self.refresh = self.findChild(QPushButton , "refresh")
        self.select = self.findChild(QPushButton , "select")
        self.select_2 = self.findChild(QPushButton , "select_2")
        self.song_name = self.findChild(QLineEdit , "song_name")
        self.song_loc = self.findChild(QLineEdit , "song_loc")
        self.add_song = self.findChild(QPushButton , "add_song")
        self.thumbnail_loc = self.findChild(QLineEdit , "thumbnail_loc")
        self.play = self.findChild(QPushButton , "play")
        self.scrollArea = self.findChild(QScrollArea , "scrollArea")
        ##########################################################################
        self.play.clicked.connect(lambda : PLAY())
        self.add_song.clicked.connect(lambda :ad_song())
        self.select.clicked.connect(lambda : sel())
        self.select_2.clicked.connect(lambda : sel_2())
        self.refresh.clicked.connect(lambda : refrsh())
        self.back.clicked.connect(lambda : prev_win())
        ############################################################################
        self.list_name.setText(nam)
        pixmap =QPixmap(loc)
        self.thumbnail_list.setPixmap(pixmap)
        global nm , lc                                                                 
        nm = nam ;lc=loc
        query = f"SELECT music_name , music_thumbnail FROM {nm}"
        cur.execute(query)
        a = cur.fetchall()
        name_songs = []
        thumbnails = []
        thumbnail = []
        nm_songs = []
        formlayout = QFormLayout()
        groupbox = QGroupBox()
        groupbox.setStyleSheet("border-radius:10px")
        try:
            x = 1
            for songs in a:
                name_songs.append(songs[0])  
                thumbnails.append(songs[1]) 
            for detail in range(len(name_songs)):
                label_1 = QLabel(f"  {x}. {name_songs[detail]}")
                x +=1
                label_1.setFont(QFont('Bahnschrift SemiBold', 12))
                label = QLabel()
                pixmap = QPixmap(f"{thumbnails[detail]}")
                pixmap = pixmap.scaled(70, 55)
                label.setPixmap(pixmap)
                label_1.setStyleSheet("color: #fff")
                thumbnail.append(label_1)
                nm_songs.append(label)
                formlayout.addRow(nm_songs[detail],thumbnail[detail])
        except :
            pass
        groupbox.setLayout(formlayout)
        self.scrollArea.setWidget(groupbox)
        ############################################################################
        def PLAY():
            win_main.addWidget(win(nm))
            win_main.setCurrentIndex(0)
        def ad_song():
            song_name = self.song_name.text()
            song_location =   self.song_loc.text()     
            song_thumbnail = self.thumbnail_loc.text()
            query = f"INSERT INTO {nm} VALUES('{song_name}' , '{song_location}' , '{song_thumbnail}')"
            cur.execute(query)
            db.commit()
            formlayout = QFormLayout()
            groupbox = QGroupBox()
            groupbox.setStyleSheet("background-color:#3D304C ; border-radius:10px")
            query = f"SELECT music_name , music_thumbnail FROM {nm}"
            cur.execute(query)
            a = cur.fetchall()
            name_songs = []
            thumbnails = []
            nm_songs = []
            thumbnail=[] 
            x=1
            for songs in a:
                name_songs.append(songs[0])  
                thumbnails.append(songs[1]) 
            for detail in range(len(name_songs)):
                label_1 = QLabel(f"{x}. {name_songs[detail]}")
                x +=1
                label_1.setFont(QFont('Bahnschrift SemiBold', 12))
                label = QLabel()
                pixmap = QPixmap(f"{thumbnails[detail]}")
                pixmap = pixmap.scaled(51, 32)
                label.setPixmap(pixmap)
                label_1.setStyleSheet("color: rgb(202, 202, 202)")
                nm_songs.append(label_1)
                thumbnail.append(label)
                formlayout.addRow(thumbnail[detail],nm_songs[detail])
            groupbox.setLayout(formlayout)
            self.scrollArea.setWidget(groupbox)
            refrsh()
        def sel_2():
            file_lbl = QFileDialog.getOpenFileName(self,"Open image","D:\Desktop-apps\yt\youtube","png (*.png);;jpeg (*.jpg)")
            file_loc = file_lbl[0]
            self.thumbnail_loc.setText(file_loc)
        def sel():
            file_lbl = QFileDialog.getOpenFileName(self,"Open image","D:\Desktop-apps\yt\youtube","wav (*.wav);;opus (*.opus)")
            file_loc = file_lbl[0]
            self.song_loc.setText(file_loc)
        def refrsh():
            pixmap =QPixmap(lc)
            self.list_name.setText(nm)
            self.thumbnail_list.setPixmap(pixmap)
            self.thumbnail_loc.setText("")
            self.song_loc.setText("")
            query = f"SELECT music_name , music_thumbnail FROM {nm}"
            cur.execute(query)
            a = cur.fetchall()
            name_songs = []
            thumbnails = []
            thumbnail = []
            nm_songs = []
            formlayout = QFormLayout()
            groupbox = QGroupBox()
            groupbox.setStyleSheet("border-radius:10px")
            x = 1
            for songs in a:
                name_songs.append(songs[0])  
                thumbnails.append(songs[1]) 
            for detail in range(len(name_songs)):
                label_1 = QLabel(f"  {x}. {name_songs[detail]}")
                x +=1
                label_1.setFont(QFont('Bahnschrift SemiBold', 12))
                label = QLabel()
                pixmap = QPixmap(f"{thumbnails[detail]}")
                pixmap = pixmap.scaled(70, 55)
                label.setPixmap(pixmap)
                label_1.setStyleSheet("color: #fff")
                thumbnail.append(label_1)
                nm_songs.append(label)
                formlayout.addRow(nm_songs[detail],thumbnail[detail])
            groupbox.setLayout(formlayout)
            self.scrollArea.setWidget(groupbox)
        def prev_win():
            win_main.setWindowTitle("Music Player")
            win_main.setCurrentIndex(win_main.currentIndex()-1)
app = QApplication(sys.argv)
win_main = QStackedWidget()
win_main.addWidget(win())
win_main.addWidget(create())
win_main.addWidget(win_play())
win_main.setFixedSize(964,641)
win_main.setWindowTitle("Music Player")
win_main.setWindowIcon(QtGui.QIcon("E:\Python Practice\GUI PyQt5\ICONS FOR APP\icons8_headphone_64_Vu5_icon.ico"))
 
win_main.show()
app.exec_()
