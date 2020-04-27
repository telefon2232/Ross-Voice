import socket
from tkinter import *
from tkinter import ttk
import pyperclip
import pyaudio
import numpy
import threading
from PIL import ImageTk, Image



class Client:

    def __init__(self):
        self.server = '185.195.25.113', 4999
        self.key = 'hi'
        numpy.set_printoptions(threshold=sys.maxsize)
        self.chunk = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100  # In digital audio, 44,100 Hz
        p = pyaudio.PyAudio()
        self.stream_read = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, output=True, frames_per_buffer=self.chunk)
        self.stream_write = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, output=True, frames_per_buffer=self.chunk)
        self.root = Tk()
        self.root.title('Ross-Voice')
        folder_image='images'
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        render = ImageTk.PhotoImage(file=folder_image+"/icon.png")
        create_image = ImageTk.PhotoImage(file=folder_image+"/create.png")
        join_image = ImageTk.PhotoImage(file=folder_image+"/join.png")
        exit_button = ImageTk.PhotoImage(file=folder_image+"/exit.png")
        self.image_connect = ImageTk.PhotoImage(file=folder_image+"/connect.png")
        self.disconnect_image = ImageTk.PhotoImage(file=folder_image+"/disconnect.png")
        Label(self.root, image=render).pack(anchor=N)  # Name main-window
        voice_button = Button(image=create_image, borderwidth=0, highlightthickness=0, highlightbackground='#323232',
                              highlightcolor='#323232', bg='#323232', activebackground='#323232',
                              command=lambda: threading.Thread(target=self.voice).start())

        create_button = Button(image=create_image, borderwidth=0, highlightthickness=0, highlightbackground='#323232',
                               highlightcolor='#323232', bg='#323232', activebackground='#323232', command=self.create_room)
        create_button.pack(expand=1, side=LEFT)

        join_button = Button(image=join_image, borderwidth=0, highlightthickness=0, highlightbackground='#323232',
                             highlightcolor='#323232', bg='#323232', activebackground='#323232', command=self.join_room)
        join_button.pack(expand=1, side=RIGHT)

        closeButton = Button(image=exit_button, borderwidth=0, highlightthickness=0, highlightbackground='#323232',
                             highlightcolor='#323232', bg='#323232', activebackground='#323232', command=self.close)

        closeButton.pack(anchor=NW, expand=1)

        self.root["bg"] = "#323232"
        self.root.geometry('600x260')
        self.root.mainloop()

    def create_room(self):  # new window definition

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IP_V4 и UDP протокол
        sock.bind(('0.0.0.0', 4999))

        def lister():

            while True:
                data, address = (sock.recvfrom(200))
                if data:
                    pyperclip.copy(data.decode('utf-8'))
                    print(data.decode('utf-8'))
                    sock.close()
                    return

        server = '185.195.25.113', 4999

        threading.Thread(target=lister, args=()).start()
        sock.sendto(b'create_room', server)

    def join_room(self):  # new window definition
        newwin2 = Toplevel()
        newwin2.geometry('500x150')
        newwin2.title("join")
        newwin2["bg"] = "#323232"
        display = Label(newwin2, text="Join to room", fg='white')

        text1 = Entry(newwin2, width=70)

        display.config(width=10, bg='#323232', height=2, font='Arial 24')

        display.pack()
        text1.pack(anchor='center', expand=1, ipady=3)

        get_text_ = Button(newwin2, image=self.image_connect, borderwidth=0, highlightthickness=0,
                          highlightbackground='#323232',
                          highlightcolor='#323232', bg='#323232', activebackground='#323232',
                          command=lambda: self.found_server(text1))
        get_text_.pack(expand=1)


    def my_room(self):
        newwin3 = Toplevel()

        newwin3.geometry('500x150')
        newwin3.title("room")
        newwin3["bg"] = "#323232"
        get_text_ = Button(newwin3, image=self.disconnect_image, borderwidth=0, highlightthickness=0,
                          highlightbackground='#323232',
                          highlightcolor='#323232', bg='#323232', activebackground='#323232',
                          command=lambda: self.close())
        get_text_.pack(expand=1)

    def close(self):
        print('Window close')
        self.stream_read.close()
        self.stream_write.close()

        sys.exit()

    def voice(self):
        pass

    def refactor(self,data):
        data = data[::2]
        z = 0
        for i in data:
            data = numpy.insert(data, z, i)
            z += 1
        return data


    def found_server(self, message):
        inputValue = message.get()
        inputValue=inputValue.encode('utf-8')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IP_V4 и UDP протокол
        sock.bind(('0.0.0.0', 5000))
        sock.sendto(bytes(inputValue), self.server)

        def lister():
            while True:
                data, address = (sock.recvfrom(5))
                if data:
                    self.my_room()
                    print(data.decode('utf-8'))
                    sock.close()
                    threading.Thread(target=self.send_voice, args=(data.decode('utf-8'),)).start()

                    return
        threading.Thread(target=lister, args=()).start()

    def send_voice(self, port):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IP_V4 и UDP протокол
        sock.bind(('0.0.0.0', int(port)))
        threading.Thread(target=self.listen_voice, args=(sock,)).start()
        while True:
            mensahe = self.stream_read.read(self.chunk,
                                  exception_on_overflow=False)  # Прочитать данные с микрофона и записать в переменную (2 параметр для работы без ошибок переполнения буфера)
           # print(mensahe)
            decoded = numpy.fromstring(mensahe, dtype=numpy.int16)
            decoded=self.refactor(decoded)
            decoded=decoded.tobytes()
            mensahe=decoded

            sock.sendto(mensahe, (self.server[0],int(port)))



    def listen_voice(self,sock):
            while True:
                data = sock.recv(4096)
                if data:

                  #  decoded = numpy.fromstring(data, dtype=numpy.int16)
                   # data = self.decryption(self.key, decoded)
                    self.stream_write.write(data)

a=Client()
