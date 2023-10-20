# alleles.py

#%%
from __future__ import annotations
import sys
from collections.abc import Collection, Sequence
from typing import Annotated, Union

import pandas as pd
from Bio.AlignIO import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqIO import SeqRecord
from vcfpy import Call, Reader, Record

import oddsnends as oed
from genomicspy.main import SeqType, copy_multipleseqalignment, seq_astype


__all__ = [
    "SampleErrorHandlingType",
    "VCF_DEFAULT_DICT",
    "_combine_ivrs_variants",
    "calc_circular",
    "calc_end_pos",
    "calc_ivrs",
    "check_overlap",
    "gen_alleles_for_chrom_vcf",
    "gen_alleles_from_variants_df",
    "gen_alleles_from_vcf",
]

SampleErrorHandlingType = Annotated[str, "ignore", "force", "raise" ]

VCF_DEFAULT_DICT = {"ID": [],
                    "QUAL": None,
                    "FILTER": ["PASS"],
                    "INFO": {},
                    "FORMAT": ["GT"],
                    }
#%%


def calc_circular(pos: pd.Series, length: int):
    """Calculate real positions on circle as 1-indexed"""
    return (pos % length).mask(lambda ser: ser == 0, length)

def calc_end_pos(ser: pd.Series = None,
                 seq: SeqType = None,
                 start_pos: int = None,
                 seq_field: str = "ALLELES",
                 start_field: str = "POS",
                 closed: bool = True) -> int:
    """Calculate end position using length of sequence.

    Parameters
    ----------
    ser: pd.Series
        Contains sequence(s) and start positions. If None, seq and start_pos
        are required. If ser[seq_field] has multiple seqs, the first is taken
    seq: SeqType
        Sequence for which to calculate end pos. If None, ser is required
    start_pos: int
        starting position (assumes left-closed). Required if ser is None
    seq_field: str
        Name of field containing sequence object
    start_field: str
        Name of field containing starting position
    closed: bool
        Whether end position should be closed or open

    Returns:  end position as int
    """
    if ser is not None:
        start_pos = oed.default(start_pos, ser[start_field])
        seq = oed.default(seq, ser[seq_field])

        # multiple seqs given. Use the first
        if isinstance(seq, (MultipleSeqAlignment, Sequence)):
            seq = seq[0]

    return start_pos + len(seq) - (1 if closed else 0)




def check_overlap(variants: pd.DataFrame,
                  chrom: str,
                  chrom_col: str = "CHROM",
                  start_col: str = "POS",
                  end_col: str = "END_POS",
                  length: int = None,
                  is_circular: bool = False,
                  errout: str = ".",
                  ) -> None:
    """Check if intervals of entries overlap.

    Intervals are right-open and 1-indexed.

    Parameters
    ------------
    df: pd.DataFrame
    chrom:      str
    chrom_col:  str     Name of chrom col. Default "CHROM
    start_col:  str     Col name of interval start index
    end_col:    str     Col name of interval end index
    length:     int     Total contig length. Required if is_circular is True

    Optional:
    is_circular: bool   Treat entries on circular contig. Default False
    errout:      str    Output directory for error files. Default "."

    Returns:  None
    """
    assert not(is_circular and length is None), \
        f"is_circular is {is_circular} but length is {length}"


    # get interval start and end columns
    entries = variants.loc[variants["CHROM"] == chrom, [start_col, end_col]]

    # group entries by each position and count
    # resulting df has index as pos, values as ids from entries index and n_ids
    positions = oed.intervals2locs(
        entries, col_from=start_col, col_to=end_col,
        ignore_index=False, drop_duplicates=False)


    if is_circular:

        # calculate real position on a circular chromosome
        positions = calc_circular(positions, length)

        # make same pos val as dot for easier reading
        entries[f"{end_col}_circ"] = (
            calc_circular(entries[end_col], length)
            .mask(lambda ser: entries[end_col] <= ser, ".")
        )


    positions = (
        positions
        .rename_axis("variants_index")
        .reset_index(name="pos")
        .pivot_table("variants_index", "pos", aggfunc=lambda x: x)
    )
    positions["n_variants"] = positions["variants_index"].apply(
        lambda x: x if isinstance(x, Collection) else [x]).apply(len)

    try:
        # check if there are overlaps
        overlaps = positions.loc[positions.n_variants > 1]
        assert len(overlaps) == 0, "Overlapping entries exist."

    except AssertionError:

        # ranges of overlap
        overlap_ranges = oed.calc_intervals(overlaps.index, closed=True)

        # ids corresponding to entries index
        overlap_ids = overlaps["variants_index"].explode().drop_duplicates()

        overlap_entries = (
            entries.loc[overlap_ids, :]
            .assign(**{chrom_col: chrom})
            .pipe(variants.merge, "inner", on=[chrom_col, start_col, end_col])
            )

        suffix = oed.default(chrom, "", has_value=f".{chrom}")

        # save entries for review
        positions_check_fname = f"positions_check{suffix}.tsv"
        positions.to_csv(f"{errout}/{positions_check_fname}", sep="\t")

        overlap_entries_fname = f"overlapping_variants{suffix}.tsv"
        overlap_entries.to_csv(f"{errout}/{overlap_entries_fname}", sep="\t")

        print(
            ">> OVERLAPS",
            f">> {len(overlap_ranges)} intervals span {len(overlaps)} position:",
            "",
            *(f"{chrom}:{i}-{j}" for i, j in overlap_ranges),
            "",
            f">> {len(overlap_entries)} overlapping entries:",
            overlap_entries.to_string(),
            "",
            ">> Checks and ranges saved to:",
            f"    {positions_check_fname} and ",
            f"    {overlap_entries_fname}",
            sep="\n", file=sys.stderr, flush=True)





