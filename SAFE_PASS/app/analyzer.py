def analyze_password(password):
    score = 0
    feedback = []

    # Uzunluk kontrolü
    if len(password) < 12:
        feedback.append("Şifreniz çok kısa, en az 12 karakter olmalı.")
    else:
        score += 25

    # Büyük harf kontrolü
    if any(char.isupper() for char in password):
        score += 25
    else:
        feedback.append("Büyük harf eklemeyi unutmayın.")

    # Küçük harf kontrolü
    if any(char.islower() for char in password):
        score += 25
    else:
        feedback.append("Küçük harf kullanmalısınız.")

    # Özel karakter kontrolü
    if any(char in "!@#$%^&*()_+" for char in password):
        score += 25
    else:
        feedback.append("Özel karakter kullanmayı deneyin.")

    return score, feedback


def get_password_strength_feedback(password):
    score, feedback = analyze_password(password)
    return feedback