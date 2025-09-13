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
