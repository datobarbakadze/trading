import time
from random import randrange
import json
import socket
from iqoptionapi.stable_api import IQ_Option
from threading import Thread, active_count
from tkinter import Label
import _thread
class Helper:
    PORT = 8888
    HOST = '127.0.0.1'
    thread_list = []
    result_row_counter = 0
    def login(self,widget_list,email,password,mode,money,expire,msg_label, button,frame):
        if(button.cget("text") == "Start"):
            self.main_log_frame  = frame;
            self.email = email.get()
            self.password = password.get()
            # bdato269@gmail.com Dazeface1
            self.api = IQ_Option(self.email, self.password)
            connection_msg  = self.api.connect()
            if connection_msg[0]!=True:
                err_msg = json.loads(connection_msg[1])["message"]
                msg_label.config(text=err_msg,fg="#d90f4f")
                # print(err_msg)
                # print(json.loads(connection_msg[1]))
                return
            else:
                msg_label.config(text="Connected!",fg="#00bf89")
                self.account_type = mode.get()
                self.money = float(str(money.get()).strip())
                self.expire_time = float(str(expire.get()).strip())
            self.api.change_balance(self.account_type)
            #
            self.server_thread = Thread(target=self.start_server)
            self.server_thread.start()

        self.change_button(button, widget_list,msg_label)
        return
    def checker(self,id,actives):
        # print("Begin Checking for id: "+str(id));
        self.result_row_counter += 1;
        result = self.api.check_win_v3(id);
        if float(result) > 0:
            Label(self.scrollable_frame, font="Arial 10 bold", text=actives+" - ID:"+str(id)+" - WIN! -  Amount:"+str(result)+"$", bg="#00bf89", fg="white", padx=0, pady=0, width=50, height=2, anchor='w').pack()#grid(row=self.result_row_counter, column=0, pady=1, sticky="ew")

        if float(result) ==0:
            Label(self.scrollable_frame, font="Arial 10 bold", text=actives+" - ID:"+str(id)+" - DRAW!", bg="#e37d00", fg="white", padx=0, pady=0, width=50, height=2, anchor='w').pack()#grid(row=self.result_row_counter, column=0, pady=1, sticky="ew")

        if float(result) < 0:
            Label(self.scrollable_frame, font="Arial 10 bold", text=actives+" - ID:"+str(id)+" - LOOSE! -  Amount:"+str(result)+"$", bg="#d90f4f", fg="white", padx=0, pady=0, width=50, height=2, anchor='w').pack()#grid(row=self.result_row_counter, column=0, pady=1, sticky="ew")

        # print(result);

    def bet(self,action,actives):
        check,id = self.api.buy(self.money, actives, action, self.expire_time)
        checkerThred = Thread(target=self.checker, args=[id,actives])
        checkerThred.start()
    def start_server(self):
        self.running = True
        self.socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        self.socket.bind((self.HOST,self.PORT))
        self.socket.listen(50)


        # print("client has been connected")
        while True:
            if self.running == False:
                self.socket.close()
                self.socket = None
                _thread.exit()
                break
            con, adr = self.socket.accept()
            client_thread = Thread(target=self.onNewCon, args=[con,adr])
            client_thread.start()
            print("newcon");
        _thread.exit()
        return
    def onNewCon(self,con,adr):

        while True:
            print(active_count())
            data = con.recv(1024).decode('utf-8').strip().split("|")
            if self.running == False:
                self.con.close()
                _thread.exit()
                break
            print(data[0]+" | "+data[1])
            actives = str(data[1])
            signal = str(data[0])
            if signal == "UP":
                betThread = Thread(target=self.bet, args=["call",actives])
            elif signal == "DOWN":
                betThread = Thread(target=self.bet, args=["put",actives])
            else:
                betThread = False
            if betThread:
                betThread.start()
    def change_button(self, button,widget_list,msg_label):
        button_text = button.cget('text')
        if button_text=="Start":
            button.config(text='Stop')
            self.disable_widgets(widget_list)
        elif button_text=="Stop":
            self.stop_server()
            button.config(text='Start')
            msg_label.config(text="Disconnected",fg="#e37d00")
            self.enable_widgets(widget_list)

    def disable_widgets(self,widget_list):
        for widget in widget_list:
            widget.config(state='disabled')

    def enable_widgets(self, widget_list):
        for widget in widget_list:
            widget.config(state='normal')

    def stop_server(self):

        self.running = False
        try:
            self.socket
            self.socket.close()
            self.socket = None
        except:
            pass

        print("Closed")
