import tkinter as tk
from tkinter import filedialog


class TkFileDialog:
    """
    A class to manage common file dialog operations.
    """

    @staticmethod
    def open_file_dialog(title="Open File", file_types=(("All Files", "*.*"),)):
        """
        Opens a file dialog to select a file for opening.

        Args:
            title (str, optional): The title of the file dialog. Defaults to "Open File".
            file_types (tuple, optional): The file types to display. Defaults to all file types.

        Returns:
            str: The path to the selected file or an empty string if no file was selected.
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title=title, filetypes=file_types)
        return file_path

    @staticmethod
    def save_file_dialog(title="Save File", file_types=(("All Files", "*.*"),), default_extension=""):
        """
        Opens a file dialog to select a file for saving.

        Args:
            title (str, optional): The title of the file dialog. Defaults to "Save File".
            file_types (tuple, optional): The file types to display. Defaults to all file types.
            default_extension (str, optional): The default file extension. Defaults to an empty string.

        Returns:
            str: The path to the selected file or an empty string if no file was selected.
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.asksaveasfilename(title=title, filetypes=file_types, defaultextension=default_extension)
        return file_path

    @staticmethod
    def open_directory_dialog(title="Select Directory"):
        """
        Opens a file dialog to select a directory.

        Args:
            title (str, optional): The title of the directory dialog. Defaults to "Select Directory".

        Returns:
            str: The path to the selected directory or an empty string if no directory was selected.
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        dir_path = filedialog.askdirectory(title=title)
        return dir_path

