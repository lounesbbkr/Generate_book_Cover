import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont

# Modèles de mèmes (ajoute tes propres images dans le dossier 'templates')
TEMPLATES = {
    "Distracted Boyfriend": "templates/distracted_boyfriend.jpg",
    "Drake Hotline Bling": "templates/drake_hotline_bling.jpg",
    "Change My Mind": "templates/change_my_mind.jpg",
    "Two Buttons": "templates/two_buttons.jpg",
    "Expanding Brain": "templates/expanding_brain.jpg",
}

# Configuration des polices
FONT_PATH = "arial.ttf"  # Utilise une police système ou fournis ton propre fichier .ttf
TEXT_FONT_SIZE = 30

class MemeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Generator")
        self.root.geometry("400x400")

        # Variables
        self.selected_template = tk.StringVar(value=list(TEMPLATES.keys())[0])
        self.top_text = tk.StringVar()
        self.bottom_text = tk.StringVar()
        self.text_color = "white"
        self.text_font_size = TEXT_FONT_SIZE

        # Interface utilisateur
        tk.Label(root, text="Select Meme Template:").pack()
        template_menu = tk.OptionMenu(root, self.selected_template, *TEMPLATES.keys())
        template_menu.pack()

        tk.Label(root, text="Top Text:").pack()
        tk.Entry(root, textvariable=self.top_text).pack()

        tk.Label(root, text="Bottom Text:").pack()
        tk.Entry(root, textvariable=self.bottom_text).pack()

        tk.Label(root, text="Text Font Size:").pack()
        self.text_font_size_entry = tk.Entry(root)
        self.text_font_size_entry.insert(0, str(TEXT_FONT_SIZE))
        self.text_font_size_entry.pack()

        tk.Button(root, text="Choose Text Color", command=self.choose_text_color).pack()
        tk.Button(root, text="Generate Meme", command=self.generate_meme).pack()

    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_color = color

    def generate_meme(self):
        # Récupère les entrées de l'utilisateur
        template_name = self.selected_template.get()
        top_text = self.top_text.get()
        bottom_text = self.bottom_text.get()
        text_font_size = int(self.text_font_size_entry.get())

        # Vérifie que les champs sont remplis
        if not top_text and not bottom_text:
            messagebox.showerror("Error", "Please enter at least one text field.")
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
        font = ImageFont.truetype(FONT_PATH, text_font_size)

        # Position du texte (ajuste en fonction du mème)
        width, height = image.size
        if top_text:
            top_position = (width // 2, 10)  # En haut au centre
            draw.text(top_position, top_text, font=font, fill=self.text_color, anchor="mt")
        if bottom_text:
            bottom_position = (width // 2, height - 20)  # En bas au centre
            draw.text(bottom_position, bottom_text, font=font, fill=self.text_color, anchor="mb")

        # Enregistre le mème généré
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if save_path:
            image.save(save_path)
            messagebox.showinfo("Success", f"Meme saved to {save_path}")

# Lance l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = MemeGenerator(root)
    root.mainloop()