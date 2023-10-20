#!/usr/bin/env python

# Saver.py

# class for Saver (used in dedup_rename_gts_vcfpy.py)

from __future__ import annotations
import pandas as pd
from genomicspy.records_chunk import Chunk

__all__ = ["Saver"]

class Saver:
    """Class for save functions without having to init or check conditions"""
    
    accepted_dtypes = [("chunks", "pkl"),
                        ("gts", "pkl"),
                        ("gts", "tsv"),
                        ("meta", "pkl"),
                        ("meta", "tsv"),
                        ("seqids", "pkl"),
                        ("seqids", "tsv"),
                        ]
    def __init__(self):
        pass

    @classmethod
    def save(cls, chunk: Chunk, dpaths: dict[tuple[str, str], str]) -> None:
        """Save chunk data according to dpaths
        Arguments:
          chunk:  Chunk object
          dpaths: dict with keys as tuples (dtype, fmt) and values as dir paths.
                  Accepted dtypes:
                    - ("chunks", "pkl")
                    - ("gts", "pkl")
                    - ("gts", "tsv")
                    - ("meta", "pkl")
                    - ("meta", "tsv")
                    - ("seqids", "pkl")
                    - ("seqids", "tsv")
        Returns: None
        """
        for dtype, dpath in dpaths.items():
            match dtype:
                case ("chunks", "pkl"):
                    cls.save_chunks_pkl(chunk, dpath)
                case ("gts", "pkl"):
                    cls.save_gts_pkl(chunk, dpath)
                case ("gts", "tsv"):
                    cls.save_gts_tsv(chunk, dpath)
                case ("meta", "pkl"):
                    cls.save_meta_pkl(chunk, dpath)
                case ("meta", "tsv"):
                    cls.save_meta_tsv(chunk, dpath)
                case ("seqids", "pkl"):
                    cls.save_seqids_pkl(chunk, dpath)
                case ("seqids", "tsv"):
                    cls.save_seqids_tsv(chunk, dpath)
                case _:
                    raise ValueError("Unrecognized dtype", dtype)


    @staticmethod
    def save_chunks_pkl(chunk: Chunk, dpath: str):
        """Save chunk as pickle to directory dpath"""
        chunk.to_pickle(f"{dpath}/{chunk.pos}.chunk.pkl.gz")
    
    @staticmethod
    def save_gts_pkl(chunk: Chunk, dpath: str):
        """Save genotypes as pickle to directory dpath"""
        chunk.gts.to_pickle(
            f"{dpath}/{chunk.pos}.gts.pkl.gz", compression="gzip")

    @staticmethod
    def save_gts_tsv(chunk: Chunk, dpath: str):
        """Save genotypes as tsv to directory dpath"""
        gts_to_csv = chunk.gts.copy()
        gts_to_csv.columns = ['_'.join([str(x) for x in col])
                              for col in gts_to_csv.columns.to_flat_index()]
        gts_to_csv.to_csv(f"{dpath}/{chunk.pos}.gts.tsv.gz", sep="\t")

    @staticmethod
    def save_meta_pkl(chunk: Chunk, dpath: str):
        """Save metadata as pkl to directory dpath"""
        chunk.meta.to_pickle(
            f"{dpath}/{chunk.pos}.meta.pkl.gz", compression="gzip")
    
    @staticmethod
    def save_meta_tsv(chunk: Chunk, dpath: str):
        """Save metadata as tsv to directory dpath"""
        chunk.meta.assign(SEQID=chunk.meta.SEQID.str.join(';')).to_csv(
            f"{dpath}/{chunk.pos}.meta.tsv.gz", sep="\t")
        
    @staticmethod
    def save_seqids_pkl(chunk: Chunk, dpath: str):
        """Save seqids as pkl to directory dpath"""
        pd.concat({chunk.pos: chunk.seqids}, names=["CHUNK_POS"]).to_pickle(
            f"{dpath}/{chunk.pos}.seqids.pkl.gz", compression="gzip")
        
    @staticmethod
    def save_seqids_tsv(chunk: Chunk, dpath: str):
        """Save metadata as tsv to directory dpath"""
        pd.concat({chunk.pos: chunk.seqids}, names=["CHUNK_POS"]).to_csv(
            f"{dpath}/{chunk.pos}.seqids.tsv.gz", sep="\t")
