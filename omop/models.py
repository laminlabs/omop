from __future__ import annotations

from datetime import datetime  # noqa

from django.db import models
from lnschema_core.fields import (
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    TextField,
)
from lnschema_core.models import CanCurate, Record, TracksRun, TracksUpdates


class CareSite(Record, CanCurate, TracksRun, TracksUpdates):
    """Uniquely identified healthcare delivery unit or an organizational unit, where healthcare services are provided."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    care_site_id: int = IntegerField(primary_key=True)
    care_site_name: str | None = CharField(max_length=255, blank=True, null=True)
    place_of_service_concept: Concept | None = ForeignKey(
        "Concept", models.DO_NOTHING, blank=True, null=True
    )
    location: Location | None = ForeignKey(
        "Location", models.DO_NOTHING, blank=True, null=True
    )
    care_site_source_value: str | None = CharField(max_length=50, blank=True, null=True)
    place_of_service_source_value: str | None = CharField(
        max_length=50, blank=True, null=True
    )


class CdmSource(Record, CanCurate, TracksRun, TracksUpdates):
    """Source database and the process details used to transform the data into the OMOP Common Data Model."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    cdm_source_name: str = CharField(max_length=255)
    cdm_source_abbreviation: str = CharField(max_length=25)
    cdm_holder: str = CharField(max_length=255)
    source_description: str | None = TextField(blank=True, null=True)
    source_documentation_reference: str | None = CharField(
        max_length=255, blank=True, null=True
    )
    cdm_etl_reference: str | None = CharField(max_length=255, blank=True, null=True)
    source_release_date: datetime = DateField()
    cdm_release_date: datetime = DateField()
    cdm_version: str | None = CharField(max_length=10, blank=True, null=True)
    cdm_version_concept: Concept = ForeignKey("Concept", models.DO_NOTHING)
    vocabulary_version: str = CharField(max_length=20)


class Cohort(Record, CanCurate, TracksRun, TracksUpdates):
    """Records of subjects that satisfy a given set of criteria for a duration of time.

    The definition of the cohort is contained within the COHORT_DEFINITION table.
    It is listed as part of the RESULTS schema because it is a table that users of the database as well as tools such as ATLAS need to be able to write to.
    The CDM and Vocabulary tables are all read-only so it is suggested that the COHORT and COHORT_DEFINTION tables are kept in a separate schema to alleviate confusion.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    cohort_definition_id: int = IntegerField()
    subject_id: int = IntegerField()
    cohort_start_date: datetime = DateField()
    cohort_end_date: datetime = DateField()


class CohortDefinition(Record, CanCurate, TracksRun, TracksUpdates):
    """Records defining a Cohort derived from the data through the associated description and syntax and upon instantiation (execution of the algorithm) placed into the COHORT table.

    Cohorts are a set of subjects that satisfy a given combination of inclusion criteria for a duration of time.
    The COHORT_DEFINITION table provides a standardized structure for maintaining the rules governing the inclusion of a subject into a cohort,
    and can store operational programming code to instantiate the cohort within the OMOP Common Data Model.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    cohort_definition_id: int = IntegerField()
    cohort_definition_name: str = CharField(max_length=255)
    cohort_definition_description: str = TextField(blank=True, null=True)
    definition_type_concept: Concept = ForeignKey("Concept", models.DO_NOTHING)
    cohort_definition_syntax: str = TextField(blank=True, null=True)
    subject_concept: Concept = ForeignKey(
        "Concept",
        models.DO_NOTHING,
        related_name="cohortdefinition_subject_concept_set",
    )
    cohort_initiation_date = DateField(blank=True, null=True)


class Concept(Record, CanCurate, TracksRun, TracksUpdates):
    """The Standardized Vocabularies contain records, or Concepts, that uniquely express clinical information in all domain tables of the CDM.

    Concepts are derived from vocabularies, which represent clinical information across a domain (e.g. conditions, drugs, procedures) through the use of codes and associated descriptions.
    Some Concepts are designated Standard Concepts, meaning these Concepts can be used as normative expressions of a clinical entity within the OMOP Common Data Model and within standardized analytics.
    Each Standard Concept belongs to one domain, which defines the location where the Concept would be expected to occur within data tables of the CDM.
    Concepts can represent broad categories (like Cardiovascular disease), detailed clinical elements (Myocardial infarction of the anterolateral wall) or modifying characteristics and attributes that define Concepts at various levels of detail (severity of a disease, associated morphology, etc.).
    Records in the Standardized Vocabularies tables are derived from national or international vocabularies such as SNOMED-CT, RxNorm, and LOINC, or custom Concepts defined to cover various aspects of observational data analysis.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    concept_id: int = IntegerField(primary_key=True)
    concept_name: str = CharField(max_length=255)
    domain_id: str = CharField(max_length=255)
    vocabulary_id: str = CharField(max_length=255)
    concept_class: str = CharField(max_length=255)
    standard_concept: str = CharField(max_length=1, blank=True, null=True)
    concept_code: str = CharField(max_length=50)
    valid_start_date: datetime = DateField()
    valid_end_date: datetime = DateField()
    invalid_reason: str = CharField(max_length=1, blank=True, null=True)


class ConceptAncestor(Record, CanCurate, TracksRun, TracksUpdates):
    """Hierarchical relationships between Concepts.

    Only direct parent-child relationships between Concepts are stored in the CONCEPT_RELATIONSHIP table.
    To determine higher level ancestry connections, all individual direct relationships would have to be navigated at analysis time.
    The CONCEPT_ANCESTOR table includes records for all parent-child relationships, as well as grandparent-grandchild relationships and those of any other level of lineage.
    Using the CONCEPT_ANCESTOR table allows for querying for all descendants of a hierarchical concept. For example, drug ingredients and drug products are all descendants of a drug class ancestor.
    This table is entirely derived from the CONCEPT, CONCEPT_RELATIONSHIP and RELATIONSHIP tables.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    ancestor_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    descendant_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conceptancestor_descendant_concept_set",
    )
    min_levels_of_separation: int = IntegerField()
    max_levels_of_separation: int = IntegerField()


