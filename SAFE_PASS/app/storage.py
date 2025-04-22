# storage.py
import csv
import os


# --------------------------------------------------
# KULLANICILAR
# --------------------------------------------------
def load_users(file_path="/data/users.csv"):
    users = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8-sig") as f:
            for row in csv.reader(f):
                if len(row) >= 2:
                    users.append({"username": row[0], "password_hash": row[1]})
    return users


def save_user(
    username, hashed_password, _feedback, _status, file_path="data/users.csv"
):
    with open(file_path, "a", encoding="utf-8") as f:
        csv.writer(f).writerow([username, hashed_password])


def check_password_exists(username, hashed_password, file_path="data/users.csv"):
    return any(
        u["username"] == username and u["password_hash"] == hashed_password
        for u in load_users(file_path)
    )


def delete_user(
    username, users_path="data/users.csv", hist_path="data/password_report.csv"
):
    # users.csv güncelle
    users = [u for u in load_users(users_path) if u["username"] != username]
    with open(users_path, "w", encoding="utf-8") as f:
        w = csv.writer(f)
        for u in users:
            w.writerow([u["username"], u["password_hash"]])

    # şifre geçmişinden temizle
    if os.path.exists(hist_path):
        with open(hist_path, "r", encoding="utf-8") as f:
            lines = [ln for ln in f if not ln.startswith(username + ",")]
        with open(hist_path, "w", encoding="utf-8") as f:
            f.writelines(lines)


# --------------------------------------------------
# ŞİFRE GEÇMİŞİ
# --------------------------------------------------
def load_password_history(username, file_path="data/password_report.csv"):
    """
    CSV Düzeni: kullanıcı, hashli_şifre, skor, tarih
    """
    history = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for ln in f:
                row = ln.strip().split(",")
                # en az 4 sütun ve doğru kullanıcı
                if len(row) >= 4 and row[0] == username:
                    try:
                        history.append(
                            {
                                "password": row[1],  # hash
                                "score": int(row[2]),  # ✓ skor artık row[2]
                                "timestamp": row[3],
                            }
                        )
                    except ValueError:
                        # skor int'e dönüşmezse satırı atla
                        continue
    except FileNotFoundError:
        pass
    return history


def filter_passwords(username, level, file_path="data/password_report.csv"):
    """
    level: 'zayıf' (<60)  |  'orta' (60‑79)  |  'güçlü' (>=80)
    """
    filtered = []
    for entry in load_password_history(username, file_path):
        sc = entry["score"]
        if (
            (level == "zayıf" and sc < 60)
            or (level == "orta" and 60 <= sc < 80)
            or (level == "güçlü" and sc >= 80)
        ):
            filtered.append(entry)
    return filtered


def clear_password_history(username, file_path="data/password_report.csv"):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.startswith(username + ",")]
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)