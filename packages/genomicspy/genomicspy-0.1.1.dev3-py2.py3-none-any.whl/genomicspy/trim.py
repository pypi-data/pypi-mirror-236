# trim.py

"""Trimming alleles"""

from __future__ import annotations
from collections.abc import Collection
from typing import Annotated, Union

import pandas as pd
from Bio.AlignIO import MultipleSeqAlignment
from Bio.Seq import MutableSeq, Seq
from Bio.SeqIO import SeqRecord

import oddsnends as oed
from genomicspy.main import SeqType, copy_seqrecord

__all__ = [
    "trim_alleles",
    "trim_allele_seqs",
]

# FIXME: ALL!! closed interval


def _calc_new_pos(anns: dict, left=None, right=None, pos_field: str = "POS",
                 end_pos_field: str = "END_POS") -> dict[str, int]:
    """Calculate new positions after trimming"""
    
    new_anns = {}
    try:
        new_anns |= {"POS": anns[pos_field] + left,
                     "OLD_POS": anns[pos_field]}
    except (KeyError, TypeError):
        pass
    
    try:
        # +1 because end pos bound is open
        new_anns |= {"END_POS": anns[end_pos_field] - right + 1, 
                     "OLD_END_POS": anns[end_pos_field]}
        
    except (KeyError, TypeError):
        pass
    
    return new_anns
    


def _trim_seqs(seqs: Collection[Union[str, Seq, MutableSeq]],
               left: int = None,
               right: int = None,
               length: int = None,
               ) -> Collection[Union[str, Seq, MutableSeq]]:
    """Makes a copy of the allele sequences and adjust for short seqs"""    
    
    if length is None:
        length = max(len(s) for s in seqs)
    
    if right is not None:
        for i, seq in enumerate(seqs):
            t_right = right - (length - len(seq))
            seqs[i] = seq[:-t_right]
        
    elif left is not None:
        for i, seq in enumerate(seqs):
            t_left = left - (length - len(seq))
            seqs[i] = seq[t_left:]
                
    return seqs


def _trim_seq_recs(records: Collection[SeqRecord],
                   left: int = None,
                   right: int = None,
                   length: int = None,
                   inplace: bool = False,
                   ) -> Union[list[SeqRecord], None]:
    """Trim alleles inplace, adjusting for short seqs"""
    
    if length is None:
        length = max(len(rec.seq) for rec in records)

    trimmed = [[rec, rec.seq, {}] for rec in records]

    if right is not None:
        
        for i, (_, seq, _) in enumerate(trimmed):
            t_right = right - (length - len(seq))
            trimmed[i][1] = seq[:-t_right]
            trimmed[i][2] |= {"SEQ_TRIMMED_RIGHT": t_right}

    if left is not None:
        for i, (_, seq, _) in enumerate(trimmed):
            t_left = left - (length - len(seq))
            trimmed[i][1] = seq[t_left:]
            trimmed[i][2] |= {"SEQ_TRIMMED_RIGHT": t_left}
            
    if inplace:
        for rec, seq, anns in trimmed:
            rec.seq = seq
            rec.annotations |= anns
    
    else:
        return [copy_seqrecord(rec, seq=seq, annotations=anns, append=True)
                for rec, seq, anns in trimmed]


def _trim_mutableseqs(seqs: Collection[MutableSeq],
                      left: int = None,
                      right: int = None,
                      length: int = None,
                      ) -> list[tuple[MutableSeq, int, int]]:
    
    """Trims MutableSeq in place"""
    
    if length is None:
        length = max(len(s) for s in seqs)    
    
    if right is not None:
        for seq in seqs:
            t_right = right - (length - len(seq))
            for _ in range(t_right):
                seq.pop()
            
    elif left is not None:
        for seq in seqs:
            t_left = left - (length - len(seq))
            for _ in range(t_left):
                seq.pop(0)


def _trim_mutableseq_recs(records: Collection[SeqRecord],
                          left: int = None,
                          right: int = None,
                          length: int = None,
                          ) -> list[tuple[MutableSeq, int, int]]:
    
    """Trims records with MutableSeq in place"""
    
    if length is None:
        length = max(len(rec.seq) for rec in records)
    
    if right is not None:
        for rec in records:
            t_right = right - (length - len(rec.seq))
            for _ in range(t_right):
                rec.seq.pop()
            rec.annotations |= {"SEQ_TRIMMED_RIGHT": t_right}
            
    elif left is not None:
        for rec in records:
            t_left = left - (length - len(rec.seq))
            for _ in range(t_left):
                rec.seq.pop(0)
            rec.annotations |= {"SEQ_TRIMMED_LEFT": t_left}



