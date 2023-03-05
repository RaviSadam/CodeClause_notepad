from tkinter import *
from tkinter import filedialog,simpledialog,messagebox
from tkinter import colorchooser,font
from tkinter.ttk import *
from io import* 


curr_font='Helvetica'
curr_font_size=13
file_path=None
files = [('All Files', '*.*'), ('Python Files', '*.py'),('Text Document', '*.txt')]
fileSaved=False
tags=set()
curr_tag_count=0
row,col=1,1
#key event for updating the status bar
def on_key_press(event):
    global curr_font,curr_font_size,row,col
    row,col=body.index("end-1c").split(".")
    status_bar.config(text="Font: "+curr_font+"             Font Size: "+str(curr_font_size)+"           Row: "+str(row)+"       Col: "+str(col))
    global fileSaved
    fileSaved=False
#saving the file
def save():
    global file_path
    if(file_path!=None):
        f=open(file_path,"w")
        f.write(body.get("1.0","end"))
        f.flush()
        f.close()
        messagebox.showinfo("Info","File Saved Successful")
    else:
        saveAs()
#saving the new File
def saveAs():
    global files,file_path
    file=filedialog.asksaveasfile(filetypes=files,defaultextension=files)
    file_path=file.name
    file.write(body.get("1.0","end"))
    file.flush()
    file.close()
    messagebox.showinfo("Info","File Saved Successful")
#opening the file
def openFileDialog():
    global file_path
    file=filedialog.askopenfile(parent=root,title="Open A file")
    file_path=file.name
    data=file.read()
    file.close()
    body.delete("1.0","end")
    body.insert("1.0",data)
#Copying the selected text
def copy():
    try:
        global copyed_text
        copyed_text=body.selection_get()
    except:
        MessageDialog("Warring","No Selection Present")
#citting the selected text
def cut():
    global copyed_text
    try:
        temp=body.selection_get()
        copyed_text=temp
        SEL_FIRST,SEL_LAST,end=body.index("sel.first"),body.index("sel.last"),body.index("end")
        last_text=body.get(SEL_LAST,end).strip()
        body.delete(SEL_FIRST,end)
        if(last_text):
            body.insert(body.index("end"),last_text)
    except:
        MessageDialog("Warring","No Selection Present")
#pasting the text
def past():
    end=body.index("end")
    try:
        global copyed_text
        SEL_FIRST,SEL_LAST=body.index("sel.first"),body.index("sel.last")
        last_text=body.get(SEL_LAST,end).strip()
        body.delete(SEL_FIRST,end)
        if(copyed_text):
            body.insert(body.index("end"),copyed_text)
        if(last_text):
            body.insert(body.index("end"),last_text)
    except:
        body.insert(end,copyed_text)
#deleting the selected text
def delete():
    try:
        SEL_FIRST,SEL_LAST,end=body.index("sel.first"),body.index("sel.last"),body.index("end")
        last_text=body.get(SEL_LAST,end).strip()
        body.delete(SEL_FIRST,end)
        if(last_text):
            body.insert(body.index("end"),last_text)
    except:
        MessageDialog("Warring","No Selection Present")
#removing the labels
def removeTags():
    global tags
    for i in tags:
        body.tag_delete(i)
#finding the specific text seraching and labling the text
def find():
    global curr_tag_count,tags
    responce=simpledialog.askstring(parent=root,title="Input",prompt="Enter Text To Find")
    print(responce)
    idx = '1.0'
    tag_name="find"+str(curr_tag_count)
    curr_tag_count+=1
    l=len(responce)
    while 1:
        idx = body.search(responce, idx, nocase=1,stopindex=END)
        if not idx: 
            break
        lastidx = '%s+%dc' % (idx, l)
        body.tag_add(tag_name, idx, lastidx)
        idx = lastidx
    body.tag_config(tag_name,background='blue')
    tags.add(tag_name)
    body.after(800,removeTags)
#Closing operations
def exit_code():
    global fileSaved
    if(not fileSaved):
        yorn=messagebox.askyesno("Warring","File Not Saved")
        if(yorn):
            save()
    root.destroy()

