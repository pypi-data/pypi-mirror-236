// Copyright 2023PANDA GmbH
#include <drift_bytes/bytes.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <utility>

namespace py = pybind11;
using drift_bytes::InputBuffer;
using drift_bytes::kSupportedType;
using drift_bytes::OutputBuffer;
using drift_bytes::Shape;
using drift_bytes::Type;
using drift_bytes::VarArray;
using drift_bytes::Variant;

template <typename T>
std::vector<T> make_array(const Variant &variant) {
  std::vector<T> ary(std::accumulate(variant.shape().begin(),
                                     variant.shape().end(), 1,
                                     std::multiplies<int64_t>()));
  for (int i = 0; i < ary.size(); ++i) {
    try {
      ary[i] = std::get<T>(variant.data()[i]);
    } catch (const std::bad_variant_access &) {
      throw std::runtime_error(
          "Type mismatch: " + kSupportedType[variant.type()] +
          " != " + kSupportedType[std::variant<T>().index()]);
    }
  }
  return ary;
}

PYBIND11_MODULE(_drift_bytes, m) {
  m.def("supported_types",
        []() -> std::vector<std::string> { return kSupportedType; });

  auto variant = py::class_<Variant>(m, "Variant");
  variant.def_static("from_none", []() -> Variant { return {}; })
      .def_static("from_bools",
                  [](Shape shape, std::vector<bool> array) -> Variant {
                    VarArray var_array(array.size());
                    for (int i = 0; i < array.size(); ++i) {
                      var_array[i] = static_cast<bool>(
                          array[i]);  // We do it because apple-clang converts
                                      // bool to int
                    }

                    return {std::move(shape), std::move(var_array)};
                  })
      .def_static(
          "from_int8s",
          [](Shape shape, std::vector<int8_t> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_uint8s",
          [](Shape shape, std::vector<uint8_t> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_int16s",
          [](Shape shape, std::vector<int16_t> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_uint16s",
          [](Shape shape, std::vector<uint16_t> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_int32s",
          [](Shape shape, std::vector<int32_t> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_uint32s",
          [](Shape shape, std::vector<uint32_t> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_int64s",
          [](Shape shape, std::vector<int64_t> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_uint64s",
          [](Shape shape, std::vector<uint64_t> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_float32s",
          [](Shape shape, std::vector<float> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_float64s",
          [](Shape shape, std::vector<double> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def_static(
          "from_strings",
          [](Shape shape, std::vector<std::string> array) -> Variant {
            return {std::move(shape), VarArray(array.begin(), array.end())};
          })
      .def("to_bools",
           [](Variant &variant) -> std::vector<bool> {
             return make_array<bool>(variant);
           })
      .def("to_int8s",
           [](Variant &variant) -> std::vector<int8_t> {
             return make_array<int8_t>(variant);
           })
      .def("to_uint8s",
           [](Variant &variant) -> std::vector<uint8_t> {
             return make_array<uint8_t>(variant);
           })
      .def("to_int16s",
           [](Variant &variant) -> std::vector<int16_t> {
             return make_array<int16_t>(variant);
           })
      .def("to_uint16s",
           [](Variant &variant) -> std::vector<uint16_t> {
             return make_array<uint16_t>(variant);
           })
      .def("to_int32s",
           [](Variant &variant) -> std::vector<int32_t> {
             return make_array<int32_t>(variant);
           })
      .def("to_uint32s",
           [](Variant &variant) -> std::vector<uint32_t> {
             return make_array<uint32_t>(variant);
           })
      .def("to_int64s",
           [](Variant &variant) -> std::vector<int64_t> {
             return make_array<int64_t>(variant);
           })
      .def("to_uint64s",
           [](Variant &variant) -> std::vector<uint64_t> {
             return make_array<uint64_t>(variant);
           })
      .def("to_float32s",
           [](Variant &variant) -> std::vector<float> {
             return make_array<float>(variant);
           })
      .def("to_float64s",
           [](Variant &variant) -> std::vector<double> {
             return make_array<double>(variant);
           })
      .def("to_strings",
           [](Variant &variant) -> std::vector<std::string> {
             return make_array<std::string>(variant);
           })
      .def("type",
           [](Variant &variant) -> std::string {
             return kSupportedType.at(variant.type());
           })
      .def("shape", [](Variant &variant) -> Shape { return variant.shape(); });

  auto input_buffer = py::class_<InputBuffer>(m, "InputBuffer");
  input_buffer
      .def_static("from_bytes",
                  [](py::bytes bytes) { return InputBuffer(std::move(bytes)); })
      .def("pop", [](InputBuffer &buffer) -> Variant { return buffer.pop(); })
      .def("get",
           [](InputBuffer &buffer, size_t index) -> Variant {
             return buffer[index];
           })
      .def("empty", [](InputBuffer &buffer) -> bool { return buffer.empty(); })
      .def("size", [](InputBuffer &buffer) -> size_t { return buffer.size(); });

  auto output_buffer = py::class_<OutputBuffer>(m, "OutputBuffer");
  output_buffer.def(py::init([](size_t size) { return OutputBuffer(size); }))
      .def("push", [](OutputBuffer &buffer,
                      const Variant &variant) { buffer.push_back(variant); })
      .def("set", [](OutputBuffer &buffer, size_t index,
                     const Variant &variant) { buffer[index] = variant; })
      .def("bytes",
           [](OutputBuffer &buffer) -> py::bytes { return buffer.str(); })
      .def("size",
           [](OutputBuffer &buffer) -> size_t { return buffer.size(); });
}
