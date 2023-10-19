# Import standard libraries
import shutil

# Import third-party libraries
from datasets import load_dataset, load_from_disk, DatasetDict


class DatasetManager:
    def __init__(self) -> None:
        self.dataset: DatasetDict = None

    def load_from_hub(self, dataset_name: str) -> DatasetDict:
        """Loads a dataset from HuggingFace's dataset hub.

        Args:
            dataset_name (str): The name of the dataset to load.

        Return:
            DatasetDict: The loaded dataset.
        """
        self.dataset = load_dataset(dataset_name)
        return self.dataset

    def load_from_disk(self, path: str) -> DatasetDict:
        """Loads a dataset from disk.

        Args:
            path (str): The path to the dataset on disk.

        Returns:
            DatasetDict: The loaded dataset.
        """
        self.dataset = load_from_disk(path)
        return self.dataset

    def save_to_disk(self, path: str) -> None:
        """Saves the current dataset to disk.

        Args:
            path (str): The path where the dataset will be saved.

        Raises:
            ValueError: If no dataset is loaded.
        """
        if self.dataset is not None:
            self.dataset.save_to_disk(path)
        else:
            raise ValueError("No dataset loaded, cannot save.")

    def archive_dataset(self, dataset_dir: str, archive_path: str, archive_format: str = "zip") -> None:
        """Archives the dataset directory into a zip file or tarball.

        Args:
            dataset_dir (str): Path to the dataset directory.
            archive_path (str): Path where the archive will be saved.
            archive_format (str): Format of the archive, "zip" or "tar".
        """
        if archive_format not in ["zip", "tar"]:
            raise ValueError("Invalid archive format. Use 'zip' or 'tar'.")

        shutil.make_archive(
            base_name=archive_path,
            format=archive_format,
            root_dir=dataset_dir
        )