def calc_ivrs(intervals: Union[pd.DataFrame, Collection[tuple[int, int]]],
              refseq: SeqType,
              col_start: str = "POS",
              col_end: str = "END_POS",
              chrom: str = None,
              start: int = 1,
              end: int = None,
              col_seq: str = "SEQ",
              closed: oed.ClosedIntervalType = True,
              indexing: Annotated[int, 0, 1] = 1,
              ) -> pd.DataFrame:
    """Calculate intervariant region POS and END_POS

    intervals are 1-indexed

    Parameters
    ------------
    intervals:   pd.DataFrame or Collection of 2-tuples
        Variant start and end positions (1-indexed, right-open)
    refseq:  str, Seq, or SeqRecord
        Reference sequence
    col_start: str
        Col name for allele start positions
    col_end: str,
        Col name for allele end positions
    Optional
    --------
    chrom:  name of chromosome, if refseq does not have an id (i.e. is not a Seqrecord)
    astype:  type. Choices: str, Seq, SeqRecord or MultipleSeqAlignment,
        default None is str.
        Cast allele seq as this type. If MultipleSeqAlignment, allele data
        are assigned to column MSA instead of ALLELES
    closed: str or bool or None
        Passed to oddsnends.setops_ranges(), also accessible through
        genomicspy.oed.setops_ranges(). See documentation.
    indexing: 0 or 1
        Intervals are based on 0- or 1-indexing system. Default 1
    col_seq: str
        Name of output column with sequence. Default "SEQ"

    To calculate for a subregion of refseq, specify:
    -------
    start:   int, default 1
    end:     int, default None (to end of refseq)

    Returns: pd.DataFrame with cols CHROM, POS, END_POS,
        SEQ: str, Seq, SeqRecord or MSA
    """

    # define vars from args
    if end is None:
        end = len(refseq)

    if len(intervals) == 0:
        ivrs = pd.DataFrame([(start, end)], columns=[col_start, col_end])

    else:
        # calculate the ivr positions and merge into ranges
        ivrs = oed.setops_ranges(intervals,
                                 [(start, end)],
                                 col_from=col_start,
                                 col_to=col_end,
                                 how="right_only",
                                 closed=closed,
                                 indexing=indexing,
                                 )

    # get allele sequences
    # shift intervals
    shift_start, shift_end = oed.shift_interval(closed, "left", indexing, 0)

    seqs = ivrs.apply(
        lambda ser: refseq[ser[col_start] + shift_start
                           :ser[col_end] + shift_end],
        axis=1)

    ivrs = ivrs.assign(**{"CHROM": chrom, col_seq: seqs})

    return ivrs


## Allele generation - helpers

# Note: this is not made available
def _combine_ivrs_variants(ivrs: pd.DataFrame,
                           variants: Collection[pd.DataFrame],
                           astype: Annotated[
                               type, SeqType, MultipleSeqAlignment] = str,
                           seq_col: str = "ALLELES",
                           ) -> pd.DataFrame:
    """Post-calc_ivrs() commands common between gen_alleles_from_variants_df
    or from vcf

    Includes generation of ALLELES field, drop SEQ and concat
    """
    # assert start is not None, "start required"
    # assert end is not None, "end required"

    index_cols = ["CHROM", "POS", "END_POS"]

    # shared kws
    seq_astype_kws = {"astype": astype, "seq_col": seq_col}
    if astype == MultipleSeqAlignment:
        seq_astype_kws["msa_anns"] = index_cols
    else:
        seq_astype_kws["rec_anns"] = index_cols

    ivrs.rename({seq_col : "ALLELES"}, axis=1, inplace=True, errors="ignore")

    ivrs["ALLELES"] = ivrs.apply(
        seq_astype, axis=1, astype=astype, seq_col="ALLELES")

    # FIXME: debug here (follow seq_astype)
    for var_df in variants:
        var_df = var_df.assign(
            ALLELES=var_df.apply(seq_astype, **seq_astype_kws, axis=1))

    alleles = pd.concat([*variants, ivrs]).sort_values(index_cols)

    # make as an iterable list
    if not issubclass(astype, MultipleSeqAlignment):
        alleles["ALLELES"].update(alleles["ALLELES"].apply(lambda seq: [seq]))

    return alleles

