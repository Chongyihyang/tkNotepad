#import  
import tkinter.font, tkinter, os, subprocess, pypandoc, time, tkinter.font as tkFont  
import tkinter as tk
import subprocess
from tkinter import *
from tkinter import ttk, Button,filedialog, messagebox, font, colorchooser
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Queue   #needed for selenium  
from audioplayer import AudioPlayer
from selenium import webdriver
from platform import system
from time import strftime
import time, calendar
from datetime import date
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
#our window called root
__root = tk.Tk()
__root.state('zoomed')
yes = os.path.dirname(os.path.abspath(__file__))
def find(name, path):
    global lol
    for root, dir,files in os.walk(path):
        if name in files:
            lol = (os.path.join(root, name))
            print(lol)
__root.title("Untitled - Notepad")
FrameGod = Frame(__root)
FrameGod.pack(side=TOP, fill = X)
showmenuvar = IntVar()
def showmenu():
    varb = showmenuvar.get()
    if 1:
        FrameGod.pack_forget()

#God
__thisFileMenu = tk.Menu(FrameGod, tearoff = 0)
__thisFileMenubutton = ttk.Menubutton(FrameGod, text='File', menu=__thisFileMenu, direction='below')
__thisFileMenubutton.grid(row=0, column=0, sticky='w')

__thisHomeMenu = tk.Menu(FrameGod, tearoff = 0)
__thisHomebutton = ttk.Menubutton(FrameGod, text='Text', menu=__thisHomeMenu, direction='below')
__thisHomebutton.grid(row=0, column=1, sticky='w')

__thisEditMenu = tk.Menu(FrameGod, tearoff = 0)
__thisEditMenubutton = ttk.Menubutton(FrameGod, text='Edit', menu=__thisEditMenu, direction='below')
__thisEditMenubutton.grid(row=0, column=2, sticky='w')

__thisViewMenu = tk.Menu(FrameGod, tearoff = 0)
__thisViewMenubutton = ttk.Menubutton(FrameGod, text='View', menu=__thisViewMenu, direction='below')
__thisViewMenubutton.grid(row=0, column=3, sticky='w')

#Widgets
class MyScroll(Text):
    frame = ttk.Frame()
    def __init__(self, master=None, **kw):
        self.vbar = ttk.Scrollbar(self.frame, command=self.yview)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.hbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.xview)
        self.hbar.pack(side=BOTTOM, fill=X)
        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        #cannot understand this part
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
        #until here
    def __str__(self):
        return str(self.frame)
__lineNumber = Canvas(MyScroll.frame ,width="30", borderwidth=0, highlightthickness=0 , relief='ridge')
__lineNumber.config(state=DISABLED)
__lineNumber.pack(fill=Y, side=LEFT)
__thisTextPad = MyScroll(__root, background="black",wrap="none",  foreground="white", font="bahnscrift 12",  insertbackground = "white" )
__thisTextPad.config()
__thisTextPad.pack(expand=True, fill=BOTH,  side=RIGHT )
show_time = IntVar()
def showtime():
    global lbl
    lbl = Label(FrameGod)
    var = show_time.get()
    if var:
        lbl.grid(row=0, column=5, sticky='sw') 
        time()
    elif not var:
        yes = Label(FrameGod, text="                                                                                                                                                                        ")
        yes.grid(row=0, column=5, sticky='sw')
        lbl.grid_remove()
showtime()
__thisViewMenu.add_checkbutton(label="Show Time", variable=show_time, command=lambda: showtime())
__thisViewMenu.add_checkbutton(label="Hide Menu bar", variable=showmenuvar, command=lambda: showmenu())
def time(): 
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]  
    string = strftime('Day:  '+ day+ '    Date:  ''%d/%m/%Y' + '    Time:  ' + '%H:%M:%S %p') 
    lbl.config(text = string) 
    lbl.after(1000, time) 
def clear():
    ii= __thisTextPad.index("@0,0")
    dline = __thisTextPad.dlineinfo(ii)
    xray = dline[2]
    yray = dline[1]
    if yray == "1.0" and xray=="0":
        __thisTextPad.delete(1.0, END)
def Redraw( event=NONE):
    global __file
    try:
        file = open(__file, "w")
        file.write(__thisTextPad.get(1.0, END))
        file.close()
    except:
        pass
    __lineNumber.delete("all")
    objectIds = []
    si = __thisTextPad.index("@0,0")
    while True:
        dline = __thisTextPad.dlineinfo(si)
        if dline is None:
            break
        y = dline[1]
        x =dline[2]
        liNum = str(si).split(".")[0]
        __lineNumber.configure(bg="#242429", borderwidth=0, highlightthickness=0)
        __lineNumber.create_text(2, y, anchor="nw", text=liNum, fill="white", font="bahnscrift 9", justify=RIGHT)
        si = __thisTextPad.index(f"{si}+1line")
