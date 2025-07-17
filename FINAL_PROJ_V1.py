# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 20:57:48 2025

@author: Saksham Gupta
"""
#this is a change done here.
import requests
import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

VERIPHONE_API_URL = "https://api.veriphone.io/v2/verify"
VERIPHONE_API_KEY = "C92F0A5B17794E88A8C837331C0BCFAB"  

def choose_options():
    print("Choose : \n")
    print("1. Check Individual Number.")
    print("2. Check Bulk Records from CSV.\n")
    choose = input("Enter : ")
    if choose == '1':
        ph_num = ph_num_input()
        veriphone_report(ph_num)
    elif choose == '2':
        open_file_dialog_for_bulk()
    else:
        print("Wrong Input, Please try again.")
        choose_options()

def open_file_dialog_for_bulk():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        bulk_check(file_path)
    else:
        print("No file selected. Returning to menu.")
        choose_options()

def bulk_check(in_file):
    op_file = f"All_records.csv"
    failed_file = f"failed_records.csv"
    file_exists = os.path.isfile(op_file)
    failed_exists = os.path.isfile(failed_file)
    existing_numbers = set()
    stats = {"total": 0, "valid": 0, "invalid": 0, "skipped": 0}

    if file_exists:
        with open(op_file, 'r', newline='') as existing:
            existing_reader = csv.DictReader(existing)
            for row in existing_reader:
                existing_numbers.add(row["Ph_Number"])

    with open(in_file, 'r', newline='') as f, \
         open(op_file, 'a', newline='') as out, \
         open(failed_file, 'a', newline='') as fail:

        reader = csv.DictReader(f)
        writer = csv.writer(out)
        failed_writer = csv.writer(fail)

        if not file_exists:
            writer.writerow(["Ph_Number", "Valid", "Country", "Carrier", "Line Type", "Checked At"])
        if not failed_exists:
            failed_writer.writerow(["Ph_Number", "Reason"])

        for row in reader:
            numberf = row.get("Ph_num")
            stats["total"] += 1

            if not numberf:
                stats["skipped"] += 1
                continue
            if not numberf.startswith('+'):
                numberf = '+' + numberf
            if numberf in existing_numbers:
                print(f"⏩ Skipping already existing number: {numberf}")
                stats["skipped"] += 1
                continue
            if not is_valid_number_format(numberf):
                failed_writer.writerow([numberf, "Invalid format"])
                stats["invalid"] += 1
                continue

            vp_data = get_veriphone_data(numberf)

            if not vp_data or not vp_data.get("phone_valid"):
                print(f"⚠️ Invalid or empty data for {numberf}: {vp_data}")
                failed_writer.writerow([numberf, "API validation failed"])
                stats["invalid"] += 1
                continue

            writer.writerow([
                numberf,
                vp_data.get("phone_valid"),
                vp_data.get("country"),
                vp_data.get("carrier"),
                vp_data.get("phone_type"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
            existing_numbers.add(numberf)
            stats["valid"] += 1

    print(f"\nBulk report appended to: {op_file}")
    print(f"Invalid entries stored in: {failed_file}")
    print("\n-----------------------------SUMMARY-----------------------------")
    print(f"Total numbers processed: {stats['total']}")
    print(f"✔️ Valid: {stats['valid']}")
    print(f"❌ Invalid: {stats['invalid']}")
    print(f"⏭️ Skipped (duplicates): {stats['skipped']}")

def veriphone_report(ph_num):
    data = get_veriphone_data(ph_num)
    if data and data.get("phone_valid"):
        print("\n✅ Phone Number is VALID!")
        print("\n-------------PHONE NUMBER REPORT-------------")
        print(f"📍 Country: {data.get('country')}")
        print(f"📡 Carrier: {data.get('carrier')}")
        print(f"📞 Line Type: {data.get('phone_type')}")
        print(f"🌐 International Format: {data.get('phone')}")
    else:
        print("\n❌ Invalid Phone Number! Or request limit exceeded.")

def get_veriphone_data(ph_num):
    params = {
        "phone": ph_num,
        "key": VERIPHONE_API_KEY
    }
    try:
        response = requests.get(VERIPHONE_API_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code} for number {ph_num}")
    except Exception as e:
        print(f"Exception occurred during API call for {ph_num}: {e}")
    return None

def is_valid_number_format(ph_num):
    number_part = ph_num[1:]
    if not number_part.isdigit():
        return False
    return len(number_part[-10:]) == 10

def ph_num_input():
    while True:
        ph_num = input("Enter phone number with country code : ").strip()
        if not ph_num.startswith('+'):
            print("Number must start with '+'. Try again.")
            continue
        number_part = ph_num[1:]
        if not number_part.isdigit():
            print("Number must contain only digits after '+'. Try again.")
            continue
        if len(number_part[-10:]) == 10:
            print("✅ Valid Entry.")
            return ph_num
        else:
            print("Number must be exactly 10 digits. Try again.")

print("\n-----------------------------MOBILE NUMBER REPORT-----------------------------\n")
choose_options()
