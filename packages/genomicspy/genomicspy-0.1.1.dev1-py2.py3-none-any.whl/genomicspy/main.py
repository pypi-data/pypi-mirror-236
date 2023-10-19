"""Main module."""
# alleles.py
from __future__ import annotations
import logging
from collections.abc import Collection, Hashable
from typing import Annotated, Union

import pandas as pd
from Bio.AlignIO import MultipleSeqAlignment
from Bio.Seq import MutableSeq, Seq
from Bio.SeqIO import SeqRecord

import oddsnends as oed

__all__ = [
    "SeqType",
    "copy_multipleseqalignment",
    "copy_seqrecord",
    "seq_astype",
]

SeqType = Union[str, Seq, MutableSeq, SeqRecord]




def copy_seqrecord(rec: SeqRecord, append: bool = True, **kws):
    """Makes a copy of SeqRecord, overriding any kwargs with **kws
    
    append: applies to dbxrefs, features, annotations, and letter_annotations
    """
    
    # defaults
    features = rec.features
    dbxrefs = rec.dbxrefs
    annotations = rec.annotations
    letter_annotations = rec.letter_annotations
    
    # set defaults
    if append:
        features += kws.pop("features", [])
        dbxrefs += kws.pop("dbxrefs", [])
        annotations |= kws.pop("annotations", {})
        letter_annotations |= kws.pop("letter_annotations", {})
    
    
    kws = {"seq": rec.seq,
           "name": rec.name,
           "id": rec.id,
           "description": rec.description,
           "dbxrefs": dbxrefs,
           "features": features,
           "annotations": annotations,
           "letter_annotations": letter_annotations,
           } | kws
    return SeqRecord(**kws)


def copy_multipleseqalignment(msa: MultipleSeqAlignment, append: bool = True,
                              **kws):
    """Makes a copy of MultipleSeqAlignment, overriding with any **kws
    
    append applies to records, annotations and column_annotations
    """
    # defaults
    
    records =  [copy_seqrecord(rec) for rec in msa]
    annotations = msa.annotations
    column_annotations = msa.column_annotations
    
    try:
        if append:
            kws["records"] = records + kws["records"]
    except KeyError:
        kws["records"] = records
    
    try:
        if isinstance(kws["annotations"], Collection) and \
                not isinstance(kws["annotations"], dict):
            kws["annotations"] = dict(
                (k, records[0].get(k, None)) for k in kws["annotations"] )
            
        if append:
            kws["annotations"] = annotations | kws["annotations"]
    
    except KeyError:
        kws["annotations"] = annotations
        
    try:
        if append:
            kws["column_annotations"] = \
                column_annotations + kws["column_annotations"]
    except KeyError:
        kws["column_annotations"] = column_annotations
    

    return MultipleSeqAlignment(**kws)
    
    