def entry_ctrl_bs(event):
  __thisTextPad = event.widget
  __text = __thisTextPad.get(1.0, END)
  __word1 = __text.split(" ")
  __lel = len(__word1)
  __lel -= 1
  if __lel == 0:
    __thisTextPad.delete(1.0 , END )  
  else:
    __words = __text.split()[-1]
    __tabwidth = len(__words)
    __thisTextPad.delete("insert -%d chars" % __tabwidth, "insert" )
__thisTextPad.bind('<Control-BackSpace>', entry_ctrl_bs)
#servants
#File menu
def __newFile():
    __root.title("Untitled - Notepad")
    __thisTextPad.delete(1.0 , END )  
__thisFileMenu.add_command(label="New", accelerator='Ctrl + N',compound=LEFT, command=__newFile)
__root.bind("<Control-n>", lambda x: __newFile())
def __openFile():
    global __file
    __file = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if __file == "":
        __file = None
    else:
        __root.title(os.path.basename(__file) + " - Notepad")
        __thisTextPad.delete(1.0, END)
        file = open(__file, "r")
        __thisTextPad.insert(1.0, file.read())
        file.close()
        filename, file_extension= os.path.splitext(__file)
        if file_extension == '.py':
            Percolator(__thisTextPad).insertfilter(ColorDelegator())
__thisFileMenu.add_command(label="Open", accelerator='Ctrl + O',compound=LEFT,command = __openFile)
__root.bind("<Control-o>", lambda x: __openFile())
__thisTextPad.bind_all('<Return>', Redraw)
__thisTextPad.bind_all('<BackSpace>', Redraw)
__thisTextPad.bind_all('<Key>',Redraw)
__thisTextPad.bind_all('<Button-4>', Redraw)
__thisTextPad.bind_all('<Button-5>', Redraw)
__thisTextPad.bind_all('<MouseWheel>', Redraw)
__root.after_idle(Redraw)   
__root.bind_all('<Motion>', Redraw)
def __saveAsFile():
    global __file
    __file = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

    if __file == "":
        __file = None
    else:

        # Try to save the file
        file = open(__file, "w")
        file.write(__thisTextPad.get(1.0, END))
        file.close()
        filename, file_extension= os.path.splitext(__file)
        if file_extension == '.py':
            Percolator(__thisTextPad).insertfilter(ColorDelegator())
        # Change the window title
        __root.title(os.path.basename(__file) + " - Notepad")
__thisFileMenu.add_command(label="Save as",  accelerator='Ctrl + Alt + S', compound=LEFT, command = __saveAsFile)
__root.bind("<Control-s>", lambda x: __saveAsFile())
def terminal():
    try:      
        subprocess.Popen('cmd.exe')
    except:
        pass
__thisFileMenu.add_command(label="Terminal", accelerator='Ctrl + Alt + T',compound=LEFT, command = terminal)
__root.bind("<Control-Alt-t>", lambda x: terminal())
def run():
    try:
        p = subprocess.Popen(["start", "cmd", "/k", "python " + __file], shell = True) 
        p.wait()    # I can wait until finished (although it too finishes after start finishes)
    except:
        messagebox.showerror('error', 'cannot run')    
__thisFileMenu.add_command(label="Run", accelerator='Ctrl + R',compound=LEFT, command = run)
__root.bind("<Control-r>", lambda x: run())
def debug():
    try:
        p = subprocess.Popen(["start", "cmd", "/k", "pylint " + __file], shell = True) 
        p.wait()    # I can wait until finished (although it too finishes after start finishes)
    except:
        messagebox.showerror('error', 'cannot run')    
__thisFileMenu.add_command(label="pylint", accelerator='Ctrl + Alt + B',compound=LEFT, command = debug)
__root.bind("<Control-Alt-b>", lambda x: debug())
def __word():
    __file1 = filedialog.askopenfilename(defaultextension=".docx",filetypes=[("All Files", "*.*"), ("Text Documents", "*.docs")])
    if __file1 == "":
        __file1 = None
    else:
        __file2 = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        pypandoc.convert_file(__file1, 'plain', outputfile=__file2)
