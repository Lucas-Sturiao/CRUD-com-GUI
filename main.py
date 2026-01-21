from database import Database
from app_ui import AppUI

if __name__ == "__main__":
    # 1. Inicia o Banco de Dados
    db = Database()
    
    # 2. Inicia a Interface passando o banco para ela
    app = AppUI(db)
    
    # 3. Roda o loop principal
    app.mainloop()