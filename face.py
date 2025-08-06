import tkinter as tk
import math
import random

class FaceTheo(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, width=800, height=300, highlightthickness=0, **kwargs)
        self.fase = 0
        self.falando_ativo = False
        self.animar_onda()

    def animar_onda(self):
        self.delete("onda")
        largura = int(self["width"])
        altura = int(self["height"])
        centro = altura // 2

        base_amplitude = 10 if not self.falando_ativo else random.uniform(40, 70)
        frequencia = 0.02
        x_step = 5  # menos pontos, mais leve

        # Desenha da camada mais larga (brilho externo) até a mais fina (centro)
        camadas = [
            {"cor": "#002aff", "largura": 4},  # glow externo
            {"cor": "#005fff", "largura": 2},  # meio glow
            {"cor": "#00d0ff", "largura": 1},  # linha principal
        ]

        for camada in camadas:
            pontos = []
            for x in range(0, largura, x_step):
                y = centro + math.sin(x * frequencia + self.fase) * base_amplitude
                pontos.append((x, y))
            for i in range(len(pontos) - 1):
                self.create_line(
                    pontos[i], pontos[i+1],
                    fill=camada["cor"],
                    width=camada["largura"],
                    tags="onda"
                )

        self.fase += 0.25
        self.after(50, self.animar_onda)  # ~20 FPS

    def falando(self):
        self.falando_ativo = True

    def neutro(self):
        self.falando_ativo = False
