"""This version of code replace of all temperatures above 1200 because OpenSEES material cant handle
data more than that """

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
import os
import pandas as pd
import numpy as np

root = tk.Tk()
root.title("FDS2OpenSEES")
root.geometry("500x300")


frame1 = tk.LabelFrame(root, text="Creation of Boundary Condition", padx=5, pady=5)
frame1.grid(row=0, column=0, sticky="nsew")


def location():  # Directory Location
    get = filedialog.askdirectory()
    os.chdir(get)


tk.Button(frame1, text="Directory", command=location, width=25, height=1).grid(row=0, column=1)
tk.Label(frame1, width=20, text="Get Working Directory", anchor='e').grid(row=0, column=0, padx=5, pady=5)


def createFolder(directory):  # creating folders in the directory
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating Directory.' + directory)


data = ["AST", "AST_HTC", "HF", "HF_HTC"]
clicked2 = tk.StringVar()
clicked2.set(data[0])  # use variables as list
drop = tk.OptionMenu(frame1, clicked2, *data)
drop.config(width=12)
drop.grid(row=1, column=1, padx=5, pady=5)
tk.Label(frame1, width=20, text="Boundary Condition", anchor='e').grid(row=1, column=0, padx=5, pady=5)


def openfile():    # function to open the FDS output file (DEVC file)
    global filename
    filename = filedialog.askopenfilename(title="Select a file", filetypes=(('All files', '*.*'),
                                                                            ('Text Files', ('*.txt', '*.csv'))))


tk.Button(frame1, text="Browse File", command=openfile, width=15, height=1).grid(row=2, column=1, padx=10, pady=10)
tk.Label(frame1, width=20, text="Browse FDS Output File", anchor='e').grid(row=2, column=0, padx=5, pady=5)

num = tk.Entry(frame1, width=15)
num.grid(row=5, column=1, padx=5, pady=5)
tk.Label(frame1, width=20, text="Number of Devices", anchor='e').grid(row=5, column=0, padx=5, pady=5)


filename3 = ''


def fdsFile():
    global filename3
    filename3 = 'Devices.csv'
    with open(filename) as f:
        with open(filename3, 'w') as f1:
            next(f)  # skip header line
            for line in f:
                f1.write(line)


# below button will update the FDS file, it will remove the header lines from the output also keep open the file
tk.Button(frame1, text="Update File", command=fdsFile, width=15).grid(row=4, column=1, padx=5, pady=5)
tk.Label(frame1, width=20, text="Reformat FDS File", anchor='e').grid(row=4, column=0, padx=5, pady=5)


def bcfile(counter):  # this function generate the files for each boundary condition
    df1 = pd.read_csv(filename3)
    df1 = df1.round(1)
    c1 = df1.columns[0]
    dfT = df1.iloc[:, 0]
    newFile = open("TempFile/Devices2.csv", 'w', newline='')
    df1 = df1.drop([c1], axis=1)
    df1.to_csv(newFile, index=False)
    newFile.close()
    df = pd.read_csv("TempFile/Devices2.csv")
    frame = np.asarray(df)
    frame[frame > 1200] = 1200
    df = pd.DataFrame(frame)
    device3 = open("TempFile/Devices3.csv", 'w', newline='')
    df.to_csv(device3, index=False)
    device3.close()

    while counter <= int(num.get()):
        df3 = pd.read_csv("TempFile/Devices3.csv")
        df3 = df3.round(1)
        dfX = df3.iloc[:, (counter-1)]
        dfHF = pd.read_csv("TempFile/Devices2.csv")
        dfHF = dfHF.round(3)
        heatFlux = df3.iloc[:, (int(num.get()) + counter-1)]
        htc = df3.iloc[:, (2*int(num.get()) + counter-1)]
        if clicked2.get() == "AST":
            data1 = open("AST/AST{}.dat".format(counter), 'w', newline='')
            result = pd.concat([dfT, dfX], axis=1, sort=False)
            result.to_csv(data1, sep=" ", header=None, index=False)
            data1.close()
        if clicked2.get() == "HF":
            data1 = open("HF/HF{}.dat".format(counter), 'w', newline='')
            result = pd.concat([dfT, heatFlux*1000], axis=1, sort=False)
            result.to_csv(data1, sep=" ", header=None, index=False)
            data1.close()
        if clicked2.get() == "AST_HTC":
            data1 = open("AST_HTC/AST_HTC{}.dat".format(counter), 'w', newline='')
            result = pd.concat([dfT, dfX, htc], axis=1, sort=False)
            result.to_csv(data1, sep=" ", header=None, index=False)
            data1.close()
        if clicked2.get() == "HF_HTC":
            data1 = open("HF_HTC/HF_HTC{}.dat".format(counter), 'w', newline='')
            result = pd.concat([dfT, heatFlux*1000, htc], axis=1, sort=False)
            result.to_csv(data1, sep=" ", header=None, index=False)
            data1.close()

        counter += 1


def output():  # this is the main function for providing the output based on the user requirement
    iDev = 1   # counter for devices
    createFolder("./TempFile")
    if clicked2.get() == "AST":
        createFolder("./AST")
        bcfile(iDev)
    if clicked2.get() == "HF":
        createFolder("./HF")
        bcfile(iDev)
    if clicked2.get() == "AST_HTC":
        createFolder("./AST_HTC")
        bcfile(iDev)
    if clicked2.get() == "HF_HTC":
        createFolder("./HF_HTC")
        bcfile(iDev)


tk.Button(frame1, text="Save File", command=output, width=15, height=1).grid(row=6, column=1, padx=5, pady=5)

root.mainloop()
