#!/usr/bin/env python

# Chunk.py

# class for Chunk (used in dedup_rename_gts_vcfpy.py)

from __future__ import annotations
import pickle
import os
from collections.abc import Collection, Iterable
from typing import Union
import pandas as pd
import vcfpy

from oddsnends import sort_levels

__all__ = ["Chunk"]

class Chunk:
    """Class for handling chunks of vcfpy.Records"""

    DEFAULT_ID_NAME = 'CHUNK_GT'

    def __init__(self,
                 records: Collection[vcfpy.Record] = None,
                 pos: int = None,
                 anns: dict = None,
                 **kwargs
                 ) -> None:
        # self._records = records
        self._pos = pos
        self._anns = {} if anns is None else anns

        # init other attributes
        self._gts = None
        self._seqids = None
        self._meta = None
        self._id_name = self.DEFAULT_ID_NAME
        
        if records is not None:
            self.process_records(records, inplace=True, **kwargs)

    def __len__(self):
        return self.nsites

    @staticmethod
    def group_assign_id(data: pd.DataFrame, id_name: str = 'INDEX') -> pd.DataFrame:
        """Group identical rows and assign unique index ID, sorts by min row sum

        Returns: pd.DataFrame with values dist and INDEX,
            index.values as data values, index.names as data.columns
        """
        # parse rows
        grouped = data.groupby(data.columns.to_list(), dropna=False).apply(
            lambda g: g.index).apply(list).rename(data.index.name).pipe(sort_levels)

        ## Assign ids
        # sort by row sum
        ids = grouped.index.to_frame().pipe(
            lambda df: df.rename(dict((c, i) for i, c in enumerate(df.columns)),
                                axis=1))

        # calculate and sort by distance (num differences) from ref
        ids = ids.assign(dist=ids.sum(axis=1)).sort_values(
            ["dist", *ids.columns]).drop(ids.columns, axis=1)

        non_refs = ids.loc[ids.dist > 0].pipe(
            lambda df: df.assign(**{id_name: range(1, len(df) + 1)}))

        ref = ids.loc[ids.dist == 0].assign(**{id_name: 0})

        combined = pd.concat([grouped, pd.concat([ref, non_refs], axis=0)], axis=1)
        combined.sort_values(id_name, inplace=True)
        return combined



    def process_records(self,
                        records: Iterable[vcfpy.Record],
                        pos: int = None,
                        gt_allele_idx: int = 0,
                        id_name: str = None,
                        inplace: bool = True
                        ) -> Union[dict, None]:
        """Process chunk of vcfpy.Records obtained from reader
        default id_name is Chunk.ID_NAME
        """
        # assert self._records is not None, "chunk.records not initialized"
        
        if pos is not None:
            self._pos = pos
        
        if id_name is None:
            id_name = self._id_name
        else:
            self._id_name = id_name
        
        # if len(self._records) == 0:
        if len(records) == 0:
            
            # hack together empty dataframes
            meta_cols = ["dist", "SEQID"]  # dist is from group_assign_id()
            
            idx_id_name = pd.Index([], name=id_name)
            multix_chrom_pos = pd.MultiIndex.from_tuples(
                [], names=["CHROM", "POS"])
            
            gts = pd.DataFrame(index=idx_id_name, columns=multix_chrom_pos)
            meta = pd.DataFrame(index=idx_id_name, columns=meta_cols)
            seqids = pd.DataFrame(index=pd.Index([], name="SEQID"),
                                  columns=[id_name])
        else:
            # extract info from calls
            calls = pd.DataFrame(
                ([rec.CHROM,
                rec.POS,
                call.gt_alleles[gt_allele_idx],
                call.sample] for rec in records for call in rec
                # ] for rec in self.records for call in rec
                ), columns=['CHROM', 'POS', 'GT', 'SEQID'])

            chunk = calls.pivot_table("GT", "SEQID", ["CHROM", "POS"], lambda x: x
                                    ).pipe(self.group_assign_id, id_name=id_name)

            # dataframe with values GTs, index CHUNK_GT, columns (CHROM, POS)
            gts = chunk.index.to_frame().join(chunk[id_name]).set_index(id_name)

            gts.columns = pd.MultiIndex.from_tuples(
                gts.columns.values, names=["CHROM", "POS"])

            meta = chunk.set_index(id_name).pipe(
                lambda df: df[[*df.columns.drop("SEQID"), "SEQID"]])

            # dataframe with values SEQID, CHUNK_GT
            seqids = chunk[[id_name, "SEQID"]].explode(
                "SEQID", ignore_index=True).set_index("SEQID")

            
        if self._pos is not None:
            gts = pd.concat({self._pos: gts}, names=["CHUNK_POS"])
            meta = pd.concat({self._pos: meta}, names=["CHUNK_POS"])

        if inplace:
            self._gts = gts
            self._seqids = seqids
            self._meta = meta
        else:
            return {"gts": gts, "seqids": seqids, "meta": meta}

    def to_pickle(self, fpath, **kwargs) -> None:
        """Save as pickle. file is either fpath or object with write attribute.
        **kwargs passed to pickle.dump
        """
        try:
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            fpath.write(pickle.dumps(self, **kwargs))
            
        except (AttributeError, TypeError):
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            with open(fpath, 'wb') as fout:
                fout.write(pickle.dumps(self, **kwargs))

    @property
    def anns(self):
        return self._anns

    @property
    def pos(self):
        """Chunk "position" number"""
        return self._pos

    @pos.setter
    def pos(self, value) -> None:
        if self._gts is not None:
            self._gts.rename({self._pos: value}, axis=0, level="CHUNK_POS")
        if self._meta is not None:
            self._meta.rename({self._pos: value}, axis=0, level="CHUNK_POS")
        self._pos = value


    @property
    def id_name(self):
        """Returns name used for chunk id"""
        return self._id_name
    
    @id_name.setter
    def id_name(self, value) -> None:
        if self._gts is not None:
            self._gts.rename_axis({self._id_name: value}, axis=0, inplace=True)
        if self._meta is not None:
            self._meta.rename_axis({self._id_name: value}, axis=0, inplace=True)
        if self._seqids is not None:
            self._seqids.rename({self._id_name: value}, axis=1, inplace=True)
        self._id_name = value
    
    @property
    def gts(self):
        """DataFrame of chunk gt index and genotypes"""
        return self._gts

    @property
    def meta(self):
        """DataFrame of chunk gt indx to metadata (dist, seqid list)"""
        return self._meta

    @property
    def seqids(self):
        """DataFrame of seqid to chunk gt index"""
        return self._seqids

    @property
    def shape(self):
        """Returns shape as (num. of sites, num. of genotype combinations)"""
        return None if self._gts is None else self._gts.shape[::-1]
    
    @property
    def nsamples(self):
        """Returns number of sequences"""
        return None if self._seqids is None else len(self._seqids)
    
    @property
    def nsites(self):
        """Returns number of sites"""
        return None if self._gts is None else len(self._gts.columns)

