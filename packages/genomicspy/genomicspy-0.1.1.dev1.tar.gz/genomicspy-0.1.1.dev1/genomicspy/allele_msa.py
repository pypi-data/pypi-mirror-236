#!/usr/bin/env python

# allele_msa.py

# Functions to read in MSAs of alleles

# Used in parse_allele_msas.py (moved to here 05 Oct 2023)


from __future__ import annotations
import os
from collections.abc import Callable, Hashable, Iterable
from typing import Union

import pandas as pd
import regex
from Bio import AlignIO
from Bio.AlignIO import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqIO import SeqRecord
from regex import Pattern

import oddsnends as oed 

__all__ = ["annotate_allele_msa",
           "apply_seqs", 
           "gen_allele_records",
           "gen_allele_records",
           "gen_msa_from_alleles", 
           "gen_msa_records", 
           "parse_concat_allele_msas", 
           "rename_seqs", 
           "seq_name_to_anns_regex", 
           "seq_name_to_anns_split", 
           ]

def annotate_allele_msa(msa: MultipleSeqAlignment, **other_anns
                        ) -> MultipleSeqAlignment:
    """Annotates MSA with CHROM, POS, begin, end, based on first seq in MSA
    
    Note: begin, end: 1-indexed, right-open interval
    **other_anns: extra annotations to add. Takes priority over seq anns.
    """
    ref = msa[0]
    ref_anns = ref.annotations
    msa.annotations |= dict(CHROM=ref_anns["CHROM"],
                            POS=ref_anns["POS"],
                            begin=ref_anns["POS"],
                            end=ref_anns["POS"] + len(ref),
                            length=len(ref),
                            ) | other_anns
    return msa

def apply_seqs(msa: MultipleSeqAlignment, fn: Callable, *args, **kwargs
                ) -> MultipleSeqAlignment:
    """Wrapper for apply function to each sequence in MSA
    
    Arguments:
        msa: MultipleSeqAlignment object
        fn: Callable to apply to each SeqRecord, taking seq as first 
            positional arg, and then any *args, **kwargs.
        *args, **kwargs: passed to func
    Returns: the same msa (for piping)
    """
    for seq in msa:
        fn(seq, *args, **kwargs)
    return msa


def gen_allele_records(root_dir: str) -> MultipleSeqAlignment:
    """Generator to find and read MSA fasta files in root dir"""
    for direc, _, files in os.walk(root_dir):
        for fname in files:
            yield AlignIO.read(f"{direc}/{fname}", "fasta")
            

def gen_msa_records(root_dir: str, max_return: int = None
                            ) -> MultipleSeqAlignment:
    """Yields parsed index info and SeqIO records in root_dir (walk)"""
        
    # separate this to avoid condition checks if max_records is None
    if max_return is None:
        for rec in gen_allele_records(root_dir):
            yield rec
    else:
        for i, msa in enumerate(
                gen_allele_records(root_dir)):
            if i >= max_return:
                return
            yield msa

def gen_msa_from_alleles(chrom: str, pos: int, alleles: Iterable[str]
                        ) -> MultipleSeqAlignment:
    """Returns MSA for comma-separated string of alleles, assigning GT"""
    records = []
    
    msa_anns = {"CHROM": chrom, "POS": pos}
    for i, allele in enumerate(alleles):
        name = f"{chrom}|{pos}|{i}"
        records.append(SeqRecord(
            Seq(allele), id=name, name=name, description=f"{name}|{allele}",
            annotations=msa_anns | {"GT": i}))
    
    return MultipleSeqAlignment(records, annotations=msa_anns)



def rename_seqs(seq: SeqRecord, fmt: str) -> None:
    """Updates sequence name and id based on fmt
    
    fmt is a str with kw placeholders corresponding to seq.annotation fields
    """
    seq.name = seq.id = fmt.format(**seq.annotations)


