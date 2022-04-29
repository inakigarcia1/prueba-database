from tkinter import *
import sqlite3 as sql
from tkinter.messagebox import *


class Login:
    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.interfaz.title('Login page')
        self.interfaz.resizable(False, False)
        self.widgets()

    def widgets(self):
        title = Label(self.interfaz, text='Introduzca usuario y contraseña', pady=10, padx=50)
        title.grid(row=0, column=0, columnspan=2)

        user_label = Label(self.interfaz, text='Usuario:', pady=20, padx=15)
        user_label.grid(row=1, column=0)

        user_box = Entry(self.interfaz, width=25)
        user_box.grid(row=1, column=1)

        password_label = Label(self.interfaz, text='Contraseña:', pady=20, padx=15)
        password_label.grid(row=2, column=0)

        password_box = Entry(self.interfaz, width=25, show='*')
        password_box.grid(row=2, column=1)

        login_button = Button(self.interfaz, text='Ingresar', pady=10, padx=100,
                              command=lambda: self.check_login(user_box.get(), password_box.get()))
        login_button.grid(row=3, column=0, columnspan=2)

        register_button_login = Button(self.interfaz, text='Registrarse',
                                       pady=10, padx=100, command=self.go_to_register)
        register_button_login.grid(row=4, column=0, columnspan=2)

    def go_to_register(self):
        root2 = Toplevel(self.interfaz)
        root2.grab_set()
        Registrar(root2)

    @staticmethod
    def check_login(username, password):
        if username != '' and password != '':
            conn = sql.connect('sqlite/users.db')
            cursor = conn.cursor()
            instruction = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            cursor.execute(instruction)
            login_info = cursor.fetchall()
            conn.commit()
            conn.close()
            if not login_info:
                showerror(title='Error',
                          message='Usuario no encontrado')
            else:
                showinfo(title='Login',
                         message='Se ha logeado correctamente')
        else:
            showerror(title='Error',
                      message='Uno de los campos se encuentra vacio')


class Registrar:
    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.interfaz.title('Register page')
        self.interfaz.resizable(False, False)
        self.widgets()

    def widgets(self):
        title = Label(self.interfaz, text='Introduzca usuario y contraseña para registrarse', pady=10, padx=50)
        title.grid(row=0, column=0, columnspan=2)

        user_label = Label(self.interfaz, text='Usuario:', pady=20, padx=15)
        user_label.grid(row=1, column=0)

        user_box = Entry(self.interfaz, width=25)
        user_box.grid(row=1, column=1)

        password_label = Label(self.interfaz, text='Contraseña:', pady=20, padx=15)
        password_label.grid(row=2, column=0)

        self.password_box = Entry(self.interfaz, width=25, show='*')
        self.password_box.grid(row=2, column=1)

        password_label = Label(self.interfaz, text='Confirmar contraseña:', pady=20, padx=15)
        password_label.grid(row=3, column=0)

        self.password_box_confirm = Entry(self.interfaz, width=25, show='*')
        self.password_box_confirm.grid(row=3, column=1)

        register_confirm_button = Button(self.interfaz, text='Registrarse',
                                         pady=10, padx=100,
                                         command=lambda: self.add_user(user_box.get(), self.password_box.get()))
        register_confirm_button.grid(row=4, column=0, columnspan=2)

    def add_user(self, username, password):
        if password == self.password_box_confirm.get():
            if username != '':
                if password == '' and self.password_box_confirm.get() == '':
                    showerror(title='Error',
                              message='Hay uno o mas campos de contraseña vacíos')
                else:
                    conn = sql.connect('sqlite/users.db')
                    cursor = conn.cursor()
                    instruction = f"INSERT INTO users VALUES (Null, '{username}', '{password}')"
                    cursor.execute(instruction)
                    conn.commit()
                    conn.close()
                    showinfo(title='Registro',
                             message='Se ha registrado correctamente, puede logearse.')
                    self.interfaz.destroy()
            else:
                showerror(title='Error',
                          message='El usuario no puede estar vacio.')
        else:
            showerror(title='Error',
                      message='Las contraseñas no coinciden')


main_window = Login(Tk())

main_window.interfaz.mainloop()
