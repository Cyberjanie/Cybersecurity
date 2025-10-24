#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BitMixerSim - Visual simulator for bit shifts, rotations, reverse permutation,
custom P-box permutation, and XOR mixing.

- Single-file Tkinter app
- Supports 4..64 bits
- Input in bin (0b...), hex (0x...), or decimal
- Logical shifts (left/right), rotates (left/right)
- Reverse bits (mirror)
- Custom permutation (comma-separated indices)
- XOR with key
- Step or Run with adjustable speed
- Resizable window with scrollable canvas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import re

MIN_BITS = 4
MAX_BITS = 64
BOX_W = 36
BOX_H = 46
BOX_GAP = 8
TOP_MARGIN = 60
SIDE_MARGIN = 40
ANIM_STEPS = 16  # per move

def clamp(n, a, b):
    return max(a, min(b, n))

def parse_int_auto(s: str) -> int:
    s = s.strip().lower()
    if s.startswith("0b"):
        return int(s, 2)
    if s.startswith("0x"):
        return int(s, 16)
    # allow spaces/underscores
    s = s.replace("_", "").replace(" ", "")
    # hex like deadbeef without 0x if contains a-f
    if re.fullmatch(r"[0-9a-f]+", s) and re.search(r"[a-f]", s):
        return int(s, 16)
    return int(s, 10)

def int_to_bitlist(x: int, nbits: int):
    return [(x >> i) & 1 for i in range(nbits)][::-1]  # MSB first

def bitlist_to_int(bits):
    v = 0
    for b in bits:
        v = (v << 1) | (1 if b else 0)
    return v