# class ConceptClass(Record, CanCurate, TracksRun, TracksUpdates):
#     """The CONCEPT_CLASS table is a reference table, which includes a list of the classifications used to differentiate Concepts within a given Vocabulary.

#     This reference table is populated with a single record for each Concept Class.
#     """

#     class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
#         abstract = False

#     concept_class_id = CharField(primary_key=True, max_length=20)
#     concept_class_name = CharField(max_length=255)
#     concept_class_concept = ForeignKey(
#         Concept, models.DO_NOTHING
#     )  # introduce a loop


class ConceptRelationship(Record, CanCurate, TracksRun, TracksUpdates):
    """Records that define direct relationships between any two Concepts and the nature or type of the relationship.

    Each type of a relationship is defined in the RELATIONSHIP table.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    concept_id_1: Concept = ForeignKey(
        Concept, models.DO_NOTHING, db_column="concept_id_1"
    )
    concept_id_2: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        db_column="concept_id_2",
        related_name="conceptrelationship_concept_id_2_set",
    )
    relationship: Relationship = ForeignKey("Relationship", models.DO_NOTHING)
    valid_start_date: datetime = DateField()
    valid_end_date: datetime = DateField()
    invalid_reason: str = CharField(max_length=1, blank=True, null=True)


class ConceptSynonym(Record, CanCurate, TracksRun, TracksUpdates):
    """Alternate names and descriptions for Concepts."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    concept_synonym_name: str = CharField(max_length=1000)
    language_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="conceptsynonym_language_concept_set"
    )


class ConditionEra(Record, CanCurate, TracksRun, TracksUpdates):
    """Span of time when the Person is assumed to have a given condition.

    Similar to Drug Eras, Condition Eras are chronological periods of Condition Occurrence. Combining individual Condition Occurrences into a single Condition Era serves two purposes:
        It allows aggregation of chronic conditions that require frequent ongoing care, instead of treating each Condition Occurrence as an independent event.
        It allows aggregation of multiple, closely timed doctor visits for the same Condition to avoid double-counting the Condition Occurrences.
        For example, consider a Person who visits her Primary Care Physician (PCP) and who is referred to a specialist.
        At a later time, the Person visits the specialist, who confirms the PCPs original diagnosis and provides the appropriate treatment to resolve the condition.
        These two independent doctor visits should be aggregated into one Condition Era.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    condition_era_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    condition_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    condition_era_start_date: datetime = DateField()
    condition_era_end_date: datetime = DateField()
    condition_occurrence_count: int = IntegerField(blank=True, null=True)


class ConditionOccurrence(Record, CanCurate, TracksRun, TracksUpdates):
    """Records of Events of a Person.

    These events suggest the presence of a disease or medical condition stated as a diagnosis, a sign,
    or a symptom, which is either observed by a Provider or reported by the patient.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    condition_occurrence_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    condition_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    condition_start_date: datetime = DateField()
    condition_start_datetime: datetime = DateTimeField(blank=True, null=True)
    condition_end_date: datetime = DateField(blank=True, null=True)
    condition_end_datetime: datetime = DateTimeField(blank=True, null=True)
    condition_type_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_type_concept_set",
    )
    condition_status_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_status_concept_set",
        blank=True,
        null=True,
    )
    stop_reason: str = CharField(max_length=20, blank=True, null=True)
    provider: Provider = ForeignKey(
        "Provider", models.DO_NOTHING, blank=True, null=True
    )
    visit_occurrence: VisitOccurrence = ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    condition_source_value: str = CharField(max_length=50, blank=True, null=True)
    condition_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_source_concept_set",
        blank=True,
        null=True,
    )
    condition_status_source_value: str = CharField(max_length=50, blank=True, null=True)


