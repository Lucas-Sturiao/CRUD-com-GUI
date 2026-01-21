import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- CLASSE PRINCIPAL DA INTERFACE ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Inventário CRUD")
        self.geometry("800x500")
        ctk.set_appearance_mode("dark")

        # Configuração de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRA LATERAL (ENTRADAS) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_titulo = ctk.CTkLabel(self.sidebar, text="GERENCIADOR", font=("Roboto", 20, "bold"))
        self.lbl_titulo.pack(pady=20, padx=10)

        self.entry_nome = ctk.CTkEntry(self.sidebar, placeholder_text="Nome do Produto")
        self.entry_nome.pack(pady=10, padx=20)

        self.entry_qtd = ctk.CTkEntry(self.sidebar, placeholder_text="Quantidade")
        self.entry_qtd.pack(pady=10, padx=20)

        self.entry_preco = ctk.CTkEntry(self.sidebar, placeholder_text="Preço (ex: 10.50)")
        self.entry_preco.pack(pady=10, padx=20)

        self.btn_add = ctk.CTkButton(self.sidebar, text="Adicionar Item", command=self.adicionar_item)
        self.btn_add.pack(pady=20, padx=20)
        
        self.btn_limpar = ctk.CTkButton(self.sidebar, text="Limpar Banco", fg_color="transparent", border_width=1, command=self.limpar_banco)
        self.btn_limpar.pack(pady=10, padx=20)

        # --- ÁREA PRINCIPAL (EXIBIÇÃO) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.lista_label = ctk.CTkLabel(self.main_frame, text="Itens no Inventário", font=("Roboto", 16))
        self.lista_label.pack(pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="ID | Nome | Qtd | Preço")
        self.scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.atualizar_lista()

    # --- LÓGICA DO CRUD ---
    def adicionar_item(self):
        nome = self.entry_nome.get()
        qtd = self.entry_qtd.get()
        preco = self.entry_preco.get()

        if nome and qtd and preco:
            try:
                conn = sqlite3.connect("inventario.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, int(qtd), float(preco)))
                conn.commit()
                conn.close()
                self.atualizar_lista()
                self.entry_nome.delete(0, 'end')
                self.entry_qtd.delete(0, 'end')
                self.entry_preco.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Erro", "Quantidade e Preço devem ser números.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def atualizar_lista(self):
        # Limpa o frame de scroll
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        rows = cursor.fetchall()
        
        for row in rows:
            item_text = f"{row[0]} | {row[1]} | {row[2]} | R$ {row[3]:.2f}"
            frame_item = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            frame_item.pack(fill="x", pady=2)
            
            ctk.CTkLabel(frame_item, text=item_text).pack(side="left", padx=10)
            ctk.CTkButton(frame_item, text="X", width=30, fg_color="#d9534f", hover_color="#c9302c", 
                          command=lambda r=row[0]: self.deletar_item(r)).pack(side="right", padx=5)
        
        conn.close()

    def deletar_item(self, id_item):
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_item,))
        conn.commit()
        conn.close()
        self.atualizar_lista()

    def limpar_banco(self):
        if messagebox.askyesno("Confirmar", "Deseja apagar todos os registros?"):
            conn = sqlite3.connect("inventario.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos")
            conn.commit()
            conn.close()
            self.atualizar_lista()

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()