def trim_allele_seqs(alleles: Union[MultipleSeqAlignment, Collection[SeqType]],
                     left: int = None,
                     right: int = None,
                     length: int = None,
                     dtype: Annotated[
                         Union[str, type], "first", SeqType] = "first",
                     inplace: bool = False
                     ) -> Union[MultipleSeqAlignment,
                                Collection[SeqType], None]:
    """Trim alleles. Supply only one of left or right
    
    Parameters
    ----------
    alleles:  MultipleSeqAlignment or list-like of SeqType obj
        Alleles to trim
    left:   int
        If given, trim this many bases from the left
    right:   int
        If given, trim this many bases from the right
    length: int
        Length of MSA (used for adjust cutting short sequences). Default 
        longest allele in given data
    dtype:  SeqType type or 'first'
        data type of the alleles. Default checks the first allele
    inplace: bool
        For MutableSeq, SeqRecord, and MultipleSeqAlignment. Trim in place.
        Default False
    
    Returns:  trimmed alleles or None (if inplace is True)
    """
    
    
    def _get_new_pos(rec: SeqRecord, left: int = None, right: int = None
                     ) -> dict:
        
        anns = {}
        try:
            new_pos = rec.annotations["POS"] + left
        except (KeyError, TypeError):
            pass
        else:
            anns |= {"POS": new_pos, "OLD_POS": rec.annotations["POS"]}
        
        try:
            new_end_pos = rec.annotations["END_POS"] - right
        except (KeyError, TypeError):
            pass
        else:
            anns |= {"END_POS": new_end_pos,
                     "OLD_END_POS": rec.annotations["END_POS"]}
        
    
    # add annotations
    annotations = {"TRIMMED_LEFT": left, "TRIMMED_RIGHT": right}
    
    if len(alleles) == 0:
        return alleles
    
    if dtype == "first":
        dtype = type(alleles[0])
    
    if length is None:
        length = max(len(a) for a in alleles)
    
    trimmed = None  # init here for easier returns
    
    # process based on input dtype
    if issubclass(dtype, MutableSeq) and inplace:
        _trim_mutableseqs(alleles, left=left, right=right, length=length)
    
    # either a list-like of SeqRecords or a MultipleSeqAlignment
    elif issubclass(dtype, SeqRecord):
        
        msa_anns = {"MSA_TRIMMED_LEFT": left,
                    "MSA_TRIMMED_RIGHT": right} | \
                    _calc_new_pos(alleles.annotations, left=left, right=right)
        
        if inplace:    
            mutableseqs = [
                rec for rec in alleles if isinstance(rec.seq, MutableSeq)]
            
            immutableseqs = [
                rec for rec in alleles if not isinstance(rec.seq, MutableSeq)]
            # MutableSeqs
            _trim_mutableseq_recs(
                mutableseqs, left=left, right=right, length=length)
            
            # non-mutable Seq
            _trim_seq_recs(
                immutableseqs, left=left, right=right, length=length,
                inplace=inplace)
        
            for rec in alleles:
                rec.annotations |= _calc_new_pos(
                    rec.annotations, left=left, right=right)
        
            # add higher-order annotations for MSA
            if isinstance(alleles, MultipleSeqAlignment):
                    alleles.annotations |= msa_anns
                    
        else:
            trimmed =_trim_seq_recs(
                alleles, left=left, right=right, length=length,
                inplace=inplace)
        
            for rec in trimmed:
                rec.annotations |= _calc_new_pos(
                    rec.annotations, left=left, right=right)
        
            if isinstance(alleles, MultipleSeqAlignment):
                
                trimmed = MultipleSeqAlignment(
                    trimmed,
                    annotations=alleles.annotations | msa_anns,
                    column_annotations=alleles.column_annotations,
                    )
    
    # str, Seq, or MutableSeq with inplace=False
    else:
        trimmed = _trim_seqs(
            [a for a in alleles], left=left, right=right, length=length)
            
            
    return trimmed
       

def trim_alleles(alleles: pd.DataFrame, 
                 start: int = 1,
                 end: int = None,
                 col_start: str = "POS",
                 col_end: str = "END_POS",
                 closed: oed.ClosedIntervalType = "left") -> pd.DataFrame:
    """Trim alleles that span over start/end of interval. Assumes closed
    
    
    
    closed:  'left', 'lower', 'right', 'upper', 'both', True, False, or None
    Treat ranges as closed on the 
    - 'left' or 'lower':  left/lower bound only, i.e. [from, to)
    - 'right' or 'upper': right/upper bound only, i.e. (from, to]
    - 'both' or True:     both bounds (interval is closed), i.e. [from, to]
    - None or False:      interval is open, i.e. (from, to)
    Default 'lower' (which is the native python range interpretation) 

    """
    # drop positions that are wholly out of interval
    

    if end is None:
        end = max(alleles[col_end])
        
    match closed:
        
        case "left" | "lower":
            left_cond = alleles[col_end] >= start
            right_cond = alleles[col_start] < end
        
        case "right" | "upper":
            left_cond = alleles[col_end] > start
            right_cond = alleles[col_start] <= end
        
        case "both" | True:
            left_cond = alleles[col_end] >= start
            right_cond = alleles[col_start] <= end
            
        case None | False:
            left_cond = alleles[col_end] > start
            right_cond = alleles[col_start] < end
    
        case _:
            raise ValueError("closed", closed)
            
    pruned = alleles.loc[left_cond & right_cond]
 
    # check for spanning left, spanning right, and calculate num bases to trim
    span_left = pruned.loc[pruned[col_start] < start].assign(TRIMMED=None)
    
    if len(span_left) > 0:
        span_left["TRIMMED"] = span_left.apply(
            lambda ser: trim_allele_seqs(
                ser["ALLELES"], left=start - ser[col_start]), axis=1)
    
    
    # +1 because end position is open
    span_right = pruned.loc[pruned[col_end] > end].assign(TRIMMED=None)
    if len(span_right) > 0:
        span_right["TRIMMED"] = span_right.apply(
            lambda ser: trim_allele_seqs(
                ser["ALLELES"], right=ser[col_end] - end + 1), axis=1)

    
    id_cols = ["CHROM", "POS", "END_POS"]
    
    
    trimmed = (
        pd.concat([span_left, span_right], axis=0)[[*id_cols, "TRIMMED"]]
        .merge(pruned, how="outer", on=id_cols)
        .pipe(lambda df: df.fillna({"TRIMMED": df["ALLELES"]}))
        .sort_values(id_cols)
        )
    
    return trimmed
