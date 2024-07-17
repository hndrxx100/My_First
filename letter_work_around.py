import os
from datetime import datetime
import shutil


def registrant_letter(firstname, lastname, registration_type, snack_preferences, extra_services):
    # Sample data (replace with actual data as needed)
    data = {
        'firstname': f'{firstname}',
        'lastname': f'{lastname}',
        'user_registration': f'{registration_type}',
        'snack_preference': f'{snack_preferences}',
        'extraservice': f'{extra_services}',
        '2024': f'{datetime.now().year}'
    }

    # Use the application context to ensure Flask app context
    # Paths to the template and the new file
    template_path = os.path.join('static', 'email_temps', 'template_registrant_notif.txt')
    output_path = os.path.join('static', 'email_temps', 'registrant_notif.txt')

    # Copy template to output file
    shutil.copyfile(template_path, output_path)

    # Read the content from the output file
    with open(output_path, 'r') as registrant:
        read_registrant = registrant.read()

    # Perform replacements with actual data
    updated_content = read_registrant
    for placeholder, value in data.items():
        updated_content = updated_content.replace(f'[{placeholder}]', value)

    # Write the updated content back to the output file
    with open(output_path, 'w') as file:
        file.write(updated_content)

    return updated_content


def admin_letter(firstname, lastname, email, phone, registration_type, snack_preferences, extra_services):
    # Sample data (replace with actual data as needed)
    data = {
        'firstname': f'{firstname}',
        'lastname': f'{lastname}',
        'email': f'{email}',
        'phone': f'{phone}',
        'user_registration': f'{registration_type}',
        'snack_preference': f'{snack_preferences}',
        'extraservice': 'VIP Access',
        '2024': f'{datetime.now().year}'
    }

    # Paths to the template and the new file
    template_path = os.path.join('static', 'email_temps', 'template_admin_notif.txt')
    output_path = os.path.join('static', 'email_temps', 'admin_notif.txt')

    # Copy template to output file
    shutil.copyfile(template_path, output_path)

    # Read the content from the output file
    with open(output_path, 'r') as registrant:
        read_registrant = registrant.read()

    # Perform replacements with actual data
    updated_content = read_registrant
    for placeholder, value in data.items():
        updated_content = updated_content.replace(f'[{placeholder}]', value)

    # Write the updated content back to the output file
    with open(output_path, 'w') as file:
        file.write(updated_content)

    return updated_content