def seq_astype(ser: pd.Series = None,
               seqs: Union[SeqType, MultipleSeqAlignment, Collection[SeqType]] = None,
               astype: Annotated[type, SeqType, MultipleSeqAlignment] = SeqRecord,
               seq_col: Hashable = "SEQ",
               seqid: str = None,
               inplace: bool = False,
               msa_kws: dict = None,
               rec_kws: dict = None,
               mutable: bool = False,
               **kwargs) -> Union[SeqType, MultipleSeqAlignment]:
    """ser with SEQ, CHROM, POS
    
    Must provide either ser or seqs
    Parameters
    ----------
    ser: pd.Series
        Contains CHROM, POS, and sequence (in field defined by seq_col) 
    seqs: Union[SeqType, MultipleSeqAlignment, Collection[SeqType]]
        Sequence or collection of sequences or MSA to cast
    astype: Annotated[type, SeqType, MultipleSeqAlignment]
        Cast as this type. Default SeqRecord
    seq_col: Hashable 
        For ser: field in which to find seq_col
    seqid: str
        id for new records. Inferred if ser is given. Default None.
    inplace: bool
        For MutableSeq, SeqRecord and MSAs. Modify inplace. Default False
    rec_kws: dict
        (Override) keywords to pass to SeqRecord() except for annotations. 
        Default None. (See rec_anns)
    msa_kws: dict
        (Override) keywords to pass to MultipleSeqAlignment() except for 
        annotations. Default None. (See msa_anns)
    mutable: bool
        For SeqRecord and MSA. Cast seqs as MutableSeq instead of Seq. 
        Default False

    **kwargs takes:
    rec_anns: dict or list
        For annotating SeqRecords. If ser is given and if list is given, 
        looks up values in ser. Default annotations include CHROM, col_start,
        and col_end.
    msa_anns: dict or list
        For annotating MSAs. If list is given, looks up values in ser.

    
    **<msa,erc> kws passed to update or construct the (new) MSA or SeqRec
    """
    msa_kws = oed.defaults(msa_kws, {})
    rec_kws = oed.defaults(rec_kws, {})
    
    if seqs is None:  # get info from series
        seq_obj = ser[seq_col]
    
        # for making brand new records (not copy)
        seqid = oed.default("seqid", f"{ser['CHROM']}|{ser['POS']}|0")
    
        anns = {"CHROM": ser["CHROM"],
                "POS": ser["POS"],
                "END_POS": ser["END_POS"],
                }
        
        rec_kws.setdefault("annotations", anns)
        rec_kws["annotations"] |= kwargs.get("rec_anns", {})
        
        msa_kws.setdefault("annotations", anns)
        
        msa_anns = kwargs.get("msa_anns", {})
        
        if isinstance(msa_anns, dict):
            msa_kws["annotations"] |= msa_anns
            
        elif isinstance(msa_anns, Collection
                        ) and not isinstance(msa_anns, str):
            msa_kws["annotations"] |= dict(
                (k, ser.get(k, None)) for k in kwargs["msa_anns"])
            
        else:
            msa_kws["annotations"][msa_anns] = ser[msa_anns]
                
    
    # return an MSA
    if issubclass(astype, MultipleSeqAlignment):

        # check input type            
        if isinstance(seq_obj, MultipleSeqAlignment):
            return copy_multipleseqalignment(seq_obj, **msa_kws) \
                if not inplace else seq_obj
                
        elif isinstance(seq_obj, Collection) and not isinstance(seq_obj, SeqRecord):
            records = [seq_astype(seq, astype=SeqRecord, rec_kws=rec_kws,
                                  mutable=mutable)]
            
        else:
            match seq_obj:
                case SeqRecord():
                    rec = copy_seqrecord(seq_obj, **rec_kws) if not inplace else seq_obj
                    
                case MutableSeq():
                    rec = SeqRecord(
                        MutableSeq(seq_obj) if not inplace else seq_obj, id=seqid)
                
                case Seq():
                    rec = SeqRecord(Seq(seq_obj) if not inplace else seq_obj, id=seqid)
                    
                case str():
                    rec = SeqRecord(Seq(f"{seq_obj}"), id=seqid)
                
            return MultipleSeqAlignment(
                [rec], **({"annotations": anns} | msa_kws))
        
    # this comes after checking if output is MSA
    if isinstance(seq_obj, MultipleSeqAlignment) and len(seq_obj) > 1:
        logging.warning("More than one seq in MSA. Using first seq")

    # return as SeqRecord
    if issubclass(astype, SeqRecord):
        
        # check input type
        match seq_obj:
            case MultipleSeqAlignment():
                return copy_seqrecord(seq_obj[0], **rec_kws) if not inplace \
                    else seq_obj[0]
            
            case SeqRecord():
                return copy_seqrecord(seq_obj, **rec_kws) if not inplace \
                    else seq_obj
        
        # construct/get seq first, then make new record
        match seq_obj:    
            case MutableSeq():
                seq = MutableSeq(seq_obj) if not inplace else seq_obj
                
            case Seq():
                seq = Seq(seq_obj) if not inplace else seq_obj
            
            case _:
                seq = Seq(f"{seq_obj}")
                
        return SeqRecord(seq, **(dict(id=seqid, annotations=anns) | rec_kws))


    # return as Seq
    if issubclass(astype, MutableSeq):
        
        # get seq and then copy/cast as MutableSeq
        match seq_obj:
            case MultipleSeqAlignment():
                seq = seq_obj[0].seq  # str or Seq from first record
            
            case SeqRecord():
                seq = seq_obj.seq
            
            case _:  # str, MutableSeq or Seq
                seq = seq_obj
            
        if inplace and isinstance(seq, MutableSeq):
            return seq
        else:
            return MutableSeq(f"{seq}")
    
    # return as Seq
    if issubclass(astype, Seq):
        
        match seq_obj:
            case MultipleSeqAlignment():
                seq = seq_obj[0].seq  # str or Seq from first record
            
            case SeqRecord():
                seq = seq_obj.seq
            
            case _:  # str, MutableSeq or Seq
                seq = seq_obj
            
        return Seq(f"{seq}") if isinstance(seq, str) or not inplace else seq
    
    # return as str
    if issubclass(astype, str):
        
        match seq_obj:
            case MultipleSeqAlignment():
                seq = seq_obj[0].seq  # str or Seq from first record
            
            case SeqRecord():
                seq = seq_obj.seq
            
            case _:  # str or Seq
                seq = seq_obj

        return seq

    else:
        raise ValueError("Bad astype arg", astype)
