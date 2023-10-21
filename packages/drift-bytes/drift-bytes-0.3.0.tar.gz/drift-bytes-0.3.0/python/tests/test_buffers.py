"""Test the InputBuffer and OutputBuffer classes."""
from drift_bytes import Variant, InputBuffer, OutputBuffer


def test_input_output():
    """Should push and pop"""
    out_buf = OutputBuffer()
    out_buf.push(Variant([1, 2, 3, 4, 5, 6]))

    in_buf = InputBuffer(out_buf.bytes())

    var = in_buf.pop()
    assert var.type == "int64"
    assert var.shape == [6]
    assert var.value == [1, 2, 3, 4, 5, 6]

    assert in_buf.empty()


def test_item_access():
    """Should access items"""
    out_buf = OutputBuffer(3)
    out_buf[0] = None
    out_buf[1] = Variant(2)
    out_buf[2] = [1.0, 2.0, 3.0]

    in_buf = InputBuffer(out_buf.bytes())

    assert in_buf[0].value is None
    assert in_buf[1].value == 2
    assert in_buf[2].value == [1.0, 2.0, 3.0]
