import os
from tkinter import * 
from tkinter import ttk
from urllib.request import url2pathname
from pytube import *
from PIL import Image,ImageTk
import requests
import io

class Utube_down:
    def __init__(self,root):
        self.root=root      
        self.root.title("Youtube Dowloader by JARVIS(Rahul)")
        self.root.geometry("500x420+300+50")
        self.root.resizable(False,False)
        self.root.config(bg='white')

        title=Label(self.root,text='Youtube Dowloader by JARVIS(Rahul)',font=("algerian",15),bg="#262626",fg='white').pack(side=TOP,fill=X)
        
        self.var_url=StringVar()

        lbl_url=Label(self.root,text='Video URL',font=("times new roman",15),bg='white').place(x=10,y=50)
        txt_url=Entry(self.root,textvariable=self.var_url,font=("times new roman",13),bg="#d9fcff").place(x=120,y=50,width=340,height=30)
        lbl_ftype=Label(self.root,text='File Type',font=("times new roman",15),bg='white').place(x=10,y=90)

        self.var_fileType=StringVar()
        self.var_fileType.set('Video')
        video_radio=Radiobutton(self.root,text='Video',variable=self.var_fileType,value='Video',font=("times new roman",13),bg='white',activebackground='white').place(x=120,y=90)
        audio_radio=Radiobutton(self.root,text='Audio',variable=self.var_fileType,value='Audio',font=("times new roman",13),bg='white',activebackground='white').place(x=220,y=90)
        btn_search=Button(self.root,text='Search',font=('times new roman',15),bg='lightblue',command=self.search).place(x=350,y=90,width=120,height=35)
        
        frame_=Frame(self.root,bd=2,relief=RIDGE,bg='#d9fcff')
        frame_.place(x=10,y=140,width=470,height=180)

        self.video_title=Label(frame_,text='Video Title : ',font=("times new roman",15),bg="white",anchor='w')
        self.video_title.place(x=0,y=0,relwidth=1)

        self.video_img=Label(frame_,text='Video \nImage ',font=("times new roman",15),bg="lightgrey",bd=2,relief=RIDGE)
        self.video_img.place(x=5,y=32,width=180,height=140)

        lbl_des=Label(frame_,text='Description : ',font=("times new roman",15),bg="#d9fcff").place(x=190,y=32)
        
        self.video_des=Text(frame_,font=("times new roman",12),bg="#d9fcff")
        self.video_des.place(x=190,y=60,width=270,height=110)
        
        self.lbl_size=Label(self.root,text='Total Size : MB',font=("times new roman",13),bg='white')
        self.lbl_size.place(x=10,y=330)

        self.lbl_per=Label(self.root,text='Downloading : 0%',font=("times new roman",13),bg='white')
        self.lbl_per.place(x=160,y=330)

        btn_clear=Button(self.root,text='Clear',command=self.clear,font=('times new roman',13),bg='red',fg='white').place(x=330,y=330,width=60,height=25)
        self.btn_download=Button(self.root,text='Download',state=DISABLED,command=self.dwnld,font=('times new roman',13),bg='green',fg='white')
        self.btn_download.place(x=400,y=330,width=90,height=25)
        
        self.pro=ttk.Progressbar(self.root,orient=HORIZONTAL,length=590,mode='determinate')
        self.pro.place(x=10,y=360,width=485,height=20)

        self.msg=Label(self.root,text='',font=("times new roman",13),bg='white')
        self.msg.place(x=0,y=385,relwidth=1)

        if os.path.exists('Audios')==False:
            os.mkdir('Audios')
        if os.path.exists('Videos')==False:
            os.mkdir('Videos')


    def search(self):
        if self.var_url.get()=='':
            self.msg.config(text='Please enter url',fg='red')
        else:
            yt=YouTube(self.var_url.get())
            res=requests.get(yt.thumbnail_url)
            img_byte=io.BytesIO(res.content)
            self.image=Image.open(img_byte)
            self.image=self.image.resize((180,140),Image.ANTIALIAS)
            self.image=ImageTk.PhotoImage(self.image)
            self.video_img.config(image=self.image)


            if self.var_fileType.get()=='Video':
                dot=fvid=yt.streams.filter(progressive=True).first()
            if self.var_fileType.get()=='Audio':
                dot=faud=yt.streams.filter(only_audio=True).first()

            self.size_byte=dot.filesize
            maxsize=self.size_byte/1024000
            self.mb=str(round(maxsize))+'MB'
            self.lbl_size.config(text='Total Size : '+self.mb)

            self.video_title.config(text=yt.title)
            self.video_des.delete('1.0',END)
            self.video_des.insert(END,yt.description[:250])
            self.btn_download.config(state=NORMAL)


    def progress(self,streams,chunk,bytes_remaining):
        percent=(float(abs(bytes_remaining-self.size_byte)/self.size_byte))*float(100)
        self.pro['value']=percent
        self.pro.update()
        self.lbl_per.config(text=f'Downloading : {str(round(percent,2))}%')

        if round(percent,2)==100:
            self.msg.config(text='Download Completed',fg='green')
            self.btn_download.config(state=DISABLED)


    def clear(self):
        self.var_fileType.set('Video')
        self.var_url.set('')
        self.pro['value']=0
        self.btn_download.config(state=DISABLED)
        self.msg.config(text='')
        self.video_title.config(text='Video Title : ')
        self.video_des.delete('1.0',END)
        self.video_img.config(image='')
        self.lbl_size.config(text='Total Size : MB')
        self.lbl_per.config(text="Downloading : 0%")


    def dwnld(self):
        yt=YouTube(self.var_url.get(),on_progress_callback=self.progress)
        if self.var_fileType.get()=='Video':
            dot=fvid=yt.streams.filter(progressive=True).first()
            dot.download('Videos/')
        if self.var_fileType.get()=='Audio':
            dot=faud=yt.streams.filter(only_audio=True).first()
            dot.download('Audios/')



root=Tk()
obj=Utube_down(root)
root.mainloop()