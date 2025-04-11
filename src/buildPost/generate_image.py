from PIL import Image, ImageDraw, ImageFont, ImageColor
from datetime import datetime
from pilmoji import Pilmoji
import textwrap


def create_image(news_topics, output_dir):
    logo_path = 'assets/logo_no_background.png'
    bold_font_path = "assets/arialBold.ttf"
    regular_font_path = "assets/arial.ttf"

    img_size = 1024
    extra_top_padding = 40
    top_section_height = 330
    gradient_height = 10
    padding = 60
    logo_size = 120
    headline_spacing = 160

    logo = Image.open(logo_path).resize((logo_size, logo_size))

    img = Image.new('RGB', (img_size, img_size + extra_top_padding), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)

    draw.rectangle(
        [(0, top_section_height + gradient_height), (img_size, img_size + extra_top_padding)],
        fill=(255, 255, 255)
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

    bold_font = ImageFont.truetype(bold_font_path, 70)
    regular_font = ImageFont.truetype(regular_font_path, 40)
    draw.text((padding, padding + extra_top_padding), "Your Daily News Update", fill="white", font=bold_font)
    today_date = datetime.now().strftime("%Y-%m-%d")
    draw.text((padding, padding + 80 + extra_top_padding), today_date, fill="white", font=regular_font)

    headline_font = ImageFont.truetype(regular_font_path, 50)
    max_width = 35
    text_start_offset = padding + 80
    news_section_start = top_section_height + gradient_height + extra_top_padding + 50

    with Pilmoji(img) as pilmoji:
        for i, topic in enumerate(news_topics):
            icon = topic.get("icon", "")
            headline = topic.get("headline", "No headline")
            wrapped_headline = textwrap.fill(headline, width=max_width)

            pilmoji.text(
                (padding, news_section_start + i * headline_spacing),
                icon,
                fill="black",
                font=headline_font
            )
            pilmoji.text(
                (text_start_offset, news_section_start + i * headline_spacing),
                wrapped_headline,
                fill="black",
                font=headline_font
            )

    logo_position = (img_size - logo.width - padding + 40, img_size - logo.height - padding + 50)

    # Create a fading circle behind the logo
    circle_diameter = logo_size + 0
    circle_radius = circle_diameter // 2
    circle_center = (logo_position[0] + logo.width // 2, logo_position[1] + logo.height // 2)
    for y in range(circle_diameter):
        for x in range(circle_diameter):
            dx = x - circle_radius
            dy = y - circle_radius
            distance = (dx**2 + dy**2)**0.5
            if distance <= circle_radius:
                fade_ratio = distance / circle_radius
                r1, g1, b1 = (0, 0, 0)  # Black
                r2, g2, b2 = (68, 0, 173)  # Purple
                r = int(r1 + (r2 - r1) * fade_ratio)
                g = int(g1 + (g2 - g1) * fade_ratio)
                b = int(b1 + (b2 - b1) * fade_ratio)
                draw.point((circle_center[0] - circle_radius + x, circle_center[1] - circle_radius + y), fill=(r, g, b))

    img.paste(logo, logo_position, logo)

    watermark_text = "@Daily Software Development WhatsApp Channel"
    watermark_font = ImageFont.truetype(regular_font_path, 25)
    watermark_position = (padding, img_size + extra_top_padding - 30)
    draw.text(watermark_position, watermark_text, fill="white", font=watermark_font)

    file_path = f"{output_dir}/image.png"
    img.save(file_path)
    print(f"Image saved successfully to {file_path}")
