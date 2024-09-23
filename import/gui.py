import sys
import random
import csv
import os
import hashlib
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QRadioButton,
    QGroupBox,
    QFileDialog,
    QMessageBox,
    QSpinBox,
)
from PyQt6.QtCore import Qt


def generate_member_id(include_letters, letter_count, id_length):
    if include_letters:
        letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=letter_count))
        numbers = ''.join(random.choices('0123456789', k=id_length - letter_count))
        return letters + numbers
    else:
        return ''.join(random.choices('0123456789', k=id_length))


def generate_line_uid():
    uid = 'U' + ''.join(random.choices('0123456789abcdef', k=32))
    return uid if re.match(r"^U[0-9a-f]{32}$", uid) else None


def generate_phone_number(country_code, include_plus, format_pattern):
    phone_number = f"{random.randint(100000000, 999999999)}"

    if country_code:
        if include_plus:
            return (
                f"+{country_code}{phone_number}"
                if not format_pattern
                else f"+{country_code} {phone_number[:4]} {phone_number[4:]}"
            )
        return (
            f"{country_code}{phone_number}"
            if not format_pattern
            else f"{country_code} {phone_number[:4]} {phone_number[4:]}"
        )
    return phone_number if not format_pattern else f"{phone_number[:4]} {phone_number[4:]}"


def hash_phone_number(phone_number):
    return hashlib.sha256(phone_number.encode('utf-8')).hexdigest()


def generate_email(length, format_check, hash_email):
    local_part = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))
    domain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)) + ".com"
    email = f"{local_part}@{domain}"

    if format_check:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Generated email is not in valid format")

    if hash_email:
        email = hashlib.sha256(email.encode('utf-8')).hexdigest()

    return email


def generate_tags(tags, distribute_evenly, amount, random_tag_count=False, min_tags=1, max_tags=3):
    all_tags = []
    for i in range(amount):
        if random_tag_count:
            num_tags = random.randint(min_tags, max_tags)
            all_tags.append(random.sample(tags, k=num_tags))
        else:
            if distribute_evenly:
                all_tags.append([tags[i % len(tags)]])
            else:
                all_tags.append([random.choice(tags)])
    return all_tags


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
            header.append(tag_title)
            writer.writerow(header)

        for row in data_list:
            writer.writerow(row)


class MemberListGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Member List Generator')

        self.amount_label = QLabel('生成成員數量:')
        self.amount_input = QLineEdit(self)

        self.include_uid_checkbox = QCheckBox('包含 LINE UID', self)
        self.include_member_id_checkbox = QCheckBox('包含會員編號', self)
        self.include_phone_checkbox = QCheckBox('包含電話號碼', self)
        self.include_email_checkbox = QCheckBox('包含 Email', self)

        self.tags_label = QLabel('輸入標籤（用逗號分隔）:')
        self.tags_input = QLineEdit(self)

        self.random_tag_count_checkbox = QCheckBox('隨機生成標籤數量', self)
        self.min_tags_label = QLabel('最小標籤數量:')
        self.min_tags_spinbox = QSpinBox(self)
        self.min_tags_spinbox.setMinimum(1)
        self.max_tags_label = QLabel('最大標籤數量:')
        self.max_tags_spinbox = QSpinBox(self)
        self.max_tags_spinbox.setMinimum(1)

        self.generate_button = QPushButton('Generate Member List', self)
        self.generate_button.clicked.connect(self.generate_member_list)

        layout = QVBoxLayout()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.include_uid_checkbox)
        layout.addWidget(self.include_member_id_checkbox)
        layout.addWidget(self.include_phone_checkbox)
        layout.addWidget(self.include_email_checkbox)
        layout.addWidget(self.tags_label)
        layout.addWidget(self.tags_input)
        layout.addWidget(self.random_tag_count_checkbox)
        layout.addWidget(self.min_tags_label)
        layout.addWidget(self.min_tags_spinbox)
        layout.addWidget(self.max_tags_label)
        layout.addWidget(self.max_tags_spinbox)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate_member_list(self):
        try:
            amount = int(self.amount_input.text())
            include_uid = self.include_uid_checkbox.isChecked()
            include_member_id = self.include_member_id_checkbox.isChecked()
            include_phone = self.include_phone_checkbox.isChecked()
            include_email = self.include_email_checkbox.isChecked()

            tags = self.tags_input.text().split(',')
            random_tag_count = self.random_tag_count_checkbox.isChecked()
            min_tags = self.min_tags_spinbox.value()
            max_tags = self.max_tags_spinbox.value()

            data_list = []
            tags_list = generate_tags(tags, False, amount, random_tag_count, min_tags, max_tags)

            for i in range(amount):
                member_data = []

                if include_uid:
                    line_uid = generate_line_uid()
                    member_data.append(line_uid)

                if include_member_id:
                    member_id = generate_member_id(True, 2, 8)
                    member_data.append(member_id)

                if include_phone:
                    phone = generate_phone_number('886', True, False)
                    member_data.append(phone)

                if include_email:
                    email = generate_email(10, True, False)
                    member_data.append(email)

                member_data.append(', '.join(tags_list[i]))

                data_list.append(member_data)

            file_path, _ = QFileDialog.getSaveFileName(
                self, 'Save CSV', os.path.expanduser('~/Downloads'), 'CSV files (*.csv)'
            )
            if file_path:
                export_to_csv(
                    data_list, True, 'LINE UID', 'Member ID', 'Phone', 'Tags', 'Email', file_path
                )
                QMessageBox.information(self, 'Success', f'檔案已匯出到: {file_path}')
            else:
                QMessageBox.warning(self, 'Warning', '未選擇保存路徑')

        except ValueError:
            QMessageBox.critical(self, 'Error', '請輸入有效的數量。')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'發生錯誤: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MemberListGenerator()
    window.show()
    sys.exit(app.exec())
