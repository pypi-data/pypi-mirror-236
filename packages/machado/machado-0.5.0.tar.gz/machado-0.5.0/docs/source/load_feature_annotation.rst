Loading Feature Additional Info
===============================

Please notice the features must be loaded in advance.
If the annotation or sequence was loaded previously, it will be replaced.

Load Annotation
---------------

.. code-block:: bash

    python manage.py load_feature_annotation --file feature_annotation.tab --soterm polypeptide --cvterm display --organism 'Arabidopsis thaliana'

* Loading this file can be faster if you increase the number of threads (--cpu).

.. code-block:: bash

    python manage.py load_feature_annotation --help

=============   ==========================================================================================
--file 		    Two-column tab separated file (feature.accession<TAB>annotation text). *
--organism  	Species name (eg. Homo sapiens, Mus musculus) *
--soterm        SO Sequence Ontology Term (eg. mRNA, polypeptide) *
--cvterm 	    cvterm.name from cv feature_property. (eg. display, note, product, alias, ontology_term, annotation) *
--doi 		    DOI of a reference stored using *load_publication* (eg. 10.1111/s12122-012-1313-4)
--cpu 		    Number of threads
=============   ==========================================================================================

\* required fields


Remove Annotation
-----------------

If, by any reason, you need to remove a feature annotation you should use the command *remove_feature_annotation*.

.. code-block:: bash

    python manage.py remove_feature_annotation --help


Load Sequence
-------------

.. code-block:: bash

    python manage.py load_feature_sequence --organism 'Arabidopsis thaliana' --file Athaliana_transcripts.fasta --soterm mRNA

* Loading this file can be faster if you increase the number of threads (--cpu).

.. code-block:: bash

    python manage.py load_feature_sequence --help

=============== ==========================================================================================
--file 		FASTA file. *
--organism  	Species name (eg. Homo sapiens, Mus musculus) *
--soterm        SO Sequence Ontology Term (eg. chromosome, assembly, mRNA, polypeptide) *
--cpu 		Number of threads
=============== ==========================================================================================

\* required fields


Remove Sequence
---------------

If, by any reason, you need to remove a feature sequence you should use the command *load_feature_sequence* itself and provide a FASTA file with no sequence. For example:

.. code-block:: bash

    >chr1

    >chr2


Load Publication
----------------

.. code-block:: bash

    python manage.py load_feature_publication --organism 'Arabidopsis thaliana' --file feature_publication.tab

* Loading this file can be faster if you increase the number of threads (--cpu).

.. code-block:: bash

    python manage.py load_feature_publication --help

=============   ==========================================================================================
--file 		Two-column tab separated file (feature.accession<TAB>DOI). *
--organism  	Species name (eg. Homo sapiens, Mus musculus) *
--cpu 		Number of threads
=============   ==========================================================================================

\* required fields


Remove Publication
------------------

If, by any reason, you need to remove a feature publication attribution, you should use the command *remove_publication*.

.. code-block:: bash

    python manage.py remove_publication --help


Load DBxRef
----------------

.. code-block:: bash

    python manage.py load_feature_dbxrefs --organism 'Arabidopsis thaliana' --file feature_dbxrefs.tab --soterm mRNA

* Loading this file can be faster if you increase the number of threads (--cpu).

.. code-block:: bash

    python manage.py load_feature_dbxrefs --help

=============   ==========================================================================================
--file 		Two-column tab separated file (feature.accession<TAB>db:dbxref). *
--organism  	Species name (eg. Homo sapiens, Mus musculus) *
--soterm        SOTERM SO Sequence Ontology Term (eg. chromosome, assembly, mRNA, polypeptide) *
--cpu 		Number of threads
=============   ==========================================================================================

\* required fields
