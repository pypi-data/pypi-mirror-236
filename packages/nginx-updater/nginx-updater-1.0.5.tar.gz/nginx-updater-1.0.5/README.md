# nginx-updater

Python module updater that uses nginx as backend

## Installation

You can install the package via pip:

```bash
pip install nginx-updater
```

## Usage

```python
from nginx_updater.updater import check_for_updates

config = [
    {
        "name": "package",
        "url": "https://static.example.com/package.tar.bz2",
        "username": "username",
        "password": "password",
        "file_path": "dist/package.tar.bz2",
        "extract_dir": "downloaded",
        "exclude": [],
    },
]


check_for_updates(config, restart=False)
```

## License

This project is licensed under the terms of the MIT license.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

If you want to contact me you can reach me at pradishbijukchhe@gmail.com.
