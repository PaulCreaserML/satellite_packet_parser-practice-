# AE-1 Series Telemetry Parser (Python Implementation)

A clean and robust Python function for parsing and validating binary health telemetry packets from the fictional ArkEdge Space "AE-1" series satellite.

## Project Overview

This project provides a critical component for a satellite ground segment: a function to parse raw binary telemetry packets into a human-readable format. The implementation is written in Python, leveraging the standard `struct` library for efficient binary data handling. It correctly processes big-endian byte order, validates packet integrity via checksums, and decodes the data according to the provided specification.

## Features

* **Validation First:** Ensures packet integrity by verifying the Sync Word and an 8-bit XOR checksum before parsing.

* **Pythonic and Readable:** Uses standard Python libraries and returns data in an easy-to-use dictionary or `None` on failure.

* **Big-Endian Handling:** Correctly decodes multi-byte fields from the network byte order (big-endian).

* **No External Dependencies:** Runs with a standard Python 3 installation.

* **Unit Tested:** Comes with a suite of tests using the built-in `unittest` module to verify correctness for both valid and invalid packets.

## Packet Specification

The AE-1 health telemetry packet is a fixed-length, 20-byte message. The data is encoded in **big-endian** byte order.

| Byte(s) | Field | Data Type | Description | 
 | ----- | ----- | ----- | ----- | 
| 0-1 | Sync Word | `uint16` | Fixed synchronization pattern: `0xAE5F`. | 
| 2 | Packet ID | `uint8` | Identifies the packet type. For this health packet, it's `0x1B`. | 
| 3 | Payload Length | `uint8` | The length of the payload section in bytes. Always 15 for this packet. | 
| 4-7 | Timestamp | `uint32` | The time the packet was generated, as a Unix timestamp. | 
| 8 | Status | `uint8` | An enumeration of the satellite's mode: `0=SAFE`, `1=NOMINAL`, `2=SCIENCE`. | 
| 9-10 | Temperature | `int16` | Main bus temperature in degrees Celsius. | 
| 11-12 | Battery Voltage | `uint16` | Battery bus voltage in millivolts (mV). | 
| 13-14 | Wheel 1 Speed | `int16` | Speed of reaction wheel 1 in Revolutions Per Minute (RPM). | 
| 15-16 | Wheel 2 Speed | `int16` | Speed of reaction wheel 2 in RPM. | 
| 17-18 | Wheel 3 Speed | `int16` | Speed of reaction wheel 3 in RPM. | 
| 19 | Checksum | `uint8` | 8-bit XOR checksum calculated over all preceding bytes (0-18). | 

## Getting Started

### Prerequisites

You will need Python 3.6 or newer installed on your system.

### Setup

1. **Clone the repository (or download the files):**# satellite_packet_parser-practice-

git clone <repository-url>
cd <repository-directory>


2. The project consists of two files:

* `telemetry_parser.py`: Contains the main parsing function.

* `test_telemetry_parser.py`: The unit tests.

### Running the Tests

To verify the implementation, run the unit tests from the project's root directory.

python -m unittest test_telemetry_parser.py


A successful run will show that the tests passed.

## Usage Example

To use the parser, import the `parse_telemetry` function from the `telemetry_parser.py` module.

**`main.py`**

from telemetry_parser import parse_telemetry
import json

A valid raw telemetry packet received from the satellite.
hex_string = "AE5F1B0F68E54D600100191D4C0BB8FC18000052"
raw_packet = bytes.fromhex(hex_string)

parsed_data = parse_telemetry(raw_packet)

if parsed_data:
print("--- Telemetry Packet Parsed Successfully ---")
# Use json.dumps for pretty printing the dictionary
print(json.dumps(parsed_data, indent=4))
else:
print("Failed to parse telemetry packet. It may be invalid.")


**Run your application:**

python main.py


## API Reference

### `parse_telemetry(packet: bytes) -> dict | None`

Parses a raw 20-byte telemetry packet.

* **`packet`** (`bytes`): A `bytes` object of length 20 containing the raw packet data.

* **Returns**: A `dictionary` containing the parsed data on success. On failure (e.g., checksum mismatch, invalid sync word, or wrong length), it returns `None`.

**Example Success Return:**

{
"timestamp": 1757107200,
"status": "NOMINAL",
"temperature_c": 25,
"battery_mv": 7500,
"wheel_speeds_rpm": {
"x": 3000,
"y": -1000,
"z": 0
}
}


## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
