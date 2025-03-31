from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pilmoji import Pilmoji
import textwrap 


def create_image(news_topics, output_dir):
    logo_path = 'assets/logo_no_background.png'

    logo = Image.open(logo_path)
    logo_size = 150 
    logo = logo.resize((logo_size, logo_size))

    img_size = 1024 
    img = Image.new('RGB', (img_size, img_size), color=(128, 0, 128))
    draw = ImageDraw.Draw(img)

    top_gradient_height = 300 
    for x in range(img_size):
        r = 123 + (34 - 123) * x / img_size
        g = 6 + (6 - 6) * x / img_size
        b = 244 + (63 - 244) * x / img_size
        draw.line([(x, 0), (x, top_gradient_height)], fill=(int(r), int(g), int(b)))

    headline_section_top = top_gradient_height
    draw.rectangle(
        [(0, headline_section_top), (img_size, img_size)],
        fill=(50, 50, 50)
    )

    padding = 60

    bold_font = ImageFont.truetype("assets/arialBold.ttf", 70) 
    draw.text((padding, padding), "Your Daily News Update", fill="white", font=bold_font)

    date_font = ImageFont.truetype("assets/arial.ttf", 40)
    today_date = datetime.now().strftime("%Y-%m-%d")
    draw.text((padding, padding + 80), today_date, fill="white", font=date_font)

    headline_font = ImageFont.truetype("assets/arial.ttf", 50) 
    max_width = 35
    text_start_offset = padding + 80
    headline_section_top_offset = headline_section_top + 100

    with Pilmoji(img) as pilmoji:
        for i, topic in enumerate(news_topics):
            icon = topic.get("icon", "")
            headline = topic.get("headline", "No headline")

            wrapped_headline = textwrap.fill(headline, width=max_width)

            pilmoji.text(
                (padding, headline_section_top_offset + i * 160), 
                icon,
                fill="white",
                font=headline_font
            )

            pilmoji.text(
                (text_start_offset, headline_section_top_offset + i * 160), 
                wrapped_headline,
                fill="white",
                font=headline_font
            )

    img.paste(
        logo,
        (img.width - logo.width - padding + 40, img.height - logo.height - padding + 40),
        logo
    )

    file_path = f"{output_dir}/image.png"
    img.save(file_path)
    print(f"Image saved successfully to {file_path}")