__thisFileMenu.add_command(label="Convert to txt",compound=LEFT,command = __word)
def Internet():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("http://www.google.com")
__thisFileMenu.add_command(label="Browser",compound=LEFT,command = Internet)
def music():
    global paused, vollabel , repeat
    paused = False
    player = None
    buttons_glyph = ('⏏','▶', '⏯' ,'⏹')  if system() == 'Windows' else ('⏏️', '▶️', '⏯️', '⏹️')

    def load():
        global player, root
        fname = filedialog.askopenfilename()
        if fname:
            player = AudioPlayer(fname)
            changevolume(0)  # update UI
            namelabel.config(text=os.path.basename(player.fullfilename))
            try:
                player.play()
            except Exception as e:
                messagebox.showerror('Error', e)


    def tooglepause():
        global player, paused
        if not player is None:
            if paused:
                player.resume()
            else:
                player.pause()
            paused = not paused


    def play():
        global player
        if not player is None:
            try:
                player.play()
            except Exception as e:
                messagebox.showerror('Error', e)


    def stop():
        global player
        if not player is None:
            player.stop()


    def changevolume(delta):
        global player, vollabel
        if not player is None:
            player.volume += delta
            vollabel.config(text='{}%'.format(player.volume))


    btnfont = (None, 30)
    lblfont = (None, 8)

    # Build UI
    t1 = Toplevel(__root)
    t1.title('Music Player')
    t1.transient(__root)
    t1.attributes('-topmost', True)
    t1.resizable(False, False)
    t1.attributes('-topmost', False)

    botframe = tkinter.Frame()
    botframe.pack(fill=tkinter.X, side=tkinter.TOP)
    namelabel = tkinter.Label(botframe,
                            anchor=tkinter.W, font=lblfont)
    namelabel.pack(fill=tkinter.X, expand=1, side=tkinter.LEFT, padx=2)
    vollabel = tkinter.Label(botframe, text='100%', anchor=tkinter.E, font=lblfont)
    vollabel.pack(side=tkinter.LEFT, padx=0)

    toolbar = tkinter.Frame(t1)
    toolbar.pack(side=tkinter.TOP)
    tkinter.Button(toolbar, text=buttons_glyph[0], font=btnfont, width=2,
                command=load).pack(side=tkinter.LEFT)
    tkinter.Button(toolbar, text=buttons_glyph[1], font=btnfont, width=2,
                command=play).pack(side=tkinter.LEFT)
    tkinter.Button(toolbar, text=buttons_glyph[2], font=btnfont, width=2,
                command=tooglepause).pack(side=tkinter.LEFT)
    tkinter.Button(toolbar, text=buttons_glyph[3], font=btnfont, width=2,
                command=stop).pack(side=tkinter.LEFT)
    volframe = tkinter.Frame(toolbar)
    volframe.pack(side=tkinter.LEFT, expand=1, fill=tkinter.BOTH)
    tkinter.Button(volframe, text='➕', command=lambda: changevolume(10)).pack(side=tkinter.TOP, expand=1, fill=tkinter.BOTH)
    tkinter.Button(volframe, text='➖', command=lambda: changevolume(-10)).pack(side=tkinter.TOP, expand=1, fill=tkinter.BOTH)

    t1.mainloop()
__thisFileMenu.add_command(label="Music",compound=LEFT,command = music)   
def __exit():
    __root.destroy()
__thisFileMenu.add_command(label="Exit",compound=LEFT, accelerator='Alt + F4',command=__exit)
__thisTextPad.bind("<Alt-KeyPress-F4>", lambda x: __exit())
#Home menu
def italicise():
    italicise_font = tkFont.Font(__thisTextPad, __thisTextPad.cget("font"))
    italicise_font.configure(slant="italic")
    __thisTextPad.tag_configure("italic", font = "bahnscrift 12 italic")
    try:
        current_tags = __thisTextPad.tag_names("sel.first")
        if "italic" in current_tags:
            __thisTextPad.tag_remove("italic", "sel.first", "sel.last")
        else:
            __thisTextPad.tag_add("italic", "sel.first", "sel.last")
    except:
        pass
__thisHomeMenu.add_command(label="Italicise", accelerator='Ctrl + J',command=italicise)
__thisTextPad.bind("<Control-j>", lambda x: italicise())
def bold():
    bold_font = font.Font(__thisTextPad, __thisTextPad.cget("font"))
    bold_font.configure(weight="bold")
    __thisTextPad.tag_configure("bold", font="bahnscrift 12 bold")
    try:
        current_tags = __thisTextPad.tag_names("sel.first")
        if "bold" in current_tags:
            __thisTextPad.tag_remove("bold", "sel.first", "sel.last")
        else:
            __thisTextPad.tag_add("bold", "sel.first", "sel.last")
    except:
        pass
