from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pilmoji import Pilmoji
import textwrap  # Import textwrap for wrapping text


def create_image(news_topics):
    logo_path = 'assets/logo_no_background.png'

    # Load the logo
    logo = Image.open(logo_path)
    logo_size = 100  # Set the logo size to 100x100 pixels
    logo = logo.resize((logo_size, logo_size))

    # Create a new image with a purple background
    img_size = 1024  # Set the image size to 1024x1024 pixels for a square image
    img = Image.new('RGB', (img_size, img_size), color=(128, 0, 128))
    draw = ImageDraw.Draw(img)

    # Create a vertical gradient background from dark purple to lighter purple
    bottom_color = (34, 6, 63)  # Dark purple
    top_color = (123, 6, 244)  # Lighter purple
    for i in range(img_size):
        r = top_color[0] + (bottom_color[0] - top_color[0]) * i / img_size
        g = top_color[1] + (bottom_color[1] - top_color[1]) * i / img_size
        b = top_color[2] + (bottom_color[2] - top_color[2]) * i / img_size
        draw.line([(0, i), (img_size, i)], fill=(int(r), int(g), int(b)))

    # Define padding
    left_padding = 80  # Increased padding for the left
    top_padding = 60   # Significantly increased padding for the top

    # Add headline with updated padding and larger font size
    bold_font = ImageFont.truetype("assets/arialBold.ttf", 55)  # Increased font size to 60
    draw.text((left_padding, top_padding), "Your daily software news update", fill="white", font=bold_font)

    # Add date with updated padding and larger font size
    date_font = ImageFont.truetype("assets/arial.ttf", 30)  # Increased font size for the date
    today_date = datetime.now().strftime("%Y-%m-%d")
    draw.text((left_padding, top_padding + 80), today_date, fill="white", font=date_font)

    # Add news topics dynamically using Pilmoji for colored emojis
    headline_font = ImageFont.truetype("assets/arial.ttf", 50)  # Increased font size for news topics
    max_width = 30  # Maximum number of characters per line
    text_start_offset = left_padding + 100  # Offset for text after the icon (adjust as needed)

    with Pilmoji(img) as pilmoji:
        for i, topic in enumerate(news_topics):
            # Add icon and headline
            icon = topic.get("icon", "")
            headline = topic.get("headline", "No headline")

            # Wrap the headline text
            wrapped_headline = textwrap.fill(headline, width=max_width)

            # Render the icon
            pilmoji.text(
                (left_padding, top_padding + 400 + i * 160),  # Position for the icon
                icon,
                fill="white",
                font=headline_font
            )

            # Render the wrapped headline, starting after the icon
            pilmoji.text(
                (text_start_offset, top_padding + 400 + i * 160),  # Position for the text
                wrapped_headline,
                fill="white",
                font=headline_font
            )

    # Place the logo in the lower right corner
    img.paste(logo, (img.width - logo.width - left_padding, img.height - logo.height - left_padding), logo)

    return img
