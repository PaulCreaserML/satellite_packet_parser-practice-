import struct

def parse_telemetry(packet: bytes) -> dict | None:
    """
    Parses a 20-byte AE-1 series telemetry packet.

    Args:
        packet: A bytes object representing the raw telemetry packet.

    Returns:
        A dictionary containing the parsed data if the packet is valid,
        otherwise None.
    """
    # 1. Validate Packet Structure and Length
    if not isinstance(packet, bytes) or len(packet) != 20:
        print("Error: Input must be a 20-byte object.")
        return None

    # 2. Validate Checksum
    calculated_checksum = 0
    for i in range(19):
        calculated_checksum ^= packet[i]

    if calculated_checksum != packet[19]:
        print(f"Error: Checksum mismatch. Expected {packet[19]}, got {calculated_checksum}.")
        return None

    # Unpack the header to validate Sync Word
    # '>' denotes big-endian byte order
    sync_word, packet_id, payload_length = struct.unpack('>HBB', packet[0:4])

    # 3. Validate Sync Word
    if sync_word != 0xAE5F:
        print(f"Error: Invalid sync word. Expected 0xAE5F, got {hex(sync_word)}.")
        return None
        
    # 4. Validate Packet ID and Payload Length for this specific packet type
    if packet_id != 0x1B or payload_length != 15:
        print(f"Error: Invalid Packet ID or Payload Length for health packet.")
        return None

    # 5. Parse the Data Fields
    try:
        # Unpack the payload fields
        # >I B h H h h h
        # I: uint32 (Timestamp)
        # B: uint8 (Status)
        # h: int16 (Temperature)
        # H: uint16 (Battery Voltage)
        # h: int16 (Wheel 1 Speed)
        # h: int16 (Wheel 2 Speed)
        # h: int16 (Wheel 3 Speed)
        (
            timestamp,
            status_enum,
            temperature,
            battery_voltage,
            wheel1_speed,
            wheel2_speed,
            wheel3_speed,
        ) = struct.unpack('>IBhHhhh', packet[4:19])

        # Convert status enum to string
        status_map = {0: "SAFE", 1: "NOMINAL", 2: "SCIENCE"}
        status_str = status_map.get(status_enum, "UNKNOWN")

        # 6. Return the structured result
        return {
            "timestamp": timestamp,
            "status": status_str,
            "temperature_c": temperature,
            "battery_mv": battery_voltage,
            "wheel_speeds_rpm": {
                "x": wheel1_speed,
                "y": wheel2_speed,
                "z": wheel3_speed,
            },
        }

    except struct.error as e:
        print(f"Error unpacking packet data: {e}")
        return None

