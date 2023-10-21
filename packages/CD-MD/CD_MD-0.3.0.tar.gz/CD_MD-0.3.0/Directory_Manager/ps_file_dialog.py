from PySide6.QtWidgets import QFileDialog


class FileDialogPySide6:
    """
    A class to manage common file dialog operations using PySide6.
    """

    @staticmethod
    def open_file_dialog(title="Open File", file_filter="All Files (*.*);;"):
        """
        Opens a file dialog to select a file for opening.

        Args:
            title (str, optional): The title of the file dialog. Defaults to "Open File".
            file_filter (str, optional): The file types to display. Defaults to all file types.

        Returns:
            str: The path to the selected file or an empty string if no file was selected.
        """
        file_path, _ = QFileDialog.getOpenFileName(None, title, "", file_filter)
        return file_path

    @staticmethod
    def save_file_dialog(title="Save File", file_filter="All Files (*.*);;"):
        """
        Opens a file dialog to select a file for saving.

        Args:
            title (str, optional): The title of the file dialog. Defaults to "Save File".
            file_filter (str, optional): The file types to display. Defaults to all file types.

        Returns:
            str: The path to the selected file or an empty string if no file was selected.
        """
        file_path, _ = QFileDialog.getSaveFileName(None, title, "", file_filter)
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
        dir_path = QFileDialog.getExistingDirectory(None, title)
        return dir_path
