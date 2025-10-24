#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vigenère Guided Demo – Teaching Mode (Tkinter)
----------------------------------------------
A precise, step-by-step visual simulation for teaching how to use the Vigenère
square **and** the secret key alignment. Two modes: Encrypt / Decrypt.

What's new in this version
- **Perfect visual alignment**: message and key are rendered in the **same grid**
  so every character column lines up exactly.
- **Correct key repetition**: the key advances **only on letters**; at
  non-letter positions the current key letter is **shown in red** (not
  consumed), making the behavior explicit for students.
- Clear phases per letter, whole row/column highlighting, and word banner.

Run: `python vigenere_guided_demo.py`
Requirements: Python ≥ 3.8 (no external libs)
"""

import string
import tkinter as tk
from tkinter import ttk

ALPHABET = string.ascii_uppercase
N = len(ALPHABET)

# ---------- Colors ----------
COLOR_BG = "#0b1220"
COLOR_HDR_BG = "#2b395b"
COLOR_HDR_FG = "white"
COLOR_CELL_BG = "#131b2e"
COLOR_CELL_FG = "#e8eaf6"
COLOR_COL = "#1e88e5"      # Column = message/plain
COLOR_ROW = "#43a047"      # Row = key
COLOR_INTER = "#f6bf26"    # Intersection
COLOR_INTER_FG = "#000000"
COLOR_DIM = "#90a4ae"      # Dimmed text for non-letter message positions
COLOR_SKIP = "red"          # Key shown in red over non-letter message positions

# ---------- Helpers ----------

def sanitize_letters_keep(text: str) -> str:
    """Uppercase letters; keep punctuation/spaces for display and skipping."""
    out = []
    for ch in text:
        out.append(ch.upper() if ch.isalpha() else ch)
    return "".join(out)


def key_letters_from(key: str):
    letters = [c for c in key.upper() if c.isalpha()]
    return letters if letters else ["A"]


def align_key_to_message_visual(msg: str, key_letters: list[str]) -> list[str]:
    """Return a list `key_for_pos` of length len(msg):
    - For **letter** positions: consume next key letter.
    - For **non-letter** positions: display the current key letter (for teaching)
      but **do not consume** it (so it repeats and is colored red).
    """
    out = []
    p = 0
    L = len(key_letters)
    for ch in msg:
        out.append(key_letters[p % L])
        if ch.isalpha():
            p += 1
    return out


class GuidedVigenere(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vigenère – Guided Demo")
        self.geometry("1220x960")
        self.minsize(1120, 880)
        self.configure(bg=COLOR_BG)

        # State
        self.mode = tk.StringVar(value="Encrypt")  # or "Decrypt"
        self.running = False
        self.step_phase = 0        # 0: row+col, 1: intersection+formula, 2: commit
        self.i = 0                 # index in message

        self._build_ui()
        self._build_table()
        self._reset_all()

    # ---------- UI ----------
    def _build_ui(self):
        # Inputs
        top = ttk.Frame(self, padding=8)
        top.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top, text="Message :").grid(row=0, column=0, sticky="w")
        self.entry_msg = ttk.Entry(top, width=70)
        self.entry_msg.grid(row=0, column=1, columnspan=6, sticky="we", padx=(6, 16))
        self.entry_msg.insert(0, "JE SUIS EN ITALIE, AVEC MARIA !")

        ttk.Label(top, text="Clé :").grid(row=1, column=0, sticky="w")
        self.entry_key = ttk.Entry(top, width=32)
        self.entry_key.grid(row=1, column=1, sticky="w", padx=(6, 16))
        self.entry_key.insert(0, "BIBMATH")

        ttk.Label(top, text="Mode :").grid(row=1, column=2, sticky="e")
        ttk.Radiobutton(top, text="Chiffrer", variable=self.mode, value="Encrypt").grid(row=1, column=3, sticky="w")
        ttk.Radiobutton(top, text="Déchiffrer", variable=self.mode, value="Decrypt").grid(row=1, column=4, sticky="w")

        ttk.Label(top, text="Vitesse (ms/étape) :").grid(row=1, column=5, sticky="e")
        self.speed_scale = ttk.Scale(top, from_=120, to=1200, orient=tk.HORIZONTAL)
        self.speed_scale.set(500)
        self.speed_scale.grid(row=1, column=6, sticky="we")
        top.columnconfigure(6, weight=1)

        # Control buttons
        btns = ttk.Frame(self, padding=(8, 0, 8, 8))
        btns.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(btns, text="▶︎ Démarrer", command=self.start).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="⏸ Pause", command=self.pause).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="⏭ Étape suivante", command=self.step_once).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="⟲ Réinitialiser", command=self.reset_inputs).pack(side=tk.LEFT, padx=12)
        ttk.Button(btns, text="Exemple", command=self.load_example).pack(side=tk.LEFT, padx=4)

        # Status row
        status = ttk.Frame(self, padding=8)
        status.pack(side=tk.TOP, fill=tk.X)
        self.lbl_progress = ttk.Label(status, text="Index: 0/0 | Phase: 0")
        self.lbl_progress.pack(side=tk.LEFT)
        self.lbl_formula = ttk.Label(status, text="C = (P + K) mod 26 | P = (C - K) mod 26")
        self.lbl_formula.pack(side=tk.LEFT, padx=20)

        # Big red banner (current word)
        self.word_var = tk.StringVar(value="")
        self.lbl_word = tk.Label(self, textvariable=self.word_var, font=("Consolas", 30, "bold"), fg="red", bg=COLOR_BG)
        self.lbl_word.pack(side=tk.TOP, pady=(4, 8))

        # Alignment panel (single grid to ensure perfect column alignment)
        align = ttk.LabelFrame(self, text="Alignement Message / Clé (rouge = clé ignorée sur espace/ponctuation)")
        align.pack(side=tk.TOP, fill=tk.X, padx=8, pady=(0, 8))
        self.align_grid = ttk.Frame(align)
        self.align_grid.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        # Output panel
        out = ttk.Frame(self, padding=8)
        out.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(out, text="Résultat :").pack(side=tk.LEFT)
        self.result_var = tk.StringVar(value="")
        ttk.Label(out, textvariable=self.result_var, font=("Consolas", 16)).pack(side=tk.LEFT, padx=8)

        # Legend
        legend = ttk.Frame(self, padding=8)
        legend.pack(side=tk.BOTTOM, fill=tk.X)
        self._legend_label(legend, "Colonne = Lettre du message", bg=COLOR_COL)
        self._legend_label(legend, "Ligne = Lettre de la clé", bg=COLOR_ROW)
        self._legend_label(legend, "Intersection = Lettre résultante", bg=COLOR_INTER)

        # Table container (scrollable)
        container = ttk.Frame(self, padding=8)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(container, background=COLOR_BG, highlightthickness=0)
        self.table_frame = ttk.Frame(self.canvas)
        self.scroll_y = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_x = ttk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.table_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _legend_label(self, parent, text, bg):
        frm = tk.Frame(parent, bg=bg)
        frm.pack(side=tk.LEFT, padx=8)
        tk.Label(frm, text="  ", bg=bg).pack(side=tk.LEFT)
        tk.Label(frm, text=text).pack(side=tk.LEFT, padx=6)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    # ---------- Table ----------
    def _build_table(self):
        style_hdr = {"font": ("Consolas", 11, "bold"), "bg": COLOR_HDR_BG, "fg": COLOR_HDR_FG, "padx": 6, "pady": 4}
        style_cell = {"font": ("Consolas", 11), "bg": COLOR_CELL_BG, "fg": COLOR_CELL_FG, "padx": 6, "pady": 2}
        self.labels = []

        corner = tk.Label(self.table_frame, **style_hdr, text="")
        corner.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        for j, ch in enumerate(ALPHABET, start=1):
            tk.Label(self.table_frame, **style_hdr, text=ch).grid(row=0, column=j, sticky="nsew", padx=1, pady=1)
        for i, row_char in enumerate(ALPHABET, start=1):
            tk.Label(self.table_frame, **style_hdr, text=row_char).grid(row=i, column=0, sticky="nsew", padx=1, pady=1)
            row_labels = []
            shift = ALPHABET.index(row_char)
            row_text = ALPHABET[shift:] + ALPHABET[:shift]
            for j, ch in enumerate(row_text, start=1):
                lbl = tk.Label(self.table_frame, **style_cell, text=ch, width=2)
                lbl.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                row_labels.append(lbl)
            self.labels.append(row_labels)
        self.col_headers = [self.table_frame.grid_slaves(row=0, column=j)[0] for j in range(1, N+1)]
        self.row_headers = [self.table_frame.grid_slaves(row=i, column=0)[0] for i in range(1, N+1)]

    def _reset_table_colors(self):
        for i in range(N):
            for j in range(N):
                self.labels[i][j].configure(bg=COLOR_CELL_BG, fg=COLOR_CELL_FG)
        for hdr in self.col_headers:
            hdr.configure(bg=COLOR_HDR_BG, fg=COLOR_HDR_FG)
        for hdr in self.row_headers:
            hdr.configure(bg=COLOR_HDR_BG, fg=COLOR_HDR_FG)

    def _highlight_row_col(self, row_idx: int, col_idx: int):
        for j in range(N):
            self.labels[row_idx][j].configure(bg=COLOR_ROW, fg="white")
        self.row_headers[row_idx].configure(bg=COLOR_ROW, fg="white")
        for i in range(N):
            self.labels[i][col_idx].configure(bg=COLOR_COL, fg="white")
        self.col_headers[col_idx].configure(bg=COLOR_COL, fg="white")

    # ---------- Alignment row rendering (single grid) ----------
    def _render_alignment(self, msg: str, key_for_pos: list[str]):
        # Clear previous
        for w in self.align_grid.winfo_children():
            w.destroy()
        # Head labels
        tk.Label(self.align_grid, text="Message :", font=("Consolas", 14, "bold"), bg=COLOR_BG, fg="white").grid(row=0, column=0, sticky="e", padx=(0,6))
        tk.Label(self.align_grid, text="Clé     :", font=("Consolas", 14, "bold"), bg=COLOR_BG, fg="white").grid(row=1, column=0, sticky="e", padx=(0,6))
        # Cells (two rows, same columns)
        for idx, ch in enumerate(msg):
            # message cell
            tk.Label(self.align_grid, text=ch, font=("Consolas", 14, "bold"), bg=COLOR_BG,
                     fg=("white" if ch.isalpha() else COLOR_DIM), width=2).grid(row=0, column=idx+1, padx=0)
            # key cell
            kch = key_for_pos[idx]
            color = "white" if ch.isalpha() else COLOR_SKIP
            tk.Label(self.align_grid, text=kch, font=("Consolas", 14, "bold"), bg=COLOR_BG,
                     fg=color, width=2).grid(row=1, column=idx+1, padx=0)
        # Make character columns uniform width across both rows
        total_cols = len(msg) + 1
        for c in range(1, total_cols):
            self.align_grid.grid_columnconfigure(c, uniform="chars", minsize=22)
        self.align_grid.grid_columnconfigure(0, minsize=110)

    def _update_alignment_focus(self, idx: int):
        # Reset fonts for all cells (rows 0 and 1, columns 1..len(msg))
        L = len(self.msg)
        for r in (0, 1):
            for c in range(1, L+1):
                cell = self._get_align_cell(r, c)
                if cell is not None:
                    cell.configure(font=("Consolas", 14, "bold"))
        # Enlarge current column
        if 0 <= idx < L:
            for r in (0, 1):
                cell = self._get_align_cell(r, idx+1)
                if cell is not None:
                    cell.configure(font=("Consolas", 18, "bold"))

    def _get_align_cell(self, row: int, col: int):
        items = self.align_grid.grid_slaves(row=row, column=col)
        return items[0] if items else None

    # ---------- Controls API ----------
    def reset_inputs(self):
        self.pause()
        self._reset_all()

    def load_example(self):
        self.entry_msg.delete(0, tk.END)
        self.entry_msg.insert(0, "JE SUIS EN ITALIE, AVEC MARIA !")
        self.entry_key.delete(0, tk.END)
        self.entry_key.insert(0, "BIBMATH")
        self.reset_inputs()

    def start(self):
        if not self.running:
            self.running = True
            self._tick()

    def pause(self):
        self.running = False

    def step_once(self):
        self._tick(single_step=True)

    def _reset_all(self):
        self.result_var.set("")
        self.i = 0
        self.step_phase = 0
        self._reset_table_colors()
        msg_raw = self.entry_msg.get()
        key_raw = self.entry_key.get()
        self.msg = sanitize_letters_keep(msg_raw)
        self.key_letters = key_letters_from(key_raw)
        self.key_for_pos = align_key_to_message_visual(self.msg, self.key_letters)
        self._render_alignment(self.msg, self.key_for_pos)
        self.word_var.set("")
        self._update_status()

    # ---------- Progress helpers ----------
    def _update_status(self, P="", K="", OUT=""):
        total = len(self.msg)
        self.lbl_progress.configure(text=f"Index: {self.i}/{total} | Phase: {self.step_phase}")
        if self.mode.get() == "Encrypt":
            self.lbl_formula.configure(text=f"Chiffrement: C = (P + K) mod 26 | P={P or ' '} K={K or ' '} ⇒ C={OUT or ' '}")
        else:
            self.lbl_formula.configure(text=f"Déchiffrement: P = (C - K) mod 26 | C={P or ' '} K={K or ' '} ⇒ P={OUT or ' '}")

    def _current_word(self):
        idx = self.i
        if idx >= len(self.msg):
            return ""
        k = idx
        while k < len(self.msg) and not self.msg[k].isalpha():
            k += 1
        if k >= len(self.msg):
            return ""
        start = k
        while start > 0 and self.msg[start-1].isalpha():
            start -= 1
        end = k
        while end < len(self.msg) and self.msg[end].isalpha():
            end += 1
        return self.msg[start:end]

    def _update_banner(self):
        word = self._current_word()
        if not word:
            self.word_var.set("")
            return
        action = "Chiffrement" if self.mode.get() == "Encrypt" else "Déchiffrement"
        self.word_var.set(f"{action} : {word}")

    # ---------- Core tick ----------
    def _tick(self, single_step: bool=False):
        if self.i >= len(self.msg):
            self.pause()
            return

        ch = self.msg[self.i]
        K = self.key_for_pos[self.i]
        self._reset_table_colors()
        self._update_alignment_focus(self.i)
        self._update_banner()

        if not ch.isalpha():
            # Non-letter: copy through, do not consume key (already aligned)
            self.result_var.set(self.result_var.get() + ch)
            self.i += 1
            self.step_phase = 0
            self._update_status(P=ch, K=K)
            self._schedule_next(single_step)
            return

        row_idx = ALPHABET.index(K)
        if self.mode.get() == "Encrypt":
            col_idx = ALPHABET.index(ch)
            if self.step_phase == 0:
                self._highlight_row_col(row_idx, col_idx)
                self._update_status(P=ch, K=K)
                self.step_phase = 1
            elif self.step_phase == 1:
                out_ch = self.labels[row_idx][col_idx].cget("text")
                self._highlight_row_col(row_idx, col_idx)
                self.labels[row_idx][col_idx].configure(bg=COLOR_INTER, fg=COLOR_INTER_FG)
                self._update_status(P=ch, K=K, OUT=out_ch)
                self.step_phase = 2
            else:
                out_ch = self.labels[row_idx][col_idx].cget("text")
                self.result_var.set(self.result_var.get() + out_ch)
                self.i += 1
                self.step_phase = 0
                self._update_status()
        else:
            # Decrypt: find column in key-row where value equals cipher ch
            found_col = None
            for j in range(N):
                if self.labels[row_idx][j].cget("text") == ch:
                    found_col = j
                    break
            if found_col is None:
                found_col = 0
            plain = ALPHABET[found_col]
            if self.step_phase == 0:
                self._highlight_row_col(row_idx, found_col)
                self._update_status(P=ch, K=K)
                self.step_phase = 1
            elif self.step_phase == 1:
                self._highlight_row_col(row_idx, found_col)
                self.labels[row_idx][found_col].configure(bg=COLOR_INTER, fg=COLOR_INTER_FG)
                self._update_status(P=ch, K=K, OUT=plain)
                self.step_phase = 2
            else:
                self.result_var.set(self.result_var.get() + plain)
                self.i += 1
                self.step_phase = 0
                self._update_status()

        self._schedule_next(single_step)

    def _schedule_next(self, single_step: bool):
        if self.running and not single_step:
            delay = int(self.speed_scale.get())
            self.after(delay, self._tick)


if __name__ == "__main__":
    app = GuidedVigenere()
    app.mainloop()
 