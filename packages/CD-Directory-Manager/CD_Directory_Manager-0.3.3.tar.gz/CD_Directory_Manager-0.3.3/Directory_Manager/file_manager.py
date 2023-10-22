import os
import json
import pickle
import csv
import platform


class FileManager:
    """
    A class to manage file-related operations.
    """

    @staticmethod
    def _get_encoding() -> str:
        """
        Determines the appropriate file encoding based on the operating system.

        Returns:
            str: The file encoding type.
        """
        system = platform.system()
        if system == "Windows":
            return "utf-16"
        else:
            return "utf-8"

    @staticmethod
    def create_file(path: str, content: str) -> bool:
        """
        Creates a file at the specified path with the given content.

        Args:
            path (str): The path where the file should be created.
            content (str): The content to be written to the file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(path, 'w', encoding=FileManager._get_encoding()) as file:
                file.write(content.strip())
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def delete_file(path: str) -> bool:
        """
        Deletes a file at the specified path.

        Args:
            path (str): The path of the file to be deleted.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            os.remove(path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def read_file(path: str) -> str:
        """
        Reads the content of a file at the specified path.

        Args:
            path (str): The path of the file to be read.

        Returns:
            str: The content of the file.
        """
        try:
            with open(path, 'r', encoding=FileManager._get_encoding()) as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error: {e}")
            return ""

    @staticmethod
    def write_file(path: str, content: str) -> bool:
        """
        Writes the given content to a file at the specified path.

        Args:
            path (str): The path where the file should be written.
            content (str): The content to be written to the file.

        Returns:
            bool: True if successful, False otherwise.
        """
        return FileManager.create_file(path, content)

    @staticmethod
    def list_to_file(path: str, data: list) -> bool:
        """
        Writes a list of strings to a file, each on a new line.

        Args:
            path (str): The path where the file should be written.
            data (list): The list of strings to be written to the file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(path, 'w', encoding=FileManager._get_encoding()) as file:
                for item in data:
                    file.write(f"{item}\n")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def list_from_file(path: str) -> list:
        """
        Reads a file and returns its content as a list of strings.

        Args:
            path (str): The path of the file to be read.

        Returns:
            list: A list of strings, each representing a line from the file.
        """
        try:
            with open(path, 'r', encoding=FileManager._get_encoding()) as file:
                return [line.strip() for line in file.readlines()]
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def read_json(path: str) -> dict:
        """
        Reads a JSON file and returns its content as a dictionary.

        Args:
            path (str): The path of the JSON file to be read.

        Returns:
            dict: The content of the JSON file.
        """
        try:
            with open(path, 'r', encoding=FileManager._get_encoding()) as file:
                return json.load(file)
        except Exception as e:
            print(f"Error: {e}")
            return {}

    @staticmethod
    def write_json(path: str, data: dict) -> bool:
        """
        Writes a dictionary to a file in JSON format.

        Args:
            path (str): The path where the JSON file should be written.
            data (dict): The dictionary to be written to the file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(path, 'w', encoding=FileManager._get_encoding()) as file:
                json.dump(data, file)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def read_pickle(path: str):
        """
        Reads a Pickle file and returns its content.

        Args:
            path (str): The path of the Pickle file to be read.

        Returns:
            Any: The content of the Pickle file.
        """
        try:
            with open(path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def write_pickle(path: str, data: any) -> bool:
        """
        Writes data to a file in Pickle format.

        Args:
            path (str): The path where the Pickle file should be written.
            data (any): The data to be written to the file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(path, 'wb') as file:
                pickle.dump(data, file)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def read_html(path: str) -> str:
        """
        Reads an HTML file and returns its content as a string.

        Args:
            path (str): The path of the HTML file to be read.

        Returns:
            str: The content of the HTML file.
        """
        return FileManager.read_file(path)

    @staticmethod
    def write_html(path: str, content: str) -> bool:
        """
        Writes a string to an HTML file.

        Args:
            path (str): The path where the HTML file should be written.
            content (str): The content to be written to the file.

        Returns:
            bool: True if successful, False otherwise.
        """
        return FileManager.write_file(path, content)

    @staticmethod
    def read_csv(path: str) -> list:
        """
        Reads a CSV file and returns its content as a list of dictionaries.

        Args:
            path (str): The path of the CSV file to be read.

        Returns:
            list: A list of dictionaries, each representing a row from the CSV file.
        """
        try:
            with open(path, 'r', encoding=FileManager._get_encoding()) as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def write_csv(path: str, data: list, headers: list) -> bool:
        """
        Writes a list of dictionaries to a CSV file.

        Args:
            path (str): The path where the CSV file should be written.
            data (list): The list of dictionaries to be written to the file.
            headers (list): The list of headers for the CSV file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(path, 'w', encoding=FileManager._get_encoding(), newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

