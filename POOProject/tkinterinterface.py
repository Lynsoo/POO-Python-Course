import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

class BibliothequeDB:
    def __init__(self, db_name="bibliotheque.db"):
        self.db_name = db_name
        self.creer_table()

    def connexion(self):
        return sqlite3.connect(self.db_name)

    def creer_table(self):
        db = self.connexion()
        cur = db.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                annee INTEGER,
                disponible TEXT DEFAULT 'Oui'
            )
        """)
        db.commit()
        db.close()

    def ajouter_livre(self, titre, auteur, annee):
        db = self.connexion()
        cur = db.cursor()
        cur.execute("INSERT INTO livres (titre, auteur, annee) VALUES (?, ?, ?)", (titre, auteur, annee))
        db.commit()
        db.close()

    def supprimer_livre(self, id_livre):
        db = self.connexion()
        cur = db.cursor()
        cur.execute("DELETE FROM livres WHERE id=?", (id_livre,))
        db.commit()
        db.close()

    def modifier_livre(self, id_livre, titre, auteur, annee):
        db = self.connexion()
        cur = db.cursor()
        cur.execute("UPDATE livres SET titre=?, auteur=?, annee=? WHERE id=?", (titre, auteur, annee, id_livre))
        db.commit()
        db.close()

    def recuperer_livres(self):
        db = self.connexion()
        cur = db.cursor()
        cur.execute("SELECT * FROM livres")
        rows = cur.fetchall()
        db.close()
        return rows

    def emprunter_livre(self, id_livre):
        db = self.connexion()
        cur = db.cursor()
        cur.execute("SELECT disponible FROM livres WHERE id=?", (id_livre,))
        dispo = cur.fetchone()
        if dispo and dispo[0] == "Oui":
            cur.execute("UPDATE livres SET disponible='Non' WHERE id=?", (id_livre,))
            db.commit()
            resultat = True
        else:
            resultat = False
        db.close()
        return resultat

    def rendre_livre(self, id_livre):
        db = self.connexion()
        cur = db.cursor()
        cur.execute("UPDATE livres SET disponible='Oui' WHERE id=?", (id_livre,))
        db.commit()
        db.close()


class BibliothequeApp:
    def __init__(self, root):
        self.db = BibliothequeDB()
        self.root = root
        self.root.title("📚 Gestion de Bibliothèque")
        self.root.geometry("950x700")
        self.root.configure(bg="#E8F5E9")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#4CAF50", foreground="white")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="#FAFAFA", fieldbackground="#FAFAFA")
        self.style.map("Treeview", background=[("selected", "#81C784")])
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, relief="flat")
        self.style.map("TButton", background=[("active", "#66BB6A")], foreground=[("active", "white")])

        self.colors = ["#FFCDD2", "#F8BBD0", "#E1BEE7", "#D1C4E9", "#BBDEFB", "#B2EBF2", "#C8E6C9", "#FFF9C4", "#FFECB3", "#FFE0B2"]
        self.creer_widgets()
        self.afficher_livres()

    def creer_widgets(self):
        header = tk.Label(self.root, text="📖 Gestion de la Bibliothèque", font=("Segoe UI", 22, "bold"),
                          bg=random.choice(self.colors), fg="#2E7D32", pady=10)
        header.pack(fill="x", pady=(0, 10))

        frame_form = tk.LabelFrame(self.root, text="Détails du livre", bg="#E8F5E9", font=("Segoe UI", 12, "bold"),
                                   fg="#1B5E20", bd=3, labelanchor="n", padx=10, pady=10)
        frame_form.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_form, text="Titre :", bg="#E8F5E9", font=("Segoe UI", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_titre = ttk.Entry(frame_form, width=50)
        self.entry_titre.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Auteur :", bg="#E8F5E9", font=("Segoe UI", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_auteur = ttk.Entry(frame_form, width=50)
        self.entry_auteur.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Année :", bg="#E8F5E9", font=("Segoe UI", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_annee = ttk.Entry(frame_form, width=50)
        self.entry_annee.grid(row=2, column=1, padx=10, pady=5)

        frame_btn = tk.Frame(self.root, bg="#E8F5E9")
        frame_btn.pack(pady=15)

        btn_ajouter = ttk.Button(frame_btn, text="➕ Ajouter", command=self.ajouter_livre)
        btn_modifier = ttk.Button(frame_btn, text="✏️ Modifier", command=self.modifier_livre)
        btn_supprimer = ttk.Button(frame_btn, text="🗑️ Supprimer", command=self.supprimer_livre)
        btn_emprunter = ttk.Button(frame_btn, text="📕 Emprunter", command=self.emprunter_livre)
        btn_rendre = ttk.Button(frame_btn, text="📗 Rendre", command=self.rendre_livre)
        btn_actualiser = ttk.Button(frame_btn, text="🔄 Actualiser", command=self.afficher_livres)

        btn_ajouter.grid(row=0, column=0, padx=10)
        btn_modifier.grid(row=0, column=1, padx=10)
        btn_supprimer.grid(row=0, column=2, padx=10)
        btn_emprunter.grid(row=0, column=3, padx=10)
        btn_rendre.grid(row=0, column=4, padx=10)
        btn_actualiser.grid(row=0, column=5, padx=10)

        frame_table = tk.Frame(self.root, bg="#E8F5E9", bd=2, relief="ridge")
        frame_table.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ("ID", "Titre", "Auteur", "Année", "Disponible")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=14)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center")

        scrollbar_y = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        self.tree.pack(pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.selectionner_livre)

    def afficher_livres(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.db.recuperer_livres():
            color = random.choice(self.colors)
            self.tree.insert("", tk.END, values=row, tags=("color",))
            self.tree.tag_configure("color", background=color)

    def ajouter_livre(self):
        titre = self.entry_titre.get().strip()
        auteur = self.entry_auteur.get().strip()
        annee = self.entry_annee.get().strip()
        if titre == "" or auteur == "":
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs obligatoires.")
            return
        self.db.ajouter_livre(titre, auteur, annee)
        self.afficher_livres()
        self.effacer_champs()

    def supprimer_livre(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Suppression", "Veuillez sélectionner un livre à supprimer.")
            return
        id_livre = self.tree.item(selected[0])["values"][0]
        self.db.supprimer_livre(id_livre)
        self.afficher_livres()
        self.effacer_champs()

    def modifier_livre(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Modification", "Veuillez sélectionner un livre à modifier.")
            return
        id_livre = self.tree.item(selected[0])["values"][0]
        titre = self.entry_titre.get().strip()
        auteur = self.entry_auteur.get().strip()
        annee = self.entry_annee.get().strip()
        self.db.modifier_livre(id_livre, titre, auteur, annee)
        self.afficher_livres()
        self.effacer_champs()

    def emprunter_livre(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Emprunt", "Veuillez sélectionner un livre à emprunter.")
            return

        id_livre = self.tree.item(selected[0])["values"][0]
        titre = self.tree.item(selected[0])["values"][1]
        disponible = self.tree.item(selected[0])["values"][4]

        if disponible == "Non":
            messagebox.showwarning("Indisponible", f"Le livre '{titre}' est déjà emprunté.")
            return

        resultat = self.db.emprunter_livre(id_livre)
        if resultat:
            messagebox.showinfo("Succès", f"Vous avez emprunté le livre '{titre}'.")
        else:
            messagebox.showwarning("Erreur", "Impossible d'emprunter ce livre.")

        self.afficher_livres()

    def rendre_livre(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Retour", "Veuillez sélectionner un livre à rendre.")
            return

        id_livre = self.tree.item(selected[0])["values"][0]
        titre = self.tree.item(selected[0])["values"][1]
        disponible = self.tree.item(selected[0])["values"][4]

        if disponible == "Oui":
            messagebox.showinfo("Info", f"Le livre '{titre}' est déjà disponible.")
            return

        self.db.rendre_livre(id_livre)
        messagebox.showinfo("Succès", f"Le livre '{titre}' a été rendu avec succès.")
        self.afficher_livres()

    def selectionner_livre(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        livre = self.tree.item(selected[0])["values"]
        self.entry_titre.delete(0, tk.END)
        self.entry_titre.insert(0, livre[1])
        self.entry_auteur.delete(0, tk.END)
        self.entry_auteur.insert(0, livre[2])
        self.entry_annee.delete(0, tk.END)
        self.entry_annee.insert(0, livre[3])

    def effacer_champs(self):
        self.entry_titre.delete(0, tk.END)
        self.entry_auteur.delete(0, tk.END)
        self.entry_annee.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = BibliothequeApp(root)
    root.mainloop()
