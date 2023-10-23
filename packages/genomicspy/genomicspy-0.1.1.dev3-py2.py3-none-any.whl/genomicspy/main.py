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
    "add_gaps",
    "copy_multipleseqalignment",
    "copy_seqrecord",
    "seq_astype",
]

SeqType = Union[str, Seq, MutableSeq, SeqRecord]



def add_gaps(alleles: Union[MultipleSeqAlignment, Collection[SeqType]]
                ):
    "Appends sequences with gaps. Assumes alleles are left-aligned"""
    msa_len = max(len(a) for a in alleles)
    gapped = [a + "-" * (msa_len - len(a)) for a in alleles]
    if isinstance(alleles, MultipleSeqAlignment):
        new_msas = copy_multipleseqalignment(
            alleles, records=gapped, append=False)
        return new_msas
    return gapped



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
    
    if ser is None:  # get info from series
        seq_obj = seqs
        
    else:
        seq_obj = ser[seq_col]
    
        # for making brand new records (not copy)
        seqid = oed.default(seqid, f"{ser['CHROM']}|{ser['POS']}|0")
    
        anns = {"CHROM": ser.get("CHROM", None),
                "POS": ser.get("POS", None),
                "END_POS": ser.get("END_POS", None),
                }
        
        # sort out SeqRecord kws
        rec_kws = {"annotations": {}, "id": seqid} | rec_kws
        try:
            rec_kws["annotations"] |= kwargs["rec_anns"]
        except KeyError:
            rec_kws["annotations"] = anns

        rec_kws["id"] = str(rec_kws["id"])
        
        # sort out MultipleSeqAlignment kws    
        try:
            
            # no anns at all. use default
            assert ("annotations" in msa_kws) or ("msa_anns" in kwargs)
            
            msa_anns = kwargs.get("msa_anns", {})
            
            if isinstance(msa_anns, dict):  # already dict
                pass
                
            elif isinstance(msa_anns, Collection
                            ) and not isinstance(msa_anns, str):
                # need to look up values in ser
                msa_anns = dict(
                    (k, ser.get(k, None)) for k in kwargs["msa_anns"])
            else:
                # look up a single value 
                msa_anns = {msa_anns: ser[msa_anns]}
        
        except AssertionError:  # no anns at all. use default
            msa_kws["annotations"] = anns
                
        else:
            msa_kws.setdefault("annotations", {})
            msa_kws["annotations"] |= msa_anns

        
    # return an MSA
    if issubclass(astype, MultipleSeqAlignment):

        # check input type            
        if isinstance(seq_obj, MultipleSeqAlignment):
            return copy_multipleseqalignment(seq_obj, **msa_kws) \
                if not inplace else seq_obj
                
        elif isinstance(seq_obj, Collection) and \
                not isinstance(seq_obj, SeqType):
            
            #FIXME: why records still return as list        
            # assume that alleles are left-aligned
            records = [seq_astype(seqs=seq, astype=SeqRecord,
                                  inplace=inplace, mutable=mutable
                                  ) for seq in add_gaps(seq_obj)]
            
            return MultipleSeqAlignment(records, **msa_kws)
        
        elif isinstance(seq_obj, SeqRecord):
            rec = seq_obj if inplace else copy_seqrecord(seq_obj, **rec_kws)
            return MultipleSeqAlignment([rec], **msa_kws)
            
        else:
            match seq_obj:

                case MutableSeq() if not inplace:
                    seq = MutableSeq(seq_obj)
                
                case Seq() if not inplace:
                    seq = Seq(seq_obj)
                    
                case str():
                    seq = Seq(f"{seq_obj}")
                
                case _:
                    seq = seq_obj
            
            return MultipleSeqAlignment(
                [SeqRecord(seq, **rec_kws)], **msa_kws)

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
            case MutableSeq() if not inplace:
                seq = MutableSeq(seq_obj)
                
            case Seq() if not inplace:
                seq = Seq(seq_obj)
            
            case str():
                seq = Seq(f"{seq_obj}")
                
            case _ if mutable:
                seq = MutableSeq(seq_obj)
                
            case _:
                seq = seq_obj
                
        return SeqRecord(seq, **rec_kws)


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
