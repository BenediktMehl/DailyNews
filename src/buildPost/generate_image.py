from PIL import Image, ImageDraw, ImageFont, ImageColor
from datetime import datetime
from pilmoji import Pilmoji
import textwrap


def create_image(news_topics, output_dir):
    logo_path = 'assets/logo_no_background.png'

    logo = Image.open(logo_path)
    logo_size = 150
    logo = logo.resize((logo_size, logo_size))

    img_size = 1024
    extra_top_padding = 40
    top_section_height = 330
    gradient_height = 10
    img = Image.new('RGB', (img_size, img_size + extra_top_padding), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)

    draw.rectangle(
        [(0, top_section_height + gradient_height), (img_size, img_size + extra_top_padding)],
        fill=(200, 200, 200)
    )

    gradient_colors = ["#080573", "#570691", "#bf0be3", "#ffffff"]
    num_colors = len(gradient_colors) - 1
    for x in range(img_size):
        ratio = x / img_size
        segment = int(ratio * num_colors)
        segment_ratio = (ratio * num_colors) - segment
        r1, g1, b1 = ImageColor.getrgb(gradient_colors[segment])
        r2, g2, b2 = ImageColor.getrgb(gradient_colors[segment + 1])
        r = int(r1 + (r2 - r1) * segment_ratio)
        g = int(g1 + (g2 - g1) * segment_ratio)
        b = int(b1 + (b2 - b1) * segment_ratio)
        draw.line([(x, top_section_height), (x, top_section_height + gradient_height)], fill=(r, g, b))

    padding = 60
    bold_font = ImageFont.truetype("assets/arialBold.ttf", 70)
    draw.text((padding, padding + extra_top_padding), "Your Daily News Update", fill="white", font=bold_font)

    date_font = ImageFont.truetype("assets/arial.ttf", 40)
    today_date = datetime.now().strftime("%Y-%m-%d")
    draw.text((padding, padding + 80 + extra_top_padding), today_date, fill="white", font=date_font)

    headline_font = ImageFont.truetype("assets/arial.ttf", 50)
    max_width = 35
    text_start_offset = padding + 80
    news_section_start = top_section_height + gradient_height + extra_top_padding + 50

    with Pilmoji(img) as pilmoji:
        for i, topic in enumerate(news_topics):
            icon = topic.get("icon", "")
            headline = topic.get("headline", "No headline")

            wrapped_headline = textwrap.fill(headline, width=max_width)

            pilmoji.text(
                (padding, news_section_start + i * 160),
                icon,
                fill="black",
                font=headline_font
            )

            pilmoji.text(
                (text_start_offset, news_section_start + i * 160),
                wrapped_headline,
                fill="black",
                font=headline_font
            )

    img.paste(
        logo,
        (img_size - logo.width - padding + 40, img_size - logo.height - padding + 50),
        logo
    )

    watermark_font = ImageFont.truetype("assets/arial.ttf", 25)
    watermark_text = "@Daily Software Development WhatsApp Channel"
    draw.text(
        (padding, img_size + extra_top_padding - 30),
        watermark_text,
        fill="white",
        font=watermark_font
    )

    file_path = f"{output_dir}/image.png"
    img.save(file_path)
    print(f"Image saved successfully to {file_path}")
