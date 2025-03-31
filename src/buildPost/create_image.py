from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pilmoji import Pilmoji
import textwrap  # Import textwrap for wrapping text


def create_image(news_topics, output_dir):
    logo_path = 'assets/logo_no_background.png'

    # Load the logo
    logo = Image.open(logo_path)
    logo_size = 100  # Set the logo size to 100x100 pixels
    logo = logo.resize((logo_size, logo_size))

    # Create a new image
    img_size = 1024  # Set the image size to 1024x1024 pixels for a square image
    img = Image.new('RGB', (img_size, img_size), color=(128, 0, 128))
    draw = ImageDraw.Draw(img)

    # Create a horizontal gradient background (left-to-right) at the top
    top_gradient_height = 300  # Height of the gradient section
    for x in range(img_size):
        r = 123 + (34 - 123) * x / img_size
        g = 6 + (6 - 6) * x / img_size
        b = 244 + (63 - 244) * x / img_size
        draw.line([(x, 0), (x, top_gradient_height)], fill=(int(r), int(g), int(b)))

    # Fill the bottom section with dark grey for the headlines
    headline_section_top = top_gradient_height
    draw.rectangle(
        [(0, headline_section_top), (img_size, img_size)],
        fill=(50, 50, 50)  # Dark grey color
    )

    # Define padding
    left_padding = 80  # Increased padding for the left
    top_padding = 60   # Significantly increased padding for the top

    # Add headline with updated padding and larger font size
    bold_font = ImageFont.truetype("assets/arialBold.ttf", 55)
    draw.text((left_padding, top_padding), "Your daily software news update", fill="white", font=bold_font)

    # Add date with updated padding and larger font size
    date_font = ImageFont.truetype("assets/arial.ttf", 30)  # Increased font size for the date
    today_date = datetime.now().strftime("%Y-%m-%d")
    draw.text((left_padding, top_padding + 80), today_date, fill="white", font=date_font)

    # Add news topics dynamically using Pilmoji for colored emojis
    headline_font = ImageFont.truetype("assets/arial.ttf", 40)
    max_width = 40
    text_start_offset = left_padding + 60
    headline_section_top_offset = headline_section_top + 250

    with Pilmoji(img) as pilmoji:
        for i, topic in enumerate(news_topics):
            # Add icon and headline
            icon = topic.get("icon", "")
            headline = topic.get("headline", "No headline")

            # Wrap the headline text
            wrapped_headline = textwrap.fill(headline, width=max_width)

            # Render the icon
            pilmoji.text(
                (left_padding, headline_section_top_offset + i * 120),  # Position for the icon
                icon,
                fill="white",
                font=headline_font
            )

            # Render the wrapped headline, starting after the icon
            pilmoji.text(
                (text_start_offset, headline_section_top_offset + i * 120),  # Position for the text
                wrapped_headline,
                fill="white",
                font=headline_font
            )

    # Place the logo in the lower right corner with a smaller margin
    margin = 20  # Margin from the edges
    img.paste(
        logo,
        (img.width - logo.width - margin, img.height - logo.height - margin),
        logo
    )

    # Save the image
    file_path = f"{output_dir}/image.png"
    img.save(file_path)
    print(f"Image saved successfully to {file_path}")