def MessageDialog(title,message):
    messagebox.showwarning(title,message)
#for changnig the font style of body text and updating the font style in status bar
def change_font(font_style):#pending
    global curr_font_size,curr_font,row,col
    curr_font=font_style
    status_bar.config(text="Font: "+curr_font+"             Font Size: "+str(curr_font_size)+"           Row: "+str(row)+"       Col: "+str(col))
    body.configure(font=(curr_font,str(curr_font_size)))
#for changnig the font size and updating the font size in status bar
def font_size_config():
    global curr_font_size,curr_font,col,row
    val=simpledialog.askinteger(title="Font Size",parent=root,prompt="Enter Font value")
    curr_font_size=val
    status_bar.config(text="Font: "+curr_font+"             Font Size: "+str(curr_font_size)+"           Row: "+str(row)+"       Col: "+str(col))
    body.configure(font=(curr_font,val))
#background color changing
def bg():
    color_code = colorchooser.askcolor(title ="Choose color")
    body.configure(background=color_code[1])
#Text Color Changing
def tc():
    color_code = colorchooser.askcolor(title ="Choose color")
    body.configure(foreground=color_code[1])
#Main Window
root=Tk()
root.title("Nodepad")
root.geometry("800x600")
root.resizable(0,0)
# create a menubar
menubar = Menu(root)
root.config(menu=menubar)
#
#Main body (text area)
#
body=Text(root,width=90,height=38)
body.config(font=(curr_font,curr_font_size))
body.grid(row=1,column=0)   
body.bind("<KeyRelease>",on_key_press)
#
#Status bar
#
status_bar=Label(text="Font: "+curr_font+"             Font Size: "+str(curr_font_size)+"           Row:1"+"       Col:1",width=135,background="#34a145")
status_bar.grid(row=0,column=0,sticky=W)
#
# create a File menu
#
file_menu = Menu(menubar,tearoff=0,font=("Incised",11))
file_menu.add_command(label="Save",command=save)
file_menu.add_command(label="Save As",command=saveAs)
file_menu.add_command(label="Open",command=openFileDialog)
file_menu.add_separator()
file_menu.add_command(label='Exit',command=root.destroy)
menubar.add_cascade(label="File",menu=file_menu)
#
#Edit menu
#
edit_menu=Menu(menubar,tearoff=0,font=("Incised",11))
edit_menu.add_command(label="Copy",command=copy)
edit_menu.add_command(label="Past",command=past)
edit_menu.add_command(label="Cut",command=cut)
edit_menu.add_command(label="Delete",command=delete)
edit_menu.add_separator()
edit_menu.add_command(label="Find",command=find)
edit_menu.add_command(label="Select All")
edit_menu.add_command(label="Exit",command=exit_code)
menubar.add_cascade(label="Edit",menu=edit_menu)
#
#Font Size
#
font_size_menu=Menu(menubar,tearoff=0)
font_size_menu.add_command(label="Give Font size",command=font_size_config)
menubar.add_cascade(label="Font Size",menu=font_size_menu)
#
#Font Style
#
font_style_menu=Menu(menubar,tearoff=0)
available_fonts =["System","Modern","Roman","Script","Ms Serif","Ms Sans Serif","Small Fonts",'Terminal',"Tekton pro","Stencil Std","Curier","Fixessys","Ravie","Helvetica"]
for font_family in available_fonts:
    font_style_menu.add_command(label=font_family, command=lambda font_family=font_family: change_font(font_family))
menubar.add_cascade(label="Font Style",menu=font_style_menu)
#
#Background Color
#
background_color=Menu(menubar,tearoff=0)
background_color.add_command(label="Choose Color",command=bg,font=("dom casual",13))
menubar.add_cascade(label="Background Color",menu=background_color)
#
#Text Color
#
foreground_color=Menu(menubar,tearoff=0)
foreground_color.add_command(label="Choose Color",command=tc,font=("dom casual",13))
menubar.add_cascade(label="Text Color",menu=foreground_color)
#Main Loop
root.mainloop()