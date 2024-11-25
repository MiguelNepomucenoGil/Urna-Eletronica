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
  
     
        tk.Button(self.root, text="Carregar Eleitores", command=self.carregar_eleitores).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Carregar Candidatos", command=self.carregar_candidatos).grid(row=0, column=1, padx=10, pady=5)

  
        tk.Label(self.root, text="Título do Eleitor:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_titulo = tk.Entry(self.root, width=20)
        self.entry_titulo.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Verificar Eleitor", command=self.verificar_eleitor).grid(row=1, column=2, padx=10, pady=5)

     
        self.label_eleitor = tk.Label(self.root, text="", fg="blue")
        self.label_eleitor.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

 
        tk.Label(self.root, text="Número do Candidato:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_num_candidato = tk.Entry(self.root, width=20)
        self.entry_num_candidato.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Registrar Voto", command=self.registrar_voto).grid(row=3, column=2, padx=10, pady=5)

      
        tk.Button(self.root, text="Voto Branco", command=lambda: self.registrar_voto(branco=True)).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Voto Nulo", command=lambda: self.registrar_voto(nulo=True)).grid(row=4, column=1, padx=10, pady=5)

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


if __name__ == "__main__":
    root = tk.Tk()
    urna = UrnaEletronica(root)
    root.mainloop()
