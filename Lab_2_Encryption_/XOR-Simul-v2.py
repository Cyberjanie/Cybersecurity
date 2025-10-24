#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox

# =========================
#    Utilitaires parsing
# =========================
def parse_int_auto(s: str) -> int:
    """
    Parse une chaîne en int avec auto-détection :
    - Binaire : '0b1010' ou '1010' si constitué uniquement de 0/1
    - Hexa    : '0x2F' ou '2F' si hexa valide
    - Sinon   : décimal
    """
    s = s.strip().lower()
    if not s:
        raise ValueError("Valeur vide.")
    # Préfixes standard
    if s.startswith("0b"):
        return int(s, 2)
    if s.startswith("0x"):
        return int(s, 16)
    # Heuristique binaire sans préfixe
    if all(c in "01" for c in s):
        return int(s, 2)
    # Heuristique hexa sans préfixe
    if all(c in "0123456789abcdef" for c in s):
        # Ambigu : '10' peut être décimal ou hexa—on privilégie décimal.
        # On considère hexa seulement si au moins une lettre a-f est présente.
        if any(c in "abcdef" for c in s):
            return int(s, 16)
    # Sinon décimal
    return int(s, 10)


def to_bin_n(x: int, n: int) -> str:
    """Retourne la représentation binaire sur n bits (tronquée à droite si besoin)."""
    if n <= 0:
        raise ValueError("La taille en bits doit être > 0.")
    return format(x & ((1 << n) - 1), f"0{n}b")


def clamp_bits(n: int, min_n=2, max_n=64) -> int:
    return max(min_n, min(max_n, n))


