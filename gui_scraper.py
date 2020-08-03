import tkinter as tk
from tkinter.filedialog import askopenfilename


def checkfunc(val):
    print(val)

def selectfile(label):
    filename = askopenfilename()
    label.config(text=filename)
# Create the main window
root = tk.Tk()
root.title("ALI EXPRESS SCRAPER")
# root.geometry("400x250")

# Create label
label = tk.Label(root, text="ENTER THE KEY")
label.grid(row=1, column =0)

key = tk.Entry(root)
key.grid(row=1, column=1)

verify_key = tk.Button(root, text="VERIFY KEY", command=lambda: checkfunc(key.get()))
verify_key.grid(row=1, column=2)

label2 = tk.Label(root, text=" SELECT A CURRENCY")
label2.grid(row=3,column=0)

currency_file = open("currency_list.txt", "r")
currency_list = currency_file.readlines()
currency_list = [i.strip() for i in currency_list]
dropdown_var = tk.StringVar(root)
dropdown_var.set(currency_list[0])
# print(len(currency_list))
dropdown = tk.OptionMenu(root, dropdown_var, *currency_list)
dropdown.config(height=0)
dropdown.grid(row=3,column=1)

label3 = tk.Label(root, text="SCHEDULE A REFRESH")
label3.grid(row=4,column=0)
days=list(range(0,30))
time=list(range(0,24))
days = [ str(day) + " day" for day in days]
time = [str(hr) + " hrs" for hr in time]
dropdown_day = tk.StringVar(root)
dropdown_time = tk.StringVar(root)

dropdown_day.set(days[0])
dropdown_time.set(time[0])

dropdown_day_item = tk.OptionMenu(root, dropdown_day, *days)
dropdown_time_item = tk.OptionMenu(root, dropdown_time, *time)

dropdown_day_item.grid(row=4,column=3,columnspan=1)
dropdown_time_item.grid(row=4,column=2,columnspan=1)


CheckVar1 = tk.IntVar()
C1 = tk.Checkbutton(root, text="YES", variable=CheckVar1, onvalue=1, offvalue=0)
C1.grid(row=4,column=1)

# askopenfilename()
label4 = tk.Label(root, text="The program looks in aliexpressurl.txt by default")
label4.grid(row=5,column=1)


select_file = tk.Button(root, text="LOAD URL FROM FILE", command=lambda: selectfile(label4))
select_file.grid(row=6, column=1)

select_file = tk.Button(root, text="START SCRAPING", command=lambda: print("WILL INTEGRATE THE PROGRAM"))
select_file.grid(row=7, column=1)



# Run forever!
root.mainloop()
