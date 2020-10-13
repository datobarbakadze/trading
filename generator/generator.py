from tkinter import *
from tkinter import ttk


class Generator():
    modeOptions = ["MQ4", "MQ5"]
    def init_elements(self):
        mode = StringVar()
        self.variables = Entry(self.root, font="Arial 10")
        self.countLabel = Label(self.root,font="Arial 10",bg="#002c38", fg="white", text="Variable Count: 0",anchor=W)
        self.mode = ttk.Combobox(self.root, values=self.modeOptions, state="readonly", justify=CENTER, textvariable=mode)
        self.variables.pack(ipadx=30, ipady=5, fill=X, pady=3)
        self.mode.pack(ipadx=30, ipady=5, fill=X, pady=3)
        Button(self.root, width=50, text="GENERATE CODE",bg="#db4e21", fg="white", font="Arial 13",command=self.genFile).pack(pady=5,padx=0, fill=X)
        self.countLabel.pack(ipadx=30,  fill=X,)
    def getvariables(self):
        varArray = []
        varstring = self.variables.get()
        if len(varstring.strip()) ==0:
            varArray = []
            return varArray
        if  len(varstring.strip()) !=0 and "," not in varstring:
            varArray.insert(0,varstring)
        else:
            varArray = varstring.split(",")
        return varArray;
    def __init__(self):

        self.root = Tk()  # main tkinter object
        windowWidth = 300
        windowHeight = 200
        self.root.geometry(str(windowWidth) + 'x' + str(windowHeight))
        self.root.configure(bg='#002c38')
        self.init_elements()
        self.root.bind_all("<Key>",self.keypress)
        self.root.mainloop()
    def keypress(self, event):
        count = len(self.getvariables())
        self.countLabel.config(text="Variable Count: "+str(count))
    def gen_strings(self):
        variableArray = self.getvariables()
        variableString =""
        iCustomString = "        handle=iCustom(NULL,0,indicator"
        for index, variable in enumerate(variableArray):
            variableString += " input " + variable.strip() + " v" + str(index) + ";"
            if index != (len(variableArray) - 1):
                iCustomString += ",v" + str(index)
            else:
                iCustomString += ",v" + str(index) + self.icustom_ending
        return variableString, iCustomString

    def genFile(self):
        if self.mode.get() == "MQ4":
            self.icustom_ending = ",0,0);"
            extension = "mq4"
            template = "template_mq4.bot"
        elif self.mode.get() == "MQ5":
            self.icustom_ending = ");"
            extension = "mq5"
            template = "template_mq5.bot"
        variableString, iCustomString=self.gen_strings()
        read_open= open(template,"r")
        lines = read_open.readlines();
        icustom_line = "";
        input_vars_line = "";
        for index,line in enumerate(lines):
            if "input_vars" in line:
                lines[index] = variableString
            if "icustom" in line:
                lines[index] = iCustomString
        write_open = open("detector."+extension,"w")
        write_open.writelines(lines)
        read_open.close()
        write_open.close()


Generator = Generator()