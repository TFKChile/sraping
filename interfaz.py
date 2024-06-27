import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
from main import start_scraping

def create_gui():
    root = tk.Tk()
    root.title("Twitter Scraper")

    tk.Label(root, text="Links de Twitter (uno por línea):").grid(row=0, column=0, padx=10, pady=10)
    url_text = tk.Text(root, width=50, height=10)
    url_text.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Minero:").grid(row=1, column=0, padx=10, pady=10)
    minero_entry = tk.Entry(root, width=50)
    minero_entry.grid(row=1, column=1, padx=10, pady=10)

    scrape_button = tk.Button(root, text="Iniciar Scraping", command=lambda: on_scrape_button_click(url_text, minero_entry, scrape_button, loading_label))
    scrape_button.grid(row=2, column=0, columnspan=2, pady=10)

    loading_label = ttk.Label(root, text="", foreground="green")
    loading_label.grid(row=3, column=0, columnspan=2, pady=10)

    def on_scrape_button_click(url_text, minero_entry, scrape_button, loading_label):
        tweet_urls = url_text.get("1.0", tk.END).strip().split('\n')
        minero = 'Jose Escobar'
        if not tweet_urls or not minero:
            messagebox.showwarning("Advertencia", "Por favor, ingrese los Links y el nombre del Minero")
        else:
            scrape_button.config(state=tk.DISABLED)
            loading_label.config(text="Cargando...")
            threading.Thread(target=run_scraping, args=(tweet_urls, minero, scrape_button, loading_label)).start()

    def run_scraping(tweet_urls, minero, scrape_button, loading_label):
        try:
            for tweet_url in tweet_urls:
                if tweet_url.strip():  # Verificar si la URL no está vacía
                    start_scraping(tweet_url.strip(), minero)
            messagebox.showinfo("Éxito", "El scraping se ha completado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            scrape_button.config(state=tk.NORMAL)
            loading_label.config(text="")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
