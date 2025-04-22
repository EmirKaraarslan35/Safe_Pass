import os
from storage import (
    load_users,
    save_user,
    delete_user,
    check_password_exists,
    load_password_history,
    filter_passwords,
    clear_password_history,
)
from passlib.hash import sha256_crypt
from analyzer import analyze_password
from utils import (
    generate_strong_password,
    generate_password_from_keywords,
    check_repeating_patterns,
    check_pwned_password,
    save_password_to_history,
    show_password_score_graph,
)

# ⬇️ import artık klasörden geliyor


# ---------- DİL SEÇİMİ ----------
def choose_language():
    while True:
        lang_choice = input(t("lang_prompt"))
        if lang_choice == "1":
            set_lang("tr")
            break
        elif lang_choice == "2":
            set_lang("en")
            break
        else:
            print(t("invalid"))


# ---------- KAYIT ----------
def register():
    print("📌", t("register"))
    username = input("Username: ")
    password = input("Password : ")
    score, _ = analyze_password(password)
    hashed = sha256_crypt.hash(password)

    if check_password_exists(username, hashed):
        print("⚠️  Already used, choose another password.")
        return
    save_user(username, hashed, [], "Yes")
    save_password_to_history(username, password, score)
    print("✅  Registered! Please log in.\n")


# ---------- GİRİŞ ----------
def login():
    print("📌", t("login"))
    username = input("Username: ")
    password = input("Password : ")
    for u in load_users():
        if u["username"] == username and sha256_crypt.verify(
            password, u["password_hash"]
        ):
            print(f"✅  Welcome, {username}!")
            return username
    print("❌  Wrong username or password.")
    return None


# ---------- KULLANICI PANELİ ----------
def user_panel(username: str):
    while True:
        print(f"\n{t('user_panel')}")
        menu = [
            f"[1] {t('new_analysis')}",
            f"[2] {t('show_history')}",
            f"[3] {t('filter')}",
            f"[4] {t('strong_pw')}",
            f"[5] {t('keyword_pw')}",
            f"[6] {t('clear_hist')}",
            f"[7] {t('show_graph')}",
            f"[8] {t('delete_acc')}",
            f"[0] {t('change_lang')}",
            f"[9] {t('logout')}",
        ]
        print("\n".join(menu))
        choice = input(t("select_option"))

        if choice == "1":
            pw = input("Password : ")
            score, fb = analyze_password(pw)
            print("Score:", score)
            for msg in fb:
                print("-", msg)

            for w in check_repeating_patterns(username, pw):
                print("⚠️", w)
            if check_pwned_password(pw):
                print("⚠️  Found in data breaches!")

            save_password_to_history(username, pw, score)

        elif choice == "2":
            hist = load_password_history(username)
            if not hist:
                print("— history empty —")
            else:
                for h in hist:
                    print(f"- {h['password']} ({h['score']})")

        elif choice == "3":
            level = input("weak / medium / strong : ")
            for h in filter_passwords(username, level):
                print(f"- {h['password']} ({h['score']})")

        elif choice == "4":
            print("🔑", generate_strong_password())

        elif choice == "5":
            kws = input("keywords > ").split()
            print("🔑", generate_password_from_keywords(kws))

        elif choice == "6":
            if input("Confirm (E/H)? ").lower() == "e":
                clear_password_history(username)
                print("✅ History cleared.")

        elif choice == "7":
            show_password_score_graph(username)

        elif choice == "8":
            if input("Delete account (yes/no)? ").lower() == "yes":
                delete_user(username)
                print("🗑️  Account deleted.")
                break

        elif choice == "0":
            choose_language()  # dil değiştir

        elif choice == "9":
            break
        else:
            print(t("invalid"))


# ---------- ANA DÖNGÜ ----------
def main():
    choose_language()  # başlangıçta sor
    while True:
        print(f"\n{t('welcome')}")
        print(f"[1] {t('login')}")
        print(f"[2] {t('register')}")
        print(f"[3] {t('exit')}")
        sel = input(t("select_option"))

        if sel == "1":
            u = login()
            if u:
                user_panel(u)
        elif sel == "2":
            register()
        elif sel == "3":
            print("👋")
            break
        else:
            print(t("invalid"))


if __name__ == "__main__":
    main()