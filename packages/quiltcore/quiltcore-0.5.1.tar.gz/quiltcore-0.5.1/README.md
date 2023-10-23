# QuiltCore

QuiltCore is a library for building and running [Quilt](https://quiltdata.com) data packages.
It is designed to leverage standard open source technology and YAML configuration files
so that it can easily be ported to other languages and platforms.

This initial implementation is in Python.

## Key Technologies

- Apache [Arrow](https://arrow.apache.org/) for reading, writing, and representing manifests
  - [PyArrow](https://arrow.apache.org/docs/python/) for Python bindings to Arrow
- fsspec [filesystems](https://filesystem-spec.readthedocs.io/en/latest/)
  for reading and writing files from various sources
- [PyYAML](https://pyyaml.org/) for reading and writing YAML configuration files

## Example

```bash
poetry install
```

```python
#!/usr/bin/env python
import os
from quiltcore import Domain, UDI
from tempfile import TemporaryDirectory
from upath import UPath

TEST_BKT = "s3://quilt-example"
TEST_PKG = "akarve/amazon-reviews"
TEST_TAG = "1570503102"
TEST_HASH = "ffe323137d0a84a9d1d6f200cecd616f434e121b3f53a8891a5c8d70f82244c2"
TEST_KEY = "camera-reviews"
WRITE_BKT = os.environ.get("WRITE_BUCKET")
SOURCE_URI = f"quilt+{TEST_BKT}#package={TEST_PKG}:{TEST_TAG}"
DEST_URI = f"quilt+{TEST_BKT}#package={TEST_PKG}:{TEST_TAG}"
```

### Get Manifest

<!--pytest-codeblocks:cont-->
```python
remote = UDI.FromUri(SOURCE_URI)
print(f"remote: {remote}")
with TemporaryDirectory() as tmpdir:
    local = UPath(tmpdir)
    domain = Domain.FromLocalPath(local)
    print(f"domain: {domain}")
    folder = domain.pull(remote)
    print(f"folder: {folder}")
    if WRITE_BKT:
        tag = domain.push(folder, remote=UDI.FromUri(DEST_URI))
        print(f"tag: {tag}")
```
