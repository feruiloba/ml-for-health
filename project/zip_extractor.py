import zipfile
import os

class ZipExtractor:
    def __init__(self, zips_dir, out_dirs_dir):
        self.zips_dir = zips_dir
        self.out_dirs_dir = out_dirs_dir

    def extract_zips(self):
        for zip_filename in os.listdir(self.zips_dir):
            if zip_filename.endswith('.zip'):
                self.extract_zip(zip_filename)

    def extract_zip(self, zip_filename):
        zip_path = os.path.join(self.zips_dir, zip_filename)
        extraction_path = os.path.join(self.out_dirs_dir, zip_filename.replace('.zip', ''))

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extraction_path)
            print(f"Extracted {zip_filename} to {extraction_path}")
        except zipfile.BadZipFile:
            print(f"ERROR: {zip_filename} is not a valid ZIP file.")
        except Exception as e:
            print(f"ERROR extracting {zip_filename}: {e}")

if __name__ == "__main__":
    zips_directory = "downloaded_zips"
    output_directories_directory = "extracted_data"

    extractor = ZipExtractor(zips_directory, output_directories_directory)
    extractor.extract_zips()