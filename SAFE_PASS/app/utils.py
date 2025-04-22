import random
import string
import datetime
from passlib.hash import sha256_crypt
import matplotlib.pyplot as plt


def analyze_password(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 30
    else:
        feedback.append("Şifrenizin uzunluğu en az 12 karakter olmalıdır.")

    if any(char.isupper() for char in password):
        score += 20
    else:
        feedback.append("En az bir büyük harf kullanmalısınız.")

    if any(char.islower() for char in password):
        score += 20
    else:
        feedback.append("En az bir küçük harf kullanmalısınız.")

    if any(char.isdigit() for char in password):
        score += 15
    else:
        feedback.append("En az bir rakam kullanmalısınız.")

    if any(char in string.punctuation for char in password):
        score += 15
    else:
        feedback.append("En az bir özel karakter kullanmalısınız.")

    if score >= 80:
        feedback.append("Şifreniz çok güçlü!")
    elif score >= 60:
        feedback.append("Şifreniz güçlü sayılır.")
    else:
        feedback.append("Şifrenizi güçlendirmek için önerileri dikkate alınız.")

    return score, feedback


def get_password_strength_feedback(password):
    score, feedback = analyze_password(password)
    return feedback


def generate_strong_password(length=14):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(random.choice(all_chars) for _ in range(length))
        score, _ = analyze_password(password)
        if score >= 80:
            return password


def generate_password_from_keywords(keywords):
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password = ""
    for word in keywords:
        word = word.capitalize()
        word += random.choice(special_chars)
        password += word
    password += str(random.randint(10, 99))
    score, _ = analyze_password(password)
    if score < 80:
        password += random.choice(special_chars)
    return password


def save_password_to_history(
    username, password, score, file_path="data/password_report.csv"
):
    hashed_password = sha256_crypt.hash(password)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{username},{hashed_password},{score},{timestamp}\n")


def check_repeating_patterns(username, password, file_path="data/password_report.csv"):
    raw_passwords = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 4 and data[0] == username:
                    raw_passwords.append(
                        data[1]
                    )  # Hashli ama örüntü takibi için gösterim
    except FileNotFoundError:
        return []

    warnings = []
    if len(raw_passwords) >= 2:
        last_passwords = raw_passwords[-3:]
        repeat_count = sum(1 for p in last_passwords if password[-3:] in p)
        if repeat_count >= 2:
            warnings.append("Dikkat: Şifreleriniz benzer yapıya sahip olabilir.")
    return warnings


def check_pwned_password(password):
    import hashlib
    import requests

    sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]
    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        if response.status_code == 200:
            hashes = (line.split(":") for line in response.text.splitlines())
            return any(h.startswith(suffix) for h, _ in hashes)
    except Exception:
        pass
    return False


def show_password_score_graph(username, file_path="data/password_report.csv"):
    timestamps = []
    scores = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 4 and data[0] == username:
                    try:
                        score = int(data[2])
                        timestamp = data[3]
                        scores.append(score)
                        timestamps.append(timestamp)
                    except ValueError:
                        continue

        if not scores:
            print("Grafik oluşturmak için yeterli veri yok.")
            return

        if len(timestamps) != len(scores):
            print("Veri uyumsuzluğu: Zaman damgaları ve skor sayısı eşleşmiyor.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, scores, marker="o")
        plt.title(f"{username} Kullanıcısının Şifre Skor Gelişimi")
        plt.xlabel("Tarih")
        plt.ylabel("Şifre Skoru")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()
    except FileNotFoundError:
        print("Şifre geçmişi bulunamadı. Grafik oluşturulamadı.")