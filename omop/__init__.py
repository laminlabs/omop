"""OMOP Common Data Model.

Import the package::

   import omop

This is the complete API reference:

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

__version__ = "0.0.1"  # denote a pre-release for 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup


# trigger instance loading if users
# want to access attributes
def __getattr__(name):
    if name not in {"models"}:
        _check_instance_setup(from_lamindb=True)
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
