import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
import sqlite3
from datetime import datetime
from utils.helpers import (
    formatar_tempo,
    validar_receita,
    formatar_ingredientes,
    formatar_modo_preparo,
    calcular_tempo_leitura
)

class ReceitasApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Receitas Deliciosas")
        self.geometry("1100x700")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.cor_primaria = "#1f538d"
        self.cor_secundaria = "#2d7dd2"
        self.cor_accent = "#45b7d1"
        self.cor_erro = "#ff3333"
        self.cor_sucesso = "#00cc66"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0,
                                        fg_color=self.cor_primaria)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="🍳\nReceitas\nDeliciosas",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.home_button = ctk.CTkButton(
            self.sidebar_frame,
            text="  🏠  Início",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color="white",
            hover_color=self.cor_secundaria,
            anchor="w",
            command=self.home_button_event
        )
        self.home_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.add_recipe_button = ctk.CTkButton(
            self.sidebar_frame,
            text="  ➕  Nova Receita",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color="white",
            hover_color=self.cor_secundaria,
            anchor="w",
            command=self.add_recipe_event
        )
        self.add_recipe_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.favorites_button = ctk.CTkButton(
            self.sidebar_frame,
            text="  ⭐  Favoritos",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color="white",
            hover_color=self.cor_secundaria,
            anchor="w",
            command=self.favorites_event
        )
        self.favorites_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Pesquisar receitas...",
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=20
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Buscar",
            height=40,
            corner_radius=20,
            font=ctk.CTkFont(size=14),
            fg_color=self.cor_accent,
            hover_color=self.cor_secundaria,
            command=self.search_event
        )
        self.search_button.pack(side="right")

        self.content_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
        self.init_database()
        
        self.show_home()

    def init_database(self):
        """Inicializa o banco de dados e cria a estrutura necessária."""

        os.makedirs('app/data', exist_ok=True)
        

        conn = sqlite3.connect('app/data/receitas.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            modo_preparo TEXT NOT NULL,
            tempo_preparo INTEGER,
            porcoes INTEGER,
            favorito INTEGER DEFAULT 0,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()

    def home_button_event(self):
        self.show_home()

    def add_recipe_event(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()


        form_frame = ctk.CTkFrame(
            self.content_frame,
            corner_radius=15,
            fg_color=self.cor_primaria
        )
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)


        ctk.CTkLabel(
            form_frame,
            text="✨ Nova Receita",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

 
        nome_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Nome da receita",
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=20
        )
        nome_entry.pack(fill="x", padx=20, pady=10)


        ctk.CTkLabel(
            form_frame,
            text="🥗 Ingredientes (um por linha):",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10,0))

        ingredientes_text = ctk.CTkTextbox(
            form_frame,
            height=120,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        ingredientes_text.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            form_frame,
            text="👩‍🍳 Modo de Preparo (um passo por linha):",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10,0))

        modo_preparo_text = ctk.CTkTextbox(
            form_frame,
            height=150,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        modo_preparo_text.pack(fill="x", padx=20, pady=5)

        info_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)

        tempo_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        tempo_frame.pack(side="left", fill="x", expand=True, padx=(0,10))

        ctk.CTkLabel(
            tempo_frame,
            text="⏱️ Tempo de Preparo (min):",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0,10))

        tempo_entry = ctk.CTkEntry(
            tempo_frame,
            width=100,
            height=40,
            corner_radius=20
        )
        tempo_entry.pack(side="left")

        porcoes_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        porcoes_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            porcoes_frame,
            text="👥 Porções:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0,10))

        porcoes_entry = ctk.CTkEntry(
            porcoes_frame,
            width=100,
            height=40,
            corner_radius=20
        )
        porcoes_entry.pack(side="left")

        erro_label = ctk.CTkLabel(
            form_frame,
            text="",
            text_color=self.cor_erro,
            font=ctk.CTkFont(size=14)
        )
        erro_label.pack(pady=5)

        def salvar_receita():
            nome = nome_entry.get()
            ingredientes = ingredientes_text.get("1.0", tk.END)
            modo_preparo = modo_preparo_text.get("1.0", tk.END)
            tempo = tempo_entry.get()
            porcoes = porcoes_entry.get()

            erros = validar_receita(nome, ingredientes, modo_preparo, tempo, porcoes)
            
            if erros:
                erro_label.configure(text="\n".join(erros))
                return

            ingredientes_formatado = formatar_ingredientes(ingredientes)
            modo_preparo_formatado = formatar_modo_preparo(modo_preparo)

            conn = sqlite3.connect('app/data/receitas.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO receitas (nome, ingredientes, modo_preparo, tempo_preparo, porcoes)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                nome.strip(),
                ingredientes_formatado,
                modo_preparo_formatado,
                int(tempo),
                int(porcoes)
            ))
            conn.commit()
            conn.close()
            self.show_home()

        botoes_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        botoes_frame.pack(pady=20)


        ctk.CTkButton(
            botoes_frame,
            text="Cancelar",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_color=self.cor_secundaria,
            border_width=2,
            hover_color=self.cor_secundaria,
            height=40,
            width=120,
            corner_radius=20,
            command=self.show_home
        ).pack(side="left", padx=5)


        ctk.CTkButton(
            botoes_frame,
            text="✓ Salvar Receita",
            font=ctk.CTkFont(size=14),
            fg_color=self.cor_sucesso,
            hover_color="#00994d",
            height=40,
            width=120,
            corner_radius=20,
            command=salvar_receita
        ).pack(side="left", padx=5)

    def favorites_event(self):
        self.show_recipes(apenas_favoritos=True)

    def search_event(self):
        termo_busca = self.search_entry.get()
        self.show_recipes(termo_busca=termo_busca)

    def show_home(self):
        self.show_recipes()

    def show_recipes(self, termo_busca=None, apenas_favoritos=False):

        for widget in self.content_frame.winfo_children():
            widget.destroy()


        conn = sqlite3.connect('app/data/receitas.db')
        cursor = conn.cursor()


        query = "SELECT * FROM receitas"
        params = []
        if apenas_favoritos:
            query += " WHERE favorito = 1"
        if termo_busca:
            if "WHERE" in query:
                query += " AND"
            else:
                query += " WHERE"
            query += " nome LIKE ?"
            params.append(f"%{termo_busca}%")
        query += " ORDER BY data_criacao DESC"

        cursor.execute(query, params)
        receitas = cursor.fetchall()

        if not receitas:
            ctk.CTkLabel(self.content_frame, 
                        text="Nenhuma receita encontrada!",
                        font=ctk.CTkFont(size=16)).pack(pady=20)
        else:
            for receita in receitas:
                self.criar_card_receita(receita)

        conn.close()

    def ver_detalhes_receita(self, receita_id):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('app/data/receitas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receitas WHERE id = ?", (receita_id,))
        receita = cursor.fetchone()
        conn.close()

        if not receita:
            return

        detalhes_frame = ctk.CTkFrame(
            self.content_frame,
            corner_radius=15,
            fg_color=self.cor_primaria
        )
        detalhes_frame.pack(fill="both", expand=True, padx=20, pady=10)

        header_frame = ctk.CTkFrame(detalhes_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        titulo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        titulo_frame.pack(side="left")

        ctk.CTkLabel(
            titulo_frame,
            text="📖",
            font=ctk.CTkFont(size=28)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            titulo_frame,
            text=receita[1],
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(side="left")

        botoes_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        botoes_frame.pack(side="right")

        ctk.CTkButton(
            botoes_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=14),
            fg_color=self.cor_secundaria,
            hover_color=self.cor_accent,
            height=35,
            corner_radius=17,
            command=self.show_home
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botoes_frame,
            text="🗑️ Remover Receita",
            font=ctk.CTkFont(size=14),
            fg_color=self.cor_erro,
            hover_color="#cc0000",
            height=35,
            corner_radius=17,
            command=lambda: self.remover_receita(receita[0], receita[1])
        ).pack(side="left", padx=5)

        info_container = ctk.CTkFrame(detalhes_frame, fg_color="transparent")
        info_container.pack(fill="x", padx=20, pady=10)

        tempo_card = ctk.CTkFrame(
            info_container,
            corner_radius=10,
            fg_color=self.cor_secundaria
        )
        tempo_card.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(
            tempo_card,
            text="⏱️",
            font=ctk.CTkFont(size=20)
        ).pack(pady=(10,0))

        ctk.CTkLabel(
            tempo_card,
            text=formatar_tempo(receita[4]),
            font=ctk.CTkFont(size=14)
        ).pack(padx=15, pady=10)

        porcoes_card = ctk.CTkFrame(
            info_container,
            corner_radius=10,
            fg_color=self.cor_secundaria
        )
        porcoes_card.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(
            porcoes_card,
            text="👥",
            font=ctk.CTkFont(size=20)
        ).pack(pady=(10,0))

        ctk.CTkLabel(
            porcoes_card,
            text=f"{receita[5]} porções",
            font=ctk.CTkFont(size=14)
        ).pack(padx=15, pady=10)

        fav_card = ctk.CTkFrame(
            info_container,
            corner_radius=10,
            fg_color=self.cor_secundaria
        )
        fav_card.pack(side="left", padx=5, pady=5)

        fav_icon = "⭐" if receita[6] == 1 else "☆"
        ctk.CTkLabel(
            fav_card,
            text=fav_icon,
            font=ctk.CTkFont(size=20)
        ).pack(pady=(10,0))

        fav_status = "Favorita" if receita[6] == 1 else "Não favorita"
        ctk.CTkLabel(
            fav_card,
            text=fav_status,
            font=ctk.CTkFont(size=14)
        ).pack(padx=15, pady=10)

        # Card de tempo de leitura
        leitura_card = ctk.CTkFrame(
            info_container,
            corner_radius=10,
            fg_color=self.cor_secundaria
        )
        leitura_card.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(
            leitura_card,
            text="📚",
            font=ctk.CTkFont(size=20)
        ).pack(pady=(10,0))

        tempo_leitura = calcular_tempo_leitura(receita[3])
        ctk.CTkLabel(
            leitura_card,
            text=tempo_leitura,
            font=ctk.CTkFont(size=14)
        ).pack(padx=15, pady=10)

        # Seção de ingredientes
        ingredientes_frame = ctk.CTkFrame(
            detalhes_frame,
            corner_radius=10,
            fg_color=self.cor_secundaria
        )
        ingredientes_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            ingredientes_frame,
            text="🥗 Ingredientes",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        ingredientes_text = ctk.CTkTextbox(
            ingredientes_frame,
            height=120,
            font=ctk.CTkFont(size=14),
            fg_color="transparent"
        )
        ingredientes_text.pack(fill="x", padx=15, pady=(0,10))
        ingredientes_text.insert("1.0", receita[2])
        ingredientes_text.configure(state="disabled")

        preparo_frame = ctk.CTkFrame(
            detalhes_frame,
            corner_radius=10,
            fg_color=self.cor_secundaria
        )
        preparo_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            preparo_frame,
            text="👩‍🍳 Modo de Preparo",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        preparo_text = ctk.CTkTextbox(
            preparo_frame,
            font=ctk.CTkFont(size=14),
            fg_color="transparent"
        )
        preparo_text.pack(fill="both", expand=True, padx=15, pady=(0,10))
        preparo_text.insert("1.0", receita[3])
        preparo_text.configure(state="disabled")

    def criar_card_receita(self, receita):

        card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=10,
            fg_color=self.cor_primaria,
            border_width=0
        )
        card.pack(fill="x", padx=10, pady=8)


        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)


        ctk.CTkLabel(
            content_frame,
            text=receita[1],
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        ).pack(anchor="w")


        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=(5, 10))

        ctk.CTkLabel(
            info_frame,
            text=f"⏱️ {formatar_tempo(receita[4])}",
            font=ctk.CTkFont(size=13),
            text_color="white"
        ).pack(side="left", padx=(0, 15))

        ctk.CTkLabel(
            info_frame,
            text=f"👥 {receita[5]} porções",
            font=ctk.CTkFont(size=13),
            text_color="white"
        ).pack(side="left")


        botoes_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        botoes_frame.pack(fill="x")


        fav_icon = "⭐" if receita[6] == 1 else "☆"
        fav_text = "Remover dos Favoritos" if receita[6] == 1 else "Adicionar aos Favoritos"
        
        ctk.CTkButton(
            botoes_frame,
            text=f"{fav_icon} {fav_text}",
            font=ctk.CTkFont(size=13),
            fg_color=self.cor_secundaria,
            hover_color=self.cor_accent,
            height=32,
            corner_radius=16,
            command=lambda: self.toggle_favorito(receita[0])
        ).pack(side="left", padx=(0, 5))


        ctk.CTkButton(
            botoes_frame,
            text="👁️ Ver Detalhes",
            font=ctk.CTkFont(size=13),
            fg_color=self.cor_secundaria,
            hover_color=self.cor_accent,
            height=32,
            corner_radius=16,
            command=lambda: self.ver_detalhes_receita(receita[0])
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botoes_frame,
            text="🗑️",
            width=32,
            height=32,
            corner_radius=16,
            font=ctk.CTkFont(size=13),
            fg_color=self.cor_erro,
            hover_color="#cc0000",
            command=lambda: self.remover_receita(receita[0], receita[1])
        ).pack(side="right")

    def toggle_favorito(self, receita_id):
        conn = sqlite3.connect('app/data/receitas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT favorito FROM receitas WHERE id = ?", (receita_id,))
        favorito_atual = cursor.fetchone()[0]
        novo_status = 1 if favorito_atual == 0 else 0
        cursor.execute("UPDATE receitas SET favorito = ? WHERE id = ?",
                     (novo_status, receita_id))
        conn.commit()
        conn.close()
        self.show_recipes()

    def remover_receita(self, receita_id, nome_receita):
        if self.confirmar_remocao(nome_receita):
            conn = sqlite3.connect('app/data/receitas.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM receitas WHERE id = ?", (receita_id,))
            conn.commit()
            conn.close()
            self.show_home()

    def confirmar_remocao(self, nome_receita):
        dialog = ctk.CTkInputDialog(
            text=f"Digite 'CONFIRMAR' para remover a receita\n'{nome_receita}':",
            title="Confirmar Remoção",
            fg_color=self.cor_primaria,
            button_fg_color=self.cor_erro,
            button_hover_color="#cc0000"
        )
        resultado = dialog.get_input()
        return resultado == "CONFIRMAR"

if __name__ == "__main__":
    app = ReceitasApp()
    app.mainloop() 