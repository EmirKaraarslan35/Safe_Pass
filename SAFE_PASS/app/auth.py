from utils import (
    hash_password,
    check_password_exists,
    analyze_password,
)  # Doğru fonksiyonları import ettik
import datetime
from passlib.hash import sha256_crypt


# Kullanıcı kaydını yapan fonksiyon
def register_user(username, password, file_name="data/password_report.csv"):
    # Şifreyi analiz et
    score, feedback = analyze_password(password)  # Burada doğru fonksiyon çağrılıyor

    if score < 60:
        print("Hata: Şifreniz çok zayıf. Daha güçlü bir şifre girin.")
        return False, feedback

    if check_password_exists(username, password, file_name):
        print("Hata: Bu şifre daha önce kullanılmış. Lütfen farklı bir şifre seçin.")
        return False, feedback

    print(f"Şifre Gücü: {feedback}")
    confirmation = input("Şifreniz kaydedilsin mi? (E/H): ").strip().upper()

    # Kullanıcıdan onay alın
    if confirmation == "E":
        hashed_password = hash_password(password)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(f"{username},{hashed_password},{feedback},{timestamp}\n")
        print("Şifre başarıyla kaydedildi.")
        return True, feedback
    elif confirmation == "H":
        print("Şifre kaydedilmedi.")
        return False, feedback
    else:
        print("Geçersiz giriş. Lütfen 'E' veya 'H' girin.")
        return False, feedback


# Kullanıcı girişini doğrulayan fonksiyon
def authenticate_user(username, password, file_name="data/password_report.csv"):
    with open(file_name, "r", encoding="utf-8") as file:
        reader = file.readlines()
        for line in reader:
            data = line.strip().split(",")
            if data[0] == username and sha256_crypt.verify(password, data[1]):
                return True
    return False