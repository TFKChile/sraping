import tkinter as tk
from tkinter import messagebox
from main import start_scraping

def create_gui():
    root = tk.Tk()
    root.title("Twitter Scraper")

    tk.Label(root, text="Link Post del Twitter:").grid(row=0, column=0, padx=10, pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=10)

    def on_scrape_button_click():
        tweet_url = url_entry.get().strip()
        if not tweet_url:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un Link")
        else:
            start_scraping(tweet_url)

    scrape_button = tk.Button(root, text="Iniciar Scraping", command=on_scrape_button_click)
    scrape_button.grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
