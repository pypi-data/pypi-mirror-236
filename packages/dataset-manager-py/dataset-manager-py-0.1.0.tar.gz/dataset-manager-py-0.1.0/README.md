# dataset-manager-py

Python wrapper over the HuggingFace datasets library that makes it easier to load and convert datasets.

```python
# Import the DatasetManager class
from dataset.manager import DatasetManager

# Instantiate a new HuggingFaceDatasetLoader object
manager = DatasetManager()

# Download a dataset from the HuggingFace Hub
dataset = manager.load_from_hub(dataset_name="cuad")

# Calling dataset will print out the top-level detail about the dataset
dataset

DatasetDict({
    train: Dataset({
        features: ['id', 'title', 'context', 'question', 'answers'],
        num_rows: 22450
    })
    test: Dataset({
        features: ['id', 'title', 'context', 'question', 'answers'],
        num_rows: 4182
    })
})

# You can also save the dataset to disk
manager.save_to_disk(path="cuad-dataset")

# And reload the dataset from disk
reloaded_dataset = manager.load_from_disk(path="cuad-dataset")

# It's also possible to compress the dataset into either a zip file or a tarball
# Defaults to the 'zip' format
manager.archive_dataset(dataset_dir="cuad-dataset", archive_path=".", archive_format="zip")
```
