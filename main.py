from prompt_toolkit import PromptSession, shortcuts, validation, styles
import json
from PIL import Image, ImageFont, ImageDraw
import os
from datetime import datetime
import calendar

class DayValidator(validation.Validator):
    def __init__(self, month, year):
        self.month = month
        self.year = year

    def validate(self, document):
        try:
            text = document.text
            day = int(text)
            return 1 <= day <= calendar.monthrange(self.year, self.month)[1]
        except ValueError:
            return False

# Function to prompt for input with default values
def prompt_with_default(config_session, prompt, default_value):
    return config_session.prompt(f"{prompt} (default: {default_value}): ") or default_value

# Function to handle the entire configuration process
def handle_configuration(default_options, config_file_path):
    config_session = PromptSession()
    defaults = {}

    try:
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
        
        if not config_data.get('name'):
            # Prompt the user for Event Organizer name and store in defaults
            defaults['name'] = config_session.prompt('Event Organizer name: ')
        if not config_data.get('designation'):
            # Prompt the user for Event Organizer Designation and store in defaults
            defaults['designation'] = config_session.prompt('Event Organizer Designation: ')

        # Find missing keys
        missing_keys = [key for key in default_options.keys() if key not in config_data]
        new_data = {}

        if missing_keys:
            print(f"Missing keys: {', '.join(missing_keys)}")
            print("Running config_session.")

            # Your code to handle certificate generation using config_session goes here
            new_data = {key: prompt_with_default(config_session, f"Enter {key}", default_options[key]) for key in missing_keys}

        # Update the config.json file with new data
        with open(config_file_path, 'w') as config_file:
            json.dump({**defaults, **config_data, **new_data}, config_file, indent=2)

    except FileNotFoundError:
        print(f"{config_file_path} not found. Running config_session.")

        # Prompt the user for Event Organizer name and store in defaults
        defaults['name'] = config_session.prompt('Event Organizer name: ')
        # Prompt the user for Event Organizer Designation and store in defaults
        defaults['designation'] = config_session.prompt('Event Organizer Designation: ')

        # Your code to handle certificate generation using config_session goes here
        new_data = {key: prompt_with_default(config_session, f"Enter {key}", default_options[key]) for key in default_options.keys()}

        # Create a new config.json file with data from config_session and default options
        with open(config_file_path, 'w') as config_file:
            json.dump({**defaults, **default_options, **new_data}, config_file, indent=2)

# Define default options
default_options = {
    'size': 120,
    'color': '#000000',
    'signature': 'assets/signature.png',
    'template': 'assets/template.jpg',
    'title_font': 'assets/fonts/GlacialIndifference-Bold.otf',
    'font': 'assets/fonts/GlacialIndifference-Regular.otf',
    'out': 'out/'
}

# Specify the config file path
config_file_path = 'config.json'

# Call the function to handle the configuration process
handle_configuration(default_options, config_file_path)

with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

def get_text_dimensions(text_string, font):
    _, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return text_width, text_height

def make_certificate(name, description_lines, output_path=config.get('out'), font_size=config.get('size'), font_color=config.get('color')):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    title_font = ImageFont.truetype(config.get('title_font'), font_size)
    description_font = ImageFont.truetype(config.get('font'), int(font_size * 0.40))
    date_font = ImageFont.truetype(config.get('font'), int(font_size * 0.32))

    with Image.open(config.get('template')) as template:
        WIDTH, HEIGHT = template.size
        draw = ImageDraw.Draw(template)
        name_width, name_height = get_text_dimensions(name, title_font)

        draw.text(((WIDTH - name_width) / 2, (HEIGHT - name_height) / 2 - 85), name, fill=font_color, font=title_font)

        max_lines = 3
        total_description_height = 0

        for i, line in enumerate(description_lines[:max_lines]):
            line_width, line_height = get_text_dimensions(line, description_font)
            total_description_height += line_height
            draw.text(((WIDTH - line_width) / 2, (HEIGHT + name_height) / 2 + 10 + i * (line_height)), line, fill=font_color, font=description_font)

        with Image.open(config.get('signature')) as signature:
            
            target_signature_size = (1300, 80)
            signature.thumbnail(target_signature_size, Image.Resampling.LANCZOS)
            SIG_WIDTH, SIG_HEIGHT = target_signature_size
            signature_mask = signature.convert("RGBA")

            # Calculate the coordinates as integers
            paste_coordinates = (
            int((WIDTH - SIG_WIDTH) / 1.2),
            int((HEIGHT - SIG_HEIGHT) / 1.2)
            )

            # Paste the signature onto the main template using the mask
            template.paste(signature, paste_coordinates, signature_mask)

        lead = config.get('name')
        lead_width, _ = get_text_dimensions(lead, date_font)
        draw.text(((WIDTH - lead_width) / 3, HEIGHT - 200), lead, fill=font_color, font=date_font)

        lead_description = config.get('designation')
        lead_description_width, _ = get_text_dimensions(lead_description, date_font)
        draw.text(((WIDTH - lead_description_width) / 3, HEIGHT - 160), lead_description, fill=font_color, font=date_font)

        date = datetime.now().strftime("%b %d, %Y")
        date_width, _ = get_text_dimensions(date, date_font)
        draw.text(((WIDTH - date_width) / 1.5, HEIGHT - 290), date, fill=font_color, font=date_font)

        output_file = os.path.join(output_path, f"{name.title().replace(' ', '_')}_Certificate.jpg")

        try:
            template.save(output_file)
        except Exception as e:
            print(f'Error saving certificate for {name}: {e}')

if __name__ == "__main__":
    session = PromptSession()

    event_name = session.prompt("Name of the Event: ")
    year = int(session.prompt("Year of the Event: "))
    month = int(session.prompt("Month of the Event: "))

    # Ensure the provided date is valid for the given month and year
    max_day = calendar.monthrange(year, month)[1]
    # Create a Validator from the is_valid_day function
    day_validator = DayValidator(month, year)
    date = int(session.prompt(f"Date of the Event (1-{max_day}): ", validator=day_validator , validate_while_typing=True))

    event_date = datetime(year, month, date).strftime("%b %d, %Y")
    description_lines = [
        "for their active participation and enthusiasm during {} conducted on {}".format(event_name, event_date)
    ]

    with open("random_names.txt", "r") as file:
        names = [line.strip() for line in file]

    style = styles.Style.from_dict({
        'label': 'bg:#1a1b26 #61afef',
        'percentage': 'bg:#1a1b26 #61afef',
        'current': '#61afef',
        'bar': '#61afef',
    })

    formatters = shortcuts.progress_bar.formatters

    custom_formatters = [
        formatters.Label(),
        formatters.Text(': [', style='class:percentage'),
        formatters.Percentage(),
        formatters.Text(']', style='class:percentage'),
        formatters.Text(' '),
        formatters.Bar(sym_a='#', sym_b='#', sym_c='.'),
        formatters.Text('  '),
    ]

    with shortcuts.ProgressBar(style=style, formatters=custom_formatters) as pb:
        for name in pb(names, label='Generating Certificates'):
            make_certificate(name.upper(), description_lines)