class Cost(Record, CanCurate, TracksRun, TracksUpdates):
    """Records containing the cost of any medical event recorded in one of the OMOP clinical event tables.

    The event tables include DRUG_EXPOSURE, PROCEDURE_OCCURRENCE, VISIT_OCCURRENCE, VISIT_DETAIL, DEVICE_OCCURRENCE, OBSERVATION or MEASUREMENT.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    cost_id: int = IntegerField(primary_key=True)
    cost_event_id: int = IntegerField()
    cost_domain: Domain = ForeignKey("Domain", models.DO_NOTHING)
    cost_type_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    currency_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_currency_concept_set",
        blank=True,
        null=True,
    )
    total_charge: int = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    total_cost: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    total_paid: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_by_payer: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_by_patient: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_patient_copay: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_patient_coinsurance: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_patient_deductible: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_by_primary: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_ingredient_cost: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_dispensing_fee: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    payer_plan_period_id: float = IntegerField(blank=True, null=True)
    amount_allowed = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    revenue_code_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_revenue_code_concept_set",
        blank=True,
        null=True,
    )
    revenue_code_source_value: str = CharField(max_length=50, blank=True, null=True)
    drg_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_drg_concept_set",
        blank=True,
        null=True,
    )
    drg_source_value: str = CharField(max_length=3, blank=True, null=True)


class Death(Record, CanCurate, TracksRun, TracksUpdates):
    """Clinical event for how and when a Person dies.

    A person can have up to one record if the source system contains evidence about the Death,
    such as: Condition in an administrative claim, status of enrollment into a health plan, or explicit record in EHR data.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    person: Person = ForeignKey("Person", models.DO_NOTHING)
    death_date: datetime = DateField()
    death_datetime: datetime = DateTimeField(blank=True, null=True)
    death_type_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    cause_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="death_cause_concept_set",
        blank=True,
        null=True,
    )
    cause_source_value: str = CharField(max_length=50, blank=True, null=True)
    cause_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="death_cause_source_concept_set",
        blank=True,
        null=True,
    )


class DeviceExposure(Record, CanCurate, TracksRun, TracksUpdates):
    """Information about a persons exposure to a foreign physical object or instrument.

    This information is used for diagnostic or therapeutic purposes through a mechanism beyond chemical action.
    Devices include implantable objects, medical equipment and supplies,
    other instruments used in medical procedures and material used in clinical care.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    device_exposure_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    device_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    device_exposure_start_date: datetime = DateField()
    device_exposure_start_datetime: datetime = DateTimeField(blank=True, null=True)
    device_exposure_end_date: datetime = DateField(blank=True, null=True)
    device_exposure_end_datetime: datetime = DateTimeField(blank=True, null=True)
    device_type_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_device_type_concept_set",
    )
    unique_device_id: str = CharField(max_length=255, blank=True, null=True)
    production_id: str = CharField(max_length=255, blank=True, null=True)
    quantity: int = IntegerField(blank=True, null=True)
    provider: Provider = ForeignKey(
        "Provider", models.DO_NOTHING, blank=True, null=True
    )
    visit_occurrence: VisitOccurrence = ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    device_source_value: str = CharField(max_length=50, blank=True, null=True)
    device_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_device_source_concept_set",
        blank=True,
        null=True,
    )
    unit_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_unit_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value: str = CharField(max_length=50, blank=True, null=True)
    unit_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_unit_source_concept_set",
        blank=True,
        null=True,
    )


class Domain(Record, CanCurate, TracksRun, TracksUpdates):
    """OMOP-defined Domains the Concepts of the Standardized Vocabularies can belong to.

    A Domain defines the set of allowable Concepts for the standardized fields in the CDM tables.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    domain_id: str = CharField(primary_key=True, max_length=20)
    domain_name: str = CharField(max_length=255)
    domain_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)


class DoseEra(Record, CanCurate, TracksRun, TracksUpdates):
    """Span of time when the Person is assumed to be exposed to a constant dose of a specific active ingredient."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    dose_era_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    drug_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    unit_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="doseera_unit_concept_set"
    )
    dose_value: float = DecimalField(max_digits=1000, decimal_places=1000)
    dose_era_start_date: datetime = DateField()
    dose_era_end_date: datetime = DateField()


class DrugEra(Record, CanCurate, TracksRun, TracksUpdates):
    """Span of time when the Person is assumed to be exposed to a particular active ingredient.

    A Drug Era is not the same as a Drug Exposure: Exposures are individual records corresponding to the source when Drug was delivered to the Person,
    while successive periods of Drug Exposures are combined under certain rules to produce continuous Drug Eras.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    drug_era_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    drug_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    drug_era_start_date: datetime = DateField()
    drug_era_end_date: datetime = DateField()
    drug_exposure_count: int = IntegerField(blank=True, null=True)
    gap_days: int = IntegerField(blank=True, null=True)


