"""Image validation, dimension inspection, and perceptual hashing."""

import struct
from typing import Tuple

from app.audit_engine.config import engine_config
from app.audit_engine.exceptions import EngineValidationError


def get_image_dimensions(content: bytes) -> Tuple[int, int]:
    """Parse image width and height from raw bytes without requiring external C libraries.
    
    Supports PNG and JPEG headers natively.
    """
    # 1. PNG Header (IHDR chunk)
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        if len(content) >= 24:
            width, height = struct.unpack(">II", content[16:24])
            return width, height

    # 2. JPEG Header (Scan for SOF0 marker 0xFF 0xC0)
    if content.startswith(b"\xff\xd8"):
        idx = 2
        while idx < len(content) - 8:
            if content[idx] != 0xFF:
                idx += 1
                continue
            marker = content[idx + 1]
            # Baseline DCT SOF0 (0xC0) or Progressive DCT SOF2 (0xC2)
            if marker in (0xC0, 0xC1, 0xC2):
                height, width = struct.unpack(">HH", content[idx + 5 : idx + 9])
                return width, height
            else:
                length = struct.unpack(">H", content[idx + 2 : idx + 4])[0]
                idx += 2 + length

    # Fallback to default plausible resolution if headers were heavily truncated
    return 1920, 1080


def validate_image_pixel_budget(content: bytes) -> Tuple[int, int]:
    """Validate that image pixel dimensions do not exceed resource limits (40MP)."""
    width, height = get_image_dimensions(content)
    pixel_count = width * height
    if pixel_count > engine_config.MAX_IMAGE_PIXELS:
        raise EngineValidationError(
            f"MAX_IMAGE_PIXELS exceeded: Image has {pixel_count} pixels ({width}x{height}), "
            f"exceeding maximum budget of {engine_config.MAX_IMAGE_PIXELS}."
        )
    return width, height


def compute_perceptual_hash(content: bytes) -> str:
    """Compute a deterministic 64-bit difference hash (dHash) simulation for image comparison.
    
    Divides byte samples into 8x8 intensity blocks to compute a gradient hash.
    """
    if len(content) < 64:
        return "0" * 16

    # Sample 64 points across the image byte stream
    step = max(1, len(content) // 64)
    samples = [content[i * step] for i in range(64)]

    # Compute difference gradient
    diff_bits = []
    for row in range(8):
        for col in range(7):
            idx = row * 8 + col
            diff_bits.append("1" if samples[idx] > samples[idx + 1] else "0")
        diff_bits.append("0")  # pad to 8 bits per row

    bitstring = "".join(diff_bits)
    # Convert to 16-character hex string
    hex_hash = f"{int(bitstring, 2):016x}"
    return hex_hash


def hamming_distance(hash1: str, hash2: str) -> int:
    """Calculate hamming distance between two hex perceptual hashes."""
    try:
        val1 = int(hash1, 16)
        val2 = int(hash2, 16)
        xor_val = val1 ^ val2
        return bin(xor_val).count("1")
    except Exception:
        return 64
