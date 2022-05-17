import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import static_functions as sf    # Import module with function for app
# Importing all modules that I need

class App(tk.Tk):    # Declare main App class with title and styles of my app
    def __init__(self):
        super().__init__()
        self.title('Spendman')
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('ErrorLbl.TLabel', foreground='red', padding=(40, 10, 50, 10))
        self.style.configure('JustLbl.TLabel', padding=(40, 10, 50, 10))
        self.style.configure('BldLbl.TLabel', font=('Helvetica', 14, 'bold'), padding=(0, 10, 0, 10))
        self.put_frames()
        self.put_menu()

    def put_menu(self):     # Main menu bar
        self.config(menu=MainMenu(self))

    def put_frames(self):    # All 3 frames in app and their coordinates
        self.new_record_frame = NewRecord(self).grid(row=0, column=0, sticky='nswe')
        self.statictic_frame = StaticticFrame(self).grid(row=0, column=1, sticky='nswe')
        self.table_frame = TableFrame(self).grid(row=1, column=0, columnspan=2, sticky='nswe')

    def refresh(self):    # method of refreshing page
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.put_frames()
        self.put_menu()

    def quit(self):    # Quit method
        return Popup(self)


class Popup:    # Class of quit method
    def __init__(self, master):
        self.master = master
        answer = mb.askyesno('Quit?', 'Are you sure?')
        if answer is True:
            master.destroy()


class MainMenu(tk.Menu):    # Class of Main menu
    def __init__(self, mainwindow):
        super().__init__(mainwindow)

        file_menu = tk.Menu(self)
        options_menu = tk.Menu(self)

        file_menu.add_command(label='Quit', command=mainwindow.quit)
        options_menu.add_command(label='Refresh', command=mainwindow.refresh)
        self.add_cascade(label='File', menu=file_menu)
        self.add_cascade(label='Options', menu=options_menu)


class NewRecord(ttk.Frame):    # Frame where you add new Records
    def __init__(self, parent):
        super().__init__(parent)
        self.categories = sf.get_expenses_items()
        self.names = sf.get_int_name()
        self.put_widgets()

    def put_widgets(self):    # Widgets of New Record Frame and their coordinates
        self.l_choose = ttk.Label(self, text='Choose category', style='JustLbl.TLabel')
        self.f_choose = ttk.Combobox(self, values=self.categories['categories'])
        self.l_amount = ttk.Label(self, text='Enter amount', style='JustLbl.TLabel')
        self.f_amount = ttk.Entry(self, justify=tk.RIGHT, validate='key',
                                  validatecommand=(self.register(self.validate_amount), '%P'))
        self.l_date = ttk.Label(self, text='Enter date', style='JustLbl.TLabel')
        self.f_date = DateEntry(self, foreground='black', normalforeground='black',
                                selectforeground='red', background='white', date_pattern='dd-mm-YYYY')

        self.l_name = ttk.Label(self, text='Payer name', style='JustLbl.TLabel')
        self.f_name = ttk.Combobox(self, values=self.names['names'])
        self.l_desc = ttk.Label(self, text='Enter comment', style='JustLbl.TLabel')
        self.f_desc = ttk.Entry(self, justify=tk.RIGHT)
        self.sbt_button = ttk.Button(self, text='Submit', command=self.form_submit)

        self.l_choose.grid(row=0, column=0, sticky='w')
        self.f_choose.grid(row=0, column=1, sticky='e')
        self.l_amount.grid(row=1, column=0, sticky='w')
        self.f_amount.grid(row=1, column=1, sticky='e')
        self.l_date.grid(row=2, column=0, sticky='w')
        self.f_date.grid(row=2, column=1, sticky='e')
        self.l_name.grid(row=3, column=0, sticky='w')
        self.f_name.grid(row=3, column=1, sticky='e')
        self.l_desc.grid(row=4, column=0, sticky='w')
        self.f_desc.grid(row=4, column=1, sticky='e')
        self.sbt_button.grid(row=5, column=0, columnspan=2, sticky='n')

        # self.f_date._top_cal.overrideredirect(False)    # For correct work on MacOs uncomment this line.

    def validate_amount(self, input):    # Method to validate data in input
        print(input, 'input')
        try:
            x = float(input)
            return True
        except ValueError:
            self.bell()
            return False

    def form_submit(self):    # Method of adding info to database SQLite
        global amount, expense_id, payer_id
        flag = True
        payment_date = sf.get_timestamp_from_input(self.f_date.get())
        description = self.f_desc.get()
        try:
            expense_id = self.categories['accordance'][self.f_choose.get()]
            amount = float(self.f_amount.get())
            payer_id = self.names['accordance'][self.f_name.get()]
            self.l_choose['style'] = 'JustLbl.TLabel'
            self.l_amount['style'] = 'JustLbl.TLabel'
            self.l_name['style'] = 'JustLbl.TLabel'
        except KeyError:
            if self.f_choose.get() != '':
                pass
            else:
                self.l_choose['style'] = 'ErrorLbl.TLabel'
                self.l_name['style'] = 'ErrorLbl.TLabel'
                self.bell()
                flag = False
        except ValueError:
            self.l_amount['style'] = 'ErrorLbl.TLabel'
            self.bell()
            flag = False

        if flag:
            insert_payments = (amount, payment_date, expense_id, payer_id, description)
            if sf.insert_payments(insert_payments):
                self.master.refresh()