class DrugExposure(Record, CanCurate, TracksRun, TracksUpdates):
    """Records about the exposure to a Drug ingested or otherwise introduced into the body.

    A Drug is a biochemical substance formulated in such a way that when administered to a Person it will exert a certain biochemical effect on the metabolism.
    Drugs include prescription and over-the-counter medicines, vaccines, and large-molecule biologic therapies.
    Radiological devices ingested or applied locally do not count as Drugs.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    drug_exposure_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    drug_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    drug_exposure_start_date: datetime = DateField()
    drug_exposure_start_datetime: datetime = DateTimeField(blank=True, null=True)
    drug_exposure_end_date: datetime = DateField()
    drug_exposure_end_datetime: datetime = DateTimeField(blank=True, null=True)
    verbatim_end_date: datetime = DateField(blank=True, null=True)
    drug_type_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="drugexposure_drug_type_concept_set"
    )
    stop_reason: str = CharField(max_length=20, blank=True, null=True)
    refills: int = IntegerField(blank=True, null=True)
    quantity: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    days_supply: int = IntegerField(blank=True, null=True)
    sig: str = TextField(blank=True, null=True)
    route_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugexposure_route_concept_set",
        blank=True,
        null=True,
    )
    lot_number: str = CharField(max_length=50, blank=True, null=True)
    provider: Provider = ForeignKey(
        "Provider", models.DO_NOTHING, blank=True, null=True
    )
    visit_occurrence: VisitOccurrence = ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    drug_source_value: str = CharField(max_length=50, blank=True, null=True)
    drug_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugexposure_drug_source_concept_set",
        blank=True,
        null=True,
    )
    route_source_value: str = CharField(max_length=50, blank=True, null=True)
    dose_unit_source_value: str = CharField(max_length=50, blank=True, null=True)


class DrugStrength(Record, CanCurate, TracksRun, TracksUpdates):
    """Amount or concentration and associated units of a specific ingredient contained within a particular drug product.

    This table is supplemental information to support standardized analysis of drug utilization.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    drug_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    ingredient_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="drugstrength_ingredient_concept_set"
    )
    amount_value: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    amount_unit_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_amount_unit_concept_set",
        blank=True,
        null=True,
    )
    numerator_value: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    numerator_unit_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_numerator_unit_concept_set",
        blank=True,
        null=True,
    )
    denominator_value: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    denominator_unit_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_denominator_unit_concept_set",
        blank=True,
        null=True,
    )
    box_size: int = IntegerField(blank=True, null=True)
    valid_start_date: datetime = DateField()
    valid_end_date: datetime = DateField()
    invalid_reason: str = CharField(max_length=1, blank=True, null=True)


class Episode(Record, CanCurate, TracksRun, TracksUpdates):
    """Aggregates lower-level clinical events into a higher-level abstraction representing clinically and analytically relevant disease phases, outcomes and treatments.

    The EPISODE_EVENT table connects qualifying clinical events (VISIT_OCCURRENCE, DRUG_EXPOSURE, PROCEDURE_OCCURRENCE, DEVICE_EXPOSURE) to the appropriate EPISODE entry.

    For example cancers including their development over time, their treatment, and final resolution.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    episode_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    episode_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    episode_start_date: datetime = DateField()
    episode_start_datetime: datetime = DateTimeField(blank=True, null=True)
    episode_end_date: datetime = DateField(blank=True, null=True)
    episode_end_datetime: datetime = DateTimeField(blank=True, null=True)
    episode_parent_id: int = IntegerField(blank=True, null=True)
    episode_number: int = IntegerField(blank=True, null=True)
    episode_object_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="episode_episode_object_concept_set"
    )
    episode_type_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="episode_episode_type_concept_set"
    )
    episode_source_value: str = CharField(max_length=50, blank=True, null=True)
    episode_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="episode_episode_source_concept_set",
        blank=True,
        null=True,
    )


class EpisodeEvent(Record, CanCurate, TracksRun, TracksUpdates):
    """The EPISODE_EVENT table connects qualifying clinical events to the appropriate EPISODE entry.

    Clinical events include CONDITION_OCCURRENCE, DRUG_EXPOSURE, PROCEDURE_OCCURRENCE, MEASUREMENT.

    For example, linking the precise location of the metastasis (cancer modifier in MEASUREMENT) to the disease episode.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    episode: Episode = ForeignKey(Episode, models.DO_NOTHING)
    event_id: int = IntegerField()
    episode_event_field_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)


