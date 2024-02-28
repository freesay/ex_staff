import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import datetime as dt
import csv


def staff_complete(file_name):
    staff = {}
    with open(file_name, newline='', encoding='utf-8') as f:
        data = csv.reader(f, delimiter=";")
        for row in data:
            login = row[0]
            data_employee = {}
            if "Login" not in login:
                data_employee['name'] = row[1]
                data_employee['last_name'] = row[2]
                data_employee['position'] = row[4]
                data_employee['department'] = row[6]
                staff[login] = data_employee
    return staff


def employees_complete(staff):
    tmp_dict = {}
    sorted_dict = {}
    for login, data in staff.items():
        tmp_dict[login] = data['position']
    sorted_list = sorted(tmp_dict.items(), key=lambda x: x[1])
    for el in sorted_list:
        sorted_dict[el[0]] = el[1]
    return sorted_dict


def positions_complete(staff):
    positions_list = []
    for login, data in staff.items():
        positions_list.append(data["position"])
    return sorted(set(positions_list))


def departments_complete(staff):
    departments_list = []
    for login, data in staff.items():
        departments_list.append(data["department"])
    return sorted(set(departments_list))


class Common():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1000x600')
        self.root.minsize(1200, 600)
        self.root.title('ex_staff')

        self.rad_var = tk.StringVar()
        self.rad_var.set('position')
        self.date_var = tk.StringVar()
        self.date_var.set(str(dt.date.today()))
        self.ticket_var = tk.StringVar()
        self.ticket_var.set('SECALERTS-XXXXXX')

        self.data_employees = {}
        self.positions = {}
        self.departments = {}

    def init_frames(self):
        self.main_frame = ttk.Frame(self.root)
        self.btn_open_file_frame = ttk.Frame(self.main_frame)
        self.radio_btn_frame = ttk.Frame(self.main_frame)

        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas = tk.Canvas(self.canvas_frame, borderwidth=0, highlightthickness=0)
        self.canvas_scroll_y = ttk.Scrollbar(self.canvas_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.config(yscrollcommand=self.canvas_scroll_y.set)

        self.canvas.bind("<Enter>", lambda event: self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel))
        self.canvas.bind("<Leave>", lambda event: self.canvas.unbind_all("<MouseWheel>"))
        self.scrollable_frame.bind('<Configure>', lambda e: self.frame_configure())
        self.wrap_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.btn_save_frame = ttk.Frame(self.main_frame)
        self.text_frame = ttk.Frame(self.root)
        self.entry_frame = ttk.Frame(self.text_frame)
        self.entry_frame_date = ttk.LabelFrame(self.entry_frame, text='Date')
        self.entry_frame_ticket = ttk.LabelFrame(self.entry_frame, text='Ticket')

    def frame_configure(self):
        canvas = self.canvas
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfigure(self.wrap_frame, width=canvas.winfo_width())

    def on_mouse_wheel(self, event, scale=3):
        canvas = self.canvas
        if event.delta<0:
            canvas.yview_scroll(scale, "units")
        else:
            canvas.yview_scroll(-scale, "units")

    def init_buttons(self):
        self.btn_open_file = ttk.Button(self.btn_open_file_frame, text='Open File', width=70, command=self.open_file)
        self.btn_generate = ttk.Button(self.btn_save_frame, text='Generate Data', command=self.get_data_check)
        self.btn_save_txt = ttk.Button(self.btn_save_frame, text='Save to TXT', command=self.save_txt)
        self.btn_save_csv = ttk.Button(self.btn_save_frame, text='Save to CSV', command=self.save_csv)

    def init_radio_buttons(self):
        self.rad_pos = ttk.Radiobutton(self.radio_btn_frame, text='Position',
                                       variable=self.rad_var, value='position', command=self.get_type_data)
        self.rad_dep = ttk.Radiobutton(self.radio_btn_frame, text='Department',
                                       variable=self.rad_var, value='department', command=self.get_type_data)
        self.rad_emp = ttk.Radiobutton(self.radio_btn_frame, text='Employees',
                                       variable=self.rad_var, value='employees', command=self.get_type_data)

    def init_text_data(self):
        self.text_date = tk.Entry(self.entry_frame_date, textvariable=self.date_var)

    def init_text_ticket(self):
        self.text_ticket = tk.Entry(self.entry_frame_ticket, textvariable=self.ticket_var)

    def init_text_field(self):
        self.text_box = tk.Text(self.text_frame, wrap='none')
        self.scroll_y = ttk.Scrollbar(self.text_frame, orient='vertical', command=self.text_box.yview)
        self.scroll_x = ttk.Scrollbar(self.text_frame, orient='horizontal', command=self.text_box.xview)
        self.text_box.config(yscrollcommand=self.scroll_y.set)
        self.text_box.config(xscrollcommand=self.scroll_x.set)

    def pack_widgets(self):
        self.main_frame.pack(anchor='nw', side='left', fill='both', padx=5, pady=5)
        self.text_frame.pack(anchor='nw', fill='both', expand=True, padx=5, pady=5)
        self.entry_frame.pack(anchor='nw', fill='x', padx=5, pady=5)
        self.entry_frame_date.pack(side='left', fill='x', expand=True)
        self.entry_frame_ticket.pack(side='left', fill='x', expand=True)

        self.btn_open_file_frame.pack(anchor='nw', side='top', fill='x', padx=5, pady=5)
        self.btn_save_frame.pack(side='bottom', fill='x', padx=5)
        self.radio_btn_frame.pack()

        self.canvas_frame.pack(fill='both', expand=True, padx=5)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas_scroll_y.pack(side='right', fill='y')

        self.rad_pos.pack(side='left')
        self.rad_dep.pack(side='left')
        self.rad_emp.pack(side='left')

        self.text_date.pack(side='top', fill='x', expand=True, padx=5, pady=5)
        self.text_ticket.pack(side='top', fill='x', expand=True, padx=5, pady=5)
        self.scroll_y.pack(side='right', fill='y')
        self.scroll_x.pack(side='bottom', fill='x')
        self.text_box.pack(side='bottom', fill='both', expand=True, padx=5, pady=5)

        self.btn_open_file.pack(side='left', fill='x', expand=True)
        self.btn_generate.pack(side='top', fill='x', expand=True, pady=5)
        self.btn_save_txt.pack(side='left', fill='x', expand=True)
        self.btn_save_csv.pack(side='left', fill='x', expand=True)

    def open_file(self):
        self.file = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        self.file_name = self.file
        self.data_employees = staff_complete(self.file_name)
        self.positions = positions_complete(self.data_employees)
        self.departments = departments_complete(self.data_employees)
        self.employees = employees_complete(self.data_employees)
        self.update_data()
        self.root.update()

    def get_data_check(self):
        try:
            data_check = {}
            for el in self.checks:
                data_check[el] = self.checks[el].get()

            if self.rad_var.get() == 'position':
                generate_data = ''
                for key, value in data_check.items():
                    if value == 1:
                        for login, data in self.data_employees.items():
                            for el in data:
                                if key == data[el]:
                                    generate_data += f'{self.text_date.get()},{login},,"{self.text_ticket.get()}"\n'
                self.text_box.delete('1.0', 'end-1c')
                self.text_box.insert('1.0', generate_data)
            if self.rad_var.get() == 'department':
                data_list = []
                generate_data = ''
                for key, value in data_check.items():
                    if value == 1:
                        for login, data in self.data_employees.items():
                            for el in data:
                                if key == data[el]:
                                    temp = data[el]
                                    temp = temp.replace('"', '""')
                                    line = f'{self.text_date.get()},,"{temp}","{self.text_ticket.get()}"\n'
                                    if line not in data_list:
                                        data_list.append(line)
                for el in data_list:
                    generate_data += el
                self.text_box.delete('1.0', 'end-1c')
                self.text_box.insert('1.0', generate_data)
            if self.rad_var.get() == 'employees':
                generate_data = ''
                for login, value in data_check.items():
                    if value == 1:
                        generate_data += f'{self.text_date.get()},{login},,"{self.text_ticket.get()}"\n'
                self.text_box.delete('1.0', 'end-1c')
                self.text_box.insert('1.0', generate_data)
        except:
            generate_data = ''
            logins = self.text_box.get('1.0', 'end-1c')
            for login in logins.split():
                generate_data += f'{self.text_date.get()},{login.rstrip("@")},,"{self.text_ticket.get()}"\n'
            self.text_box.delete('1.0', 'end-1c')
            self.text_box.insert('1.0', generate_data)


    def get_type_data(self):
        self.rad_var.set(self.rad_var.get())
        self.update_data()

    def complete_check_data(self):
        self.checks = {}
        if self.rad_var.get() == 'position':
            temp_data = self.positions
            for el in temp_data:
                self.checks[el] = tk.IntVar()
            for el in temp_data:
                self.checkbox_frame = ttk.Frame(self.scrollable_frame)
                check_box = ttk.Checkbutton(self.checkbox_frame, text=el, variable=self.checks[el], onvalue=1, offvalue=0)
                check_box.pack(anchor='nw')
                self.checkbox_frame.pack(anchor='nw', padx=5)
        elif self.rad_var.get() == 'department':
            temp_data = self.departments
            for el in temp_data:
                self.checks[el] = tk.IntVar()
            for el in temp_data:
                self.checkbox_frame = ttk.Frame(self.scrollable_frame)
                check_box = ttk.Checkbutton(self.checkbox_frame, text=el, variable=self.checks[el], onvalue=1, offvalue=0)
                check_box.pack(anchor='nw')
                self.checkbox_frame.pack(anchor='nw', padx=5)
        else:
            temp_data = self.employees
            for el in temp_data:
                self.checks[el] = tk.IntVar()
            for key, value in temp_data.items():
                self.checkbox_frame = ttk.Frame(self.scrollable_frame)
                text = f'{key}@ - {value}'
                check_box = ttk.Checkbutton(self.checkbox_frame, text=text, variable=self.checks[key], onvalue=1, offvalue=0)
                check_box.pack(anchor='nw')
                self.checkbox_frame.pack(anchor='nw', padx=5)
        return self.checks

    def save_txt(self):
        date = self.date_var.get().split('-')
        with open(f'{date[-1]}.{date[-2]}.txt', 'w', encoding='utf-8') as f:
            f.write(self.text_box.get("1.0", 'end-1c'))

    def save_csv(self):
        date = self.date_var.get().split('-')
        with open(f'{date[-1]}.{date[-2]}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for line in self.text_box.get("1.0", 'end-1c').split('\n'):
                writer.writerow(line.split(','))

    def init_widgets(self):
        self.init_frames()
        self.init_buttons()
        self.init_radio_buttons()
        self.init_text_data()
        self.init_text_ticket()
        self.init_text_field()
        self.pack_widgets()

    def update_data(self):
        self.main_frame.destroy()
        self.text_frame.destroy()
        self.init_widgets()
        self.complete_check_data()

    def run_build(self):
        self.init_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    common = Common()
    common.run_build()
