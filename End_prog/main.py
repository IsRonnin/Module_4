import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root, db):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialogue = tk.Button(toolbar, bg="#d6d8e0", bd=0, image=self.add_img, command=self.open_dialogue)
        btn_open_dialogue.pack(side=tk.LEFT)
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'), height=45, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)
        self.tree.heading('ID',text="ID")
        self.tree.heading('name',text="ФИО")
        self.tree.heading('tel',text="Телефон")
        self.tree.heading('email',text="E-Mail")
        self.tree.heading('salary',text="Зарплата")
        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='./img/update.png')
        button_update_dialogue = tk.Button(toolbar, bg="#d7d8e0", bd=0, image=self.update_img, command=self.open_update_dialogue)
        button_update_dialogue.pack(side = tk.LEFT)
        self.search_img = tk.PhotoImage(file="./img/search.png")
        button_search = tk.Button(toolbar, bg="#d7d8e0", bd=0, image=self.search_img, command=self.open_search_dialogue)
        button_search.pack(side=tk.LEFT)
        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        button_delete_dialogue = tk.Button(toolbar, bg="#d7d8e0", bd=0, image=self.delete_img, command=self.delete_records)
        button_delete_dialogue.pack(side=tk.LEFT)
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg="#d7d8e0", bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

    def open_dialogue(self):
        Child(self)

    def records(self, name, tel, email, salary):
        self.db.insert_data(name,tel,email,salary)
        self.view_records()

    def view_records(self):
        self.db.cursor.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def open_update_dialogue(self):
        Update(self)

    def update_records(self, name, tel, email, salary):
        self.db.cursor.execute('''UPDATE db SET name=?, tel=?, email=?, salary=? WHERE id=?''', (name, tel, email, salary, self.tree.set(self.tree.selection(),'#1')))
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute('''DELETE FROM db WHERE id=?''', (self.tree.set(selection_item, "#1"),))
        self.db.conn.commit()
        self.view_records()

    def open_search_dialogue(self):
        Search(self)

    def search_records(self, name):
        name = ('%' + name + "%")
        self.db.cursor.execute('''SELECT * FROM db WHERE name LIKE ?''', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

class Search(tk.Toplevel):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.init_search()

    def init_search(self):
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)
        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)
        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)
        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)
        btn_search = tk.Button(self, text="Поиск")
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add="+")

class Child(tk.Toplevel):
    def __init__(self, view):
        super().__init__(view)
        self.view = view
        self.init_child()

    def init_child(self):
        self.title("Добавить")
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)
        label_salary = tk.Label(self, text="Зарплата:")
        label_salary.place(x=50, y=140)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=300, y=170)
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(), self.entry_tel.get(), self.entry_email.get(), self.entry_salary.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add="+")
class Update(Child):
    def __init__(self, view):
        super().__init__(view)
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title("Редактировать контакт")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_name.get(), self.entry_tel.get(), self.entry_email.get(), self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cursor.execute('''SELECT * FROM db WHERE id=?''', self.view.tree.set(self.view.tree.selection(), '#1'))
        row = self.db.cursor.fetchall()[0]
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db(
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT,
            salary TEXT
            )'''
        )
        self.conn.commit()

    def insert_data(self, name, tel, email, salary):
        self.cursor.execute(
            '''INSERT INTO db(name, tel, email, salary) VALUES(?, ?, ?, ?)''', (name, tel, email, salary))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    # Add code here to define the Main class
    app = Main(root, db)
    app.pack()
    root.title("Список Сотрудников компании")
    root.geometry("800x450")
    root.resizable(False, False)
    root.mainloop()