__thisHomeMenu.add_command(label="Bold", accelerator='Ctrl + B',command=bold)
__thisTextPad.bind("<Control-b>", lambda x: bold())
def underline():
    underline_font = font.Font(__thisTextPad, __thisTextPad.cget("font"))
    underline_font.configure(underline=True)
    __thisTextPad.tag_configure("underline", font="bahnscrift 12 underline")
    try:
        current_tags = __thisTextPad.tag_names("sel.first")
        if "underline" in current_tags:
            __thisTextPad.tag_remove("underline", "sel.first", "sel.last")
        else:
            __thisTextPad.tag_add("underline", "sel.first", "sel.last")
    except:
        pass
__thisHomeMenu.add_command(label="Underline", accelerator='Ctrl + U',command=underline)
__thisTextPad.bind("<Control-u>", lambda x: underline())
def strikethru():
    strikethru_font = font.Font(__thisTextPad, __thisTextPad.cget("font"))
    strikethru_font.configure(underline=True)
    __thisTextPad.tag_configure("strikethru", font="bahnscrift 12 overstrike")
    try:
        current_tags = __thisTextPad.tag_names("sel.first")
        if "strikethru" in current_tags:
            __thisTextPad.tag_remove("strikethru", "sel.first", "sel.last")
        else:
            __thisTextPad.tag_add("strikethru", "sel.first", "sel.last")
    except:
        pass
__thisHomeMenu.add_command(label="Strikethru", accelerator='Ctrl + Q',command=strikethru)
__thisTextPad.bind("<Control-q>", lambda x: strikethru())
def subscript():
    font.Font(__thisTextPad, __thisTextPad.cget("font"))
    __thisTextPad.tag_configure("subscript", offset=-4)
    try:
        current_tags = __thisTextPad.tag_names("sel.first")
        if "subscript" in current_tags:
            __thisTextPad.tag_remove("subscript", "sel.first", "sel.last")
        else:
            __thisTextPad.tag_add("subscript", "sel.first", "sel.last")
    except:
        pass
__thisHomeMenu.add_command(label="Subscript",accelerator='Ctrl + T', command=subscript)
__thisTextPad.bind("<Control-t>", lambda x: subscript())
def superscript():
    font.Font(__thisTextPad, __thisTextPad.cget("font"))
    __thisTextPad.tag_configure("superscript", offset=4)
    try:
        current_tags = __thisTextPad.tag_names("sel.first")
        if "superscript" in current_tags:
            __thisTextPad.tag_remove("superscript", "sel.first", "sel.last")
        else:
            __thisTextPad.tag_add("superscript", "sel.first", "sel.last")
    except:
        pass
__thisHomeMenu.add_command(label="Superscript",accelerator='Ctrl + E',command=superscript)
__thisTextPad.bind("<Control-e>", lambda x: superscript())
def color():
    my_color = colorchooser.askcolor()[1]
    color_font = font.Font(__thisTextPad, __thisTextPad.cget("font"))
    __thisTextPad.tag_configure("color", font=color_font, foreground=my_color)
    try:
        current_tags = __thisTextPad.tag_names("sel.first")
        if "color" in current_tags:
            __thisTextPad.tag_remove("color", "sel.first", "sel.last")
        else:
            __thisTextPad.tag_add("color", "sel.first", "sel.last")
    except:
        pass
__thisHomeMenu.add_command(label="color", accelerator='Ctrl + P',command=color)
__thisTextPad.bind("<Control-p>", lambda x: color())
def highlight():
    my_highlight = colorchooser.askcolor()[1]
    highlight_font = font.Font(__thisTextPad, __thisTextPad.cget("font"))
    __thisTextPad.tag_configure("highlight", font=highlight_font, background=my_highlight)
    try:
        current_tags = __thisTextPad.tag_names("sel.first")
        if "highlight" in current_tags:
            __thisTextPad.tag_remove("highlight", "sel.first", "sel.last")
        else:
            __thisTextPad.tag_add("highlight", "sel.first", "sel.last")
    except:
        pass
__thisHomeMenu.add_command(label="highlight", accelerator='Ctrl + H',command=highlight)
__thisTextPad.bind("<Control-h>", lambda x: highlight())
#Edit menu
def undo():
     __thisTextPad.event_generate("<<Undo>>")
__thisEditMenu.add_command(label="Undo", accelerator='Ctrl + Y',compound=LEFT,command=undo)
def redo():
     __thisTextPad.event_generate("<<Redo>>")
__thisEditMenu.add_command(label="Redo", accelerator='Ctrl + Z',compound=LEFT, command = redo)
def cut():
    __thisTextPad.event_generate("<<Cut>>")
