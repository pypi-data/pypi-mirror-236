# Config Injection

![Unittest](https://github.com/ahartlba/inject_config/actions/workflows/actions.yml/badge.svg?branch=main)
![Static Badge](https://img.shields.io/badge/https%3A%2F%2Fimg.shields.io%2Fbadge%2Fcode%2520style-black-black?label=codestyle)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/inject-config)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

A decorator for injecting config from files and other sources.

Example use-case:

```yaml
# conf/config.yml
target_device: /path/to/device
n_runs: 12
use_gpu: false
```

```python
from inject_config import inject_config
from start_simulation import start_simulation

@inject_config.from_yaml('conf/config.yml')
def run_simulation(sim_config: dict) -> dict:
    start_simulation(sim_config)
```

For more examples look at the tests :)