class StaticticFrame(ttk.Frame):    # Class of Frame with static info
    def __init__(self, parent):
        super().__init__(parent)
        self.put_widgets()

    def put_widgets(self):
        self.l_most_spend_category_text = ttk.Label(self, text='Biggest spending category:', style='JustLbl.TLabel')
        self.l_most_spend_category_value = ttk.Label(self, text=sf.most_spend_category(), style='BldLbl.TLabel')
        self.l_most_spend_day_text = ttk.Label(self, text='Most spending day:', style='JustLbl.TLabel')
        self.l_most_spend_day_value = ttk.Label(self, text=sf.most_exp_day(), style='BldLbl.TLabel')
        self.l_most_spend_month_text = ttk.Label(self, text='Most spending month:', style='JustLbl.TLabel')
        self.l_most_spend_month_value = ttk.Label(self, text=sf.get_most_exp_month(), style='BldLbl.TLabel')
        self.l_most_spend_ever_text = ttk.Label(self, text='Biggest spending:', style='JustLbl.TLabel')
        self.l_most_spend_ever_value = ttk.Label(self, text=sf.most_cost_spend(), style='BldLbl.TLabel')
        self.l_spender_one_text = ttk.Label(self, text='All Dmitrii spent:', style='JustLbl.TLabel')
        self.l_spender_one_value = ttk.Label(self, text=sf.get_sum_pay2(), style='BldLbl.TLabel')
        self.l_spender_two_text = ttk.Label(self, text='All Margarita spent:', style='JustLbl.TLabel')
        self.l_spender_two_value = ttk.Label(self, text=sf.get_sum_pay1(), style='BldLbl.TLabel')

        self.l_most_spend_category_text.grid(row='0', column='0', sticky='w')
        self.l_most_spend_category_value.grid(row='0', column='1', sticky='e')
        self.l_most_spend_day_text.grid(row='1', column='0', sticky='w')
        self.l_most_spend_day_value.grid(row='1', column='1', sticky='e')
        self.l_most_spend_month_text.grid(row='2', column='0', sticky='w')
        self.l_most_spend_month_value.grid(row='2', column='1', sticky='e')
        self.l_most_spend_ever_text.grid(row='3', column='0', sticky='w')
        self.l_most_spend_ever_value.grid(row='3', column='1', sticky='e')
        self.l_spender_one_text.grid(row='4', column='0', sticky='w')
        self.l_spender_one_value.grid(row='4', column='1', sticky='e')
        self.l_spender_two_text.grid(row='5', column='0', sticky='w')
        self.l_spender_two_value.grid(row='5', column='1', sticky='e')


class TableFrame(ttk.Frame):    # Class for bottom Frame with info about all the record.
    def __init__(self, parent):
        super().__init__(parent)
        self.put_widgets()

    def put_widgets(self):
        table = ttk.Treeview(self, show='headings')
        heads = ['id', 'Amount', 'Payment date', 'Category', 'Payer', 'Comment']
        table['columns'] = heads

        for header in heads:
            table.heading(header, text=header, anchor='center')
            table.column(header, anchor='center')

        for row in sf.get_table_data():    # display data from database
            table.insert('', 0, values=row)

        scroll_pane = ttk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)

app = App()

app.mainloop()
