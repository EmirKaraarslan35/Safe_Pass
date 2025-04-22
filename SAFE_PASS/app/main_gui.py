
import sys
import os

def resource_path(relative_path):
    """ .exe'de de .py'de de dosya yollarını doğru verir """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)

import json
import os, sys, locale

os.environ["LC_ALL"] = "C"
os.environ["LANG"] = "C"
locale.setlocale = lambda cat, loc=None: "C"

import tkinter as tk
import ttkbootstrap as tb
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from tkinter import ttk, messagebox
from ttkbootstrap.widgets import Label, Entry, Button, Frame
import csv
import hashlib
from passlib.hash import sha256_crypt
import random
import string
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MainPanel(Frame):
    def __init__(self, master, username, app):
        super().__init__(master)
        self.master = master
        self.username = username
        self.app = app
        self.pack(fill="both", expand=True)
        self.active_frame = None

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar = ttk.Frame(self.main_frame, width=250)
        self.sidebar.pack(side="left", fill="y")

        self.content = ttk.Frame(self.main_frame)
        self.content.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.show_welcome()

    
    def create_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo_light.png")
            if os.path.exists(logo_path):
                image = Image.open(logo_path)
                image = image.resize((80, 80))  
                self.sidebar_logo = ImageTk.PhotoImage(image)
                logo_label = Label(self.sidebar, image=self.sidebar_logo)
                logo_label.pack(pady=(20, 5))
        except Exception as e:
            print("Panel logosu yüklenemedi:", e)

        ttk.Label(
            self.sidebar,
            text=f"👋 Merhaba, {self.username}",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(10, 20))

        menu = [
            ("Şifre Analizi Yap", self.show_password_analysis),
            ("Şifre Geçmişi", self.show_password_history),
            ("Güçlü Şifre Oluştur", self.show_password_generator),
            ("Anahtar Kelimelerle Şifre", self.show_keyword_generator),
            ("Şifre Gelişim Grafiği", self.show_graph),
            ("Şifre Geçmişini Temizle", self.clear_history),
            ("Hesabımı Sil", self.delete_account),
            ("Tema Ayarları", self.show_settings),
            ("Çıkış Yap", self.logout)
        ]

        for text, action in menu:
            ttk.Button(self.sidebar, text=text, command=action).pack(
                pady=4, fill="x", padx=10
            )


    def switch_content(self, frame_func):
        if self.active_frame:
            self.active_frame.destroy()
        self.active_frame = frame_func()
        self.active_frame.pack(fill="both", expand=True)

    
    def show_welcome(self):
        def frame():
            container = ttk.Frame(self.content)
            ttk.Label(
                container,
                text="SafePASS HOŞGELDİN",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=20)
            return container
        self.switch_content(frame)

    def frame():
            container = ttk.Frame(self.content)
            ttk.Label(
                container,
                text="1. Şifre Gücü Analizi Yap",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=20)
            ttk.Label(
                container,
                text="Şifreyi Giriniz",
                font=("Segoe UI", 12),
            ).pack()
            return container

            self.switch_content(frame)

    def show_password_analysis(self):
        def frame():
            container = ttk.Frame(self.content, padding=20)
            ttk.Label(
                container,
                text="1. Şifre Analizi Yap",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=(10, 10))
            entry = ttk.Entry(container, width=40, font=("Segoe UI", 12))
            entry.pack(pady=10)
            result = ttk.Label(container, text="", font=("Segoe UI", 12))
            result.pack(pady=10)

            def analyze():
                pw = entry.get().strip()
                if not pw:
                    result.config(text="⚠️ Lütfen şifre giriniz.", foreground="orange")
                    return

                score = 0
                feedback = []

                if any(c.islower() for c in pw):
                    score += 20
                else:
                    feedback.append("En az bir küçük harf ekleyin.")

                if any(c.isupper() for c in pw):
                    score += 20
                else:
                    feedback.append("En az bir büyük harf ekleyin.")

                if any(c.isdigit() for c in pw):
                    score += 20
                else:
                    feedback.append("En az bir rakam ekleyin.")

                if any(c in "!@#$%^&*()-_+=<>?/{}[]|\:;" for c in pw):
                    score += 20
                else:
                    feedback.append("En az bir özel karakter ekleyin.")

                if len(pw) >= 12:
                    score += 20
                else:
                    feedback.append("Şifreyi en az 12 karakter yapın.")

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                hashed = sha256_crypt.hash(pw)

                if score < 40:
                    level = "🔴 Zayıf"
                    color = "red"
                elif score < 80:
                    level = "🟡 Orta"
                    color = "orange"
                else:
                    level = "🟢 Güçlü"
                    color = "green"
                result.config(
                    text=f"{level} ({score})\n" + "\n".join(feedback), foreground=color
                )

                with open(
                    os.path.join(os.path.dirname(__file__), "data", "password_report.csv"), "a", newline="", encoding="utf-8"
                ) as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:
                        writer.writerow(["username", "password", "score", "timestamp"])
                    writer.writerow([self.username, hashed, score, now])

            def clear():
                entry.delete(0, "end")
                result.config(text="")

                entry.delete(0, "end")
                result.config(text="")

            ttk.Button(
                container,
                text="Şifreyi Analiz Yap",
                bootstyle="primary",
                command=analyze,
            ).pack(pady=5)
            ttk.Button(container,
                text="Temizle", bootstyle="secondary", command=clear).pack()
            return container

        self.switch_content(frame)

    def show_password_history(self):
        def frame():
            container = ttk.Frame(self.content, padding=20)
            ttk.Label(
                container,
                text="Şifre Geçmişi",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=10)
            table_frame = ttk.Frame(container)
            table_frame.pack(fill="both", expand=True)
            columns = ("password", "score", "timestamp")
            tree = ttk.Treeview(
                table_frame, columns=columns, show="headings", height=15
            )
            for col in columns:
                tree.heading(col, text=col.capitalize())
                tree.column(col, anchor="center")
            scrollbar = ttk.Scrollbar(
                table_frame, orient="vertical", command=tree.yview
            )
            tree.configure(yscrollcommand=scrollbar.set)
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            file_path = os.path.join(os.path.dirname(__file__), "data", "password_report.csv")
            if os.path.exists(file_path):
                with open(file_path, encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if row[0] == "username":
                            continue
                        if row[0] == self.username:
                            tree.insert("", "end", values=(row[1], row[2], row[3]))
            else:
                ttk.Label(
                    container,
                    text="Anahtar Kelimeyle Şifre Oluştur",
                    foreground="red",
                ).pack()
            return container

        self.switch_content(frame)

    def show_password_generator(self):
        def frame():
            container = ttk.Frame(self.content, padding=20)
            ttk.Label(
                container,
                text="Güçlü Şifre Oluştur",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=10)
            pw_entry = ttk.Entry(container, width=40, font=("Segoe UI", 12))
            pw_entry.pack(pady=10)

            def generate_password():
                chars = string.ascii_letters + string.digits + "!@#$%^&*()-_+=<>?"
                password = "".join(random.choices(chars, k=14))
                pw_entry.delete(0, "end")
                pw_entry.insert(0, password)

            def copy_password():
                self.clipboard_clear()
                self.clipboard_append(pw_entry.get())
                messagebox.showinfo("Kopyalandı", "Şifre panoya kopyalandı.")

            ttk.Button(
                container,
                text="Oluştur",
                bootstyle="primary",
                command=generate_password,
            ).pack(pady=5)
            ttk.Button(
                container,
                text="Temizle",
                bootstyle="success",
                command=copy_password,
            ).pack(pady=5)
            return container

        self.switch_content(frame)

    def show_keyword_generator(self):
        def frame():
            container = ttk.Frame(self.content, padding=20)
            ttk.Label(
                container,
                text="Anahtar Kelimelerle Şifre",
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=10)
            keyword_entry = ttk.Entry(container, width=50, font=("Segoe UI", 12))
            keyword_entry.insert(0, "giriniz")
            keyword_entry.insert(0, "Kelimeleri ")
            keyword_entry.insert(0, "Anahtar ")
            keyword_entry.pack(pady=10)
            keyword_entry.insert(0, "")
            result_entry = ttk.Entry(container, width=50, font=("Segoe UI", 12))
            result_entry.pack(pady=10)

            def generate():
                keywords = keyword_entry.get().replace(" ", "").split(",")
                base = "".join(keywords)
                extra = "".join(
                    random.choices(string.ascii_letters + string.digits + "!@#", k=4)
                )
                combined = list(base + extra)
                random.shuffle(combined)
                password = "".join(combined)[:14]
                result_entry.delete(0, "end")
                result_entry.insert(0, password)

            def copy():
                self.clipboard_clear()
                self.clipboard_append(result_entry.get())
                messagebox.showinfo("Kopyalandı", "Şifre panoya kopyalandı.")

            def clear():
                keyword_entry.delete(0, "end")
                result_entry.delete(0, "end")

            ttk.Button(
                container,
                text="Üret",
                bootstyle="primary",
                command=generate,
            ).pack(pady=5)
            ttk.Button(
                container,
                text="Kopyala",
                bootstyle="success",
                command=copy,
            ).pack(pady=5)
            ttk.Button(
                container,
                text="Temizle",
                bootstyle="secondary",
                command=clear,
            ).pack(pady=5)
            return container

        self.switch_content(frame)

    def show_graph(self):
        def frame():
            frame = ttk.Frame(self.content)
            ttk.Label(frame, text="Şifre Gelişim Grafiği", font=("Segoe UI", 16)).pack(
                pady=10
            )
            try:
                timestamps = []
                scores = []
                with open(os.path.join(os.path.dirname(__file__), "data", "password_report.csv"), "r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if not row:
                            continue
                        if row[0] != self.username:
                            continue
                        if len(row) >= 4:
                            score = int(row[2])
                            timestamp = row[3]
                        else:
                            continue
                        timestamps.append(timestamp)
                        scores.append(score)
                fig = Figure(figsize=(8, 4), dpi=100)
                ax = fig.add_subplot(111)
                ax.plot(timestamps, scores, marker="o")
                ax.set_title("Şifre Skoru Zaman Grafiği", fontsize=12)
                ax.set_xlabel("Zaman", fontsize=10)
                ax.set_ylabel("Skor", fontsize=10)
                ax.set_ylim(0, 100)
                ax.tick_params(axis="x", labelsize=8, rotation=45)
                fig.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.draw()
                canvas.get_tk_widget().pack()
            except Exception as e:
                ttk.Label(
                    frame, text="Veri yüklenemedi: " + str(e), foreground="red"
                ).pack()
            return frame

        self.switch_content(frame)

    def clear_history(self):
        if messagebox.askyesno("Emin misiniz?", "Bu işlemi yapmak istediğinizden emin misiniz?"):
            updated_rows = []
            file_path = os.path.join(os.path.dirname(__file__), "data", "password_report.csv")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[0] != self.username:
                            updated_rows.append(row)
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(updated_rows)
                messagebox.showinfo("Tamamlandı", "İşlem başarıyla gerçekleşti.")

    def delete_account(self):
        if messagebox.askyesno("Emin misiniz?", "Bu işlemi yapmak istediğinizden emin misiniz?"):
            users_path = os.path.join(os.path.dirname(__file__), "data", "users.csv")
            if os.path.exists(users_path):
                with open(users_path, "r", encoding="utf-8") as f:
                    users = list(csv.reader(f))
                users = [row for row in users if row and row[0] != self.username]
                with open(users_path, "w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(users)
            history_path = os.path.join(os.path.dirname(__file__), "data", "password_report.csv")
            if os.path.exists(history_path):
                with open(history_path, "r", encoding="utf-8") as f:
                    records = list(csv.reader(f))
                records = [row for row in records if row and row[0] != self.username]
                with open(history_path, "w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(records)
            messagebox.showinfo("Bilgi", "İşlem tamamlandı.")
            self.pack_forget()
            self.app.geometry("600x400")
        self.app.show_entry_screen()

    def show_settings(self):

        def set_language(lang_code):

            messagebox.showinfo(
                "SAFE_PASS",
            )
            self.root.destroy()
            os.execl(sys.executable, sys.executable, *sys.argv)

        def frame():
            container = ttk.Frame(self.content, padding=20)
            ttk.Label(
                container, text="🎨 Tema Ayarları", font=("Segoe UI", 18, "bold")
            ).pack(pady=10)
            ttk.Button(
                container,
                text="Açık Tema",
                bootstyle="secondary",
                command=lambda: self.app.custom_style.theme_use("flatly"),
            ).pack(pady=5)
            ttk.Button(
                container,
                text="Koyu Tema",
                bootstyle="dark",
                command=lambda: self.app.custom_style.theme_use("darkly"),
            ).pack(pady=5)
            return container

        self.switch_content(frame)

    def logout(self):
        if messagebox.askyesno("Emin misiniz?", "Bu işlemi yapmak istediğinizden emin misiniz?"):
            self.pack_forget()
            self.app.geometry("600x400")
        self.app.show_entry_screen()




class MainApp(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.geometry("800x500")
        self.title("SAFE PASS")
        self.custom_style = Style()
        self.username = None
        self.mode = "login"
        self.content = Frame(self, padding=30)
        self.content.place(relx=0.5, rely=0.5, anchor="center")
        self.geometry("800x500")
        self.show_entry_screen()

    def show_entry_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.content = Frame(self, padding=30)
        self.content.place(relx=0.5, rely=0.5, anchor="center")
        title = "SAFEPASS" if self.mode == "login" else "KAYIT OL"
        
    
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo_light.png")
            if os.path.exists(logo_path):
                image = Image.open(logo_path)
                image = image.resize((110, 110))
                self.logo_photo = ImageTk.PhotoImage(image)
                logo_label = Label(self.content, image=self.logo_photo)
                logo_label.pack(pady=(0, 10))
        except Exception as e:
            print("Logo yüklenemedi:", e)
            
        Label(self.content, text=title, font=("Segoe UI", 20, "bold")).pack(
            pady=(0, 20)
        )
        Label(self.content, text="Kullanıcı Adı:").pack(anchor="w")
        self.username_entry = Entry(self.content, width=30)
        self.username_entry.pack(pady=(0, 10))
        Label(self.content, text="Parola:").pack(anchor="w")
        self.password_entry = Entry(self.content, show="*", width=30)
        self.password_entry.pack(pady=(0, 10))
        if self.mode == "register":
            Label(self.content, text="Parola (Tekrar):").pack(anchor="w")
            self.password_entry2 = Entry(self.content, show="*", width=30)
            self.password_entry2.pack(pady=(0, 10))
        if self.mode == "login":
            Button(
                self.content,
                text="Giriş Yap",
                bootstyle="primary",
                width=20,
                command=self.do_login,
            ).pack(pady=(10, 5))
            Button(
                self.content,
                text="Kayıt Ol",
                bootstyle="secondary",
                width=20,
                command=self.switch_to_register,
            ).pack()
        else:
            Button(
                self.content,
                text="Kaydol",
                bootstyle="success",
                width=20,
                command=self.do_register,
            ).pack(pady=(10, 5))
            Button(
                self.content,
                text="Geri Dön",
                bootstyle="secondary",
                width=20,
                command=self.switch_to_login,
            ).pack()

    def switch_to_register(self):
        self.mode = "register"
        self.geometry("800x500")
        self.show_entry_screen()

    def switch_to_login(self):
        self.mode = "login"
        self.geometry("800x500")
        self.show_entry_screen()

    
    def do_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Hata", "Lütfen kullanıcı adı ve parolayı girin.")
            return

        base_path = os.path.dirname(__file__)
        user_file = os.path.join(base_path, "data", "users.csv")

        if os.path.exists(user_file):
            with open(user_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None) 
                for row in reader:
                    if row and row[0] == username:
                        try:
                            if sha256_crypt.verify(password, row[1]):
                                self.username = username
                                self.start_main_panel()
                                return
                        except:
                            pass

        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")
    
    def do_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.password_entry2.get().strip()

        if not username or not password or not confirm:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        if password != confirm:
            messagebox.showerror("Hata", "Parolalar eşleşmiyor.")
            return

        base_path = os.path.dirname(__file__)
        user_file = os.path.join(base_path, "data", "users.csv")

        if not os.path.exists(user_file):
            with open(user_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["username", "password"])

        with open(user_file, "r", encoding="utf-8") as f:
            existing = [row for row in csv.reader(f) if row and row[0] == username]

        if existing:
            messagebox.showwarning("Uyarı", "Bu kullanıcı zaten mevcut.")
            return

        hashed = sha256_crypt.hash(password)
        with open(user_file, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([username, hashed])

        messagebox.showinfo("Başarılı", "Kayıt tamamlandı!")
        self.switch_to_login()
    
    def start_main_panel(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("900x600")
        MainPanel(self, self.username, self)


if __name__ == "__main__":
    MainApp().mainloop()