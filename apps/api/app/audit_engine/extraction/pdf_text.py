"""Native PDF text extraction engine."""

import re
import zlib
from typing import List, Tuple


def _decode_flate_streams(content: bytes) -> List[bytes]:
    """Find and decompress /FlateDecode streams in PDF bytes."""
    streams = []
    pattern = re.compile(rb"stream[\r\n]+(.*?)[\r\n]+endstream", re.DOTALL)
    for match in pattern.finditer(content):
        raw_stream = match.group(1)
        try:
            decompressed = zlib.decompress(raw_stream)
            streams.append(decompressed)
        except Exception:
            # Not a valid zlib stream or raw stream
            streams.append(raw_stream)
    return streams


def _extract_text_from_stream(stream: bytes) -> str:
    """Extract human-readable text from PDF stream operators Tj and TJ."""
    text_fragments = []

    # 1. Matches text in literal parentheses: (Sample Text) Tj
    tj_matches = re.findall(rb"\((.*?)\)\s*Tj", stream)
    for fragment in tj_matches:
        try:
            text_fragments.append(fragment.decode("latin1", errors="ignore"))
        except Exception:
            pass

    # 2. Matches array format: [(Item) -10 (Name)] TJ
    array_matches = re.findall(rb"\[(.*?)\]\s*TJ", stream)
    for arr in array_matches:
        inner_items = re.findall(rb"\((.*?)\)", arr)
        for fragment in inner_items:
            try:
                text_fragments.append(fragment.decode("latin1", errors="ignore"))
            except Exception:
                pass

    return " ".join(text_fragments)


def extract_native_pdf_text(content: bytes) -> Tuple[str, bool]:
    """Extract native text from PDF content.
    
    Returns:
        Tuple of (extracted_text, is_complete)
    """
    if not content.startswith(b"%PDF-"):
        # If passed plain text/markdown directly for synthetic tests
        try:
            return content.decode("utf-8", errors="ignore"), True
        except Exception:
            return "", False

    decompressed_streams = _decode_flate_streams(content)
    extracted_fragments = []

    for stream in decompressed_streams:
        frag = _extract_text_from_stream(stream)
        if frag.strip():
            extracted_fragments.append(frag)

    full_text = "\n".join(extracted_fragments).strip()

    # If stream parsing found minimal text, scan for raw uncompressed strings
    if len(full_text) < 20:
        raw_strings = re.findall(rb"\(([\w\s\d.,:;/-]{3,})\)", content)
        decoded = [s.decode("latin1", errors="ignore") for s in raw_strings]
        full_text = " ".join(decoded).strip()

    is_complete = len(full_text) > 0
    return full_text, is_complete
