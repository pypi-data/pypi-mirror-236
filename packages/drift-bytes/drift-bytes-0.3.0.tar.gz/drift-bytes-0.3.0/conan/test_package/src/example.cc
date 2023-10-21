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
