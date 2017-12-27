import subprocess
from tkinter import *

def show_entry_fields():
    print("E-mail: %s" % (mailveld.get(Entry)))
    
def toggleKeyboard():
    p = subprocess.Popen(['florence show'], shell=True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, universal_newlines=True)
    if not "" == p.stderr.readline():
        subprocess.Popen(['florence'], shell=True)
#toggleKeyboard()        
#root = Tk()


#Label(root, text="Vul hier uw e-mail in").grid(row=0)

#mailveld = Entry(root)
#mailveld.grid(row=0, column=1)

#Button(root, text='Show keyboard', command=toggleKeyboard).grid(row=3, column=0, sticky=W, pady=4)
#Button(root, text='Submit', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

#root.mainloop()
