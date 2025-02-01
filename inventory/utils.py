import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os

class BarcodeGenerator:
    @staticmethod
    def generate_ean13(value):
        """Génère un code-barres EAN13 valide"""
        # Compléter avec des zéros si nécessaire
        value = str(value).zfill(12)
        
        # Calculer le chiffre de contrôle
        total = 0
        for i in range(12):
            if i % 2 == 0:
                total += int(value[i])
            else:
                total += int(value[i]) * 3
        check_digit = (10 - (total % 10)) % 10
        
        # Ajouter le chiffre de contrôle
        return value + str(check_digit)

    @staticmethod
    def generate_barcode_image(ean, product_name, price):
        """Génère une image du code-barres avec le nom du produit et le prix"""
        # Générer le code-barres EAN13
        EAN = barcode.get_barcode_class('ean13')
        ean13 = EAN(ean, writer=ImageWriter())
        
        # Créer une image avec espace pour le texte
        options = {
            'module_height': 15.0,
            'module_width': 0.8,
            'quiet_zone': 6.0,
            'font_size': 12,
            'text_distance': 5.0,
        }
        
        # Générer l'image du code-barres
        buffer = BytesIO()
        ean13.write(buffer, options=options)
        
        # Ouvrir l'image avec PIL
        image = Image.open(buffer)
        
        # Créer une nouvelle image plus grande pour ajouter le texte
        new_image = Image.new('RGB', (image.width, image.height + 40), 'white')
        new_image.paste(image, (0, 20))
        
        # Ajouter le texte
        draw = ImageDraw.Draw(new_image)
        
        # Utiliser une police système par défaut
        try:
            font = ImageFont.truetype('arial.ttf', 12)
        except:
            font = ImageFont.load_default()
        
        # Ajouter le nom du produit et le prix
        product_text = f"{product_name[:30]}..." if len(product_name) > 30 else product_name
        price_text = f"{price:.2f} €"
        
        # Centrer le texte
        w, h = draw.textsize(product_text, font=font)
        draw.text(((new_image.width - w) / 2, 5), product_text, fill='black', font=font)
        
        w, h = draw.textsize(price_text, font=font)
        draw.text(((new_image.width - w) / 2, new_image.height - h - 5), 
                 price_text, fill='black', font=font)
        
        # Sauvegarder dans un nouveau buffer
        output = BytesIO()
        new_image.save(output, format='PNG')
        output.seek(0)
        
        return output

    @staticmethod
    def generate_product_label(product):
        """Génère une étiquette pour un produit donné"""
        return BarcodeGenerator.generate_barcode_image(
            product.barcode,
            f"{product.name} - {product.size} {product.color}",
            product.price
        )