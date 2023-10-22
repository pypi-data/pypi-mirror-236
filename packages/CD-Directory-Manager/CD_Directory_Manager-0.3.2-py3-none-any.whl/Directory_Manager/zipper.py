import os
import shutil
import zipfile


class ZipManager:
    """
    A class to manage ZIP-related operations with advanced features.
    """

    @staticmethod
    def zip_file(source_file: str, destination_zip: str, compression_level=zipfile.ZIP_DEFLATED, password=None) -> bool:
        """
        Zips a single file with optional password protection.

        Args:
            source_file (str): The path to the file to be zipped.
            destination_zip (str): The path where the ZIP file should be created.
            compression_level (int, optional): Compression level from zipfile. Defaults to ZIP_DEFLATED.
            password (str, optional): Password to protect the ZIP file. Defaults to None.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with zipfile.ZipFile(destination_zip, 'w', compression=compression_level) as zipf:
                zipf.write(source_file, os.path.basename(source_file))
                if password:
                    zipf.setpassword(password.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def zip_directories(source_dir: str, destination_zip: str, exclude_patterns=None, compression_level=zipfile.ZIP_DEFLATED, password=None) -> bool:
        """
        Zips a directory and its contents with optional exclusions and password protection.

        Args:
            source_dir (str): The path to the directory to be zipped.
            destination_zip (str): The path where the ZIP file should be created.
            exclude_patterns (list, optional): List of patterns to exclude. Defaults to None.
            compression_level (int, optional): Compression level from zipfile. Defaults to ZIP_DEFLATED.
            password (str, optional): Password to protect the ZIP file. Defaults to None.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with zipfile.ZipFile(destination_zip, 'w', compression=compression_level) as zipf:
                for foldername, subfolders, filenames in os.walk(source_dir):
                    for filename in filenames:
                        if exclude_patterns and any([fnmatch.fnmatch(filename, pattern) for pattern in exclude_patterns]):
                            continue
                        file_path = os.path.join(foldername, filename)
                        zipf.write(file_path, os.path.relpath(file_path, source_dir))
                if password:
                    zipf.setpassword(password.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def unzip(source_zip: str, destination_dir: str, password=None) -> bool:
        """
        Unzips a ZIP file with optional password.

        Args:
            source_zip (str): The path to the ZIP file to be unzipped.
            destination_dir (str): The path where the unzipped content should be placed.
            password (str, optional): Password to decrypt the ZIP file. Defaults to None.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with zipfile.ZipFile(source_zip, 'r') as zipf:
                if password:
                    zipf.extractall(destination_dir, pwd=password.encode('utf-8'))
                else:
                    zipf.extractall(destination_dir)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def unzip_files_and_directories(source_zip: str, destination_dir: str, password=None) -> bool:
        """
        Unzips a ZIP file containing both files and directories with optional password.

        Args:
            source_zip (str): The path to the ZIP file to be unzipped.
            destination_dir (str): The path where the unzipped content should be placed.
            password (str, optional): Password to decrypt the ZIP file. Defaults to None.

        Returns:
            bool: True if successful, False otherwise.
        """
        # The method to unzip is the same regardless of the content of the ZIP file.
        return ZipManager.unzip(source_zip, destination_dir, password)

    @staticmethod
    def get_zip_content_list(source_zip: str, password=None) -> list:
        """
        Retrieves a list of files and directories inside a ZIP file.

        Args:
            source_zip (str): The path to the ZIP file.
            password (str, optional): Password to decrypt the ZIP file. Defaults to None.

        Returns:
            list: List of files and directories inside the ZIP.
        """
        try:
            with zipfile.ZipFile(source_zip, 'r') as zipf:
                if password:
                    return zipf.namelist(pwd=password.encode('utf-8'))
                else:
                    return zipf.namelist()
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def is_zip_password_protected(source_zip: str) -> bool:
        """
        Checks if a ZIP file is password protected.

        Args:
            source_zip (str): The path to the ZIP file.

        Returns:
            bool: True if password protected, False otherwise.
        """
        try:
            with zipfile.ZipFile(source_zip, 'r') as zipf:
                return zipf.is_encrypted
        except Exception as e:
            print(f"Error: {e}")
            return False

