import os
import shutil


class DirectoryManager:
    """
    A class to manage directory-related operations.
    """

    @staticmethod
    def create_directory(path: str) -> bool:
        """
        Creates a directory at the specified path.

        Args:
            path (str): The path where the directory should be created.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            os.makedirs(path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def create_directories(path: str) -> bool:
        """
        Creates a directory at the specified path, including any necessary intermediate directories.

        Args:
            path (str): The path where the directories should be created.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            os.makedirs(path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def delete_directory_recursive(path: str) -> bool:
        """
        Deletes a directory and all its contents, including subdirectories and files.

        Args:
            path (str): The path of the directory to be deleted.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            shutil.rmtree(path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def delete_directory(path: str) -> bool:
        """
        Deletes a directory at the specified path.

        Args:
            path (str): The path of the directory to be deleted.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            os.rmdir(path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def list_files(path: str) -> list:
        """
        Lists all files in the specified directory.

        Args:
            path (str): The path of the directory.

        Returns:
            list: A list of file names in the directory.
        """
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    @staticmethod
    def list_subdirectories(path: str) -> list:
        """
        Lists all subdirectories in the specified directory.

        Args:
            path (str): The path of the directory.

        Returns:
            list: A list of subdirectory names in the directory.
        """
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    @staticmethod
    def move_directory(source_path: str, dest_path: str) -> bool:
        """
        Moves a directory from the source path to the destination path.

        Args:
            source_path (str): The current path of the directory.
            dest_path (str): The destination path where the directory should be moved.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            os.rename(source_path, dest_path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def copy_directory(source_path: str, dest_path: str) -> bool:
        """
        Copies a directory from the source path to the destination path.

        Args:
            source_path (str): The current path of the directory.
            dest_path (str): The destination path where the directory should be copied.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            import shutil
            shutil.copytree(source_path, dest_path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
