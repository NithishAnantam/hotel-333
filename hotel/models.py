import csv
import os
from django.conf import settings

# Define CSV folder path
CSV_FOLDER = os.path.join(settings.BASE_DIR, "csv_data")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure the CSV folder exists
os.makedirs(CSV_FOLDER, exist_ok=True)

def read_csv(filename):
    """Reads a CSV file and returns its contents excluding headers."""
    filepath = os.path.join(BASE_DIR, filename)  # Ensure correct path
    if not os.path.isfile(filepath):
        return []  # Return empty list if file doesn't exist
    
    with open(filepath, newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        return [row for row in reader][1:]  # Exclude header

# def write_csv(file_name, data, mode="a", headers=None):
#     """
#     Writes data to a CSV file.

#     :param file_name: Name of the CSV file.
#     :param data: List of lists (rows) or a single row to write.
#     :param mode: "a" for append (default), "w" for overwrite.
#     :param headers: Optional headers (only written if the file is new in "w" mode).
#     """
#     path = os.path.join(CSV_FOLDER, file_name)
#     file_exists = os.path.isfile(path)

#     with open(path, mode=mode, newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)

#         # Write headers only if the file is new or mode is "w"
#         if mode == "w" and headers:
#             writer.writerow(headers)
        
#         # Ensure data format is consistent
#         if isinstance(data[0], list):  # Multiple rows
#             writer.writerows(data)
#         else:  # Single row
#             writer.writerow(data)

# def write_csv(file_name, data, headers=None):
#     """
#     Writes data to a CSV file, ensuring headers are added only if needed.

#     :param file_name: The CSV file name.
#     :param data: The list of rows to write.
#     :param headers: Optional headers for the CSV file.
#     """
#     path = os.path.join(CSV_FOLDER, file_name)
    
#     write_headers = not os.path.exists(path) or os.stat(path).st_size == 0  # Only write headers if the file is new or empty

#     with open(path, mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)
        
#         if headers and write_headers:
#             writer.writerow(headers)  # Write headers only once

#         writer.writerows(data)  # Write remaining data


def write_csv(file_name, data, mode="a", headers=None):
    """
    Writes data to a CSV file, ensuring headers are added only if needed.

    :param file_name: The CSV file name.
    :param data: A list of rows (each row is a list) or a single row (list).
    :param mode: "a" (append) or "w" (overwrite). Default is "a".
    :param headers: Optional headers for the CSV file.
    """
    path = os.path.join(CSV_FOLDER, file_name)
    file_exists = os.path.exists(path) and os.stat(path).st_size > 0

    with open(path, mode=mode, newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write headers if file is new, empty, or in overwrite mode
        if headers and (mode == "w" or not file_exists):
            writer.writerow(headers)

        # Write data (handle single-row and multi-row cases)
        if isinstance(data[0], list):
            writer.writerows(data)  # Multiple rows
        else:
            writer.writerow(data)   # Single row


def delete_entry(file_name, condition_fn, headers):
    """
    Deletes an entry from a CSV file by rewriting it without the matching row.

    :param file_name: CSV file name.
    :param condition_fn: Function to filter out unwanted rows.
    :param headers: CSV headers.
    """
    path = os.path.join(CSV_FOLDER, file_name)
    
    if not os.path.isfile(path):
        return  # File doesn't exist, nothing to delete

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = [row for row in reader if not condition_fn(row)]  # Keep only non-matching rows

    # Ensure headers are passed to write_csv correctly
    write_csv(file_name, data, headers=headers)
