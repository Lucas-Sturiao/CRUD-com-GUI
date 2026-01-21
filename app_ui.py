import customtkinter as ctk
from tkinter import messagebox

class AppUI(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        self.db = db # Recebe a conexão com o banco
        
        self.title("Sistema de Inventário Profissional")
        self.geometry("900x600")
        
        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_area()
        self.atualizar_lista()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="CADASTRO", font=("Roboto", 20, "bold")).pack(pady=20)

        self.entry_nome = ctk.CTkEntry(self.sidebar, placeholder_text="Nome do Produto")
        self.entry_nome.pack(pady=10, padx=20, fill="x")

        self.entry_qtd = ctk.CTkEntry(self.sidebar, placeholder_text="Quantidade")
        self.entry_qtd.pack(pady=10, padx=20, fill="x")

        self.entry_preco = ctk.CTkEntry(self.sidebar, placeholder_text="Preço")
        self.entry_preco.pack(pady=10, padx=20, fill="x")

        self.btn_add = ctk.CTkButton(self.sidebar, text="Adicionar", command=self.adicionar)
        self.btn_add.pack(pady=20, padx=20, fill="x")

    def setup_main_area(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Produtos Cadastrados")
        self.scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

    def adicionar(self):
        try:
            nome = self.entry_nome.get()
            qtd = int(self.entry_qtd.get())
            preco = float(self.entry_preco.get())
            
            self.db.inserir(nome, qtd, preco)
            self.atualizar_lista()
            self.limpar_campos()
        except ValueError:
            messagebox.showerror("Erro", "Verifique se Quantidade e Preço são números.")

    def atualizar_lista(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for item in self.db.selecionar_todos():
            self.criar_linha_item(item)

    def criar_linha_item(self, item):
        frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        
        texto = f"ID: {item[0]} | {item[1]} | Qtd: {item[2]} | R$ {item[3]:.2f}"
        ctk.CTkLabel(frame, text=texto).pack(side="left", padx=10)
        
        ctk.CTkButton(frame, text="Excluir", width=60, fg_color="#e74c3c", 
                      command=lambda i=item[0]: self.deletar(i)).pack(side="right", padx=5)

    def deletar(self, id_item):
        self.db.deletar(id_item)
        self.atualizar_lista()

    def limpar_campos(self):
        self.entry_nome.delete(0, 'end')
        self.entry_qtd.delete(0, 'end')
        self.entry_preco.delete(0, 'end')