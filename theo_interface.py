import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import asyncio
import uuid
import edge_tts
import playsound
import speech_recognition as sr
from comandos import executar_comando
from face import FaceTheo

class TheoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("THEO")
        self.root.geometry("900x600")
        self.root.configure(bg="#0a1324")

        self.audio_ativo = False
        self.animando = False
        self.lock = threading.Lock()

        self.face_frame = tk.Frame(self.root, bg="#0a1324", width=900, height=540)
        self.face_frame.pack_propagate(False)
        self.face_frame.pack(pady=10)

        self.face = FaceTheo(self.face_frame, bg="#0a1324")
        self.face.pack(expand=True, fill="both")

        self.btn_frame = tk.Frame(root, bg="#0a1324")
        self.btn_frame.pack(side="bottom", pady=20)

        self.mic_img = tk.PhotoImage(file="assets/mic.png").subsample(12, 12)
        self.btn_ouvir = tk.Button(self.btn_frame, image=self.mic_img, command=self.toggle_audio,
                                   bg="#14264a", bd=0, activebackground="#1e3a75")
        self.btn_ouvir.grid(row=0, column=0, padx=10)

        threading.Thread(target=self.falar, args=("Inicializando sistema",), daemon=True).start()

    def toggle_audio(self):
        if self.audio_ativo:
            self.audio_ativo = False
            self.btn_ouvir.config(bg="#14264a")
        else:
            self.audio_ativo = True
            self.btn_ouvir.config(bg="#b22222")
            threading.Thread(target=self.ouvir_loop, daemon=True).start()

    def ouvir_loop(self):
        while self.audio_ativo:
            comando = self.ouvir()
            if not self.audio_ativo:
                break
            executar_comando(comando, self.falar, self.ouvir, self.reativar_microfone)

    def reativar_microfone(self):
        if not self.audio_ativo:
            self.audio_ativo = True
            self.btn_ouvir.config(bg="#b22222")
            threading.Thread(target=self.ouvir_loop, daemon=True).start()

    def ouvir(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
        try:
            comando = recognizer.recognize_google(audio, language="pt-BR")
            return comando.lower()
        except sr.UnknownValueError:
            return "não entendi"
        except sr.RequestError:
            return "erro ao se conectar"

    def animar_fala(self):
        if not self.animando:
            return
        self.face.falando()
        self.root.after(300, lambda: self.face.neutro())
        self.root.after(600, self.animar_fala)

    async def falar_async(self, texto):
        with self.lock:
            os.makedirs("temp_audio", exist_ok=True)
            nome_arquivo = os.path.join("temp_audio", f"fala_{uuid.uuid4().hex}.mp3")
            communicate = edge_tts.Communicate(texto, voice="pt-BR-AntonioNeural", rate="+20%")
            await communicate.save(nome_arquivo)

            self.animando = True
            self.animar_fala()

            playsound.playsound(nome_arquivo)
            os.remove(nome_arquivo)
            self.animando = False
            self.root.after(0, self.face.neutro)

    def falar(self, texto):
        asyncio.run(self.falar_async(texto))

if __name__ == "__main__":
    root = tk.Tk()
    app = TheoApp(root)
    root.mainloop()
