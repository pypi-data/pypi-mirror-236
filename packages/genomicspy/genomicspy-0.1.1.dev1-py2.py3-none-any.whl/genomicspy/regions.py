"""GFF3 and other functions to manipulate sequence regions"""

from __future__ import annotations

import sys
from collections.abc import Collection
from typing import Any

import pandas as pd

import oddsnends as oed

__all__ = [
    # "GFF3_COLS",
    # "parse_gff3",
    # "select_regions",
]

# ##### Params #####

# # See https://asia.ensembl.org/info/website/upload/gff3.html
# # Note: Start/end is 1-indexed, intervals are closed.
# GFF3_COLS = ["seqid", "source", "type", "start", "end", "score", "strand",
#              "phase", "attributes"]

# GFF3_INDEX_COLS = ["seqid", "start", "end", "strand"]

# def aggfunc_list_or_x(x: Any) -> Any:
#     """Checks and returns nicer typing of x (as list, single value, or None)"""

#     if isinstance(x, (str, dict)):
#         return None if len(x) == 0 else x

#     if not isinstance(x, Collection):
#         return x

#     if len(x) == 0:
#         return None

#     list_x = list(x)
#     if len(list_x) == 1:
#         return list_x[0]
#     return list_x



# def parse_gff3(ref_gff3: str) -> pd.DataFrame:
#     """Read GFF3 file, parsing attributes and ID based on GFF3 format

#     Also creates a column "name" (lower-case) that uses Name and ID columns to
#     generate a name if possible
#     """
#     def _aggfunc_list_or_x(x: Any) -> Any:
#         """Checks and returns nicer typing of x (as list, single value, or None)"""

#         if isinstance(x, (str, dict)):
#             return None if len(x) == 0 else x

#         if not isinstance(x, Collection):
#             return x

#         if len(x) == 0:
#             return None

#         list_x = list(x)
#         if len(list_x) == 1:
#             return list_x[0]
#         return list_x


#     # regex for parsing
#     pat_attr = r'(?:^|;)(?P<attribute>[A-Za-z0-9]+)\=(?P<value>[^;]+)(?:;|$)'
#     pat_id = r'(?:(?P<IdType>[^\-]*)-){,1}(?P<IdValue>.*)$'

#     # gff3 start and end are inclusive
#     gff3 = pd.read_csv(ref_gff3, sep="\t", names=GFF3_COLS, comment="#")


#     # parse attributes
#     attrs = (gff3["attributes"]
#              .str.extractall(pat_attr)
#              .droplevel(-1, axis=0)  # drop 'match' level from extractall()
#              .pipe(oed.pivot_indexed_table,
#                    values="value",
#                    columns="attribute",
#                    aggfunc=aggfunc_list_or_x,
#                    )
#             )

#     # sort out ID as different types of IDs in format <IdType>-<IdValue> or other
#     ids = (attrs["ID"]
#            .str.extract(pat_id, expand=True)
#            .fillna({"IdType": "other"})
#            .pipe(oed.pivot_indexed_table,
#                values="IdValue",
#                columns="IdType",
#                aggfunc=aggfunc_list_or_x,
#                )
#            )

#     # miscellaneous
#     if "id" in ids.columns:
#         ids = ids.assign(other=ids["id"].fillna(ids["other"])).drop("id", axis=1)

#     # suffix
#     ids.rename("{}ID".format, axis=1, inplace=True)

#     gff3 = pd.concat([gff3, ids, attrs], axis=1).drop(
#         "attributes", axis=1).replace({".": None})

#     return gff3

# def select_regions(gff3: pd.DataFrame,
#                    cds_only: bool = False,
#                    genes_only: bool = False,
#                    names_fpath: str = None,
#                    names_field: str = None,
#                    regions_tsv: str = None,
#                    ) -> pd.DataFrame:
#     """Select entries or regions from GFF3.

#     Specify either names or regions, and/or either cds_only or genes_only

#     Parameters
#     ------------
#         gff3: pd.DataFrame
#             Parsed and pivoted reference GFF3.
#         cds_only:  bool, oed.default False.
#             Select only regions with non-null cdsID
#         genes_only:  bool, oed.default False.
#             Select only regions with non-null geneID.
#         names_fpath:  str, oed.default None.
#             Filepath for list of names to find. Must provide names field.
#         names_field:  str, oed.default None.
#             GFF3 field or attribute under which to look for names. For IDs,
#             use <gene,cds,exon,rna,other>ID
#         regions_tsv:  str, oed.default None.
#             TSV of regions indicated by seqid, start, end, strand

#     Returns:  pd.DataFrame. Subset of gff3 with reset index
#     """

#     # get regions of interest
#     if names_fpath is not None:
#         with open(names_fpath, "r") as fin:
#             region_names = [line.partition("#")[0].rstrip() for line in fin]

#         regions = gff3.loc[gff3[names_field].isin(region_names)]

#         # warn of some names are not present in the gff3
#         not_present = set(region_names).difference(gff3[names_field])
#         if len(not_present) > 0:
#             print("Warning: some names are not present in GFF3:", *not_present,
#                 sep="\n", file=sys.stderr, flush=True)

#     elif regions_tsv is not None:

#         regions_to_check = pd.read_csv(regions_tsv, sep="\t").pipe(
#             pd.MultiIndex.from_frame)

#         regions = gff3.loc[regions_to_check.intersection(gff3.index)]

#         not_present = regions_to_check.difference(gff3.index)
#         if len(not_present) > 0:
#             print("Warning: some entries are not found in GFF3:", *not_present,
#                 sep="\n", file=sys.stderr, flush=True)

#     else:
#         regions = gff3

#     if cds_only:
#         regions = regions.loc[regions.cdsID.notnull()]

#     elif genes_only:
#         regions = regions.loc[regions.geneID.notnull()]

#     regions = regions.reset_index().rename_axis(["index"], axis=0)

#     return regions