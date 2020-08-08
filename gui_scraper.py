import tkinter as tk
from tkinter.filedialog import askopenfilename

class AliScraper_GUI:

        def __init__(self):
                self.root = tk.Tk()
                self.root.title("ALI EXPRESS SCRAPER")
                self.root.geometry("550x200")

                self.verifykeys()
                self.currency()
                self.cronjob()
                self.select_file()
                self.scrape_button()

                self.root.mainloop()

        def verifykeys(self):
                self.label1 = tk.Label(self.root, text="ENTER THE KEY").grid(row=1, column =0)
                self.key = tk.Entry(self.root).grid(row=1, column=1)
                self.verify_key = tk.Button(self.root, text="VERIFY KEY", command=lambda: self.checkfunc(key.get())).grid(row=1, column=2)

        def currency(self):
                self.label2 = tk.Label(self.root, text=" SELECT A CURRENCY").grid(row=3,column=0)
                self.currency_file = open("currency_list.txt", "r")
                self.currency_list = self.currency_file.readlines()
                self.currency_list = [i.strip() for i in self.currency_list]
                self.dropdown_var = tk.StringVar(self.root)
                self.dropdown_var.set(self.currency_list[0])
                self.dropdown_currency = tk.OptionMenu(self.root, self.dropdown_var, *self.currency_list).grid(row=3,column=1)

        def cronjob(self):
                self.label3 = tk.Label(self.root, text="SCHEDULE A REFRESH").grid(row=4,column=0)
                days = [ str(day) + " day" for day in list(range(0,30))]
                time = [str(hr) + " hrs" for hr in list(range(0,24))]
                self.dropdown_day = tk.StringVar(self.root)
                self.dropdown_day.set(days[0])
                self.dropdown_time = tk.StringVar(self.root)
                self.dropdown_time.set(time[0])

                self.dropdown_day_item = tk.OptionMenu(self.root, self.dropdown_day, *days).grid(row=4,column=3,columnspan=1)
                self.dropdown_time_item = tk.OptionMenu(self.root, self.dropdown_time, *time).grid(row=4,column=2,columnspan=1)

                self.cron_check = tk.IntVar()
                C1 = tk.Checkbutton(self.root, text="YES", variable=self.cron_check, onvalue=1, offvalue=0).grid(row=4, column=1)

        def select_file(self):
                self.label4 = tk.Label(self.root, text="The program looks in aliexpressurl.txt by default").grid(row=5, column=1)
                self.select_file = tk.Button(self.root, text="LOAD URL FROM FILE", command=lambda: self.selectfile()).grid(row=6, column=1)


        def scrape_button(self):
                start_scraping = tk.Button(self.root, text="START SCRAPING", command=lambda: print("WILL INTEGRATE THE PROGRAM")).grid(row=7, column=1)

        def checkfunc(self,val):
                print(val)

        def selectfile(self):
                self.label4.config(text=askopenfilename())



        # askopenfilename()







# Run forever!

scrape=AliScraper_GUI()
