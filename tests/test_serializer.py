"""Tests for Serializer."""

from pyipp import parser, serializer
from pyipp.const import DEFAULT_CHARSET, DEFAULT_CHARSET_LANGUAGE, DEFAULT_PROTO_VERSION
from pyipp.enums import IppFinishing, IppOperation, IppTag
from tests import load_fixture_binary, save_fixture_binary


def test_construct_attribute_values() -> None:
    """Test the construct_attribute_values method."""
    result = serializer.construct_attribute_values(
        IppTag.INTEGER,
        IppOperation.GET_PRINTER_ATTRIBUTES,
    )
    assert result == b"\x00\x04\x00\x00\x00\x0b"

    result = serializer.construct_attribute_values(
        IppTag.ENUM,
        IppOperation.GET_PRINTER_ATTRIBUTES,
    )
    assert result == b"\x00\x04\x00\x00\x00\x0b"

    result = serializer.construct_attribute_values(
        IppTag.BOOLEAN,
        "0",
    )
    assert result == b"\x00\x01\x01"

    result = serializer.construct_attribute_values(
        IppTag.URI,
        "ipps://localhost:631",
    )
    assert result == b"\x00\x14ipps://localhost:631"


def test_construct_attribute() -> None:
    """Test the construct_attribute method."""
    result = serializer.construct_attribute("attributes-charset", DEFAULT_CHARSET)
    assert result == b"G\x00\x12attributes-charset\x00\x05utf-8"

    result = serializer.construct_attribute(
        "operations-supported",
        [IppOperation.GET_PRINTER_ATTRIBUTES],
    )
    assert result == b"#\x00\x14operations-supported\x00\x04\x00\x00\x00\x0b"


def test_construct_attribute_no_tag_unmapped() -> None:
    """Test the construct_attribute method with no tag and unmapped attribute name."""
    result = serializer.construct_attribute(
        "no-tag-unmapped",
        None,
    )

    assert result == b""


def test_encode_dict() -> None:
    """Test the encode_dict method."""
    result = serializer.encode_dict(
        {
            "version": DEFAULT_PROTO_VERSION,
            "operation": IppOperation.GET_PRINTER_ATTRIBUTES,
            "request-id": 1,
            "operation-attributes-tag": {
                "attributes-charset": DEFAULT_CHARSET,
                "attributes-natural-language": DEFAULT_CHARSET_LANGUAGE,
                "printer-uri": "ipp://printer.example.com:361/ipp/print",
                "requesting-user-name": "PythonIPP",
            },
        },
    )

    assert result == load_fixture_binary(
        "serializer/get-printer-attributes-request-000.bin",
    )


def test_encode_dict_job_attributes_tag() -> None:
    """Test the encode_dict method."""
    result = serializer.encode_dict(
        {
            "version": DEFAULT_PROTO_VERSION,
            "operation": IppOperation.GET_PRINTER_ATTRIBUTES,
            "request-id": 1,
            "operation-attributes-tag": {
                "attributes-charset": DEFAULT_CHARSET,
                "attributes-natural-language": DEFAULT_CHARSET_LANGUAGE,
                "printer-uri": "ipp://printer.example.com:361/ipp/print",
                "requesting-user-name": "PythonIPP",
            },
            "job-attributes-tag": {
                "sides": "two-sided-long-edge",
                "finishings": IppFinishing.STAPLE_TOP_LEFT,
            },
        },
    )

    assert result == load_fixture_binary(
        "serializer/test_encode_dict_job_attributes_tag.bin",
    )


def test_serialize_deserialize_completeness() -> None:
    """Test if the tags are present after serialization-deserializing (parsing).

    This test checks for a solution of the problem that pages were not printed in duplex mode.
    Root cause was that the "sides" attribute was not serialized.
    """
    encoded_result = serializer.encode_dict(
        {
            "version": DEFAULT_PROTO_VERSION,
            "operation": IppOperation.GET_PRINTER_ATTRIBUTES,
            "request-id": 1,
            "operation-attributes-tag": {
                "sides": "two-sided-long-edge",  # Double-sided printing
                "attributes-charset": DEFAULT_CHARSET,
                "attributes-natural-language": DEFAULT_CHARSET_LANGUAGE,
                "printer-uri": "ipp://printer.example.com:361/ipp/print",
                "requesting-user-name": "PythonIPP",
            },
            "job-attributes-tag": {
                "media": "iso_a4_210x297mm",  # Paper size A4
                "media-source": "tray-2",  # Specify tray 2
                "sides": "two-sided-long-edge",  # Double-sided printing
                "print-scaling": "auto",  # Scale content to fit media
                "dummy": "dummy",  # Dummy, does not need to exist
            },
        },
    )

    save_fixture_binary(
        "serializer/test_serialize_deserialize_completeness.bin",
        encoded_result,
    )

    decoded_result = parser.parse(encoded_result)

    assert decoded_result["job-attributes-tag"]["sides"] == "two-sided-long-edge"
    assert decoded_result["job-attributes-tag"]["media"] == "iso_a4_210x297mm"
    assert decoded_result["job-attributes-tag"]["media-source"] == "tray-2"
    assert decoded_result["job-attributes-tag"]["print-scaling"] == "auto"
    assert "dummy" not in decoded_result["job-attributes-tag"]

    # "sides" belongs to "job-attributes-tag" iso "operation-attributes-tag"
    # However, encoding/decoding process should not remove it
    assert decoded_result["operation-attributes-tag"]["sides"] == "two-sided-long-edge"


if __name__ == "__main__":
    test_construct_attribute_values()
    test_construct_attribute()
    test_construct_attribute_no_tag_unmapped()
    test_encode_dict()
    test_encode_dict_job_attributes_tag()
    test_serialize_deserialize_completeness()
