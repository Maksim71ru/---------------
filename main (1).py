import tkinter as tk
from tkinter import ttk
import sqlite3

# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_maim()
        self.db = db
        self.view_records()

########################################################################################################### toolbar
    # Создание и работа с главным окном
    def init_maim(self):
        toolbar = tk.Frame(bg = '#d7d7d7', bd = 2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
########################################################################################################### кнопки

        # Открытие нового окна по кнопке Добавить
        self.add_img = tk.PhotoImage(file="C:\\Users\\dimon\\Desktop\\Итоговый_Проект\\img\\add.png")
        btn_add = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Открытие нового окна по кнопке Редактировать
        self.upd_img = tk.PhotoImage(file="C:\\Users\\dimon\\Desktop\\Итоговый_Проект\\img\\update.png")
        btn_upd = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.upd_img, command=self.open_update_dialog)
        btn_upd.pack(side=tk.LEFT)

        # Открытие нового окна по кнопке Удалить
        self.del_img = tk.PhotoImage(file="C:\\Users\\dimon\\Desktop\\Итоговый_Проект\\img\\delete.png")
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.del_img, command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # Открытие нового окна по кнопке Поиск
        self.search_img = tk.PhotoImage(file="C:\\Users\\dimon\\Desktop\\Итоговый_Проект\\img\\search.png")
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Открытие нового окна по кнопке Обновить
        self.refresh_img = tk.PhotoImage(file="C:\\Users\\dimon\\Desktop\\Итоговый_Проект\\img\\refresh.png")
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

########################################################################################################### работа с treeview

        # Добавление таблицы (создание дерева)
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'),
                                 height=45, show = 'headings')
        
        # Добавить параметры колонкам (сумма wigth должна равняться (root.geometry('645x450')))
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')

        # Упаковка
        self.tree.pack(side=tk.LEFT)

        # Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
########################################################################################################### Основные методы

    def records(self,name,phone,email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    # Отображение данных в TreeView
    def view_records(self):
        self.db.cur.execute('''SELECT * FROM users''')

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

    # метод обновления данных
    def update_record(self, name, phone, email):
        # в id выбираем id из запущеной программы
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''UPDATE users SET name=?, phone=?, email=? WHERE ID=?''',
                            (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()
    
    # метод удаоения данных
    def delete_records(self):
        for row in self.tree.selection():
            #(row, '#1'), для надурения python
            self.db.cur.execute('''DELETE FROM users WHERE ID=?''',
                                (self.tree.set(row, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод для поиска данных
    def search_records(self, name):
        name =('%'+ name +'%')
        self.db.cur.execute('''SELECT * FROM users WHERE name LIKE ?''', (name, ))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

########################################################################################################### Вызовы классов

    # метод вызывающий окно добавления
    def open_child(self):
        Child()

    # метод вызывающий окно обновления
    def open_update_dialog(self):
        Update()

    # метод вызывающий окно поиска
    def open_search(self):
        Search()

###########################################################################################################
########################################################################################################### класс child

# Создание дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Создание и работа с дочерним окном
    def init_child(self):
        self.title('Добавить контакт')
        self.geometry('400x200')
        # Перехватывает все события происходящие в приложении
        self.grab_set()
        # Захватывает фокус
        self.focus_set()

########################################################################################################### создание окна

        # place расставляет по координатам
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)

        # ttk потому что берем из дерева
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

########################################################################################################### кнопки

        # Кнопка закрытия (ttk b tk неважно, destroy уничтожает окно)
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # Кнопка добавления
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        # Срабатывает только при нажатии на ПКМ (правую кнопку мыши)
        self.btn_add.bind('<Button-1>', lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get()))
###########################################################################################################
########################################################################################################### 

# Класс редактирования контактов
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()
    
        self.btn_upd = ttk.Button(self, text='Редактировать')
        self.btn_upd.bind('<Button-1>', lambda event:
                          self.view.update_record(self.entry_name.get(),
                                                  self.entry_phone.get(),
                                                  self.entry_email.get()))
        # add='+' это разрешение на нажатие второй раз кнопки
        self.btn_upd.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_upd.place(x=200, y=170)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('''SELECT * FROM users WHERE ID=?''', (id, ))

        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])


###########################################################################################################
###########################################################################################################

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view =app

    def init_child(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False,False)
        # Перехватывает все события происходящие в приложении
        self.grab_set()
        # Захватывает фокус
        self.focus_set()

###########################################################################################################
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

###########################################################################################################

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=70)

        # кнопка поиска
        self.btn_search = ttk.Button(self, text='Найти')
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_name.get()))

###########################################################################################################
########################################################################################################### класс DB
# Класс Базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY ,
        name TEXT,
        phone TEXT,
        email TEXT
        )
        ''')
        self.conn.commit()

    def insert_data (self, name, phone, email):
        self.cur.execute(''' INSERT INTO users (name, phone, email)
                        VALUES (?, ?, ?)''', (name, phone, email))
        self.conn.commit()

###########################################################################################################

# Создание окна
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('645x450')
    # Закрепляет размер окна
    root.resizable(False,False)
    root.configure(bg="White")
    root.mainloop()