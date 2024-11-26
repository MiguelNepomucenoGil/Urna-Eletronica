import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import csv
import os

class UrnaEletronica:
    def __init__(self, root):
        self.root = root
        self.root.title("Urna Eletrônica")
        self.eleitores = []
        self.candidatos = []
        self.votos = []
        self.eleitor_atual = None
        self.criar_interface()

    def criar_interface(self):
        botoes = [
            ("Carregar Eleitores", self.carregar_eleitores, 0, 0),
            ("Carregar Candidatos", self.carregar_candidatos, 0, 1),
            ("Verificar Eleitor", self.verificar_eleitor, 1, 2),
            ("Registrar Voto", self.registrar_voto, 3, 2),
            ("Voto Branco", lambda: self.registrar_voto(branco=True), 4, 0),
            ("Voto Nulo", lambda: self.registrar_voto(nulo=True), 4, 1),
        ]

        for texto, comando, row, col in botoes:
            tk.Button(self.root, text=texto, command=comando).grid(row=row, column=col, padx=10, pady=5)

        entradas = [
            ("Título do Eleitor:", 1, 0, self.create_entry("entry_titulo", 1, 1)),
            ("Número do Candidato:", 3, 0, self.create_entry("entry_num_candidato", 3, 1)),
        ]

        for texto, row, col, _ in entradas:
            tk.Label(self.root, text=texto).grid(row=row, column=col, padx=10, pady=5)

        self.label_eleitor = tk.Label(self.root, text="", fg="blue")
        self.label_eleitor.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

    def create_entry(self, var_name, row, col):
        """Método auxiliar para criar entradas e atribuí-las a um atributo."""
        entry = tk.Entry(self.root, width=20)
        setattr(self, var_name, entry)
        entry.grid(row=row, column=col, padx=10, pady=5)
        return entry

    def carregar_arquivo(self):
      
        filepath = filedialog.askopenfilename(filetypes=[("Arquivos .pkl ou .csv", "*.pkl *.csv")])
        if not filepath:
            return None

        ext = os.path.splitext(filepath)[1]
        try:
            if ext == ".pkl":
                with open(filepath, "rb") as f:
                    return pickle.load(f)
            elif ext == ".csv":
                with open(filepath, newline='', encoding='utf-8') as f:
                    return list(csv.DictReader(f))
            else:
                messagebox.showerror("Erro", "Formato de arquivo inválido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar arquivo: {e}")
        return None

    def carregar_eleitores(self):
        """Carrega a lista de eleitores a partir de um arquivo."""
        eleitores = self.carregar_arquivo()
        if eleitores:
            self.eleitores = eleitores
            messagebox.showinfo("Sucesso", "Lista de eleitores carregada com sucesso!")

    def carregar_candidatos(self):
        """Carrega a lista de candidatos a partir de um arquivo."""
        candidatos = self.carregar_arquivo()
        if candidatos:
            self.candidatos = candidatos
            messagebox.showinfo("Sucesso", "Lista de candidatos carregada com sucesso!")

    def verificar_eleitor(self):
        """Verifica se o título do eleitor existe na lista."""
        titulo = self.entry_titulo.get()
        self.eleitor_atual = next((e for e in self.eleitores if e.get("titulo") == titulo), None)
        if self.eleitor_atual:
            self.label_eleitor.config(text=f"Eleitor: {self.eleitor_atual['nome']}")
        else:
            self.label_eleitor.config(text="")
            messagebox.showerror("Erro", "Eleitor não encontrado!")

    def registrar_voto(self, branco=False, nulo=False):
        """Registra o voto do eleitor."""
        if not self.eleitor_atual:
            messagebox.showerror("Erro", "Por favor, verifique o eleitor antes de votar!")
            return

        titulo = self.eleitor_atual["titulo"]
        if branco:
            voto = {"titulo": titulo, "voto": "Branco"}
        elif nulo:
            voto = {"titulo": titulo, "voto": "Nulo"}
        else:
            num_candidato = self.entry_num_candidato.get()
            candidato = next((c for c in self.candidatos if c.get("numero") == num_candidato), None)
            if not candidato:
                messagebox.showerror("Erro", "Candidato não encontrado!")
                return
            voto = {"titulo": titulo, "voto": candidato["nome"]}

        self.votos.append(voto)
        self.salvar_votos()
        messagebox.showinfo("Sucesso", "Voto registrado com sucesso!")
        self.resetar_urna()

    def salvar_votos(self):
        """Salva os votos registrados em um arquivo .pkl."""
        try:
            with open("votos.pkl", "wb") as f:
                pickle.dump(self.votos, f)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar votos: {e}")

    def resetar_urna(self):
        """Reseta os campos da interface para registrar outro voto."""
        self.entry_titulo.delete(0, tk.END)
        self.entry_num_candidato.delete(0, tk.END)
        self.label_eleitor.config(text="")
        self.eleitor_atual = None