## Allele generation
def gen_alleles_from_variants_df(variants: pd.DataFrame,
                                 refseqs: oed.SeriesType[str, SeqType],
                                 start: dict[str, int] = 1,
                                 end: dict[str, int] = None,
                                 astype: Annotated[
                                     type, SeqType, MultipleSeqAlignment
                                     ] = None,
                                 col_start: str = "POS",
                                 col_end: str = "END_POS",
                                 col_alleles: str = "ALLELES",
                                 closed: oed.ClosedIntervalType = True,
                                 indexing: Annotated[int, 0, 1] = 1,
                                 ) -> pd.DataFrame:
    """Generate list of all alleles (variant and invariant positions)

    Assumes no alleles span the chrom break, i.e. that on a circular chrom,
    start > end.

    Parameters
    ----------
    variants: pd.DataFrame
        Contains columns for chrom, start pos and end pos
    refseqs: pd.Series
        With index as CHROM, values as ref seqs [str, Seq, SeqRecord]
    start: int or dict[str, int]
        dict of start positions for chroms, or start position to apply to
        all chroms. 1-indexed inclusive. Default 1
    end: int or dict[str, int]
        dict of end positions for chroms, or end position to apply to
        all chroms. 1-indexed inclusive. Default None goes to end of chrom
    astype:  type
        Choices: MultipleSeqAlignment, SeqRecord, Seq, str

    pd.DataFrame options
    --------------------
    col_start: str
        Name of variants df column containing start positions. Default "POS"
    col_end: str
        Name of variants df column containing end positions. Default "END_POS"
    col_alleles: str
        Name of variants df column containing alleles. Default "ALLELES"

    Interval options:
    -----------------
    closed: str or bool or None
        How to interpret start and end positions. See oddsnends.setops_ranges()
        also accessible via. genomicspy.oed.setops_ranges(). Default True
        (i.e. closed for both bounds)
    indexing: 0 or 1
        Intervals are based on 0- or 1-indexing system. Passed to calc_ivrs().
        Default 1.

    Returns: DataFrame of CHROM, start pos, end pos, alleles for all positions
    """

    # conditions for getting subset of variants
    def _left_closed(df, pos: int, col: str): return df[col] >= pos

    def _left_open(df, pos: int, col: str): return df[col] > pos

    def _right_closed(df, pos: int, col: str): return df[col] <= pos

    def _right_open(df, pos: int, col: str): return df[col] < pos

    if astype is None:
        astype = type(variants[col_alleles].iloc[0])

    if not issubclass(astype, MultipleSeqAlignment):
        astype = type(variants[col_alleles].iloc[0][0])


    # left cond checks col_end vs start
    # right cond checks col_start vs end
    match closed:

        case "right" | "upper":
            left_cond = _left_open
            right_cond = _right_closed

        case "both" | True:
            left_cond = _left_closed
            right_cond = _right_closed

        case None | False:
            left_cond = _left_open
            right_cond = _right_open

        case "left" | "lower":
            left_cond = _left_closed
            right_cond = _right_open

        case _:
            raise ValueError("closed", closed)


    chrom_groups = variants.groupby("CHROM", as_index=False, group_keys=False)

    # apply same start to all chroms
    if isinstance(start, int):
        start = dict((chrom, start) for chrom in chrom_groups.groups.keys())

        # apply same end to all chroms
    if isinstance(end, (int, oed.NoneType)):
        end = dict((chrom, end) for chrom in chrom_groups.groups.keys())

    ivrs = {}
    subset_variants = []

    # iter groups to avoid double-run of first entry
    for chrom, group in chrom_groups:
        g_start = start.get(chrom, 1)
        g_end = end.get(chrom, None)
        group_kws = {"chrom": chrom,
                     "start": g_start,
                     "end": g_end,
                     "col_start": col_start,
                     "col_end": col_end,
                     "col_seq": "ALLELES",
                     "closed": closed,
                     "indexing": indexing
                    }
        ivrs[chrom] = calc_ivrs(group, refseqs[chrom], **group_kws)

        # this includes variants that span across start or across end pos
        # closed interval
        subset_variants.append(group.loc[
            left_cond(group, g_start, col_start) &
            right_cond(group, g_end, col_end)
        ])


    ivrs = pd.concat(ivrs, ignore_index=True)

    alleles = _combine_ivrs_variants(ivrs, subset_variants, astype=astype,
                                     seq_col="ALLELES")

    return alleles


