// Copyright 2023 PANDA GmbH

#ifndef DRIFT_BYTES_BYTES_H_
#define DRIFT_BYTES_BYTES_H_

#include <array>
#include <cassert>
#include <functional>
#include <iostream>
#include <numeric>
#include <ostream>
#include <sstream>
#include <string>
#include <utility>
#include <variant>
#include <vector>

#include <cereal/archives/portable_binary.hpp>
#include <cereal/types/string.hpp>
#include <cereal/types/vector.hpp>

namespace drift_bytes {

const uint8_t kVersion = 0;

enum Type : uint8_t {
  kBool = 0,
  kInt8 = 1,
  kUInt8 = 2,
  kInt16 = 3,
  kUInt16 = 4,
  kInt32 = 5,
  kUInt32 = 6,
  kInt64 = 7,
  kUInt64 = 8,
  kFloat32 = 9,
  kFloat64 = 10,
  kString = 11,
  kNone = 12,
};

static const std::vector<std::string> kSupportedType = {
    "bool",  "int8",   "uint8",   "int16",   "uint16", "int32", "uint32",
    "int64", "uint64", "float32", "float64", "string", "none"};

using Shape = std::vector<uint32_t>;

using VarElement =
    std::variant<bool, int8_t, uint8_t, int16_t, uint16_t, int32_t, uint32_t,
                 int64_t, uint64_t, float, double, std::string>;
using VarArray = std::vector<VarElement>;

/**
 * @brief The Variant class
 * @details This class is used to store a single value or a vector of values of
 * different types.
 */
class Variant {
 public:
  /**
   * @brief Default constructor
   * @details Creates a Variant of type None
   */
  Variant() : type_(kNone), shape_({0}), data_() {}

  /**
   * @brief Construct a new Variant object
   * @details Use first element of data to determine type
   * @param shape
   * @param data
   */
  Variant(Shape shape, VarArray data)
      : type_(), shape_(std::move(shape)), data_(std::move(data)) {
    auto size = std::accumulate(shape_.begin(), shape_.end(), 1,
                                std::multiplies<uint32_t>());
    if (data_.size() != size) {
      throw std::out_of_range("Shape and data size do not match");
    }

    if (data_.empty()) {
      type_ = kNone;
      return;
    }

    type_ = static_cast<Type>(data_[0].index());
  }

  /**
   * @brief Construct a new Variant object from a single value
   * @tparam T
   * @param value
   */
  template <typename T>
  explicit Variant(T value) : type_(), shape_(), data_() {
    shape_ = {1};
    data_ = {value};
    type_ = static_cast<Type>(data_[0].index());
  }

  /**
   * @brief check if Variant is of type None
   * @return
   */
  [[nodiscard]] bool is_none() const { return type_ == kNone; }

  /**
   * @brief cast Variant to type T and return first element
   * @tparam T
   * @return
   */
  template <typename T>
  operator T() const {
    if (type_ == kNone) {
      throw std::runtime_error("Type is None");
    }

    auto casted = VarElement(T{}).index();
    if (type_ != casted) {
      throw std::runtime_error("Type mismatch: type '" + kSupportedType[type_] +
                               "' casted to '" + kSupportedType[casted] + "'");
    }

    if (shape_ != Shape{1}) {
      throw std::runtime_error("Looks like it is a vector");
    }
    return std::get<T>(data_[0]);
  }

  [[nodiscard]] Type type() const { return type_; }

  [[nodiscard]] const Shape &shape() const { return shape_; }

  [[nodiscard]] const VarArray &data() const { return data_; }

  bool operator==(const Variant &rhs) const {
    return type_ == rhs.type_ && shape_ == rhs.shape_ && data_ == rhs.data_;
  }

  bool operator!=(const Variant &rhs) const { return !(rhs == *this); }

  friend std::ostream &operator<<(std::ostream &os, const Variant &variant) {
    os << "Variant(type:" << kSupportedType[variant.type_] << ", shape:{";
    for (auto &dim : variant.shape_) {
      os << dim << ",";
    }
    os << "}, data:{";

    for (auto &value : variant.data_) {
      switch (variant.type_) {
        case kBool: {
          os << std::get<bool>(value) << ", ";
          break;
        }
        case kInt8: {
          os << std::get<int8_t>(value) << ",";
          break;
        }
        case kUInt8: {
          os << std::get<uint8_t>(value) << ",";
          break;
        }
        case kInt16: {
          os << std::get<int16_t>(value) << ",";
          break;
        }
        case kUInt16: {
          os << std::get<uint16_t>(value) << ",";
          break;
        }
        case kInt32: {
          os << std::get<int32_t>(value) << ",";
          break;
        }
        case kUInt32: {
          os << std::get<uint32_t>(value) << ",";
          break;
        }
        case kInt64: {
          os << std::get<int64_t>(value) << ",";
          break;
        }
        case kUInt64: {
          os << std::get<uint64_t>(value) << ",";
          break;
        }
        case kFloat32: {
          os << std::get<float>(value) << ",";
          break;
        }
        case kFloat64: {
          os << std::get<double>(value) << ",";
          break;
        }
        case kString: {
          os << std::get<std::string>(value) << ",";
          break;
        }
        case kNone: {
          os << "None, ";
          break;
        }
      }
    }

    os << "})";
    return os;
  }

