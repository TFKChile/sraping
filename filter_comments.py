from langdetect import detect, LangDetectException

def is_spanish(text):
    try:
        return detect(text) == 'es'
    except LangDetectException:
        return False

def filter_spanish_comments(comments):
    return [comment for comment in comments if is_spanish(comment)]

if __name__ == "__main__":
    # Ejemplo de uso
    sample_comments = [
        "Este es un comentario en español.",
        "This is an English comment.",
        "Otro comentario en español.",
        "Un autre commentaire en français."
    ]
    filtered_comments = filter_spanish_comments(sample_comments)
    for comment in filtered_comments:
        print(comment)
