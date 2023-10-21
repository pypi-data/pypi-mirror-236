import os


class PathManager:
    """
    A class to manage path-related operations in a cross-platform manner.
    """

    @staticmethod
    def join_paths(*paths) -> str:
        """
        Joins multiple path segments into a single path.

        Args:
            *paths: Path segments to be joined.

        Returns:
            str: The combined path.
        """
        return os.path.join(*paths)

    @staticmethod
    def get_absolute_path(relative_path: str) -> str:
        """
        Converts a relative path to an absolute path.

        Args:
            relative_path (str): The relative path to be converted.

        Returns:
            str: The absolute path.
        """
        return os.path.abspath(relative_path)

    @staticmethod
    def get_basename(path: str) -> str:
        """
        Retrieves the base name of the specified path.

        Args:
            path (str): The path to retrieve the base name from.

        Returns:
            str: The base name of the path.
        """
        return os.path.basename(path)

    @staticmethod
    def get_directory(path: str) -> str:
        """
        Retrieves the directory name from the specified path.

        Args:
            path (str): The path to retrieve the directory name from.

        Returns:
            str: The directory name.
        """
        return os.path.dirname(path)

    @staticmethod
    def path_exists(path: str) -> bool:
        """
        Checks if the specified path exists.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return os.path.exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        """
        Checks if the specified path points to a file.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path points to a file, False otherwise.
        """
        return os.path.isfile(path)

    @staticmethod
    def is_directory(path: str) -> bool:
        """
        Checks if the specified path points to a directory.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path points to a directory, False otherwise.
        """
        return os.path.isdir(path)

    @staticmethod
    def get_extension(path: str) -> str:
        """
        Retrieves the file extension from the specified path.

        Args:
            path (str): The path to retrieve the extension from.

        Returns:
            str: The file extension.
        """
        return os.path.splitext(path)[1]

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalizes the specified path, eliminating double slashes, etc.

        Args:
            path (str): The path to be normalized.

        Returns:
            str: The normalized path.
        """
        return os.path.normpath(path)