# =========================
#       Application UI
# =========================
class XorSimulator(tk.Tk):
    BOX = 34         # taille des carrés bit
    GAP_X = 6        # espace horizontal entre cases
    GAP_Y = 16       # espace vertical entre lignes

    def __init__(self):
        super().__init__()
        self.title("Simulateur visuel XOR (A ⊕ B)")
        self.geometry("980x520")
        self.minsize(820, 480)
        self.configure(bg="white")

        # État
        self.bit_len = tk.IntVar(value=8)
        self.in_a = tk.StringVar(value="10101010")
        self.in_b = tk.StringVar(value="11001100")
        self.status_text = tk.StringVar(value="Prêt")
        self.anim_speed_ms = tk.IntVar(value=150)   # délai par bit
        self.anim_running = False
        self.anim_index = 0

        # Buffers de bits pour l'animation
        self.bits_a = ""
        self.bits_b = ""
        self.bits_r = ""

        # Widgets
        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=12, pady=8)

        # Taille des bits
        tk.Label(top, text="Taille (bits) :", bg="white").grid(row=0, column=0, sticky="w", padx=4)
        tk.Spinbox(top, from_=2, to=64, width=5, textvariable=self.bit_len).grid(row=0, column=1, padx=6)

        # Entrées A / B
        tk.Label(top, text="A :", bg="white").grid(row=0, column=2, sticky="e")
        tk.Entry(top, textvariable=self.in_a, width=22).grid(row=0, column=3, padx=6)

        tk.Label(top, text="B :", bg="white").grid(row=0, column=4, sticky="e")
        tk.Entry(top, textvariable=self.in_b, width=22).grid(row=0, column=5, padx=6)

        # Boutons actions
        ttk.Button(top, text="Calculer (instantané)", command=self.compute_now).grid(row=0, column=6, padx=8)
        ttk.Button(top, text="Lecture pas-à-pas ▶", command=self.start_anim).grid(row=0, column=7, padx=4)
        ttk.Button(top, text="Pause ⏸", command=self.pause_anim).grid(row=0, column=8, padx=4)
        ttk.Button(top, text="Réinitialiser ⟲", command=self.reset_anim).grid(row=0, column=9, padx=4)

        # Curseur de vitesse
        sp = tk.Frame(self, bg="white")
        sp.pack(fill="x", padx=12, pady=2)
        tk.Label(sp, text="Vitesse (ms/bit) :", bg="white").pack(side="left")
        tk.Scale(sp, from_=50, to=1000, variable=self.anim_speed_ms, orient="horizontal",
                 length=220, showvalue=True, resolution=10, bg="white", highlightthickness=0).pack(side="left", padx=8)

        # Canvas
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1, highlightbackground="#dddddd")
        self.canvas.pack(fill="both", expand=True, padx=12, pady=8)

        # Légende / status bar
        bot = tk.Frame(self, bg="white")
        bot.pack(fill="x", padx=12, pady=(0, 10))
        # Légendes couleurs
        lg = tk.Frame(bot, bg="white")
        lg.pack(side="left")
        self._legend_dot(lg, "#d32f2f"); tk.Label(lg, text="bits différents → résultat 1 (rouge)", bg="white").pack(side="left", padx=(4, 12))
        self._legend_dot(lg, "#2e7d32"); tk.Label(lg, text="bits identiques → résultat 0 (vert)", bg="white").pack(side="left", padx=(4, 12))
        ttk.Button(bot, text="?", width=3, command=self.show_help).pack(side="right")
        ttk.Label(bot, textvariable=self.status_text).pack(side="right", padx=10)

        # Dessin initial
        self._prepare_bits()
        self._draw_frame(empty_result=True)

    def _legend_dot(self, parent, color):
        c = tk.Canvas(parent, width=14, height=14, bg="white", highlightthickness=0)
        c.pack(side="left")
        c.create_oval(2, 2, 12, 12, fill=color, outline=color)

    # ---------- Aide ----------
    def show_help(self):
        messagebox.showinfo(
            "À propos de XOR (OU exclusif)",
            "XOR compare chaque bit indépendamment :\n\n"
            "  A  B | A⊕B\n"
            "  0  0 |  0\n"
            "  0  1 |  1\n"
            "  1  0 |  1\n"
            "  1  1 |  0\n\n"
            "Propriétés : A⊕0=A, A⊕A=0, A⊕1=¬A, commutatif et associatif.\n"
            "Applications : parité, masques de bits, cryptographie (C=P⊕K)."
        )

    # ---------- Logique principale ----------
    def _prepare_bits(self):
        try:
            n = clamp_bits(int(self.bit_len.get()))
            a = parse_int_auto(self.in_a.get())
            b = parse_int_auto(self.in_b.get())
        except Exception as e:
            self.status_text.set(f"Entrée invalide : {e}")
            n = clamp_bits(int(self.bit_len.get()))
            a = 0
            b = 0

        self.bits_a = to_bin_n(a, n)
        self.bits_b = to_bin_n(b, n)
        self.bits_r = to_bin_n(a ^ b, n)
        self.anim_index = 0

    def compute_now(self):
        self.anim_running = False
        self._prepare_bits()
        self._draw_frame(empty_result=False)  # affiche le résultat complet
        self.status_text.set("Calcul instantané terminé.")

    def start_anim(self):
        if self.anim_running:
            return
        self.anim_running = True
        self._prepare_bits()
        self._draw_frame(empty_result=True)
        self.status_text.set("Animation en cours…")
        self.after(20, self._tick)

    def pause_anim(self):
        self.anim_running = False
        self.status_text.set("Animation en pause.")

    def reset_anim(self):
        self.anim_running = False
        self.anim_index = 0
        self._prepare_bits()
        self._draw_frame(empty_result=True)
        self.status_text.set("Réinitialisé.")

    def _tick(self):
        if not self.anim_running:
            return
        n = len(self.bits_a)
        if self.anim_index > n:
            self.anim_running = False
            self.status_text.set("Animation terminée.")
            return
        # Redessiner avec les bits [0:anim_index] révélés
        self._draw_frame(reveal_upto=self.anim_index)
        self.anim_index += 1
        self.after(self.anim_speed_ms.get(), self._tick)

    # ---------- Dessin ----------
    def _draw_frame(self, empty_result=False, reveal_upto=None):
        """Dessine les 3 lignes A, B, A⊕B.
        - empty_result : si True, n'affiche pas la ligne résultat.
        - reveal_upto : si entier, affiche seulement les 'reveal_upto' premiers bits du résultat.
        """
        self.canvas.delete("all")

        # Mesure dynamique
        n = len(self.bits_a)
        box = self.BOX
        gapx = self.GAP_X
        start_x = 60
        start_y = 40

        # Titre et équivalents
        try:
            a_int = parse_int_auto(self.in_a.get())
            b_int = parse_int_auto(self.in_b.get())
        except Exception:
            a_int, b_int = 0, 0
        r_int = (a_int ^ b_int) & ((1 << n) - 1)

        header = f"A = {a_int} (0b{to_bin_n(a_int, n)}, 0x{format(a_int,'X')})   |   " \
                 f"B = {b_int} (0b{to_bin_n(b_int, n)}, 0x{format(b_int,'X')})   |   " \
                 f"A⊕B = {r_int} (0b{to_bin_n(r_int, n)}, 0x{format(r_int,'X')})"
        self.canvas.create_text(12, 16, text=header, anchor="w", font=("Consolas", 11), fill="#333333")

        # Lignes étiquettes
        self.canvas.create_text(start_x - 14, start_y + box/2, text="A", font=("Arial", 12, "bold"))
        self.canvas.create_text(start_x - 14, start_y + box + self.GAP_Y + box/2, text="B", font=("Arial", 12, "bold"))
        self.canvas.create_text(start_x - 28, start_y + 2*(box + self.GAP_Y) + box/2, text="A ⊕ B", font=("Arial", 12, "bold"))

        # Dessiner rangée A
        y_a = start_y
        for i, bit in enumerate(self.bits_a):
            x = start_x + i * (box + gapx)
            self._draw_bit(x, y_a, bit, fg="#000000", bg="#f7f7f7")

        # Dessiner rangée B
        y_b = start_y + (box + self.GAP_Y)
        for i, bit in enumerate(self.bits_b):
            x = start_x + i * (box + gapx)
            self._draw_bit(x, y_b, bit, fg="#000000", bg="#f7f7f7")

        # Ligne de séparation / opérateur XOR visuel
        mid_y = start_y + 2*(box + self.GAP_Y) - int(self.GAP_Y/2)
        self.canvas.create_line(start_x - 10, mid_y, start_x + n*(box + gapx) - gapx + 10, mid_y, fill="#bbbbbb", dash=(3,2))
        self.canvas.create_text(start_x - 24, mid_y - 8, text="XOR", font=("Arial", 9), fill="#666666")

        # Dessiner rangée Résultat
        y_r = start_y + 2*(box + self.GAP_Y)
        for i in range(n):
            x = start_x + i * (box + gapx)
            if empty_result:
                # cases vides
                self._draw_bit(x, y_r, "", fg="#999999", bg="#ffffff", outline="#cfcfcf")
                continue
            show = True
            if reveal_upto is not None:
                show = (i < reveal_upto)
            if show:
                bit_a = self.bits_a[i]
                bit_b = self.bits_b[i]
                bit_r = self.bits_r[i]
                # Couleur : rouge si différent (résultat 1), vert sinon (0)
                color = "#d32f2f" if bit_r == "1" else "#2e7d32"
                self._draw_bit(x, y_r, bit_r, fg=color, bg="#ffffff", bold=True)
                # Petit marqueur au-dessus pour surligner le bit courant
                if reveal_upto is not None and i == reveal_upto - 1:
                    self.canvas.create_rectangle(x-2, y_r-10, x+box+2, y_r+box+2, outline="#1976d2", width=2)
                    # Aide visuelle :  A≠B → 1   |   A=B → 0
                    txt = "différents → 1" if bit_a != bit_b else "identiques → 0"
                    self.canvas.create_text(x + box/2, y_r + box + 14, text=txt, font=("Arial", 9), fill="#1976d2")
            else:
                self._draw_bit(x, y_r, "", fg="#999999", bg="#ffffff", outline="#cfcfcf")

    def _draw_bit(self, x, y, bit, fg="#000000", bg="#ffffff", outline="#999999", bold=False):
        box = self.BOX
        self.canvas.create_rectangle(x, y, x+box, y+box, outline=outline, width=1, fill=bg)
        if bit != "":
            font = ("Consolas", 14, "bold" if bold else "normal")
            self.canvas.create_text(x + box/2, y + box/2, text=str(bit), font=font, fill=fg)


# =========================
#        Lancement
# =========================
if __name__ == "__main__":
    app = XorSimulator()
    app.mainloop()
