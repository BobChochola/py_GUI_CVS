import random
import csv
import os
import hashlib
from datetime import datetime
import re


# 產生會員編號
def generate_member_id(include_letters, letter_count, id_length):
    if include_letters:
        letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=letter_count))
        numbers = ''.join(random.choices('0123456789', k=id_length - letter_count))
        return letters + numbers
    else:
        return ''.join(random.choices('0123456789', k=id_length))


# 產生 LINE UID
def generate_line_uid():
    uid = 'U' + ''.join(random.choices('0123456789abcdef', k=32))
    return uid if re.match(r"^U[0-9a-f]{32}$", uid) else None


# 產生電話號碼
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


# 雜湊電話號碼
def hash_phone_number(phone_number):
    return hashlib.sha256(phone_number.encode('utf-8')).hexdigest()


# 產生 Email
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


# 生成標籤
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


# 匯出 CSV 檔案
def export_to_csv(
    data_list,
    include_title,
    line_uid_title,
    member_id_title,
    phone_number_title,
    tag_title,
    email_title,
):
    file_name = f"member_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.expanduser(f"~/Downloads/{file_name}")

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # 寫入標題行（只有當 include_title 為 True 時）
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

        # 寫入資料行
        for row in data_list:
            writer.writerow(row)

    print(f"檔案已成功匯出到: {file_path}")


# 生成名單
def generate_member_list(
    amount,
    include_member_id,
    include_phone_number,
    country_code,
    include_plus,
    format_pattern,
    hash_numbers,
    include_title,
    line_uid_title,
    member_id_title,
    phone_number_title,
    tag_title,
    email_title,
    include_letters,
    letter_count,
    id_length,
    email_length,
    email_format_check,
    email_hash,
    tags,
    distribute_evenly,
    random_tag_count,
    min_tags,
    max_tags,
):
    data_list = []

    # 生成成員資料
    for i in range(amount):
        member_data = []

        if line_uid_title:
            line_uid = generate_line_uid()
            member_data.append(line_uid)

        if include_member_id:
            member_id = generate_member_id(include_letters, letter_count, id_length)
            member_data.append(member_id)

        if include_phone_number:
            phone = generate_phone_number(country_code, include_plus, format_pattern)
            if hash_numbers:
                phone = hash_phone_number(phone)
            member_data.append(phone)

        if email_title:
            email = generate_email(email_length, email_format_check, email_hash)
            member_data.append(email)

        # 加入標籤
        tag_list = generate_tags(tags, distribute_evenly, 1, random_tag_count, min_tags, max_tags)
        member_data.append(", ".join(tag_list[0]))

        data_list.append(member_data)

    export_to_csv(
        data_list,
        include_title,
        line_uid_title,
        member_id_title,
        phone_number_title,
        email_title,
        tag_title,
    )


