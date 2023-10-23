"""For extracting genotypes and other data from vcfs"""

from __future__ import annotations


__all__ = [
    "VCF_COLS"
]

VCF_COLS = ["CHROM", "POS", "ID", "REF",
            "ALT", "QUAL", "FILTER", "INFO", "FORMAT"]