class FactRelationship(Record, CanCurate, TracksRun, TracksUpdates):
    """Records about the relationships between facts stored as records in any table of the CDM.

    Relationships can be defined between facts from the same domain, or different domains.
    Examples of Fact Relationships include: Person relationships, care site relationships,
    indication relationship (between drug exposures and associated conditions), usage relationships (of devices during the course of an associated procedure),
    or facts derived from one another (measurements derived from an associated specimen).
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    domain_concept_id_1: Concept = ForeignKey(
        Concept, models.DO_NOTHING, db_column="domain_concept_id_1"
    )
    fact_id_1: int = IntegerField()
    domain_concept_id_2: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        db_column="domain_concept_id_2",
        related_name="factrelationship_domain_concept_id_2_set",
    )
    fact_id_2: int = IntegerField()
    relationship_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="factrelationship_relationship_concept_set",
    )


class Location(Record, CanCurate, TracksRun, TracksUpdates):
    """Capture physical location or address information of Persons and Care Sites."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    location_id: int = IntegerField(primary_key=True)
    address_1: str = CharField(max_length=50, blank=True, null=True)
    address_2: str = CharField(max_length=50, blank=True, null=True)
    city: str = CharField(max_length=50, blank=True, null=True)
    state: str = CharField(max_length=2, blank=True, null=True)
    zip: str = CharField(max_length=9, blank=True, null=True)
    county: str = CharField(max_length=20, blank=True, null=True)
    location_source_value: str = CharField(max_length=50, blank=True, null=True)
    country_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    country_source_value: str = CharField(max_length=80, blank=True, null=True)
    latitude = DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    longitude: str = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )


class Measurement(Record, CanCurate, TracksRun, TracksUpdates):
    """Records of Measurements, i.e. structured values (numerical or categorical) obtained through systematic and standardized examination or testing of a Person or Persons sample.

    The MEASUREMENT table contains both orders and results of such Measurements as laboratory tests, vital signs, quantitative findings from pathology reports, etc.
    Measurements are stored as attribute value pairs, with the attribute as the Measurement Concept and the value representing the result.
    The value can be a Concept (stored in VALUE_AS_CONCEPT), or a numerical value (VALUE_AS_NUMBER) with a Unit (UNIT_CONCEPT_ID).
    The Procedure for obtaining the sample is housed in the PROCEDURE_OCCURRENCE table, though it is unnecessary to create a PROCEDURE_OCCURRENCE record for each measurement if one does not exist in the source data.
    Measurements differ from Observations in that they require a standardized test or some other activity to generate a quantitative or qualitative result.
    If there is no result, it is assumed that the lab test was conducted but the result was not captured.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    measurement_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    measurement_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    measurement_date: datetime = DateField()
    measurement_datetime: datetime = DateTimeField(blank=True, null=True)
    measurement_time: str = CharField(max_length=10, blank=True, null=True)
    measurement_type_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_measurement_type_concept_set",
    )
    operator_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_operator_concept_set",
        blank=True,
        null=True,
    )
    value_as_number: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    value_as_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_value_as_concept_set",
        blank=True,
        null=True,
    )
    unit_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_unit_concept_set",
        blank=True,
        null=True,
    )
    range_low: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    range_high: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    provider: Provider = ForeignKey(
        "Provider", models.DO_NOTHING, blank=True, null=True
    )
    visit_occurrence = ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    measurement_source_value: str = CharField(max_length=50, blank=True, null=True)
    measurement_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_measurement_source_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value: str = CharField(max_length=50, blank=True, null=True)
    unit_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_unit_source_concept_set",
        blank=True,
        null=True,
    )
    value_source_value: str = CharField(max_length=50, blank=True, null=True)
    measurement_event_id: int = IntegerField(blank=True, null=True)
    meas_event_field_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_meas_event_field_concept_set",
        blank=True,
        null=True,
    )


class Metadata(Record, CanCurate, TracksRun, TracksUpdates):
    """Metadata information about a dataset that has been transformed to the OMOP Common Data Model."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    metadata_id: int = IntegerField(primary_key=True)
    metadata_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    metadata_type_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="metadata_metadata_type_concept_set"
    )
    name: str = CharField(max_length=250)
    value_as_string: str = CharField(max_length=250, blank=True, null=True)
    value_as_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="metadata_value_as_concept_set",
        blank=True,
        null=True,
    )
    value_as_number: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    metadata_date: datetime = DateField(blank=True, null=True)
    metadata_datetime: datetime = DateTimeField(blank=True, null=True)


class Note(Record, CanCurate, TracksRun, TracksUpdates):
    """Unstructured information that was recorded by a provider about a patient in free text notes on a given date."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    note_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    note_date: datetime = DateField()
    note_datetime: datetime = DateTimeField(blank=True, null=True)
    note_type_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    note_class_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_note_class_concept_set"
    )
    note_title: str = CharField(max_length=250, blank=True, null=True)
    note_text: str = TextField()
    encoding_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_encoding_concept_set"
    )
    language_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_language_concept_set"
    )
    provider: Provider = ForeignKey(
        "Provider", models.DO_NOTHING, blank=True, null=True
    )
    visit_occurrence: VisitOccurrence = ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    note_source_value: str = CharField(max_length=50, blank=True, null=True)
    note_event_id: int = IntegerField(blank=True, null=True)
    note_event_field_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="note_note_event_field_concept_set",
        blank=True,
        null=True,
    )


class NoteNlp(Record, CanCurate, TracksRun, TracksUpdates):
    """Encodes all output of NLP on clinical notes. Each row represents a single extracted term from a note."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    note_nlp_id: int = IntegerField(primary_key=True)
    note_id: int = IntegerField()
    section_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    snippet: str = CharField(max_length=250, blank=True, null=True)
    offset: str = CharField(max_length=50, blank=True, null=True)
    lexical_variant: str = CharField(max_length=250)
    note_nlp_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="notenlp_note_nlp_concept_set",
        blank=True,
        null=True,
    )
    note_nlp_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="notenlp_note_nlp_source_concept_set",
        blank=True,
        null=True,
    )
    nlp_system: str = CharField(max_length=250, blank=True, null=True)
    nlp_date: datetime = DateField()
    nlp_datetime: datetime = DateTimeField(blank=True, null=True)
    term_exists: str = CharField(max_length=1, blank=True, null=True)
    term_temporal: str = CharField(max_length=50, blank=True, null=True)
    term_modifiers: str = CharField(max_length=2000, blank=True, null=True)


