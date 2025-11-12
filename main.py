import customtkinter as ctk
import sqlite3

conec = sqlite3.connect("list.db")
db = conec.cursor()

db.execute('''
CREATE TABLE IF NOT EXISTS lista (
    dia INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(30),
    horas VARCHAR(6),
    descricao VARCHAR(100)
    )
''')

conec.commit()

#funções


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x250")
        self.title("Diario de atividades")
        self.grid_anchor("center")
        self.grid_rowconfigure((1,2,3), weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.configure(fg_color="#F2DE00")
        self.overrideredirect(True)
        self.resizable(False, False)


        #funções
        self.offset_x = 0
        self.offset_y = 0

        def quantia_atv():
            db.execute('SELECT COUNT(*) FROM lista')
            valores_alunos = db.fetchone()

            self.dias_cont.configure(text=str(valores_alunos[0]))
            self.after(10000, quantia_atv)

        def start(event):
            self.offset_x = event.x
            self.offset_y = event.y

        def move(event):
            x = event.x_root - self.offset_x
            y = event.y_root - self.offset_y
            self.geometry(f"+{x}+{y}")

        def tabela():

            self.tabela = ctk.CTkToplevel(self)
            self.tabela.geometry("400x350")
            self.tabela.configure(fg_color="#F2DE00")
            self.tabela.columnconfigure(0, weight=1)
            self.tabela.rowconfigure((1,2,3), weight=1)
            self.tabela.overrideredirect(True)
            self.tabela.resizable(False, False)

            #funções
            def start_list(event):
                self.offset_x = event.x
                self.offset_y = event.y

            def move_list(event):
                x = event.x_root - self.offset_x
                y = event.y_root - self.offset_y
                self.tabela.geometry(f'+{x}+{y}')

            def add():

                def salvar():
                    nome = self.entry_nome.get()
                    descricao = self.entry_desc.get()
                    horario = self.entry_horario.get()
                    self.adic.destroy()

                    def start_conf(event):
                        self.msg_confir.offset_x = event.x
                        self.msg_confir.offset_y = event.y

                    def move_conf(event):
                        x = event.x_root - self.msg_confir.offset_x
                        y = event.y_root - self.msg_confir.offset_y
                        self.msg_confir.geometry(f'+{x}+{y}')

                    if nome == "":
                        print("erro")

                    elif descricao == "":
                        print("erro")

                    elif horario == "":
                       print("erro")
                    else:
                        try:
                            db.execute('''INSERT INTO lista (nome,horas,descricao) VALUES (?,?,?)''', (nome, horario, descricao))
                            conec.commit()

                            self.msg_confir = ctk.CTkToplevel(self)
                            self.msg_confir.geometry("245x150")
                            self.msg_confir.configure(fg_color="#F2DE00")
                            self.tabela.columnconfigure(0, weight=1)
                            self.tabela.rowconfigure((1, 2, 3), weight=1)
                            self.msg_confir.resizable(False, False)
                            self.msg_confir.overrideredirect(True)

                            self.titulo_3 = ctk.CTkFrame(self.msg_confir, fg_color="#474300", corner_radius=0,height=10)
                            self.titulo_label_3 = ctk.CTkLabel(self.titulo_3, text="Confirmação",text_color="#ffffff", font=("Press Start 2P", 7))
                            self.titulo_btn_3 = ctk.CTkButton(self.titulo_3, text="X",font=("Press Start 2P", 7), width=20, height=10,fg_color="#474300", text_color="#ffffff",command=self.msg_confir.destroy)

                            self.titulo_3.bind("<Button-1>", start_conf)
                            self.titulo_3.bind("<B1-Motion>", move_conf)

                            self.titulo_3.grid(row=1, column=0, sticky="new")
                            self.titulo_label_3.pack(side="left", padx=70, pady=5)
                            self.titulo_btn_3.pack(side="right", padx=5, pady=5)

                            self.msg = ctk.CTkLabel(self.msg_confir, font=("Press Start 2P", 13), text_color="#000000",text="Adição feita")
                            self.destroy = ctk.CTkButton(self.msg_confir, text="Fechar",font=("Press Start 2P", 10), width=50, height=30,text_color="#000000",fg_color="#F2DE00",corner_radius=0, border_width=2, border_color="#000000",command=self.msg_confir.destroy,)

                            self.msg.grid(row=2,column=0, padx=10, pady=10)
                            self.destroy.grid(row=3,column=0, padx=10, pady=10)
                            self.tabela.destroy()
                            tabela()
                            return None
                        except sqlite3.Error:
                            print("erro")
                            return None



                self.adic = ctk.CTkToplevel(self.tabela)
                self.adic.geometry("400x300")
                self.adic.configure(fg_color="#F2DE00")
                self.adic.columnconfigure(1, weight=1)
                self.adic.rowconfigure(1, weight=1)
                self.adic.resizable(False, False)

                self.titulo_4 = ctk.CTkFrame(self.adic, fg_color="#474300", corner_radius=0, height=10)
                self.titulo_label_4 = ctk.CTkLabel(self.titulo_4, text="Adição de atividade", text_color="#ffffff", font=("Press Start 2P", 9))
                self.titulo_btn_4 = ctk.CTkButton(self.titulo_4, font=("Press Start 2P", 9), text="X", width=20, height=10, fg_color="#474300",text_color="#ffffff", command=self.adic.destroy)

                self.titulo_4.grid(row=1, column=1, sticky="new")
                self.titulo_label_4.pack(side="left", padx=70, pady=5)
                self.titulo_btn_4.pack(side="right", padx=5, pady=5)

                self.label_nome = ctk.CTkLabel(self.adic, font=("Press Start 2P", 9), text_color="#000000",text="Coloque o nome:")
                self.entry_nome = ctk.CTkEntry(self.adic, font=("Press Start 2P", 9),fg_color="#F2DE00" ,text_color="#000000", width=150, height=30,corner_radius=0,border_width=2, border_color="#000000")

                self.label_horario = ctk.CTkLabel(self.adic, font=("Press Start 2P", 9), text_color="#000000",text="Coloque a quantia do tempo:")
                self.entry_horario = ctk.CTkEntry(self.adic, font=("Press Start 2P", 9),fg_color="#F2DE00" ,text_color="#000000", width=150, height=30,corner_radius=0,border_width=2, border_color="#000000")

                self.label_descricao = ctk.CTkLabel(self.adic, font=("Press Start 2P", 9), text_color="#000000",text="Coloque a descrição:")
                self.entry_desc = ctk.CTkEntry(self.adic, font=("Press Start 2P", 9),fg_color="#F2DE00",corner_radius=0,border_width=2, border_color="#000000", text_color="#000000",width=150, height=30)

                self.enviar = ctk.CTkButton(self.adic, width=100, height=30, text="Enviar",font=("Press Start 2P", 10),fg_color="#F2DE00", text_color="#000000", border_width=2,corner_radius=0,border_color="#000000", command=lambda: salvar())
                self.enviar.grid(row=8, column=1, padx=10, pady=10)

                self.label_nome.grid(row=2, column=1, padx=10, pady=0)
                self.entry_nome.grid(row=3, column=1, padx=10, pady=0)
                self.label_horario.grid(row=4, column=1, padx=10, pady=0)
                self.entry_horario.grid(row=5, column=1, padx=10, pady=0)
                self.label_descricao.grid(row=6, column=1, padx=10, pady=0)
                self.entry_desc.grid(row=7, column=1, padx=10, pady=0)
                self.entry_nome.focus_force()
                return None

            def minimizar_2():
                if not hasattr(self.tabela, '_minimizado'):
                    self.tabela._minimizado = False

                if self.tabela._minimizado:
                    self.tabela_list.grid(row=2, column=0, padx=30, pady=30)
                    self.destroy_tabela.grid(row=3, column=0, padx=10, pady=10, sticky="w")
                    self.edit_tabela.grid(row=3, column=0, padx=10, pady=10, sticky="s")
                    self.add_tabela.grid(row=3, column=0, padx=10, pady=10, sticky="e")
                    self.tabela.geometry("400x300")
                    self.tabela._minimizado = False
                else:
                    self.tabela_list.grid_forget()
                    self.destroy_tabela.grid_forget()
                    self.edit_tabela.grid_forget()
                    self.add_tabela.grid_forget()
                    self.tabela.geometry("400x32")
                    self.tabela._minimizado = True

            #titulo
            self.titulo_2 = ctk.CTkFrame(self.tabela, fg_color="#474300", corner_radius=0, height=10)
            self.titulo_label_2 = ctk.CTkLabel(self.titulo_2, text="Atividades feitas",font=("Press Start 2P", 9), text_color="#ffffff")
            self.titulo_btn_2 = ctk.CTkButton(self.titulo_2, text="X",font=("Press Start 2P", 9), width=20, height=10, fg_color="#474300",text_color="#ffffff", command=self.tabela.destroy)
            self.titulo_min_2 = ctk.CTkButton(self.titulo_2, text="-", font=("Press Start 2P", 11), width=20, height=10,fg_color="#474300", text_color="#ffffff", command=minimizar_2)

            self.titulo_min_2.place(x=340, y=10)
            self.titulo_2.grid(row=1, column=0, sticky="new")
            self.titulo_label_2.pack(side="left", padx=70, pady=5)
            self.titulo_btn_2.pack(side="right", padx=5, pady=5)

            self.titulo_2.bind("<Button-1>", start_list)
            self.titulo_2.bind("<B1-Motion>", move_list)

            #Tabela e btns
            self.tabela_list = ctk.CTkTextbox(self.tabela, width=350, height=150, font=("Press Start 2P", 8),text_color="#000000", fg_color="#F2DE00",corner_radius=0 ,border_width=2 ,border_color="#000000")

            self.destroy_tabela = ctk.CTkButton(self.tabela, width= 50, height= 30, text="<-",font=("Press Start 2P", 10),text_color="#000000", fg_color="#F2DE00",corner_radius=0 ,border_width=2, border_color="#000000", command=self.tabela.destroy)
            self.add_tabela = ctk.CTkButton(self.tabela, width= 50, height= 30, text="+",font=("Press Start 2P", 10),text_color="#000000", fg_color="#F2DE00",corner_radius=0 ,border_width=2, border_color="#000000", command=add)
            self.edit_tabela = ctk.CTkButton(self.tabela, width=50, height=30, text="e",font=("Press Start 2P", 10), text_color="#000000", fg_color="#F2DE00",corner_radius=0 , border_width=2, border_color="#000000")

            self.tabela_list.grid(row=2, column=0, padx=30, pady=30)

            self.destroy_tabela.grid(row=3, column=0, padx=10, pady=10, sticky="w")
            self.edit_tabela.grid(row=3, column=0,padx=10, pady=(20,0), sticky="n")
            self.add_tabela.grid(row=3, column=0, padx=10, pady=10, sticky="e")

            db.execute('SELECT * FROM lista')
            valores_alunos = db.fetchall()

            self.tabela_list.configure(state="normal")
            texto_formatado = ""
            for aluno in valores_alunos:
                linha = "         |   ".join(str(campo) for campo in aluno) + "\n"
                texto_formatado += linha
            self.tabela_list.insert("end", texto_formatado)
            (self.tabela_list.configure(state="disabled"))

            return None

        def minimizar():
            if not hasattr(self, '_minimizado'):
                self._minimizado = False

            if self._minimizado:
                self.geometry("400x250")
                self._minimizado = False
            else:
                self.geometry("400x32")
                self._minimizado = True



        #titulo
        self.titulo = ctk.CTkFrame(self, fg_color="#474300", corner_radius= 0, height= 10 )
        self.titulo_label = ctk.CTkLabel(self.titulo,text="Diario de atividades", text_color="#ffffff", font=("Press Start 2P", 9) )
        self.titulo_btn = ctk.CTkButton(self.titulo,text="X",font=("Press Start 2P", 9),width=20, height=10, fg_color="#474300", text_color="#ffffff", command=self.destroy)
        self.titulo_min = ctk.CTkButton(self.titulo,text="_",font=("Press Start 2P", 11),width=20, height=10, fg_color="#474300", text_color="#ffffff", command=minimizar)



        self.titulo.grid(row=1, column=1, sticky="new")
        self.titulo_label.pack(side="left", padx=70, pady=5)
        self.titulo_min.place(x= 340, y=10)
        self.titulo_btn.pack(side="right", padx=5, pady=5)

        self.titulo.bind("<Button-1>", start)
        self.titulo.bind("<B1-Motion>", move)

        #frame de mostrar os dias
        self.dias = ctk.CTkFrame(self, fg_color="#F2DE00", corner_radius= 0, height= 30, width= 40, border_width = 2, border_color= "#000000")
        self.dias_cont = ctk.CTkLabel(self.dias, text="001", text_color="#000000", font=("Press Start 2P" , 13), height= 30, width= 40)
        self.to_do = ctk.CTkLabel(self, text="TO DO", text_color="#000000", font=("Press Start 2P", 15), height= 30, width= 60)

        self.dias.grid(row=1, column=1, padx= 20, pady=50, sticky="e")
        self.dias_cont.pack(side="top", padx=5, pady=5)
        self.to_do.grid(row=1, column=1, padx= 10, pady=30, sticky="w")

        #Frase
        self.frase = ctk.CTkLabel(self, text="Hoje vc vai conseguir fazer aquele APP!!!", text_color="#000000", font=("Press Start 2P", 15),width=200, wraplength=200)
        self.frase.place(x=100 , y=130 )

        #Btn para tabela
        self.btn_tabela = ctk.CTkButton(self, text="Atividades",font=("Press Start 2P", 15), width=180, height=30,corner_radius=0,border_width=2, border_color="#000000", fg_color="#F2DE00", text_color="#000000", command=tabela)
        self.btn_tabela.grid(row=3, column=1, padx=5, pady=5, sticky="s")


        quantia_atv()

if __name__ == "__main__":
    app = App()
    app.mainloop()