# ogmios

[![Pipeline](https://gitlab.com/viperscience/ogmios-python/badges/main/pipeline.svg)](https://gitlab.com/viperscience/ogmios-python/-/pipelines)
[![Documentation Status](https://readthedocs.org/projects/ogmios-python/badge/?version=latest)](https://ogmios-python.readthedocs.io/en/latest/?badge=latest)
[![PyPI - Version](https://img.shields.io/pypi/v/ogmios.svg)](https://pypi.org/project/ogmios)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ogmios.svg)](https://pypi.org/project/ogmios)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

1. Install cardano-node and Ogmios server as described [here](https://ogmios.dev/getting-started/). (Docker installation is recommended.)
2. Install ogmios-python using pip:

```console
pip install ogmios
```

## Quickstart

To see how easy it is to build on Cardano with ogmios-python, let's use the library to view new blocks as they are added to the 

```console
import time
import ogmios

with ogmios.Client() as client:
    # Set chain pointer to origin
    _, tip, _ = client.find_intersection.execute([ogmios.Origin()])

    # Now set chain pointer to tip
    _, _, _ = client.find_intersection.execute([tip.to_point()])

    # # Tail blockchain as new blocks come in beyond the current tip
    while True:
        client.next_block.execute()
        time.sleep(1)
```

For more examples, see the documentation and example scripts in the repo.

## License

`ogmios-python` is distributed under the terms of the [GPL-3.0-or-later](https://spdx.org/licenses/GPL-3.0-or-later.html) license.