class Observation(Record, CanCurate, TracksRun, TracksUpdates):
    """Clinical facts about a Person obtained in the context of examination, questioning or a procedure.

    Any data that cannot be represented by any other domains, such as social and lifestyle facts, medical history, family history, etc. are recorded here.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    observation_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    observation_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    observation_date: datetime = DateField()
    observation_datetime: datetime = DateTimeField(blank=True, null=True)
    observation_type_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_observation_type_concept_set",
    )
    value_as_number: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    value_as_string: str = CharField(max_length=60, blank=True, null=True)
    value_as_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_value_as_concept_set",
        blank=True,
        null=True,
    )
    qualifier_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_qualifier_concept_set",
        blank=True,
        null=True,
    )
    unit_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_unit_concept_set",
        blank=True,
        null=True,
    )
    provider: Provider = ForeignKey(
        "Provider", models.DO_NOTHING, blank=True, null=True
    )
    visit_occurrence: VisitOccurrence = ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    observation_source_value: str = CharField(max_length=50, blank=True, null=True)
    observation_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_observation_source_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value: str = CharField(max_length=50, blank=True, null=True)
    qualifier_source_value: str = CharField(max_length=50, blank=True, null=True)
    value_source_value: str = CharField(max_length=50, blank=True, null=True)
    observation_event_id: int = IntegerField(blank=True, null=True)
    obs_event_field_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_obs_event_field_concept_set",
        blank=True,
        null=True,
    )


class ObservationPeriod(Record, CanCurate, TracksRun, TracksUpdates):
    """Records which define spans of time during which two conditions are expected to hold.

    (i) Clinical Events that happened to the Person are recorded in the Event tables, and
    (ii) absense of records indicate such Events did not occur during this span of time.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    observation_period_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    observation_period_start_date: datetime = DateField()
    observation_period_end_date: datetime = DateField()
    period_type_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)


class PayerPlanPeriod(Record, CanCurate, TracksRun, TracksUpdates):
    """Details of the period of time that a Person is continuously enrolled under a specific health Plan benefit structure from a given Payer.

    Each Person receiving healthcare is typically covered by a health benefit plan, which pays for (fully or partially), or directly provides, the care.
    These benefit plans are provided by payers, such as health insurances or state or government agencies.
    In each plan the details of the health benefits are defined for the Person or her family, and the health benefit Plan might change over time typically with increasing utilization (reaching certain cost thresholds such as deductibles), plan availability and purchasing choices of the Person.
    The unique combinations of Payer organizations, health benefit Plans and time periods in which they are valid for a Person are recorded in this table.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    payer_plan_period_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey("Person", models.DO_NOTHING)
    payer_plan_period_start_date: datetime = DateField()
    payer_plan_period_end_date: datetime = DateField()
    payer_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    payer_source_value: str = CharField(max_length=50, blank=True, null=True)
    payer_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_payer_source_concept_set",
        blank=True,
        null=True,
    )
    plan_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_plan_concept_set",
        blank=True,
        null=True,
    )
    plan_source_value: str = CharField(max_length=50, blank=True, null=True)
    plan_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_plan_source_concept_set",
        blank=True,
        null=True,
    )
    sponsor_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_sponsor_concept_set",
        blank=True,
        null=True,
    )
    sponsor_source_value: str = CharField(max_length=50, blank=True, null=True)
    sponsor_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_sponsor_source_concept_set",
        blank=True,
        null=True,
    )
    family_source_value: str = CharField(max_length=50, blank=True, null=True)
    stop_reason_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_stop_reason_concept_set",
        blank=True,
        null=True,
    )
    stop_reason_source_value: str = CharField(max_length=50, blank=True, null=True)
    stop_reason_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_stop_reason_source_concept_set",
        blank=True,
        null=True,
    )


class Person(Record, CanCurate, TracksRun, TracksUpdates):
    """Identity management for all Persons in the database.

    Records that uniquely identify each person or patient, and some demographic information.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    person_id: int = IntegerField(primary_key=True)
    gender_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    year_of_birth: int = IntegerField()
    month_of_birth: int = IntegerField(blank=True, null=True)
    day_of_birth: int = IntegerField(blank=True, null=True)
    birth_datetime: datetime = DateTimeField(blank=True, null=True)
    race_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="person_race_concept_set"
    )
    ethnicity_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="person_ethnicity_concept_set"
    )
    location: Location = ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    provider: Provider = ForeignKey(
        "Provider", models.DO_NOTHING, blank=True, null=True
    )
    care_site: CareSite = ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    person_source_value: str = CharField(max_length=50, blank=True, null=True)
    gender_source_value: str = CharField(max_length=50, blank=True, null=True)
    gender_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_gender_source_concept_set",
        blank=True,
        null=True,
    )
    race_source_value: str = CharField(max_length=50, blank=True, null=True)
    race_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_race_source_concept_set",
        blank=True,
        null=True,
    )
    ethnicity_source_value: str = CharField(max_length=50, blank=True, null=True)
    ethnicity_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_ethnicity_source_concept_set",
        blank=True,
        null=True,
    )


