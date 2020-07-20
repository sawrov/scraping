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

# Run forever!
root.mainloop()
