# Copyright 2018 by Embrapa.  All rights reserved.
#
# This code is part of the machado distribution and governed by its
# license. Please see the LICENSE.txt and README.md files that should
# have been included as part of this package for licensing information.

"""Sequence."""

from datetime import datetime, timezone
from hashlib import md5

from Bio.SeqRecord import SeqRecord
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from machado.loaders.common import retrieve_feature_id
from machado.loaders.exceptions import ImportingError
from machado.models import Cvterm, Db, Dbxref, Dbxrefprop, Feature, FeaturePub, Organism
from machado.models import PubDbxref


class SequenceLoader(object):
    """Load sequence records."""

    def __init__(
        self,
        filename: str,
        organism: Organism,
        doi: str = None,
        description: str = None,
        url: str = None,
    ) -> None:
        """Execute the init function."""
        # Save DB file info
        self.db, created = Db.objects.get_or_create(
            name="FASTA_SOURCE", description=description, url=url
        )
        self.filename = filename
        self.organism = organism

        # Retrieve sequence ontology object
        self.cvterm_contained_in = Cvterm.objects.get(
            name="located in", cv__name="relationship"
        )

        # Retrieve DOI's Dbxref
        dbxref_doi = None
        self.pub_dbxref_doi = None
        if doi:
            try:
                dbxref_doi = Dbxref.objects.get(accession=doi)
            except ObjectDoesNotExist as e:
                raise ImportingError(e)
            try:
                self.pub_dbxref_doi = PubDbxref.objects.get(dbxref=dbxref_doi)
            except ObjectDoesNotExist as e:
                raise ImportingError(e)

    def store_biopython_seq_record(
        self,
        seq_obj: SeqRecord,
        soterm: str,
        ignore_residues: bool = False,
    ) -> None:
        """Store Biopython SeqRecord."""
        try:
            soterm_obj = Cvterm.objects.get(name=soterm, cv__name="sequence")
        except ObjectDoesNotExist as e:
            raise ImportingError(
                "The soterm {} is not registered ({}).".format(soterm, e)
            )

        try:
            dbxref, created = Dbxref.objects.get_or_create(
                db=self.db, accession=seq_obj.id
            )
            Dbxrefprop.objects.get_or_create(
                dbxref=dbxref,
                type_id=self.cvterm_contained_in.cvterm_id,
                rank=0,
            )
            retrieve_feature_id(
                accession=seq_obj.id, soterm=soterm, organism=self.organism
            )
            raise ImportingError(
                "The sequence {} is already registered.".format(seq_obj.id)
            )
        except ObjectDoesNotExist:
            residues = seq_obj.seq

            m = md5(str(seq_obj.seq).encode()).hexdigest()
            if ignore_residues is True:
                residues = ""

            name = None
            if seq_obj.description != "<unknown description>":
                name = seq_obj.description

            # storing feature
            feature = Feature(
                dbxref=dbxref,
                organism=self.organism,
                uniquename=seq_obj.id,
                name=name,
                residues=residues,
                seqlen=len(seq_obj.seq),
                md5checksum=m,
                type=soterm_obj,
                is_analysis=False,
                is_obsolete=False,
                timeaccessioned=datetime.now(timezone.utc),
                timelastmodified=datetime.now(timezone.utc),
            )
            feature.save()

            # DOI: try to link sequence to publication's DOI
            if feature and self.pub_dbxref_doi:
                try:
                    FeaturePub.objects.create(
                        feature=feature, pub_id=self.pub_dbxref_doi.pub_id
                    )
                except IntegrityError as e:
                    raise ImportingError(e)

    def add_sequence_to_feature(self, seq_obj: SeqRecord, soterm: str) -> None:
        """Store Biopython SeqRecord."""
        try:
            feature_id = retrieve_feature_id(
                accession=seq_obj.id, soterm=soterm, organism=self.organism
            )
        except ObjectDoesNotExist:
            raise ImportingError("The feature {} does NOT exist.".format(seq_obj.id))

        feature_obj = Feature.objects.get(feature_id=feature_id)
        feature_obj.md5 = md5(str(seq_obj.seq).encode()).hexdigest()
        feature_obj.residues = seq_obj.seq
        feature_obj.save()
