# DriftBytes

A serializer for typed data in the Drift infrastructure.

## Description

This is an alternative to [WaveletBuffer](https://github.com/panda-official/WaveletBuffer) that uses a different serialization format
which is suitable for non-floating point data.

## Features

* Supports all integer types
* Supports all floating point types
* Supports UTF-8 strings
* Supports vectors and matrices of all supported types

## Requirements

* CMake >= 3.16
* C++17 compiler
* conan >= 1.56, < 2.0


## Bindings

* [Python](python/README.md)

## Usage Example

```c++
#include <drift_bytes/bytes.h>

#include <iostream>

using drift_bytes::InputBuffer;
using drift_bytes::OutputBuffer;
using drift_bytes::Variant;

int main() {
  Variant some_value{42};

  OutputBuffer buffer(1);
  buffer[0] = some_value;

  InputBuffer input(buffer.str());
  Variant new_val = input[0];

  std::cout << new_val << std::endl;
}

```

## Bulding

```bash
mkdir build && cd build
conan install ../conan --build=missing -of .
cmake .. -DCMAKE_TOOLCHAIN_FILE=./build/Release/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build .
```