 private:
  Type type_;
  Shape shape_;
  VarArray data_;
};

/**
 * @brief The OutputBuffer class
 * @details This class is used to deserialize a string of bytes into an array of
 * Variants
 */
class InputBuffer {
 public:
  /**
   * @brief Construct a new Input Buffer object from a string
   * @param bytes
   */
  explicit InputBuffer(std::string &&bytes) {
    std::stringstream buffer;
    buffer << bytes;

    {
      cereal::PortableBinaryInputArchive archive(buffer);
      uint8_t version;
      archive(version);

      if (version != kVersion) {
        throw std::runtime_error("Version mismatch: received " +
                                 std::to_string(version) + ", expected " +
                                 std::to_string(kVersion));
      }
    }

    while (buffer.rdbuf()->in_avail() != 0) {
      cereal::PortableBinaryInputArchive arc(buffer);

      Type type;
      Shape shape;
      arc(type, shape);

      auto size = std::accumulate(shape.begin(), shape.end(), 1,
                                  std::multiplies<uint32_t>());
      VarArray data(size);
      for (auto &value : data) {
        switch (type) {
          case kBool: {
            bool bool_value;
            arc(bool_value);
            value = bool_value;
            break;
          }
          case kInt8: {
            int8_t int8_value;
            arc(int8_value);
            value = int8_value;
            break;
          }
          case kUInt8: {
            uint8_t uint8_value;
            arc(uint8_value);
            value = uint8_value;
            break;
          }

          case kInt16: {
            int16_t int16_value;
            arc(int16_value);
            value = int16_value;
            break;
          }
          case kUInt16: {
            uint16_t uint16_value;
            arc(uint16_value);
            value = uint16_value;
            break;
          }
          case kInt32: {
            int32_t int32_value;
            arc(int32_value);
            value = int32_value;
            break;
          }
          case kUInt32: {
            uint32_t uint32_value;
            arc(uint32_value);
            value = uint32_value;
            break;
          }
          case kInt64: {
            int64_t int64_value;
            arc(int64_value);
            value = int64_value;
            break;
          }
          case kUInt64: {
            uint64_t uint64_value;
            arc(uint64_value);
            value = uint64_value;
            break;
          }
          case kFloat32: {
            float float_value;
            arc(float_value);
            value = float_value;
            break;
          }
          case kFloat64: {
            double double_value;
            arc(double_value);
            value = double_value;
            break;
          }
          case kString: {
            std::string string_value;
            arc(string_value);
            value = string_value;
            break;
          }
          case kNone: {
            throw std::runtime_error("None");
          }

          default:
            throw std::runtime_error("Unknown type");
        }
      }

      data_.emplace_back(std::move(shape), std::move(data));
    }
  }

  /**
   * @brief pop a Variant from the buffer
   * @return
   */
  Variant pop() {
    if (data_.empty()) {
      throw std::runtime_error("Buffer is empty");
    }
    auto variant = data_.front();
    data_.erase(data_.begin());
    return variant;
  }

  Variant operator[](size_t index) const { return data_[index]; }

  [[nodiscard]] bool empty() const { return data_.empty(); }

  [[nodiscard]] size_t size() const { return data_.size(); }

 private:
  std::vector<Variant> data_;
};

/**
 * @brief The OutputBuffer class
 * @details This class is used to serialize an array of Variants into a string
 */
class OutputBuffer {
 public:
  OutputBuffer() : data_() {}

  explicit OutputBuffer(size_t size) : data_(size) {}

  [[nodiscard]] std::string str() const {
    std::stringstream buffer;
    {
      cereal::PortableBinaryOutputArchive archive(buffer);
      archive(kVersion);
    }

    for (auto &variant : data_) {
      cereal::PortableBinaryOutputArchive arc(buffer);
      arc(variant.type(), variant.shape());
      for (const auto &value : variant.data()) {
        switch (variant.type()) {
          case kBool:
            arc(std::get<bool>(value));
            break;
          case kInt8:
            arc(std::get<int8_t>(value));
            break;
          case kUInt8:
            arc(std::get<uint8_t>(value));
            break;
          case kInt16:
            arc(std::get<int16_t>(value));
            break;
          case kUInt16:
            arc(std::get<uint16_t>(value));
            break;
          case kInt32:
            arc(std::get<int32_t>(value));
            break;
          case kUInt32:
            arc(std::get<uint32_t>(value));
            break;
          case kInt64:
            arc(std::get<int64_t>(value));
            break;
          case kUInt64:
            arc(std::get<uint64_t>(value));
            break;
          case kFloat32:
            arc(std::get<float>(value));
            break;
          case kFloat64:
            arc(std::get<double>(value));
            break;
          case kString:
            arc(std::get<std::string>(value));
            break;
          case kNone:
            throw std::runtime_error("None");
            break;
          default:
            throw std::runtime_error("Unknown type");
        }
      }
    }
    return buffer.str();
  }

  void push_back(const Variant &variant) { data_.push_back(variant); }

  Variant &operator[](size_t index) { return data_.at(index); }

  const Variant &operator[](size_t index) const { return data_.at(index); }

  [[nodiscard]] size_t size() const { return data_.size(); }

  [[nodiscard]] bool empty() const { return data_.empty(); }

 private:
  std::vector<Variant> data_;
};

}  // namespace drift_bytes
#endif  // DRIFT_BYTES_BYTES_H_
