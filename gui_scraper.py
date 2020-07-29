import tkinter as tk


def checkfunc(val):
    print(val)


# Create the main window
root = tk.Tk()
root.title("ALI EXPRESS SCRAPER")
root.geometry("400x250")
# Create label
label = tk.Label(root, text="PLEASE ENTER THE KEY PROVIDED")
label.pack()

key = tk.Entry(root)
key.pack()

verify_key = tk.Button(root, text="VERIFY KEY", command=lambda: checkfunc(key.get()))
verify_key.pack()

label2 = tk.Label(root, text="PLEASE SELECT A CURRENCY")
label2.pack()

currency_file = open("currency_list.txt", "r")
currency_list = currency_file.readlines()
currency_list=[i.strip() for i in currency_list]
dropdown_var=tk.StringVar(root)
dropdown_var.set(currency_list[0])
# print(len(currency_list))
dropdown = tk.OptionMenu(root, dropdown_var, *currency_list)
dropdown.config(height=0)
dropdown.pack()

CheckVar1 = tk.IntVar()
C1 = tk.Checkbutton(root, text = "SCHEDULE REFRESH", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0)
C1.pack()

# Run forever!
root.mainloop()