class ProcedureOccurrence(Record, CanCurate, TracksRun, TracksUpdates):
    """Records of activities or processes ordered by, or carried out by, a healthcare provider on the patient with a diagnostic or therapeutic purpose."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    procedure_occurrence_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey(Person, models.DO_NOTHING)
    procedure_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    procedure_date: datetime = DateField()
    procedure_datetime: datetime = DateTimeField(blank=True, null=True)
    procedure_end_date: datetime = DateField(blank=True, null=True)
    procedure_end_datetime: datetime = DateTimeField(blank=True, null=True)
    procedure_type_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_procedure_type_concept_set",
    )
    modifier_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_modifier_concept_set",
        blank=True,
        null=True,
    )
    quantity: int = IntegerField(blank=True, null=True)
    provider: Provider = ForeignKey(
        "Provider", models.DO_NOTHING, blank=True, null=True
    )
    visit_occurrence: VisitOccurrence = ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    procedure_source_value: str = CharField(max_length=50, blank=True, null=True)
    procedure_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_procedure_source_concept_set",
        blank=True,
        null=True,
    )
    modifier_source_value: str = CharField(max_length=50, blank=True, null=True)


class Provider(Record, CanCurate, TracksRun, TracksUpdates):
    """Uniquely identified healthcare providers.

    Individuals providing hands-on healthcare to patients, such as physicians, nurses, midwives, physical therapists etc.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    provider_id: int = IntegerField(primary_key=True)
    provider_name: str = CharField(max_length=255, blank=True, null=True)
    npi: str = CharField(max_length=20, blank=True, null=True)
    dea: str = CharField(max_length=20, blank=True, null=True)
    specialty_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    care_site: CareSite = ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    year_of_birth: int = IntegerField(blank=True, null=True)
    gender_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_gender_concept_set",
        blank=True,
        null=True,
    )
    provider_source_value: str = CharField(max_length=50, blank=True, null=True)
    specialty_source_value: str = CharField(max_length=50, blank=True, null=True)
    specialty_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_specialty_source_concept_set",
        blank=True,
        null=True,
    )
    gender_source_value: str = CharField(max_length=50, blank=True, null=True)
    gender_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_gender_source_concept_set",
        blank=True,
        null=True,
    )


class Relationship(Record, CanCurate, TracksRun, TracksUpdates):
    """All types of relationships that can be used to associate any two concepts in the CONCEPT_RELATIONSHP table."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    relationship_id: str = CharField(primary_key=True, max_length=20)
    relationship_name: str = CharField(max_length=255)
    is_hierarchical: str = CharField(max_length=1)
    defines_ancestry: str = CharField(max_length=1)
    reverse_relationship_id: str = CharField(max_length=20)
    relationship_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)


class SourceToConceptMap(Record, CanCurate, TracksRun, TracksUpdates):
    """The source to concept map table is a legacy data structure within the OMOP Common Data Model.

    It is recommended for use in ETL processes to maintain local source codes which are not available as Concepts in the Standardized Vocabularies,
    and to establish mappings for each source code into a Standard Concept as target_concept_ids that can be used to populate the Common Data Model tables.
    The SOURCE_TO_CONCEPT_MAP table is no longer populated with content within the Standardized Vocabularies published to the OMOP community.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    source_code: str = CharField(max_length=50)
    source_concept: str = ForeignKey(Concept, models.DO_NOTHING)
    source_vocabulary_id: str = CharField(max_length=20)
    source_code_description: str = CharField(max_length=255, blank=True, null=True)
    target_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="sourcetoconceptmap_target_concept_set"
    )
    target_vocabulary: Vocabulary = ForeignKey("Vocabulary", models.DO_NOTHING)
    valid_start_date: datetime = DateField()
    valid_end_date: datetime = DateField()
    invalid_reason: str = CharField(max_length=1, blank=True, null=True)


