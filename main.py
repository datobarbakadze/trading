from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from Functions.Helper import Helper
import atexit
class IQ(Helper):
    modeOptions = ["PRACTICE", "REAL"]

    def onscroll(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=200, height=200)
    def create_elements(self):
        email,passw,mode,money,expire = StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
        #
        # mode.set(self.modeOptions[0])
        # style = ttk.Style()
        load = Image.open("./images/icon.png")
        render = ImageTk.PhotoImage(load)
        self.imageLabel = Label(self.root, image=render,bg="#002c38")
        self.imageLabel.image = render

        self.logFrame = Frame(self.logWindow,bg="#002c38",borderwidth=0)
        self.logFrame.place(x=0, y=0,height=self.frameHeight,width=self.frameWidth)
        self.canvas = Canvas(self.logFrame,bg="#002c38",borderwidth=0)
        self.scrollable_frame = Frame(self.canvas,bg="#002c38",borderwidth=0)
        self.scrollbar = Scrollbar(self.logFrame, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill=Y)

        self.canvas.pack(side="left",expand=True,fill=BOTH)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.scrollable_frame.bind("<Configure>", self.onscroll)



        # differen type of situation
        # self.testingLabel = Label(self.scrollable_frame,font="Arial 10 bold", text="ID:21313241 - WIN! -  Amount:30$", bg="#00bf89", fg="white", padx=0, pady=0,width=50,height=2,anchor='w')
        # self.testingLabel1 = Label(self.scrollable_frame,font="Arial 10 bold", text="Your did not gain or get the money", bg="#e37d00", fg="white", padx=0, pady=0,width=50, height=2, anchor='w')
        # self.testingLabel2 = Label(self.scrollable_frame,font="Arial 10 bold", text="You lost the money", bg="#d90f4f", fg="white", padx=0, pady=0,width=50, height=2, anchor='w')
        # end of situation


        self.emailLabel = Label(self.root, text="Your E-mail:", bg="#002c38",fg="white",padx=0,pady=0,justify=CENTER,width=30)
        self.passwordLabel = Label(self.root, text="Your Password: ", bg="#002c38",fg="white",padx=0,pady=0,justify=CENTER,width=30)
        self.modeLabel = Label(self.root, text="Choose Account type: ", bg="#002c38", fg="white", padx=0, pady=0,justify=CENTER, width=30)
        self.msg_label = Label(self.root, text="", bg="#002c38",fg="white",padx=0,pady=0,justify=CENTER,width=30,wraplength=250)
        self.expireLabel = Label(self.root, text="Expiration time(minutes/digits only):", bg="#002c38",fg="white",padx=0,pady=0,justify=CENTER,width=30)
        self.moneyLabel = Label(self.root, text="Money per trade(1.0=1.0$/digits only):", bg="#002c38",fg="white",padx=0,pady=0,justify=CENTER,width=30)

        self.email = Entry(self.root, font=60,width=30,borderwidth=0,justify=CENTER,textvariable=email)
        self.password = Entry(self.root, font=60,width=30,borderwidth=0,justify=CENTER,textvariable=passw,show="*")
        self.mode = ttk.Combobox(self.root,values=self.modeOptions,state="readonly",justify=CENTER,textvariable=mode)
        self.expire = Entry(self.root, font=60,width=30,borderwidth=0,justify=CENTER, text="1", textvariable=expire)
        self.expire.insert(0, "1")
        self.money =  Entry(self.root, font=60,width=30,borderwidth=0,justify=CENTER, text="1", textvariable=money)
        self.money.insert(0,"1")
        # self.logButton  = Button(self.root, pady=9,width=30, text="Show log",bg="#480d80", borderwidth=0,fg="#ccc",font="Arial 13 bold")

        self.mode.current(0)
        widgetlist = [self.email, self.password, self.mode,self.expire,self.money]
        self.StartButton = Button(self.root, font="Arial 13 bold",text="Start",cursor="hand2",borderwidth=0, bg="#db4e21", width=30,  fg="white",  padx=0, pady=9, command=lambda: self.login(widgetlist,email,passw,mode,money,expire,self.msg_label, self.StartButton,self.logFrame))


    def init_elements(self):
        self.imageLabel.grid(row=0, column=0, padx=20,pady=15, columnspan=3, sticky="ew")

        # diferent situation
        # self.testingLabel.pack()
        # self.testingLabel1.pack()
        # self.testingLabel2.pack()
        # end of it

        self.emailLabel.grid(row=1, column=0, padx=20, columnspan=3, sticky="ew")
        self.passwordLabel.grid(row=3, column=0, padx=20, columnspan=3, sticky="ew")
        self.modeLabel.grid(row=5, column=0, padx=20, columnspan=3, sticky="ew")


        self.email.grid(row=2,column=0,ipady=7,pady=6,padx=20,columnspan=3,sticky="ew" )
        self.password.grid(row=4,column=0,ipady=7,pady=5,padx=20,columnspan=3,sticky="ew" )
        self.mode.grid(row=6,column=0,ipady=7,pady=5,padx=20,columnspan=3,sticky="ew")

        self.expireLabel.grid(row=7, column=0, padx=20, columnspan=3, sticky="ew")
        self.expire.grid(row=8,column=0,ipady=7,pady=5,padx=20,columnspan=3,sticky="ew")

        self.moneyLabel.grid(row=9, column=0, padx=20, columnspan=3, sticky="ew")
        self.money.grid(row=10,column=0,ipady=7,pady=5,padx=20,columnspan=3,sticky="ew")

        self.StartButton.grid(row=11,column=0,pady=5,padx=20,columnspan=3,sticky="ew")
        self.msg_label.grid(row=12, column=0, padx=20, columnspan=3, sticky="ew")

        # self.logButton.grid(row=12,column=0,pady=5,padx=20,columnspan=3,sticky="ew")
    def run(self):
        self.root.mainloop()

    def __init__(self):

        self.frameWidth = 405
        self.frameHeight= 540
        windowWidth = 350
        windowHeight = 540
        self.root = Tk() # main tkinter object
        self.root.geometry(str(windowWidth)+'x'+str(windowHeight))
        self.root.configure(bg='#002c38')
        self.root.resizable(False, False)
        self.root.title("IQOption-BOT");
        self.root.iconbitmap(r'./images/iqicon.ico');
        positionRight = int(self.root.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.root.winfo_screenheight() / 2 - windowHeight / 2)
        self.root.geometry("+{}+{}".format(positionRight, positionDown))

        self.logWindow = Toplevel()
        self.logWindow.geometry(str(self.frameWidth) + 'x' + str(self.frameHeight))
        self.logWindow.configure(bg='#002c38')
        self.logWindow.title("LOGS-IQOption");
        self.logWindow.iconbitmap(r'./images/iqicon.ico');
        self.logWindow.resizable(False, False)

        positionRight = int(self.root.winfo_screenwidth() / 2- windowWidth+540)
        positionDown = int(self.root.winfo_screenheight() / 2- windowWidth+80)
        self.logWindow.geometry("+{}+{}".format(positionRight, positionDown))

        self.create_elements() # create elements
        self.init_elements() # pack the elements
        self.run() # run the mainloop


main = IQ()

atexit.register(main.stop_server)