# 主程式
if __name__ == "__main__":
    try:
        # 新增詢問是否包含標題欄位
        include_title = input("是否包含標題欄位 (y/n): ").strip().lower() == 'y'

        # Step 1: 確認是否產生 LINE UID
        include_line_uid = input("是否產生 LINE UID (y/n): ").strip().lower() == 'y'
        line_uid_title = ""
        if include_line_uid:
            custom_line_uid_title = (
                input("是否自訂 LINE UID 欄位標題，否則預設為 LINE User ID (y/n): ").strip().lower()
                == 'y'
            )
            line_uid_title = (
                input("請輸入 LINE UID 欄位標題: ").strip()
                if custom_line_uid_title
                else "LINE User ID"
            )

        # Step 2: 確認是否產生會員編號
        include_member_id = input("是否產生會員編號 (y/n): ").strip().lower() == 'y'
        member_id_title = ""
        include_letters, letter_count, id_length = False, 0, 0
        if include_member_id:
            custom_member_id_title = (
                input("是否自訂會員編號欄位標題，否則預設為 Member ID (y/n): ").strip().lower()
                == 'y'
            )
            member_id_title = (
                input("請輸入會員編號欄位標題: ").strip() if custom_member_id_title else "Member ID"
            )
            include_letters = input("會員編號是否包含英文 (y/n): ").strip().lower() == 'y'
            if include_letters:
                letter_count = int(input("請輸入英文部分字數: "))
            id_length = int(input("請輸入會員編號總長度: "))

        # Step 3: 確認是否產生電話號碼
        include_phone_number = (
            input("是否產生電話號碼，否則為 Phone (y/n): ").strip().lower() == 'y'
        )
        phone_number_title = ""
        if include_phone_number:
            custom_phone_number_title = (
                input("是否自訂電話號碼欄位標題 (y/n): ").strip().lower() == 'y'
            )
            phone_number_title = (
                input("請輸入電話號碼欄位標題: ").strip() if custom_phone_number_title else "Phone"
            )
            country_code = input("請輸入國碼（例如 886，如果不需要國碼請留空）: ").strip()
            include_plus = input("是否包含 '+' 號 (y/n): ").strip().lower() == 'y'
            format_pattern = input("是否格式化電話號碼 (y/n): ").strip().lower() == 'y'

            # 問是否要對電話號碼進行 SHA256 雜湊
            hash_numbers = (
                input("是否對電話號碼進行 SHA256 雜湊處理 (y/n): ").strip().lower() == 'y'
            )
        else:
            country_code = include_plus = format_pattern = hash_numbers = False

        # Step 4: 確認是否產生 Email
        include_email = input("是否產生 Email (y/n): ").strip().lower() == 'y'
        email_title = ""
        email_length, email_format_check, email_hash = 0, False, False
        if include_email:
            custom_email_title = input("是否自訂 Email 欄位標題 (y/n): ").strip().lower() == 'y'
            email_title = (
                input("請輸入 Email 欄位標題: ").strip() if custom_email_title else "Email"
            )
            email_length = int(input("請輸入 Email 的長度: "))
            email_format_check = input("是否檢查 Email 格式 (y/n): ").strip().lower() == 'y'
            email_hash = input("是否對 Email 進行 SHA256 雜湊處理 (y/n): ").strip().lower() == 'y'

        # Step 5: 確認是否自訂標籤欄位標題
        custom_tag_title = (
            input("是否自訂標籤欄位標題，否則預設為 Tags (y/n): ").strip().lower() == 'y'
        )
        tag_title = input("請輸入標籤欄位標題: ").strip() if custom_tag_title else "Tags"

        # Step 6: 問標籤
        tags_input = input("請輸入標籤（以逗號分隔）: ").strip().split(',')
        distribute_evenly = input("是否均分標籤 (y/n): ").strip().lower() == 'y'
        random_tag_count = input("是否隨機分配每人不同數量的標籤 (y/n): ").strip().lower() == 'y'
        min_tags, max_tags = 1, 1
        if random_tag_count:
            min_tags = int(input("請輸入每人最少標籤數量: "))
            max_tags = int(input("請輸入每人最多標籤數量: "))

        # Step 7: 生成成員名單
        amount = int(input("請輸入要生成的成員數量: "))

        generate_member_list(
            amount=amount,
            include_member_id=include_member_id,
            include_phone_number=include_phone_number,
            country_code=country_code,
            include_plus=include_plus,
            format_pattern=format_pattern,
            hash_numbers=hash_numbers,
            include_title=include_title,
            line_uid_title=line_uid_title,
            member_id_title=member_id_title,
            phone_number_title=phone_number_title,
            tag_title=tag_title,
            email_title=email_title,
            include_letters=include_letters,
            letter_count=letter_count,
            id_length=id_length,
            email_length=email_length,
            email_format_check=email_format_check,
            email_hash=email_hash,
            tags=tags_input,
            distribute_evenly=distribute_evenly,
            random_tag_count=random_tag_count,
            min_tags=min_tags,
            max_tags=max_tags,
        )

    except ValueError:
        print("無效輸入，請輸入有效的數字。")
    except Exception as e:
        print(f"發生錯誤: {e}")
