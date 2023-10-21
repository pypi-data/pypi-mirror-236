# Python DriftBytes

Python bindings for [DriftBytes](https://github.com/panda-official/DriftBytes).

## Requirements

* Python >= 3.8
* CMake >= 3.16 (for building)
* C++17 compiler (for building)
* conan >= 1.56, < 2.0 (for building)

## Installation

```bash
pip install drift-bytes
```

## Usage Example

```python
from drift_bytes import Variant, InputBuffer, OutputBuffer

out_buf = OutputBuffer(3)
out_buf[0] = None
out_buf[1] = Variant(2)
out_buf[2] = [1.0, 2.0, 3.0]

in_buf = InputBuffer(out_buf.bytes())

assert in_buf[0].value is None
assert in_buf[1].value == 2
assert in_buf[2].value == [1.0, 2.0, 3.0]
```
