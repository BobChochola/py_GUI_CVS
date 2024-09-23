import csv
import random
import string
import os


def generate_line_uid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def generate_member_id(include_letters, letter_count, id_length):
    letters = (
        ''.join(random.choices(string.ascii_letters, k=letter_count)) if include_letters else ''
    )
    digits = ''.join(random.choices(string.digits, k=id_length - letter_count))
    return letters + digits


def generate_phone_number(country_code, include_plus, format_pattern):
    number = ''.join(random.choices(string.digits, k=8))
    if format_pattern:
        number = f"{number[:4]}-{number[4:]}"
    return f"{'+' if include_plus else ''}{country_code} {number}"


def generate_email(email_length, email_format_check, email_hash):
    email = (
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=email_length))
        + '@example.com'
    )
    if email_hash:
        email = hash_email(email)
    return email


def hash_email(email):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def generate_tags(tags, distribute_evenly, min_tags, max_tags):
    selected_tags = random.sample(tags, random.randint(min_tags, max_tags))
    return [selected_tags]


def export_to_csv(
    data_list,
    include_title,
    line_uid_title,
    member_id_title,
    phone_number_title,
    tag_title,
    email_title,
    file_path,
):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # If include_title is True, add the selected titles
        if include_title:
            header = []
            if line_uid_title:
                header.append(line_uid_title)
            if member_id_title:
                header.append(member_id_title)
            if phone_number_title:
                header.append(phone_number_title)
            if email_title:
                header.append(email_title)
            header.append(tag_title)  # Tags are always included
            writer.writerow(header)

        # Write the data rows
        for row in data_list:
            writer.writerow(row)

    return file_path


def generate_member_list(config):
    data_list = []

    for i in range(config["amount"]):
        member_data = []

        if config["line_uid_title"]:
            line_uid = generate_line_uid()
            member_data.append(line_uid)

        if config["include_member_id"]:
            member_id = generate_member_id(
                config["include_letters"], config["letter_count"], config["id_length"]
            )
            member_data.append(member_id)

        if config["include_phone_number"]:
            phone = generate_phone_number(
                config["country_code"], config["include_plus"], config["format_pattern"]
            )
            member_data.append(phone)

        if config["email_title"]:
            email = generate_email(
                config["email_length"], config["email_format_check"], config["email_hash"]
            )
            member_data.append(email)

        tag_list = generate_tags(
            config["tags"],
            config["distribute_evenly"],
            1,
            config["random_tag_count"],
            config["min_tags"],
            config["max_tags"],
        )
        member_data.append(", ".join(tag_list[0]))

        data_list.append(member_data)

    return export_to_csv(
        data_list,
        config["include_title"],
        config["line_uid_title"],
        config["member_id_title"],
        config["phone_number_title"],
        config["email_title"],
        config["tag_title"],
    )
