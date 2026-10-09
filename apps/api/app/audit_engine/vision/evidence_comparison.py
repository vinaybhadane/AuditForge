"""Photographic comparison and difference detection between inspection viewpoints."""

from typing import Dict
from uuid import UUID

from app.audit_engine.preprocessing.images import hamming_distance


def compare_photographs_perceptual(
    hash_a: str,
    hash_b: str,
    id_a: UUID,
    id_b: UUID,
) -> Dict:
    """Compare two photographs using perceptual difference hash.
    
    Returns similarity analysis with explicit caveats.
    """
    distance = hamming_distance(hash_a, hash_b)
    is_near_duplicate = distance <= 5

    return {
        "evidence_id_a": id_a,
        "evidence_id_b": id_b,
        "hamming_distance": distance,
        "is_near_duplicate": is_near_duplicate,
        "similarity_score": round(max(0.0, 1.0 - (distance / 64.0)), 3),
        "caveat": (
            "Perceptual similarity indicates visual resemblance of camera angles or framing; "
            "it does not constitute proof of reused work or fraudulent submission."
        ),
    }
