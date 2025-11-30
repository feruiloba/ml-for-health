import os
import csv
from pathlib import Path
from fitparse import FitFile
import sys

def parse_fit_to_csv(fit_file_path, csv_file_path):
    """
    Parse a single .fit file and convert it to CSV format.

    Args:
        fit_file_path: Path to the input .fit file
        csv_file_path: Path to the output .csv file
    """
    try:
        # Load the FIT file
        fitfile = FitFile(str(fit_file_path))

        # Collect all records
        records = []
        headers = set()

        # Parse all messages in the FIT file
        for record in fitfile.get_messages():
            record_data = {'message_type': record.name}

            # Extract all fields from the record
            for field in record:
                field_name = field.name
                field_value = field.value

                # Handle timestamp fields
                if hasattr(field_value, 'isoformat'):
                    field_value = field_value.isoformat()

                record_data[field_name] = field_value
                headers.add(field_name)

            records.append(record_data)

        # Create ordered list of headers
        headers = ['message_type'] + sorted(headers)

        # Write to CSV
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(records)

        return True, len(records)

    except Exception as e:
        return False, str(e)


def process_fit_folders(root_folder, out_folder):
    """
    Process all .fit files in a folder structure.

    Args:
        root_folder: Root folder containing day subfolders with .fit files
    """
    root_path = Path(root_folder)

    if not root_path.exists():
        print(f"Error: Folder '{root_folder}' does not exist.")
        return

    processed_count = 0
    error_count = 0

    # Walk through all subdirectories
    for day_folder in sorted(root_path.iterdir()):
        if not day_folder.is_dir():
            continue

        print(f"\nProcessing folder: {day_folder.name}")

        # Process all .fit files in the day folder
        fit_files = list(day_folder.glob("*.fit")) + list(day_folder.glob("*.FIT"))

        if not fit_files:
            print(f"  No .fit files found in {day_folder.name}")
            continue

        for fit_file in fit_files:
            # Create CSV file path (same location as .fit file)

            csv_folder = Path(out_folder).joinpath(*fit_file.parts[1:-1])
            os.makedirs(csv_folder, exist_ok=True)
            csv_file = csv_folder.joinpath(fit_file.name).with_suffix('.csv')

            print(f"  Converting: {fit_file.name} -> {csv_file}")

            success, result = parse_fit_to_csv(fit_file, csv_file)

            if success:
                print(f"    ✓ Success: {result} records")
                processed_count += 1
            else:
                print(f"    ✗ Error: {result}")
                error_count += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Successfully converted: {processed_count} files")
    print(f"Errors: {error_count} files")
    print(f"{'='*60}")


if __name__ == "__main__":
    process_fit_folders('fit_data', 'csv_data')