class BitMixerSim(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BitMixerSim — Visual Bit Shift / Rotate / Permute / XOR")
        self.geometry("1200x560")
        self.minsize(960, 480)

        self.nbits = tk.IntVar(value=16)
        self.input_str = tk.StringVar(value="0xA5F3")
        self.op = tk.StringVar(value="Shift Left (logical)")
        self.amount = tk.IntVar(value=1)
        self.perm_str = tk.StringVar(value="")  # e.g. "7,6,5,4,3,2,1,0"
        self.xor_key_str = tk.StringVar(value="0x0")
        self.speed_ms = tk.IntVar(value=8)  # smaller = faster (per frame)
        self.running = False
        self.animating = False
        self.items = []  # [(rect, text, idx_text, bit_val)]
        self.current_bits = []  # MSB..LSB list
        self.target_positions = {}  # idx -> (x,y)
        self.canvas_width = 0

        self._build_ui()
        self.bind("<Configure>", self._on_resize)

    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Left control panel
        left = ttk.Frame(self, padding=10)
        left.grid(row=0, column=0, sticky="ns")
        for i in range(12):
            left.rowconfigure(i, weight=0)

        ttk.Label(left, text="Taille (bits)").grid(row=0, column=0, sticky="w")
        spin_bits = ttk.Spinbox(left, from_=MIN_BITS, to=MAX_BITS, textvariable=self.nbits, width=6)
        spin_bits.grid(row=0, column=1, sticky="w", padx=6)

        ttk.Label(left, text="Valeur d'entrée").grid(row=1, column=0, sticky="w", pady=(8,0))
        entry_in = ttk.Entry(left, textvariable=self.input_str, width=22)
        entry_in.grid(row=1, column=1, sticky="w")

        ttk.Label(left, text="Opération").grid(row=2, column=0, sticky="w", pady=(8,0))
        ops = [
            "Shift Left (logical)",
            "Shift Right (logical)",
            "Rotate Left",
            "Rotate Right",
            "Reverse Bits",
            "Custom Permutation",
            "XOR with Key",
        ]
        cb = ttk.Combobox(left, values=ops, textvariable=self.op, state="readonly", width=22)
        cb.grid(row=2, column=1, sticky="w")

        ttk.Label(left, text="Amount (décalage)").grid(row=3, column=0, sticky="w", pady=(8,0))
        spin_amt = ttk.Spinbox(left, from_=0, to=MAX_BITS, textvariable=self.amount, width=6)
        spin_amt.grid(row=3, column=1, sticky="w")

        ttk.Label(left, text="Permutation (indices source)").grid(row=4, column=0, sticky="w", pady=(8,0))
        perm_entry = ttk.Entry(left, textvariable=self.perm_str, width=22)
        perm_entry.grid(row=4, column=1, sticky="w")
        ttk.Label(left, text="Ex.: 7,6,5,4,3,2,1,0 pour inverser").grid(row=5, column=0, columnspan=2, sticky="w")

        ttk.Label(left, text="XOR Key").grid(row=6, column=0, sticky="w", pady=(8,0))
        xor_entry = ttk.Entry(left, textvariable=self.xor_key_str, width=22)
        xor_entry.grid(row=6, column=1, sticky="w")

        ttk.Label(left, text="Vitesse (ms/frame)").grid(row=7, column=0, sticky="w", pady=(8,0))
        speed = ttk.Scale(left, from_=2, to=25, orient="horizontal", variable=self.speed_ms)
        speed.grid(row=7, column=1, sticky="we")

        # Buttons
        btns = ttk.Frame(left)
        btns.grid(row=8, column=0, columnspan=2, pady=(12,0), sticky="we")
        ttk.Button(btns, text="Construire les bits", command=self.build_bits).grid(row=0, column=0, padx=2)
        ttk.Button(btns, text="Étape (Step)", command=self.step_once).grid(row=0, column=1, padx=2)
        ttk.Button(btns, text="Run ▶", command=self.run_auto).grid(row=0, column=2, padx=2)
        ttk.Button(btns, text="Stop ⏹", command=self.stop_auto).grid(row=0, column=3, padx=2)
        ttk.Button(btns, text="Reset", command=self.reset_view).grid(row=0, column=4, padx=2)
        ttk.Button(btns, text="Aléatoire", command=self.randomize_value).grid(row=0, column=5, padx=2)

        # Log
        ttk.Label(left, text="Journal").grid(row=9, column=0, columnspan=2, sticky="w", pady=(12,0))
        self.log = tk.Text(left, width=42, height=12)
        self.log.grid(row=10, column=0, columnspan=2, sticky="we")
        log_scroll = ttk.Scrollbar(left, orient="vertical", command=self.log.yview)
        self.log.config(yscrollcommand=log_scroll.set)
        log_scroll.grid(row=10, column=2, sticky="ns")

        # Right canvas with scroll
        right = ttk.Frame(self, padding=(2,10,10,10))
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(right, background="#0f1115", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.hbar = ttk.Scrollbar(right, orient="horizontal", command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky="we")
        self.canvas.configure(xscrollcommand=self.hbar.set)

        self._draw_axis()
        self.build_bits(initial=True)

    def _draw_axis(self):
        self.canvas.delete("axis")
        w = self.canvas.winfo_width() or 800
        self.canvas.create_text(8, 8, text="MSB → LSB", fill="#a0a7b4",
                                anchor="nw", font=("Segoe UI", 10, "italic"), tags="axis")

    # ---- Core actions ----
    def append_log(self, s):
        self.log.insert("end", s + "\n")
        self.log.see("end")

    def randomize_value(self):
        try:
            n = clamp(self.nbits.get(), MIN_BITS, MAX_BITS)
        except tk.TclError:
            n = 16
            self.nbits.set(n)
        val = random.getrandbits(n)
        self.input_str.set(f"0x{val:X}")
        self.append_log(f"[Val] Aléatoire: {self.input_str.get()}")
        self.build_bits()

    def reset_view(self):
        self.stop_auto()
        self.build_bits()

    def build_bits(self, initial=False):
        # parse nbits & value
        try:
            n = clamp(self.nbits.get(), MIN_BITS, MAX_BITS)
        except tk.TclError:
            messagebox.showerror("Erreur", "Taille invalide.")
            return
        try:
            v = parse_int_auto(self.input_str.get())
        except Exception:
            messagebox.showerror("Erreur", "Valeur d'entrée invalide. Utilise 0b..., 0x... ou décimal.")
            return
        v &= (1 << n) - 1
        bits = int_to_bitlist(v, n)  # MSB..LSB
        self.current_bits = bits

        # clear items
        for (r, t, idx_t, _) in self.items:
            self.canvas.delete(r)
            self.canvas.delete(t)
            self.canvas.delete(idx_t)
        self.items = []

        # compute layout
        self.canvas_width = SIDE_MARGIN*2 + n * (BOX_W + BOX_GAP) - BOX_GAP
        height = max(TOP_MARGIN + BOX_H + 60, self.canvas.winfo_height() or 400)
        self.canvas.config(scrollregion=(0, 0, self.canvas_width, height))

        # draw bit boxes
        for i, b in enumerate(bits):
            x = SIDE_MARGIN + i * (BOX_W + BOX_GAP)
            y = TOP_MARGIN
            rect = self.canvas.create_rectangle(
                x, y, x+BOX_W, y+BOX_H,
                fill="#1f2630" if b == 0 else "#2a8cff",
                outline="#3b4653", width=2, tags=("bitbox", f"bit{i}")
            )
            txt = self.canvas.create_text(
                x+BOX_W/2, y+BOX_H/2,
                text=str(b), fill="#e5ecf4", font=("Consolas", 16, "bold"),
                tags=("bittext", f"bittxt{i}")
            )
            idx_txt = self.canvas.create_text(
                x+BOX_W/2, y-18, text=str(i),
                fill="#a0a7b4", font=("Segoe UI", 9),
                tags=("bitidx", f"bitidx{i}")
            )
            self.items.append((rect, txt, idx_txt, b))

        vhex = f"0x{v:X}"
        vbin = f"0b{v:0{n}b}"
        if not initial:
            self.append_log(f"[Build] n={n}, valeur={v} ({vhex} / {vbin})")

    def get_mapping_and_result(self):
        """
        Returns:
          mapping: list length n, where mapping[new_pos] = old_pos or None (for inserted zero)
          new_bits: resulting bits list (MSB..LSB)
          op_desc: string description
        """
        n = self.nbits.get()
        bits = self.current_bits[:]
        op = self.op.get()
        amt = self.amount.get() % n if n > 0 else 0

        if op == "Shift Left (logical)":
            # new[i] = old[i-amt] if i-amt >=0 else 0
            mapping = []
            new_bits = []
            for i in range(n):
                src = i - amt
                if src >= 0:
                    mapping.append(src)
                    new_bits.append(bits[src])
                else:
                    mapping.append(None)
                    new_bits.append(0)
            return mapping, new_bits, f"ShiftL {amt}"

        if op == "Shift Right (logical)":
            mapping = []
            new_bits = []
            for i in range(n):
                src = i + amt
                if src < n:
                    mapping.append(src)
                    new_bits.append(bits[src])
                else:
                    mapping.append(None)
                    new_bits.append(0)
            return mapping, new_bits, f"ShiftR {amt}"

        if op == "Rotate Left":
            mapping = []
            new_bits = []
            for i in range(n):
                src = (i - amt) % n
                mapping.append(src)
                new_bits.append(bits[src])
            return mapping, new_bits, f"RotL {amt}"

        if op == "Rotate Right":
            mapping = []
            new_bits = []
            for i in range(n):
                src = (i + amt) % n
                mapping.append(src)
                new_bits.append(bits[src])
            return mapping, new_bits, f"RotR {amt}"

        if op == "Reverse Bits":
            mapping = []
            new_bits = []
            for i in range(n):
                src = n-1 - i
                mapping.append(src)
                new_bits.append(bits[src])
            return mapping, new_bits, "Reverse"

        if op == "Custom Permutation":
            p = self.perm_str.get().strip()
            if not p:
                raise ValueError("Permutation vide. Exemple: '7,6,5,4,3,2,1,0'")
            try:
                srcs = [int(x) for x in p.split(",")]
            except Exception:
                raise ValueError("Permutation invalide. Utilise des entiers séparés par des virgules.")
            if len(srcs) != n:
                raise ValueError(f"La permutation doit contenir exactement {n} indices.")
            if any((s < 0 or s >= n) for s in srcs):
                raise ValueError("Indices hors limites dans la permutation.")
            mapping = []
            new_bits = []
            for i in range(n):
                src = srcs[i]
                mapping.append(src)
                new_bits.append(bits[src])
            return mapping, new_bits, f"P-Box {srcs}"

        if op == "XOR with Key":
            try:
                key_val = parse_int_auto(self.xor_key_str.get()) & ((1 << n) - 1)
            except Exception:
                raise ValueError("Clé XOR invalide (0b..., 0x..., ou décimal).")
            key_bits = int_to_bitlist(key_val, n)
            new_bits = [(a ^ b) for a, b in zip(bits, key_bits)]
            # For XOR, mapping is identity (visual flip)
            mapping = list(range(n))
            return mapping, new_bits, f"XOR key=0x{key_val:X}"

        raise ValueError("Opération non gérée.")

    def step_once(self):
        if self.animating:
            return
        try:
            mapping, new_bits, desc = self.get_mapping_and_result()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.append_log(f"[Step] {desc}")
        if self.op.get() == "XOR with Key":
            self._animate_xor(new_bits)
        else:
            self._animate_mapping(mapping, new_bits)

    def run_auto(self):
        if self.running:
            return
        self.running = True
        self._auto_loop()

    def stop_auto(self):
        self.running = False

    def _auto_loop(self):
        if not self.running:
            return
        if self.animating:
            # try again shortly
            self.after(30, self._auto_loop)
            return
        self.step_once()
        # keep running
        self.after(80, self._auto_loop)

    # ---- Animation helpers ----
    def _box_center(self, index):
        x = SIDE_MARGIN + index * (BOX_W + BOX_GAP)
        y = TOP_MARGIN
        return x, y

    def _animate_mapping(self, mapping, new_bits):
        """
        mapping[new_idx] = old_idx or None (inserted zero)
        Move rectangles/text to new x (y constant), then recolor values.
        """
        n = len(mapping)
        # compute target coords per *destination slot*
        targets = {}
        for new_i in range(n):
            x, y = self._box_center(new_i)
            targets[new_i] = (x, y)

        # Build movement list: for each old index, where to go?
        moves = []  # (rect, text, idx_text, from_i, to_i)
        zeros_to_paint = []  # new indices that will become zero (no source)
        taken_by = {}  # new_i -> old_i (or None)

        for new_i, old_i in enumerate(mapping):
            taken_by[new_i] = old_i
            if old_i is None:
                zeros_to_paint.append(new_i)
            else:
                rect, txt, idx_txt, _ = self.items[old_i]
                moves.append((rect, txt, idx_txt, old_i, new_i))

        # Create "ghost" rectangles for zeros (short flash)
        ghost_ids = []
        for new_i in zeros_to_paint:
            tx, ty = targets[new_i]
            # small pulse rectangle
            g = self.canvas.create_rectangle(
                tx, ty, tx+BOX_W, ty+BOX_H,
                fill="#33222a", outline="#aa4455", width=2, stipple="gray25", tags=("ghost",)
            )
            ghost_ids.append(g)

        # animate moves
        self.animating = True
        steps = ANIM_STEPS
        delay = clamp(self.speed_ms.get(), 2, 25)

        # Precompute from/to coords
        coords = []
        for (rect, txt, idx_txt, old_i, new_i) in moves:
            sx, sy = self._box_center(old_i)
            tx, ty = targets[new_i]
            coords.append((rect, txt, idx_txt, sx, sy, tx, ty))

        def tick(step=0):
            if step >= steps:
                # snap to final & recolor + reindex all
                for (rect, txt, idx_txt, sx, sy, tx, ty) in coords:
                    dx = tx - sx
                    dy = ty - sy
                    self.canvas.move(rect, dx, dy)
                    self.canvas.move(txt, dx, dy)
                    self.canvas.move(idx_txt, dx, dy)
                # Delete ghosts
                for g in ghost_ids:
                    self.canvas.delete(g)
                # Rebuild items in new order
                new_items = [None] * n
                for new_i in range(n):
                    old_i = taken_by[new_i]
                    if old_i is None:
                        # create new zero cell
                        x, y = self._box_center(new_i)
                        rect = self.canvas.create_rectangle(
                            x, y, x+BOX_W, y+BOX_H,
                            fill="#1f2630", outline="#3b4653", width=2, tags=("bitbox", f"bit{new_i}")
                        )
                        txt = self.canvas.create_text(
                            x+BOX_W/2, y+BOX_H/2, text="0",
                            fill="#e5ecf4", font=("Consolas", 16, "bold"),
                            tags=("bittext", f"bittxt{new_i}")
                        )
                        idx_txt = self.canvas.create_text(
                            x+BOX_W/2, y-18, text=str(new_i),
                            fill="#a0a7b4", font=("Segoe UI", 9),
                            tags=("bitidx", f"bitidx{new_i}")
                        )
                        new_items[new_i] = (rect, txt, idx_txt, 0)
                    else:
                        rect, txt, idx_txt, _ = self.items[old_i]
                        # update index label
                        self.canvas.itemconfigure(idx_txt, text=str(new_i))
                        new_items[new_i] = (rect, txt, idx_txt, 0)  # temp value
                # set final values and colors
                for i in range(n):
                    rect, txt, idx_txt, _ = new_items[i]
                    b = new_bits[i]
                    self.canvas.itemconfigure(txt, text=str(b))
                    self.canvas.itemconfigure(rect, fill=("#2a8cff" if b else "#1f2630"))
                    new_items[i] = (rect, txt, idx_txt, b)

                self.items = new_items
                self.current_bits = new_bits
                val = bitlist_to_int(new_bits)
                self.append_log(f"   → Résultat: 0x{val:X}  (0b{val:0{n}b})")
                self.animating = False
                return

            for (rect, txt, idx_txt, sx, sy, tx, ty) in coords:
                x = sx + (tx - sx) * (step + 1) / steps
                y = sy + (ty - sy) * (step + 1) / steps
                # Move to absolute by first getting current and then moving delta
                bx1, by1, bx2, by2 = self.canvas.coords(rect)
                cx = bx1
                cy = by1
                self.canvas.move(rect, x - cx, y - cy)
                self.canvas.move(txt, x - cx, y - cy)
                self.canvas.move(idx_txt, x - cx, y - cy)
            self.after(delay, lambda: tick(step + 1))

        tick(0)

    def _animate_xor(self, new_bits):
        """Flash boxes that flip from 0→1 or 1→0."""
        if len(new_bits) != len(self.items):
            return
        self.animating = True
        delay = clamp(self.speed_ms.get(), 2, 25)

        flips = []
        for i, ((rect, txt, idx_txt, old_b), new_b) in enumerate(zip(self.items, new_bits)):
            if old_b != new_b:
                flips.append(i)

        # flash sequence: highlight flips
        highlight_color = "#ffb020"
        normal_on = "#2a8cff"
        normal_off = "#1f2630"

        def flash(k=0):
            if k >= 6:
                # set final values
                for i, (rect, txt, idx_txt, _) in enumerate(self.items):
                    b = new_bits[i]
                    self.canvas.itemconfigure(txt, text=str(b))
                    self.canvas.itemconfigure(rect, fill=(normal_on if b else normal_off))
                    self.items[i] = (rect, txt, idx_txt, b)
                self.current_bits = new_bits
                v = bitlist_to_int(new_bits)
                n = len(new_bits)
                self.append_log(f"   → Résultat: 0x{v:X}  (0b{v:0{n}b})")
                self.animating = False
                return

            # toggle highlight state
            on = (k % 2 == 0)
            for i in flips:
                rect, txt, idx_txt, _ = self.items[i]
                self.canvas.itemconfigure(rect, fill=(highlight_color if on else normal_on if self.current_bits[i] else normal_off))
            self.after(delay*3, lambda: flash(k+1))

        if flips:
            self.append_log(f"   XOR: {len(flips)} bit(s) ont changé")
        else:
            self.append_log("   XOR: aucun bit changé")
        flash(0)

    def _on_resize(self, event):
        # keep axis text
        self._draw_axis()
        # update scroll region width if bigger
        self.canvas.config(scrollregion=(0, 0, max(self.canvas_width, self.canvas.winfo_width()), max(self.canvas.winfo_height(), 300)))

def main():
    app = BitMixerSim()
    app.mainloop()

if __name__ == "__main__":
    main()
