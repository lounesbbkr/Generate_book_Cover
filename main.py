import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont

# Modèles de couverture (ajoute tes propres images dans le dossier 'templates')
TEMPLATES = {
    "Fantasy": "templates/fantasy.jpg",
    "Romance": "templates/romance.jpg",
    "Mystery": "templates/mystery.jpg",
    "Science-Fiction": "templates/scifi.jpg",
    "Non-Fiction": "templates/nonfiction.jpg",
}

# Configuration des polices
FONT_PATH = "arial.ttf"  # Utilise une police système ou fournis ton propre fichier .ttf
TITLE_FONT_SIZE = 40
AUTHOR_FONT_SIZE = 30

class BookCoverGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Cover Generator")
        self.root.geometry("400x300")

        # Variables
        self.selected_template = tk.StringVar(value=list(TEMPLATES.keys())[0])
        self.title_text = tk.StringVar()
        self.author_text = tk.StringVar()

        # Interface utilisateur
        tk.Label(root, text="Select Template:").pack()
        template_menu = tk.OptionMenu(root, self.selected_template, *TEMPLATES.keys())
        template_menu.pack()

        tk.Label(root, text="Book Title:").pack()
        tk.Entry(root, textvariable=self.title_text).pack()

        tk.Label(root, text="Author Name:").pack()
        tk.Entry(root, textvariable=self.author_text).pack()

        tk.Button(root, text="Generate Cover", command=self.generate_cover).pack()

    def generate_cover(self):
        # Récupère les entrées de l'utilisateur
        template_name = self.selected_template.get()
        title = self.title_text.get()
        author = self.author_text.get()

        # Vérifie que les champs sont remplis
        if not title or not author:
            messagebox.showerror("Error", "Please enter both title and author.")
            return

        # Charge le modèle sélectionné
        template_path = TEMPLATES[template_name]
        try:
            image = Image.open(template_path)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Template '{template_name}' not found.")
            return

        # Ajoute le texte sur l'image
        draw = ImageDraw.Draw(image)
        title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)
        author_font = ImageFont.truetype(FONT_PATH, AUTHOR_FONT_SIZE)

        # Position du texte
        width, height = image.size
        title_position = (width // 2, height // 2 - 50)
        author_position = (width // 2, height // 2 + 20)

        # Dessine le texte
        draw.text(title_position, title, font=title_font, fill="white", anchor="mm")
        draw.text(author_position, author, font=author_font, fill="white", anchor="mm")

        # Enregistre la couverture générée
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if save_path:
            image.save(save_path)
            messagebox.showinfo("Success", f"Cover saved to {save_path}")

# Lance l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = BookCoverGenerator(root)
    root.mainloop()