__thisEditMenu.add_command(label="Cut", accelerator='Ctrl + X',compound=LEFT, command=cut)
def copy():
     __thisTextPad.event_generate("<<Copy>>")
__thisEditMenu.add_command(label="Copy", accelerator='Ctrl + C',compound=LEFT, command=copy)
def paste():
     __thisTextPad.event_generate("<<Paste>>")
__thisEditMenu.add_command(label="Paste",accelerator='Ctrl + V',compound=LEFT, command=paste)
def allSelection():
    __thisTextPad.tag_add('sel', '1.0', 'end')
__thisEditMenu.add_command(label="Select all",accelerator='Ctrl + A',compound=LEFT, command=allSelection)
#View menu
def findnreplace():
    global t2
    t2 = Toplevel(__root)
    t2.geometry('300x100+200+250')
    t2.transient(__root)
    def Pla():
        pass
    t2.protocol("WM_DELETE_WINDOW", Pla)
    def find(case):
        __thisTextPad.tag_remove('found', '1.0', END)
        count = 0
        s = edit.get()
        if (s):
            idx = '1.0'
            while 1:
                idx = __thisTextPad.search(s, idx, nocase = case,stopindex = END)
                if not idx: break
                lastidx = '% s+% dc' % (idx, len(s))
                print(lastidx)
                __thisTextPad.tag_add('found', idx, lastidx)
                idx = lastidx
                count += 1
            __thisTextPad.tag_config('found', foreground ='red')
        edit.focus_set()
        t2.title('%d matches found' %count)
    def findNreplace():
        __thisTextPad.tag_remove('found', '1.0', END)
        s = edit.get()
        r = edit1.get()
        
        if (s and r):
            idx = '1.0'
            while 1:
                idx = __thisTextPad.search(s, idx, nocase = 1,stopindex = END)
                print(idx)
                if not idx: break
                lastidx = '% s+% dc' % (idx, len(s))
                __thisTextPad.delete(idx, lastidx)
                __thisTextPad.insert(idx, r)
                lastidx = '% s+% dc' % (idx, len(r))
                __thisTextPad.tag_add('found', idx, lastidx)
                idx = lastidx
            __thisTextPad.tag_config('found', foreground ='green', background = 'yellow')
        edit.focus_set()
    def close_search():
        __thisTextPad.tag_remove('found', '1.0', END)
    def close():
        t2.destroy()
    t2.bind("<Escape>", lambda x: close())
    Label(t2, text="Find All:").grid(row=0, column=0, sticky='e')
    edit = ttk.Entry(t2)
    edit.grid(row=0, column=1, sticky='w', padx=2, pady=2)
    Label(t2, text="Replace All:").grid(row=2, column=0, sticky='e')
    edit1 = ttk.Entry(t2)
    edit1.grid(row=2, column=1, sticky='w',padx=2, pady=2)
    Button(t2, text="Find All", underline=0, command=lambda:find(c.get())).grid(row=0,
    column=2, sticky='e'+'w', padx=2, pady=2)
    Button(t2, text="Replace All", underline=0, command=findNreplace).grid(row=2,
    column=2, sticky='e'+'w', padx=2, pady=2)
    Button(t2, text='clear', bg='red', command=close_search).grid(row=3, column=2, sticky='e'+'w', padx=1, pady=1)
    c=IntVar()
    ttk.Checkbutton(t2, text='Ignore Case', variable=c).grid(row=3,column=1, sticky='e' + 'w', padx=2, pady=2) 
    edit.bind('<Return>', lambda x:find(c.get()))
    edit1.bind('<Return>', lambda x:findNreplace())
__thisViewMenu.add_command(label="Find",compound=LEFT ,  accelerator='Ctrl + F',command=findnreplace )
__root.bind("<Control-f>", lambda x: findnreplace())
show_all =IntVar()
show_all.set(0)
def pyColor():
    val = show_all.get()
    if val == 1:
        Percolator(__thisTextPad).insertfilter(ColorDelegator())
    elif val == 0:
        pass
__thisViewMenu.add_checkbutton(label="Python highlighting", onvalue=1, offvalue=0, variable=show_all, command=pyColor)
#Help menu
cmenu = Menu(__thisTextPad)
def popup(event):
    cmenu.tk_popup(event.x_root, event.y_root, 0)
for i in ('cut', 'copy', 'paste', 'undo', 'redo', 'allSelection', 'italicise', 'bold', 'underline', 'superscript', 'subscript', 'color', 'highlight'):
    cmd = eval(i)
    cmenu.add_command(label=i, compound=LEFT, command=cmd)
__thisTextPad.bind("<Button-3>", popup)
#loop
__root.mainloop()
