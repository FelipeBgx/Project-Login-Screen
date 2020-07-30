from tkinter import *
import shelve


class LoginScreen(object):
    def __init__(self, instance):
        # auxiliary variable
        self.mode_checkbutton = False
        # Frames
        self.frame_buttons = Frame(instance)
        # Labels
        self.name = Label(instance, text='Usuário', bg='#91B4FF')
        self.passwd = Label(instance, text='Senha', bg='#91B4FF')
        self.result = Label(instance, pady=5, bg='#91B4FF')
        # Entry's
        self.input_name = Entry(instance)
        self.input_passwd = Entry(instance, show='*')
        # Buttons
        self.button_enter = Button(self.frame_buttons, text='Entrar', command=self.check_database, width=15)
        self.button_register = Button(self.frame_buttons, text='Novo', command=self.register, width=15)
        self.checkbutton_remember = Checkbutton(instance, text='Lembra-me', command=self.remember_user,
                                                width=15, pady=10, bg='#91B4FF')
        # Packaging the widgets
        self.name.pack()
        self.input_name.pack()
        self.passwd.pack()
        self.input_passwd.pack()
        self.button_enter.pack(side=LEFT)
        self.button_register.pack(side=RIGHT)
        self.checkbutton_remember.pack()
        self.frame_buttons.pack()
        self.result.pack()

        self.fill()

    def check_database(self):
        db = shelve.open('shelveDB/datas.db')
        try:
            if self.input_name.get() not in db.keys():
                self.result['text'] = 'Usuário não encontrado!'
                self.result['fg'] = 'red'
            elif self.input_passwd.get() not in db.values():
                self.result['text'] = 'Senha inválida!'
                self.result['fg'] = 'red'
            else:
                if self.mode_checkbutton:
                    remember_login = open('remember login.bin', 'w')
                    remember_login.write(self.input_name.get() + '\n' + self.input_passwd.get())
                    remember_login.close()
                elif not self.mode_checkbutton:
                    remember_login = open('remember login.bin', 'w')
                    remember_login.write('mode remember_me = false')
                    remember_login.close()
                self.result['text'] = 'Seja bem-vindo %s!' % self.input_name.get()
                self.result['fg'] = 'green'
        finally:
            db.close()

    def register(self):
        # Changing widget to demonstrate input from the "creating_new_user" method
        self.input_name.delete(0, 'end')
        self.input_passwd.delete(0, 'end')
        self.name['text'] = 'Insira seu nome'
        self.passwd['text'] = 'Insira sua senha'
        self.button_register['text'] = 'Criar'
        self.result['text'] = 'Criar novo usuário'
        self.result['fg'] = 'black'
        self.button_register['command'] = self.creating_new_user

    def creating_new_user(self):
        db = shelve.open('shelveDB/datas.db')
        try:
            # Creating new user
            if self.input_name.get() in db.keys():
                self.result['text'] = 'Usuário já existe'
                self.result['fg'] = 'red'
            elif len(self.input_name.get()) == 0 or len(self.input_passwd.get()) == 0:
                self.result['text'] = 'Nenhum campo pode estar vazio!'
                self.result['fg'] = 'red'
            else:
                receive_name = self.input_name.get()
                receive_passwd = self.input_passwd.get()
                db[receive_name] = receive_passwd
                # Changing widget to demonstrate leaving the "creating_new_user" method
                self.result['fg'] = 'green'
                self.result['text'] = 'Cadastro realizado com sucesso'
                self.button_register['command'] = self.register
                self.button_register['text'] = 'Novo'
                self.input_passwd.delete(0, 'end')
        finally:
            db.close()

    def remember_user(self):
        self.mode_checkbutton = not self.mode_checkbutton

    def fill(self):
        remember_login = open('remember login.bin')
        datas = []
        for line in remember_login:
            datas.append(line)
        remember_login.close()
        if 'mode remember_me = false' not in datas:
            aux = datas[0].split('\n')
            self.input_name.insert(0, aux[0])
            self.input_passwd.insert(0, datas[1])


screen = Tk()
screen['bg'] = '#91B4FF'
LoginScreen(screen)
screen.title('Login / Register')
screen.geometry('300x200')

screen.mainloop()