def gen_alleles_for_chrom_vcf(vcf: Reader,
                              refseq: SeqType,
                              chrom: str = None,
                              start: SeqType = None,
                              end: int = None,
                              astype: Annotated[
                                  SeqType, MultipleSeqAlignment] = None,
                              closed: oed.ClosedIntervalType = True,
                              indexing: Annotated[int, 0, 1] = 1,
                              ) -> pd.DataFrame:
    """Core function

    Parameters
    ----------
    vcf: str
        variants filepath
    refseq: SeqType
        Reference sequence
    chrom: str
        Chromosome to fetch. If None, tries to get it from refseq. Required.
    start: int or dict[str, int]
        dict of start positions for chroms, or start position to apply to
        all chroms. 1-indexed inclusive. Default 1
    end: int or dict[str, int]
        dict of end positions for chroms, or end position to apply to
        all chroms. 1-indexed inclusive. Default None goes to end of chrom
    astype:  type
        Choices: MultipleSeqAlignment, SeqRecord, Seq, str

    Interval options:
    -----------------
    closed: bool
        How Output to interpret start and end positions. See oddsnends.setops_ranges()
        also accessible via. genomicspy.oed.setops_ranges(). Default True
        (i.e. closed for both bounds)
    indexing: 0 or 1
        Intervals are based on 0- or 1-indexing system. Passed to calc_ivrs().
        Default 1.
    pd.DataFrame options
    --------------------
    col_start: str
        Name of variants df column containing start positions. Default "POS"
    col_end: str
        Name of variants df column containing end positions. Default "END_POS"
    col_alleles: str
        Name of variants df column containing alleles. Default "ALLELES"

    """

    if astype is None:
        astype = type(refseq)


    # vcf indexing is 1-indexed inclusive
    shift_left, shift_right = oed.shift_interval("left", closed, 1, indexing)

    # set oed.defaults and vars
    index_cols = ["CHROM", "POS", "END_POS"]

    try:
        assert chrom is None
        chrom = refseq.id
    except (AssertionError, AttributeError):
        pass
        
    # to int (or None)
    start = start.get(chrom, 1) if isinstance(start, dict) else start
    end = end.get(chrom, None) if isinstance(end, dict) else end

    with Reader.from_path(vcf) as reader:
        variants_vcf = pd.DataFrame.from_records(
            ((
                rec.CHROM,
                rec.POS + shift_left,
                rec.POS + len(rec.REF) + shift_right,
                [rec.REF, *[alt.value for alt in rec.ALT]]
            ) for rec in reader.fetch(chrom, start - 1, end)  # vcfpy is left-open
            ), columns=["CHROM", "POS", "END_POS", "ALLELES"]
            ).sort_values(index_cols)

    ivrs = calc_ivrs(
        variants_vcf,
        refseq,
        chrom=chrom,
        start=start,
        end=end,
        col_start="POS",
        col_end="END_POS",
        col_seq="ALLELES",
        closed=closed,
        indexing=indexing,
    )

    alleles = _combine_ivrs_variants(ivrs, [variants_vcf], astype=astype)

    return alleles


def gen_alleles_from_vcf(
    vcf: str,
    refseqs: oed.SeriesType[str, SeqType],
    start: dict[str, SeqType],
    end: dict[str, int] = None,
    chrom: str = None,
    astype: Annotated[
        type, SeqType, MultipleSeqAlignment] = None,
    closed: oed.ClosedIntervalType = True,
    indexing: Annotated[int, 0, 1] = 1,
    ) -> pd.DataFrame:
    """Read in variants and get intervariant regions for the relevant region

    Parameters
    ----------
    vcf:    str
    refseqs: pd.Series
        With index as CHROM, values as ref seqs [str, Seq, SeqRecord]

    Optional:
    start, end: dict[str, int]
        dict of start and end positions for chromosomes, 1-indexed, right-open
        (GFF3 format). Default processes the entire ref seq

    Returns: pd.DataFrame of CHROM: str, POS: int, END_POS: int,
        ALLELES: list[str]
    """

    alleles = []

    with Reader.from_path(vcf) as reader:
        chroms = [ctg.id for ctg in reader.header.get_lines("contig")]

        # apply same start to all chroms
        if not isinstance(start, dict):
            start = dict((chrom, start) for chrom in chroms)

        # apply same end to all chroms
        if not isinstance(end, dict):
            end = dict((chrom, end) for chrom in chroms)

        for chrom in chroms:
            chrom_alleles = gen_alleles_for_chrom_vcf(
                chrom,
                reader,
                refseqs[chrom],
                start=start,
                end=end,
                closed=closed,
                index=indexing
            )
            alleles.append(chrom_alleles)

    alleles = pd.concat(alleles, axis=0)

    return alleles



# %%
