### DaemonStarter

DaemonStarter demo:

```python
from daemon_starter import starter, get_logger


def exec():
    while 1:
        pass


starter(exec)

# or

def run(_logger):
    watcher = Task(_logger)
    watcher.start()


if __name__ == '__main__':
    logger = get_logger('public_watcher.log')
    starter(run, _logger=logger)
```