def seq_name_to_anns_regex(seq: SeqRecord, rex: Pattern,
                            fields: Iterable[Hashable] = None) -> None:
    """Parse SeqRecord sequences in MSA in place using regex. 
    
    If regex does not have named fields, uses values in fields as keys.
    """
    match = rex.match(seq.name)
    
    try:
        new_anns = match.groupdict()  # if no match, raises AttributeError
        assert len(new_anns) > 0   # if no named fields, groupdict is empty
    except AttributeError:
        return
    except AssertionError:
        new_anns = dict(zip(fields, match.groups()))  # assign field names
    
    # parse values
    for k, v in new_anns.items():
        new_anns[k] = oed.parse_literal_eval(v)
    
    # update annotations
    seq.annotations |= new_anns


def seq_name_to_anns_split(seq: SeqRecord, fields: Iterable[Hashable],
                            sep: str = '|') -> None:
    """Parse SeqRecord sequences in MSA in place using split.
    Arguments:
        msa:  the multiple sequence alignment object
        fields: list-like of hashables, default enumerate
                Names of annotation fields corresponding to those in seq names 
        sep: str, default '|' used to parse sequence name
    """
    seq.annotations |= dict(zip(
        fields, (oed.parse_literal_eval(val) for val in seq.name.split(sep))))






def parse_concat_allele_msas(root_dir: str,
                                fields: list[str] = None, sep: str = '|',
                                rex: Union[str, Pattern] = None,
                                rename_fmt: str = '{CHROM}|{POS}|{GT}',
                                sort_by: str = "GT"
                                ) -> pd.DataFrame:
    """Search, parse and concat fastas
    Arguments:
        root_dir:  Directory in which to search for rfastas
        
    Options for parsing sequence names:
        fields:    Fields to assign fields in parsed sequence names
        sep: str, default '|'  separator for seq name fields
        rex:         regular expr to parse seq names. overrides fields/sep
        rename_fmt:  format str to rename (using annnotation fields)
        sort_by:     annotation field to use to sort sequences in MSA
    
        Annotation fields must include CHROM, POS
    
    Returns:  pd.DataFrame with columns CHROM, POS, and MSA
    """
    oed.msg(oed.now(), "Reading in allele MSAs...")
    msas = pd.Series(gen_msa_records(root_dir), name="MSA")

    oed.msg(oed.now(), "Parsing and wrangling allele sequences...")

    # annotate sequences using data in seq name
    try:
        rex_name = regex.compile(rex)
    except TypeError:
        assert fields is not None, "fields cannot be None"
        msas.apply(apply_seqs, fn=seq_name_to_anns_split,
                    fields=fields, sep=sep)
    else:
        msas.apply(apply_seqs, fn=seq_name_to_anns_regex,
                    rex=rex_name, fields=fields)


    # clean up seq id/name
    if rename_fmt is not None:
        msas.apply(apply_seqs, fn=rename_seqs, fmt=rename_fmt)
    
    # sort seqs in MSA by GT
    if sort_by is not None:
        msas.apply(lambda msa: msa.sort(
            key=lambda seq: seq.annotations[sort_by]))

    oed.msg(oed.now(), "Adding MSA annotations and sorting...")


    # annotate MSA
    msas.apply(annotate_allele_msa)

    msa_idx_cols = ["CHROM", "POS"]
    msas = msas.apply(
        lambda msa: dict((k, msa.annotations[k]) for k in msa_idx_cols)
        ).pipe(pd.DataFrame.from_records).join(msas)

    # sort msa entries by chrom, pos
    msas.sort_values(msa_idx_cols, inplace=True, ignore_index=True)

    return msas


# get module functions
# __all__ = [
#     k for k, v in filter(
#         lambda kv: hasattr(kv[1], "__globals__") and (
#             kv[1]. __globals__["__name__"] == __name__),
#         filter(lambda kv: callable(kv[1]), vars().items()))]
