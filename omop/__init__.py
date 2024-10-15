"""OMOP Common Data Model [`source <https://github.com/laminlabs/omop/blob/main/omop/models.py>`__].

Install and mount `omop` in a new instance:

>>> pip install omop
>>> lamin init --storage ./test-omop --schema omop

Import the package:

>>> import omop

Registries:

.. autosummary::
   :toctree: .

   CareSite
   CdmSource
   Cohort
   CohortDefinition
   Concept
   ConceptAncestor
   ConceptRelationship
   ConceptSynonym
   ConditionEra
   ConditionOccurrence
   Cost
   Death
   DeviceExposure
   Domain
   DoseEra
   DrugEra
   DrugExposure
   DrugStrength
   Episode
   EpisodeEvent
   FactRelationship
   Location
   Measurement
   Metadata
   Note
   NoteNlp
   Observation
   ObservationPeriod
   PayerPlanPeriod
   Person
   ProcedureOccurrence
   Provider
   Relationship
   SourceToConceptMap
   Specimen
   VisitDetail
   VisitOccurrence
   Vocabulary
"""

__version__ = "0.1.2"  # denote a pre-release for 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup


# trigger instance loading if users
# want to access attributes
def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="omop")
    return globals()[name]


if _check_instance_setup():
    import lamindb

    del __getattr__  # delete so that imports work out
    from .models import (
        CareSite,
        CdmSource,
        Cohort,
        CohortDefinition,
        Concept,
        ConceptAncestor,
        ConceptRelationship,
        ConceptSynonym,
        ConditionEra,
        ConditionOccurrence,
        Cost,
        Death,
        DeviceExposure,
        Domain,
        DoseEra,
        DrugEra,
        DrugExposure,
        DrugStrength,
        Episode,
        EpisodeEvent,
        FactRelationship,
        Location,
        Measurement,
        Metadata,
        Note,
        NoteNlp,
        Observation,
        ObservationPeriod,
        PayerPlanPeriod,
        Person,
        ProcedureOccurrence,
        Provider,
        Relationship,
        SourceToConceptMap,
        Specimen,
        VisitDetail,
        VisitOccurrence,
        Vocabulary,
    )
