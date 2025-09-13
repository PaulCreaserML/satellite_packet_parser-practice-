import unittest
from telemetry_parser import parse_telemetry

class TestTelemetryParser(unittest.TestCase):

    def test_valid_packet(self):
        """
        Tests the parser with a known valid telemetry packet.
        """
        # Input Hex String: AE5F1B0F68E54D600100191D4C0BB8FC1800005B
        test_packet = "AE5F1B0F68E54D600100191D4C0BB8FC1800005B"
        packet_bytes = bytes.fromhex(test_packet)
        
        expected_output = {
            "timestamp": 1759858016,
            "status": "NOMINAL",
            "temperature_c": 25,
            "battery_mv": 7500,
            "wheel_speeds_rpm": {
                "x": 3000,
                "y": -1000,
                "z": 0
            }
        }
        
        parsed_data = parse_telemetry(packet_bytes)
        self.assertDictEqual(parsed_data, expected_output)

    def test_invalid_checksum(self):
        """
        Tests the parser with a packet that has an incorrect checksum.
        """
        # Input Hex String: AE5F1B0F68E54D600100191D4C0BB8FC180000FF
        # The last byte is FF instead of the correct 52
        packet_bytes = bytes.fromhex("AE5F1B0F68E54D600100191D4C0BB8FC180000FF")
        parsed_data = parse_telemetry(packet_bytes)
        self.assertIsNone(parsed_data)

    def test_invalid_sync_word(self):
        """
        Tests the parser with a packet that has an incorrect sync word.
        """
        # Changed the first two bytes from AE5F to FFFF
        packet_bytes = bytes.fromhex("FFFF1B0F68E54D600100191D4C0BB8FC180000AA")
        parsed_data = parse_telemetry(packet_bytes)
        self.assertIsNone(parsed_data)
        
    def test_incorrect_length_packet(self):
        """
        Tests the parser with a packet that is shorter than 20 bytes.
        """
        packet_bytes = bytes.fromhex("AE5F1B0F")
        parsed_data = parse_telemetry(packet_bytes)
        self.assertIsNone(parsed_data)
        
    def test_non_bytes_input(self):
        """
        Tests the parser with an input that is not a bytes object.
        """
        packet_list = [1, 2, 3]
        parsed_data = parse_telemetry(packet_list)
        self.assertIsNone(parsed_data)

if __name__ == '__main__':
    unittest.main()

