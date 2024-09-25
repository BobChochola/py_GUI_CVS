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
    QFileDialog,
    QMessageBox,
    QSpinBox,
    QComboBox,
    QRadioButton,
    QButtonGroup,
    QScrollArea,
    QGroupBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from styles import StyleSheet


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


def generate_phone_number(country, include_country_code, include_plus, format_pattern):
    if country == "Taiwan":
        phone_number = f"{random.randint(10000000, 99999999)}"
        if include_country_code:
            full_number = f"8869{phone_number}"
        else:
            full_number = f"09{phone_number}"
    elif country == "Hong Kong":
        phone_number = f"{random.randint(10000000, 99999999)}"
        if include_country_code:
            full_number = f"852{phone_number}"
        else:
            full_number = f"9{phone_number}"

    if include_country_code and include_plus:
        full_number = f"+{full_number}"

    if format_pattern:
        if country == "Taiwan":
            return f"{full_number[:4]} {full_number[4:]}"
        elif country == "Hong Kong":
            return f"{full_number[:4]} {full_number[4:8]}"

    return full_number


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


def generate_tags(tags, tag_option, amount, random_tag_count=False, min_tags=1, max_tags=3):
    all_tags = []
    for i in range(amount):
        if tag_option == "all_in_one":
            all_tags.append(tags)
        elif tag_option == "separate_columns":
            all_tags.append(tags)  # 不限制標籤數量
        elif tag_option == "random":
            if random_tag_count:
                num_tags = random.randint(min_tags, min(max_tags, len(tags)))
                all_tags.append(random.sample(tags, k=num_tags))
            else:
                all_tags.append(random.sample(tags, k=1))
    return all_tags


def export_to_csv(data_list, include_title, columns, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        if include_title:
            writer.writerow(columns)

        for row in data_list:
            writer.writerow(row)


class MemberListGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Member List Generator')
        self.setStyleSheet(StyleSheet.MAIN)
        self.setMinimumWidth(450)

        self.amount_label = QLabel('生成成員數量:')
        self.amount_input = QLineEdit(self)

        self.include_uid_checkbox = QCheckBox('包含 LINE User ID', self)
        self.include_member_id_checkbox = QCheckBox('包含會員編號', self)
        self.include_phone_checkbox = QCheckBox('包含電話號碼', self)
        self.include_phone_checkbox.stateChanged.connect(self.toggle_country_code_checkbox)
        self.include_country_code_checkbox = QCheckBox('包括國碼', self)
        self.include_country_code_checkbox.setVisible(False)
        self.include_email_checkbox = QCheckBox('包含 Email', self)

        self.country_label = QLabel('選擇國家:')
        self.country_combo = QComboBox(self)
        self.country_combo.addItems(["Taiwan", "Hong Kong"])

        self.tags_label = QLabel('輸入標籤（用逗號分隔）:')
        self.tags_input = QLineEdit(self)

        self.tag_option_group = QButtonGroup(self)
        self.all_tags_in_one_radio = QRadioButton("所有標籤放置於 Tags 欄位")
        self.separate_tags_radio = QRadioButton("各個標籤放置不同欄位 (E.g. Tag1, Tag2...)")
        self.random_tags_radio = QRadioButton("隨機(需搭配下面選項使用)")
        self.tag_option_group.addButton(self.all_tags_in_one_radio)
        self.tag_option_group.addButton(self.separate_tags_radio)
        self.tag_option_group.addButton(self.random_tags_radio)
        self.all_tags_in_one_radio.setChecked(True)

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
        layout.addWidget(self.include_country_code_checkbox)
        layout.addWidget(self.include_email_checkbox)
        layout.addWidget(self.country_label)
        layout.addWidget(self.country_combo)
        layout.addWidget(self.tags_label)
        layout.addWidget(self.tags_input)
        layout.addWidget(self.all_tags_in_one_radio)
        layout.addWidget(self.separate_tags_radio)
        layout.addWidget(self.random_tags_radio)
        layout.addWidget(self.random_tag_count_checkbox)
        layout.addWidget(self.min_tags_label)
        layout.addWidget(self.min_tags_spinbox)
        layout.addWidget(self.max_tags_label)
        layout.addWidget(self.max_tags_spinbox)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def toggle_country_code_checkbox(self):
        self.include_country_code_checkbox.setVisible(self.include_phone_checkbox.isChecked())

    def generate_member_list(self):
        try:
            amount = int(self.amount_input.text())
            include_uid = self.include_uid_checkbox.isChecked()
            include_member_id = self.include_member_id_checkbox.isChecked()
            include_phone = self.include_phone_checkbox.isChecked()
            include_country_code = self.include_country_code_checkbox.isChecked()
            include_email = self.include_email_checkbox.isChecked()
            country = self.country_combo.currentText()

            tags = [tag.strip() for tag in self.tags_input.text().split(',') if tag.strip()]
            random_tag_count = self.random_tag_count_checkbox.isChecked()
            min_tags = self.min_tags_spinbox.value()
            max_tags = self.max_tags_spinbox.value()

            tag_option = "all_in_one"
            if self.separate_tags_radio.isChecked():
                tag_option = "separate_columns"
            elif self.random_tags_radio.isChecked():
                tag_option = "random"

            tags_list = generate_tags(
                tags, tag_option, amount, random_tag_count, min_tags, max_tags
            )

            data_list = []
            columns = []
            if include_uid:
                columns.append('LINE User ID')
            if include_member_id:
                columns.append('Member ID')
            if include_phone:
                columns.append('Phone')
            if include_email:
                columns.append('Email')
            if tag_option == "separate_columns":
                columns.extend([f'Tag{i+1}' for i in range(len(tags))])
            else:
                columns.append('Tags')

            for i in range(amount):
                member_data = []

                if include_uid:
                    line_uid = generate_line_uid()
                    member_data.append(line_uid)

                if include_member_id:
                    member_id = generate_member_id(True, 2, 8)
                    member_data.append(member_id)

                if include_phone:
                    phone = generate_phone_number(
                        country, self.include_country_code_checkbox.isChecked(), True, False
                    )
                    member_data.append(phone)

                if include_email:
                    email = generate_email(10, True, False)
                    member_data.append(email)

                if tag_option == "separate_columns":
                    member_data.extend(tags_list[i] + [''] * (len(tags) - len(tags_list[i])))
                else:
                    member_data.append(', '.join(tags_list[i]))

                data_list.append(member_data)

            file_path, _ = QFileDialog.getSaveFileName(
                self, 'Save CSV', os.path.expanduser('~/Downloads'), 'CSV files (*.csv)'
            )
            if file_path:
                export_to_csv(data_list, True, columns, file_path)
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