class Specimen(Record, CanCurate, TracksRun, TracksUpdates):
    """The specimen domain contains the records identifying biological samples from a person."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    specimen_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey(Person, models.DO_NOTHING)
    specimen_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    specimen_type_concept: Concept = ForeignKey(
        Concept, models.DO_NOTHING, related_name="specimen_specimen_type_concept_set"
    )
    specimen_date: datetime = DateField()
    specimen_datetime: datetime = DateTimeField(blank=True, null=True)
    quantity: float = DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    unit_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_unit_concept_set",
        blank=True,
        null=True,
    )
    anatomic_site_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_anatomic_site_concept_set",
        blank=True,
        null=True,
    )
    disease_status_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_disease_status_concept_set",
        blank=True,
        null=True,
    )
    specimen_source_id: str = CharField(max_length=50, blank=True, null=True)
    specimen_source_value: str = CharField(max_length=50, blank=True, null=True)
    unit_source_value: str = CharField(max_length=50, blank=True, null=True)
    anatomic_site_source_value: str = CharField(max_length=50, blank=True, null=True)
    disease_status_source_value: str = CharField(max_length=50, blank=True, null=True)


class VisitDetail(Record, CanCurate, TracksRun, TracksUpdates):
    """Optional table used to represents details of each record in the parent VISIT_OCCURRENCE table.

    A good example of this would be the movement between units in a hospital during an inpatient stay or claim lines associated with a one insurance claim.
    For every record in the VISIT_OCCURRENCE table there may be 0 or more records in the VISIT_DETAIL table with a 1:n relationship where n may be 0.
    The VISIT_DETAIL table is structurally very similar to VISIT_OCCURRENCE table and belongs to the visit domain.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    visit_detail_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey(Person, models.DO_NOTHING)
    visit_detail_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    visit_detail_start_date: datetime = DateField()
    visit_detail_start_datetime: datetime = DateTimeField(blank=True, null=True)
    visit_detail_end_date: datetime = DateField()
    visit_detail_end_datetime: datetime = DateTimeField(blank=True, null=True)
    visit_detail_type_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_visit_detail_type_concept_set",
    )
    provider: Provider = ForeignKey(Provider, models.DO_NOTHING, blank=True, null=True)
    care_site: CareSite = ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    visit_detail_source_value: str = CharField(max_length=50, blank=True, null=True)
    visit_detail_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_visit_detail_source_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_admitted_from_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_source_value: str = CharField(max_length=50, blank=True, null=True)
    discharged_to_source_value: str = CharField(max_length=50, blank=True, null=True)
    discharged_to_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_discharged_to_concept_set",
        blank=True,
        null=True,
    )
    preceding_visit_detail: VisitDetail = ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )
    parent_visit_detail: VisitDetail = ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="visitdetail_parent_visit_detail_set",
        blank=True,
        null=True,
    )
    visit_occurrence: VisitOccurrence = ForeignKey("VisitOccurrence", models.DO_NOTHING)


class VisitOccurrence(Record, CanCurate, TracksRun, TracksUpdates):
    """Events where Persons engage with the healthcare system for a duration of time.

    They are often also called Encounters. Visits are defined by a configuration of circumstances under which they occur, such as
    (i) whether the patient comes to a healthcare institution, the other way around, or the interaction is remote,
    (ii) whether and what kind of trained medical staff is delivering the service during the Visit, and
    (iii) whether the Visit is transient or for a longer period involving a stay in bed.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    visit_occurrence_id: int = IntegerField(primary_key=True)
    person: Person = ForeignKey(Person, models.DO_NOTHING)
    visit_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
    visit_start_date: datetime = DateField()
    visit_start_datetime: datetime = DateTimeField(blank=True, null=True)
    visit_end_date: datetime = DateField()
    visit_end_datetime: datetime = DateTimeField(blank=True, null=True)
    visit_type_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_visit_type_concept_set",
    )
    provider: Provider = ForeignKey(Provider, models.DO_NOTHING, blank=True, null=True)
    care_site: CareSite = ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    visit_source_value: str = CharField(max_length=50, blank=True, null=True)
    visit_source_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_visit_source_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_admitted_from_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_source_value: str = CharField(max_length=50, blank=True, null=True)
    discharged_to_concept: Concept = ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_discharged_to_concept_set",
        blank=True,
        null=True,
    )
    discharged_to_source_value: str = CharField(max_length=50, blank=True, null=True)
    preceding_visit_occurrence: VisitOccurrence = ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )


class Vocabulary(Record, CanCurate, TracksRun, TracksUpdates):
    """Vocabularies collected from various sources or created de novo by the OMOP community.

    Populated with a single record for each Vocabulary source and includes a descriptive name and other associated attributes for the Vocabulary.
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    vocabulary_id: str = CharField(primary_key=True, max_length=20)
    vocabulary_name: str = CharField(max_length=255)
    vocabulary_reference: str = CharField(max_length=255, blank=True, null=True)
    vocabulary_version: str = CharField(max_length=255, blank=True, null=True)
    vocabulary_concept: Concept = ForeignKey(Concept, models.DO_NOTHING)
