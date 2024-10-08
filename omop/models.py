from __future__ import annotations

from datetime import datetime

from django.db import models
from lnschema_core.models import Record, CanValidate


class CareSite(Record, CanValidate):
    """Uniquely identified healthcare delivery unit or an organizational unit, where healthcare services are provided."""

    care_site_id: int = models.IntegerField(primary_key=True)
    care_site_name: str | None = models.CharField(max_length=255, blank=True, null=True)
    place_of_service_concept: Concept | None = models.ForeignKey(
        "Concept", models.DO_NOTHING, blank=True, null=True
    )
    location: Location | None = models.ForeignKey("Location", models.DO_NOTHING, blank=True, null=True)
    care_site_source_value: str | None = models.CharField(max_length=50, blank=True, null=True)
    place_of_service_source_value: str | None = models.CharField(
        max_length=50, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "care_site"



class CdmSource(Record, CanValidate):
    """Source database and the process details used to transform the data into the OMOP Common Data Model."""

    cdm_source_name: str = models.CharField(max_length=255)
    cdm_source_abbreviation: str = models.CharField(max_length=25)
    cdm_holder: str = models.CharField(max_length=255)
    source_description: str | None = models.TextField(blank=True, null=True)
    source_documentation_reference: str | None = models.CharField(
        max_length=255, blank=True, null=True
    )
    cdm_etl_reference: str | None = models.CharField(max_length=255, blank=True, null=True)
    source_release_date: datetime.date = models.DateField()
    cdm_release_date: datetime.date = models.DateField()
    cdm_version: str | None = models.CharField(max_length=10, blank=True, null=True)
    cdm_version_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    vocabulary_version: str = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = "cdm_source"


class Cohort(Record, CanValidate):
    """Records of subjects that satisfy a given set of criteria for a duration of time.

    The definition of the cohort is contained within the COHORT_DEFINITION table.
    It is listed as part of the RESULTS schema because it is a table that users of the database as well as tools such as ATLAS need to be able to write to.
    The CDM and Vocabulary tables are all read-only so it is suggested that the COHORT and COHORT_DEFINTION tables are kept in a separate schema to alleviate confusion.
    """

    cohort_definition_id: int = models.IntegerField()
    subject_id: int = models.IntegerField()
    cohort_start_date: datetime = models.DateField()
    cohort_end_date: datetime = models.DateField()

    class Meta:
        managed = True
        db_table = "cohort"


class CohortDefinition(Record, CanValidate):
    """Records defining a Cohort derived from the data through the associated description and syntax and upon instantiation (execution of the algorithm) placed into the COHORT table.

    Cohorts are a set of subjects that satisfy a given combination of inclusion criteria for a duration of time.
    The COHORT_DEFINITION table provides a standardized structure for maintaining the rules governing the inclusion of a subject into a cohort,
    and can store operational programming code to instantiate the cohort within the OMOP Common Data Model.
    """

    cohort_definition_id: int = models.IntegerField()
    cohort_definition_name: str = models.CharField(max_length=255)
    cohort_definition_description: str = models.TextField(blank=True, null=True)
    definition_type_concept: Concept = models.ForeignKey("Concept", models.DO_NOTHING)
    cohort_definition_syntax: str = models.TextField(blank=True, null=True)
    subject_concept: Concept = models.ForeignKey(
        "Concept",
        models.DO_NOTHING,
        related_name="cohortdefinition_subject_concept_set",
    )
    cohort_initiation_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cohort_definition"


class Concept(Record, CanValidate):
    """The Standardized Vocabularies contain records, or Concepts, that uniquely express clinical information in all domain tables of the CDM.

    Concepts are derived from vocabularies, which represent clinical information across a domain (e.g. conditions, drugs, procedures) through the use of codes and associated descriptions.
    Some Concepts are designated Standard Concepts, meaning these Concepts can be used as normative expressions of a clinical entity within the OMOP Common Data Model and within standardized analytics.
    Each Standard Concept belongs to one domain, which defines the location where the Concept would be expected to occur within data tables of the CDM.
    Concepts can represent broad categories (like Cardiovascular disease), detailed clinical elements (Myocardial infarction of the anterolateral wall) or modifying characteristics and attributes that define Concepts at various levels of detail (severity of a disease, associated morphology, etc.).
    Records in the Standardized Vocabularies tables are derived from national or international vocabularies such as SNOMED-CT, RxNorm, and LOINC, or custom Concepts defined to cover various aspects of observational data analysis.
    """

    concept_id: int = models.IntegerField(primary_key=True)
    concept_name: str = models.CharField(max_length=255)
    domain_id: str = models.CharField(max_length=255)
    vocabulary_id: str = models.CharField(max_length=255)
    concept_class: str = models.CharField(max_length=255)
    standard_concept: str = models.CharField(max_length=1, blank=True, null=True)
    concept_code: str = models.CharField(max_length=50)
    valid_start_date: datetime = models.DateField()
    valid_end_date: datetime = models.DateField()
    invalid_reason: str = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "concept"


class ConceptAncestor(Record, CanValidate):
    """Hierarchical relationships between Concepts.

    Only direct parent-child relationships between Concepts are stored in the CONCEPT_RELATIONSHIP table.
    To determine higher level ancestry connections, all individual direct relationships would have to be navigated at analysis time.
    The CONCEPT_ANCESTOR table includes records for all parent-child relationships, as well as grandparent-grandchild relationships and those of any other level of lineage.
    Using the CONCEPT_ANCESTOR table allows for querying for all descendants of a hierarchical concept. For example, drug ingredients and drug products are all descendants of a drug class ancestor.
    This table is entirely derived from the CONCEPT, CONCEPT_RELATIONSHIP and RELATIONSHIP tables.
    """

    ancestor_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    descendant_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conceptancestor_descendant_concept_set",
    )
    min_levels_of_separation: int = models.IntegerField()
    max_levels_of_separation: int = models.IntegerField()

    class Meta:
        managed = True
        db_table = "concept_ancestor"


# class ConceptClass(Record):
#     """The CONCEPT_CLASS table is a reference table, which includes a list of the classifications used to differentiate Concepts within a given Vocabulary.

#     This reference table is populated with a single record for each Concept Class.
#     """

#     concept_class_id = models.CharField(primary_key=True, max_length=20)
#     concept_class_name = models.CharField(max_length=255)
#     concept_class_concept = models.ForeignKey(Concept, models.DO_NOTHING)  # introduce a loop

#     class Meta:
#         managed = True
#         db_table = "concept_class"


class ConceptRelationship(Record, CanValidate):
    """Records that define direct relationships between any two Concepts and the nature or type of the relationship.

    Each type of a relationship is defined in the RELATIONSHIP table.
    """

    concept_id_1: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, db_column="concept_id_1"
    )
    concept_id_2: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        db_column="concept_id_2",
        related_name="conceptrelationship_concept_id_2_set",
    )
    relationship: Relationship = models.ForeignKey("Relationship", models.DO_NOTHING)
    valid_start_date: datetime = models.DateField()
    valid_end_date: datetime = models.DateField()
    invalid_reason: str = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "concept_relationship"


class ConceptSynonym(Record, CanValidate):
    """Alternate names and descriptions for Concepts."""

    concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    concept_synonym_name: str = models.CharField(max_length=1000)
    language_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="conceptsynonym_language_concept_set"
    )

    class Meta:
        managed = True
        db_table = "concept_synonym"


class ConditionEra(Record, CanValidate):
    """Span of time when the Person is assumed to have a given condition.

    Similar to Drug Eras, Condition Eras are chronological periods of Condition Occurrence. Combining individual Condition Occurrences into a single Condition Era serves two purposes:
        It allows aggregation of chronic conditions that require frequent ongoing care, instead of treating each Condition Occurrence as an independent event.
        It allows aggregation of multiple, closely timed doctor visits for the same Condition to avoid double-counting the Condition Occurrences.
        For example, consider a Person who visits her Primary Care Physician (PCP) and who is referred to a specialist.
        At a later time, the Person visits the specialist, who confirms the PCPs original diagnosis and provides the appropriate treatment to resolve the condition.
        These two independent doctor visits should be aggregated into one Condition Era.
    """

    condition_era_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    condition_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    condition_era_start_date: datetime = models.DateField()
    condition_era_end_date: datetime = models.DateField()
    condition_occurrence_count: int = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "condition_era"


class ConditionOccurrence(Record, CanValidate):
    """Records of Events of a Person.
    
    These events suggest the presence of a disease or medical condition stated as a diagnosis, a sign, 
    or a symptom, which is either observed by a Provider or reported by the patient.
    """

    condition_occurrence_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    condition_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    condition_start_date: datetime = models.DateField()
    condition_start_datetime: datetime = models.DateTimeField(blank=True, null=True)
    condition_end_date: datetime = models.DateField(blank=True, null=True)
    condition_end_datetime: datetime = models.DateTimeField(blank=True, null=True)
    condition_type_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_type_concept_set",
    )
    condition_status_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_status_concept_set",
        blank=True,
        null=True,
    )
    stop_reason: str = models.CharField(max_length=20, blank=True, null=True)
    provider: Provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence: VisitOccurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    condition_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    condition_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_source_concept_set",
        blank=True,
        null=True,
    )
    condition_status_source_value: str = models.CharField(
        max_length=50, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "condition_occurrence"


class Cost(Record, CanValidate):
    """Records containing the cost of any medical event recorded in one of the OMOP clinical event tables.
    
    The event tables include DRUG_EXPOSURE, PROCEDURE_OCCURRENCE, VISIT_OCCURRENCE, VISIT_DETAIL, DEVICE_OCCURRENCE, OBSERVATION or MEASUREMENT.
    """

    cost_id: int = models.IntegerField(primary_key=True)
    cost_event_id: int = models.IntegerField()
    cost_domain: Domain = models.ForeignKey("Domain", models.DO_NOTHING)
    cost_type_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    currency_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_currency_concept_set",
        blank=True,
        null=True,
    )
    total_charge: int = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    total_cost: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    total_paid: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_by_payer: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_by_patient: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_patient_copay: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_patient_coinsurance: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_patient_deductible: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_by_primary: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_ingredient_cost: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    paid_dispensing_fee: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    payer_plan_period_id: float = models.IntegerField(blank=True, null=True)
    amount_allowed = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    revenue_code_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_revenue_code_concept_set",
        blank=True,
        null=True,
    )
    revenue_code_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    drg_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_drg_concept_set",
        blank=True,
        null=True,
    )
    drg_source_value: str = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cost"


class Death(Record, CanValidate):
    """Clinical event for how and when a Person dies.

    A person can have up to one record if the source system contains evidence about the Death, 
    such as: Condition in an administrative claim, status of enrollment into a health plan, or explicit record in EHR data.
    """

    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    death_date: datetime = models.DateField()
    death_datetime: datetime = models.DateTimeField(blank=True, null=True)
    death_type_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    cause_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="death_cause_concept_set",
        blank=True,
        null=True,
    )
    cause_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    cause_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="death_cause_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "death"


class DeviceExposure(Record, CanValidate):
    """Information about a persons exposure to a foreign physical object or instrument.
    
    This information is used for diagnostic or therapeutic purposes through a mechanism beyond chemical action.
    Devices include implantable objects, medical equipment and supplies,
    other instruments used in medical procedures and material used in clinical care.
    """

    device_exposure_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    device_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    device_exposure_start_date: datetime = models.DateField()
    device_exposure_start_datetime: datetime = models.DateTimeField(blank=True, null=True)
    device_exposure_end_date: datetime = models.DateField(blank=True, null=True)
    device_exposure_end_datetime: datetime = models.DateTimeField(blank=True, null=True)
    device_type_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_device_type_concept_set",
    )
    unique_device_id: str = models.CharField(max_length=255, blank=True, null=True)
    production_id: str = models.CharField(max_length=255, blank=True, null=True)
    quantity: int = models.IntegerField(blank=True, null=True)
    provider: Provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence: VisitOccurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    device_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    device_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_device_source_concept_set",
        blank=True,
        null=True,
    )
    unit_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_unit_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    unit_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_unit_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "device_exposure"


class Domain(Record, CanValidate):
    """OMOP-defined Domains the Concepts of the Standardized Vocabularies can belong to.
    
    A Domain defines the set of allowable Concepts for the standardized fields in the CDM tables.
    """
    domain_id: str = models.CharField(primary_key=True, max_length=20)
    domain_name: str = models.CharField(max_length=255)
    domain_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "domain"


class DoseEra(Record, CanValidate):
    """Span of time when the Person is assumed to be exposed to a constant dose of a specific active ingredient."""

    dose_era_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    drug_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    unit_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="doseera_unit_concept_set"
    )
    dose_value: float = models.DecimalField(max_digits=1000, decimal_places=1000)
    dose_era_start_date: datetime = models.DateField()
    dose_era_end_date: datetime = models.DateField()

    class Meta:
        managed = True
        db_table = "dose_era"


class DrugEra(Record, CanValidate):
    """Span of time when the Person is assumed to be exposed to a particular active ingredient.

    A Drug Era is not the same as a Drug Exposure: Exposures are individual records corresponding to the source when Drug was delivered to the Person,
    while successive periods of Drug Exposures are combined under certain rules to produce continuous Drug Eras.
    """

    drug_era_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    drug_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    drug_era_start_date: datetime = models.DateField()
    drug_era_end_date: datetime = models.DateField()
    drug_exposure_count: int = models.IntegerField(blank=True, null=True)
    gap_days: int = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "drug_era"


class DrugExposure(Record, CanValidate):
    """Records about the exposure to a Drug ingested or otherwise introduced into the body.

    A Drug is a biochemical substance formulated in such a way that when administered to a Person it will exert a certain biochemical effect on the metabolism. 
    Drugs include prescription and over-the-counter medicines, vaccines, and large-molecule biologic therapies.
    Radiological devices ingested or applied locally do not count as Drugs.
    """

    drug_exposure_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    drug_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    drug_exposure_start_date: datetime = models.DateField()
    drug_exposure_start_datetime: datetime = models.DateTimeField(blank=True, null=True)
    drug_exposure_end_date: datetime = models.DateField()
    drug_exposure_end_datetime: datetime = models.DateTimeField(blank=True, null=True)
    verbatim_end_date: datetime = models.DateField(blank=True, null=True)
    drug_type_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="drugexposure_drug_type_concept_set"
    )
    stop_reason: str = models.CharField(max_length=20, blank=True, null=True)
    refills: int = models.IntegerField(blank=True, null=True)
    quantity: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    days_supply: int = models.IntegerField(blank=True, null=True)
    sig: str = models.TextField(blank=True, null=True)
    route_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugexposure_route_concept_set",
        blank=True,
        null=True,
    )
    lot_number: str = models.CharField(max_length=50, blank=True, null=True)
    provider: Provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence: VisitOccurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    drug_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    drug_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugexposure_drug_source_concept_set",
        blank=True,
        null=True,
    )
    route_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    dose_unit_source_value: str = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "drug_exposure"


class DrugStrength(Record, CanValidate):
    """Amount or concentration and associated units of a specific ingredient contained within a particular drug product.

    This table is supplemental information to support standardized analysis of drug utilization.
    """

    drug_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    ingredient_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="drugstrength_ingredient_concept_set"
    )
    amount_value: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    amount_unit_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_amount_unit_concept_set",
        blank=True,
        null=True,
    )
    numerator_value: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    numerator_unit_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_numerator_unit_concept_set",
        blank=True,
        null=True,
    )
    denominator_value: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    denominator_unit_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_denominator_unit_concept_set",
        blank=True,
        null=True,
    )
    box_size: int = models.IntegerField(blank=True, null=True)
    valid_start_date: datetime = models.DateField()
    valid_end_date: datetime = models.DateField()
    invalid_reason: str = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "drug_strength"


class Episode(Record, CanValidate):
    """Aggregates lower-level clinical events into a higher-level abstraction representing clinically and analytically relevant disease phases, outcomes and treatments. 
    
    The EPISODE_EVENT table connects qualifying clinical events (VISIT_OCCURRENCE, DRUG_EXPOSURE, PROCEDURE_OCCURRENCE, DEVICE_EXPOSURE) to the appropriate EPISODE entry.

    For example cancers including their development over time, their treatment, and final resolution.
    """

    episode_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    episode_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    episode_start_date: datetime = models.DateField()
    episode_start_datetime: datetime = models.DateTimeField(blank=True, null=True)
    episode_end_date: datetime = models.DateField(blank=True, null=True)
    episode_end_datetime: datetime = models.DateTimeField(blank=True, null=True)
    episode_parent_id: int = models.IntegerField(blank=True, null=True)
    episode_number: int = models.IntegerField(blank=True, null=True)
    episode_object_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="episode_episode_object_concept_set"
    )
    episode_type_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="episode_episode_type_concept_set"
    )
    episode_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    episode_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="episode_episode_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "episode"


class EpisodeEvent(Record, CanValidate):
    """The EPISODE_EVENT table connects qualifying clinical events to the appropriate EPISODE entry.
    
    Clinical events include CONDITION_OCCURRENCE, DRUG_EXPOSURE, PROCEDURE_OCCURRENCE, MEASUREMENT.

    For example, linking the precise location of the metastasis (cancer modifier in MEASUREMENT) to the disease episode.
    """

    episode: Episode = models.ForeignKey(Episode, models.DO_NOTHING)
    event_id: int = models.IntegerField()
    episode_event_field_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "episode_event"


class FactRelationship(Record, CanValidate):
    """Records about the relationships between facts stored as records in any table of the CDM.

    Relationships can be defined between facts from the same domain, or different domains.
    Examples of Fact Relationships include: Person relationships, care site relationships,
    indication relationship (between drug exposures and associated conditions), usage relationships (of devices during the course of an associated procedure),
    or facts derived from one another (measurements derived from an associated specimen).
    """

    domain_concept_id_1: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, db_column="domain_concept_id_1"
    )
    fact_id_1: int = models.IntegerField()
    domain_concept_id_2: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        db_column="domain_concept_id_2",
        related_name="factrelationship_domain_concept_id_2_set",
    )
    fact_id_2: int = models.IntegerField()
    relationship_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="factrelationship_relationship_concept_set",
    )

    class Meta:
        managed = True
        db_table = "fact_relationship"


class Location(Record, CanValidate):
    """Capture physical location or address information of Persons and Care Sites."""

    location_id: int = models.IntegerField(primary_key=True)
    address_1: str = models.CharField(max_length=50, blank=True, null=True)
    address_2: str = models.CharField(max_length=50, blank=True, null=True)
    city: str = models.CharField(max_length=50, blank=True, null=True)
    state: str = models.CharField(max_length=2, blank=True, null=True)
    zip: str = models.CharField(max_length=9, blank=True, null=True)
    county: str = models.CharField(max_length=20, blank=True, null=True)
    location_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    country_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    country_source_value: str = models.CharField(max_length=80, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    longitude: str = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "location"


class Measurement(Record, CanValidate):
    """Records of Measurements, i.e. structured values (numerical or categorical) obtained through systematic and standardized examination or testing of a Person or Persons sample.

    The MEASUREMENT table contains both orders and results of such Measurements as laboratory tests, vital signs, quantitative findings from pathology reports, etc.
    Measurements are stored as attribute value pairs, with the attribute as the Measurement Concept and the value representing the result. 
    The value can be a Concept (stored in VALUE_AS_CONCEPT), or a numerical value (VALUE_AS_NUMBER) with a Unit (UNIT_CONCEPT_ID).
    The Procedure for obtaining the sample is housed in the PROCEDURE_OCCURRENCE table, though it is unnecessary to create a PROCEDURE_OCCURRENCE record for each measurement if one does not exist in the source data. 
    Measurements differ from Observations in that they require a standardized test or some other activity to generate a quantitative or qualitative result.
    If there is no result, it is assumed that the lab test was conducted but the result was not captured.
    """

    measurement_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    measurement_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    measurement_date: datetime = models.DateField()
    measurement_datetime: datetime = models.DateTimeField(blank=True, null=True)
    measurement_time: str = models.CharField(max_length=10, blank=True, null=True)
    measurement_type_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_measurement_type_concept_set",
    )
    operator_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_operator_concept_set",
        blank=True,
        null=True,
    )
    value_as_number: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    value_as_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_value_as_concept_set",
        blank=True,
        null=True,
    )
    unit_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_unit_concept_set",
        blank=True,
        null=True,
    )
    range_low: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    range_high: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    provider: Provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    measurement_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    measurement_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_measurement_source_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    unit_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_unit_source_concept_set",
        blank=True,
        null=True,
    )
    value_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    measurement_event_id: int = models.IntegerField(blank=True, null=True)
    meas_event_field_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_meas_event_field_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "measurement"


class Metadata(Record, CanValidate):
    """Metadata information about a dataset that has been transformed to the OMOP Common Data Model."""

    metadata_id: int = models.IntegerField(primary_key=True)
    metadata_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    metadata_type_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="metadata_metadata_type_concept_set"
    )
    name: str = models.CharField(max_length=250)
    value_as_string: str = models.CharField(max_length=250, blank=True, null=True)
    value_as_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="metadata_value_as_concept_set",
        blank=True,
        null=True,
    )
    value_as_number: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    metadata_date: datetime = models.DateField(blank=True, null=True)
    metadata_datetime: datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "metadata"


class Note(Record, CanValidate):
    """Unstructured information that was recorded by a provider about a patient in free text notes on a given date."""

    note_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    note_date: datetime = models.DateField()
    note_datetime: datetime = models.DateTimeField(blank=True, null=True)
    note_type_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    note_class_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_note_class_concept_set"
    )
    note_title: str = models.CharField(max_length=250, blank=True, null=True)
    note_text: str = models.TextField()
    encoding_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_encoding_concept_set"
    )
    language_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_language_concept_set"
    )
    provider: Provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence: VisitOccurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    note_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    note_event_id: int = models.IntegerField(blank=True, null=True)
    note_event_field_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="note_note_event_field_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "note"


class NoteNlp(Record, CanValidate):
    """Encodes all output of NLP on clinical notes. Each row represents a single extracted term from a note."""

    note_nlp_id: int = models.IntegerField(primary_key=True)
    note_id: int = models.IntegerField()
    section_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    snippet: str = models.CharField(max_length=250, blank=True, null=True)
    offset: str = models.CharField(max_length=50, blank=True, null=True)
    lexical_variant: str = models.CharField(max_length=250)
    note_nlp_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="notenlp_note_nlp_concept_set",
        blank=True,
        null=True,
    )
    note_nlp_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="notenlp_note_nlp_source_concept_set",
        blank=True,
        null=True,
    )
    nlp_system: str = models.CharField(max_length=250, blank=True, null=True)
    nlp_date: datetime = models.DateField()
    nlp_datetime: datetime = models.DateTimeField(blank=True, null=True)
    term_exists: str = models.CharField(max_length=1, blank=True, null=True)
    term_temporal: str = models.CharField(max_length=50, blank=True, null=True)
    term_modifiers: str = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "note_nlp"


class Observation(Record, CanValidate):
    """Clinical facts about a Person obtained in the context of examination, questioning or a procedure.

    Any data that cannot be represented by any other domains, such as social and lifestyle facts, medical history, family history, etc. are recorded here.
    """

    observation_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    observation_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    observation_date: datetime = models.DateField()
    observation_datetime: datetime = models.DateTimeField(blank=True, null=True)
    observation_type_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_observation_type_concept_set",
    )
    value_as_number: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    value_as_string: str = models.CharField(max_length=60, blank=True, null=True)
    value_as_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_value_as_concept_set",
        blank=True,
        null=True,
    )
    qualifier_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_qualifier_concept_set",
        blank=True,
        null=True,
    )
    unit_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_unit_concept_set",
        blank=True,
        null=True,
    )
    provider: Provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence: VisitOccurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    observation_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    observation_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_observation_source_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    qualifier_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    value_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    observation_event_id: int = models.IntegerField(blank=True, null=True)
    obs_event_field_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_obs_event_field_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "observation"


class ObservationPeriod(Record, CanValidate):
    """Records which define spans of time during which two conditions are expected to hold:
    
    (i) Clinical Events that happened to the Person are recorded in the Event tables, and
    (ii) absense of records indicate such Events did not occur during this span of time."""

    observation_period_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    observation_period_start_date: datetime = models.DateField()
    observation_period_end_date: datetime = models.DateField()
    period_type_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "observation_period"


class PayerPlanPeriod(Record, CanValidate):
    """Details of the period of time that a Person is continuously enrolled under a specific health Plan benefit structure from a given Payer.

    Each Person receiving healthcare is typically covered by a health benefit plan, which pays for (fully or partially), or directly provides, the care.
    These benefit plans are provided by payers, such as health insurances or state or government agencies.
    In each plan the details of the health benefits are defined for the Person or her family, and the health benefit Plan might change over time typically with increasing utilization (reaching certain cost thresholds such as deductibles), plan availability and purchasing choices of the Person.
    The unique combinations of Payer organizations, health benefit Plans and time periods in which they are valid for a Person are recorded in this table.
    """

    payer_plan_period_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey("Person", models.DO_NOTHING)
    payer_plan_period_start_date: datetime = models.DateField()
    payer_plan_period_end_date: datetime = models.DateField()
    payer_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING, blank=True, null=True)
    payer_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    payer_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_payer_source_concept_set",
        blank=True,
        null=True,
    )
    plan_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_plan_concept_set",
        blank=True,
        null=True,
    )
    plan_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    plan_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_plan_source_concept_set",
        blank=True,
        null=True,
    )
    sponsor_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_sponsor_concept_set",
        blank=True,
        null=True,
    )
    sponsor_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    sponsor_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_sponsor_source_concept_set",
        blank=True,
        null=True,
    )
    family_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    stop_reason_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_stop_reason_concept_set",
        blank=True,
        null=True,
    )
    stop_reason_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    stop_reason_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_stop_reason_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "payer_plan_period"


class Person(Record, CanValidate):
    """Identity management for all Persons in the database.

    Records that uniquely identify each person or patient, and some demographic information.
    """

    person_id: int = models.IntegerField(primary_key=True)
    gender_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    year_of_birth: int = models.IntegerField()
    month_of_birth: int = models.IntegerField(blank=True, null=True)
    day_of_birth: int = models.IntegerField(blank=True, null=True)
    birth_datetime: datetime = models.DateTimeField(blank=True, null=True)
    race_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="person_race_concept_set"
    )
    ethnicity_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="person_ethnicity_concept_set"
    )
    location: Location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    provider: Provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    care_site: CareSite = models.ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    person_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    gender_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    gender_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_gender_source_concept_set",
        blank=True,
        null=True,
    )
    race_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    race_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_race_source_concept_set",
        blank=True,
        null=True,
    )
    ethnicity_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    ethnicity_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_ethnicity_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "person"


class ProcedureOccurrence(Record, CanValidate):
    """Records of activities or processes ordered by, or carried out by, a healthcare provider on the patient with a diagnostic or therapeutic purpose."""

    procedure_occurrence_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey(Person, models.DO_NOTHING)
    procedure_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    procedure_date: datetime = models.DateField()
    procedure_datetime: datetime = models.DateTimeField(blank=True, null=True)
    procedure_end_date: datetime = models.DateField(blank=True, null=True)
    procedure_end_datetime: datetime = models.DateTimeField(blank=True, null=True)
    procedure_type_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_procedure_type_concept_set",
    )
    modifier_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_modifier_concept_set",
        blank=True,
        null=True,
    )
    quantity: int = models.IntegerField(blank=True, null=True)
    provider: Provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence: VisitOccurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail: VisitDetail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    procedure_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    procedure_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_procedure_source_concept_set",
        blank=True,
        null=True,
    )
    modifier_source_value: str = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "procedure_occurrence"


class Provider(Record, CanValidate):
    """Uniquely identified healthcare providers.

    Individuals providing hands-on healthcare to patients, such as physicians, nurses, midwives, physical therapists etc.
    """

    provider_id: int = models.IntegerField(primary_key=True)
    provider_name: str = models.CharField(max_length=255, blank=True, null=True)
    npi: str = models.CharField(max_length=20, blank=True, null=True)
    dea: str = models.CharField(max_length=20, blank=True, null=True)
    specialty_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    care_site: CareSite = models.ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    year_of_birth: int = models.IntegerField(blank=True, null=True)
    gender_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_gender_concept_set",
        blank=True,
        null=True,
    )
    provider_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    specialty_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    specialty_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_specialty_source_concept_set",
        blank=True,
        null=True,
    )
    gender_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    gender_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_gender_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "provider"


class Relationship(Record, CanValidate):
    """All types of relationships that can be used to associate any two concepts in the CONCEPT_RELATIONSHP table."""

    relationship_id: str = models.CharField(primary_key=True, max_length=20)
    relationship_name: str = models.CharField(max_length=255)
    is_hierarchical: str = models.CharField(max_length=1)
    defines_ancestry: str = models.CharField(max_length=1)
    reverse_relationship_id: str = models.CharField(max_length=20)
    relationship_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "relationship"


class SourceToConceptMap(Record, CanValidate):
    """The source to concept map table is a legacy data structure within the OMOP Common Data Model.
    
    It is recommended for use in ETL processes to maintain local source codes which are not available as Concepts in the Standardized Vocabularies,
    and to establish mappings for each source code into a Standard Concept as target_concept_ids that can be used to populate the Common Data Model tables.
    The SOURCE_TO_CONCEPT_MAP table is no longer populated with content within the Standardized Vocabularies published to the OMOP community.
    """

    source_code: str = models.CharField(max_length=50)
    source_concept: str = models.ForeignKey(Concept, models.DO_NOTHING)
    source_vocabulary_id: str = models.CharField(max_length=20)
    source_code_description: str = models.CharField(max_length=255, blank=True, null=True)
    target_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="sourcetoconceptmap_target_concept_set"
    )
    target_vocabulary: Vocabulary = models.ForeignKey("Vocabulary", models.DO_NOTHING)
    valid_start_date: datetime = models.DateField()
    valid_end_date: datetime = models.DateField()
    invalid_reason: str = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "source_to_concept_map"


class Specimen(Record, CanValidate):
    """The specimen domain contains the records identifying biological samples from a person."""

    specimen_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey(Person, models.DO_NOTHING)
    specimen_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    specimen_type_concept: Concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="specimen_specimen_type_concept_set"
    )
    specimen_date: datetime = models.DateField()
    specimen_datetime: datetime = models.DateTimeField(blank=True, null=True)
    quantity: float = models.DecimalField(
        max_digits=1000, decimal_places=1000, blank=True, null=True
    )
    unit_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_unit_concept_set",
        blank=True,
        null=True,
    )
    anatomic_site_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_anatomic_site_concept_set",
        blank=True,
        null=True,
    )
    disease_status_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_disease_status_concept_set",
        blank=True,
        null=True,
    )
    specimen_source_id: str = models.CharField(max_length=50, blank=True, null=True)
    specimen_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    unit_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    anatomic_site_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    disease_status_source_value: str = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "specimen"


class VisitDetail(Record, CanValidate):
    """Optional table used to represents details of each record in the parent VISIT_OCCURRENCE table.

    A good example of this would be the movement between units in a hospital during an inpatient stay or claim lines associated with a one insurance claim.
    For every record in the VISIT_OCCURRENCE table there may be 0 or more records in the VISIT_DETAIL table with a 1:n relationship where n may be 0.
    The VISIT_DETAIL table is structurally very similar to VISIT_OCCURRENCE table and belongs to the visit domain.
    """

    visit_detail_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey(Person, models.DO_NOTHING)
    visit_detail_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    visit_detail_start_date: datetime = models.DateField()
    visit_detail_start_datetime: datetime = models.DateTimeField(blank=True, null=True)
    visit_detail_end_date: datetime = models.DateField()
    visit_detail_end_datetime: datetime = models.DateTimeField(blank=True, null=True)
    visit_detail_type_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_visit_detail_type_concept_set",
    )
    provider: Provider = models.ForeignKey(Provider, models.DO_NOTHING, blank=True, null=True)
    care_site: CareSite = models.ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    visit_detail_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    visit_detail_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_visit_detail_source_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_admitted_from_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    discharged_to_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    discharged_to_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_discharged_to_concept_set",
        blank=True,
        null=True,
    )
    preceding_visit_detail: VisitDetail = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )
    parent_visit_detail: VisitDetail = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="visitdetail_parent_visit_detail_set",
        blank=True,
        null=True,
    )
    visit_occurrence: VisitOccurrence = models.ForeignKey("VisitOccurrence", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "visit_detail"


class VisitOccurrence(Record, CanValidate):
    """Events where Persons engage with the healthcare system for a duration of time.

    They are often also called Encounters. Visits are defined by a configuration of circumstances under which they occur, such as
    (i) whether the patient comes to a healthcare institution, the other way around, or the interaction is remote,
    (ii) whether and what kind of trained medical staff is delivering the service during the Visit, and
    (iii) whether the Visit is transient or for a longer period involving a stay in bed.
    """

    visit_occurrence_id: int = models.IntegerField(primary_key=True)
    person: Person = models.ForeignKey(Person, models.DO_NOTHING)
    visit_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)
    visit_start_date: datetime = models.DateField()
    visit_start_datetime: datetime = models.DateTimeField(blank=True, null=True)
    visit_end_date: datetime = models.DateField()
    visit_end_datetime: datetime = models.DateTimeField(blank=True, null=True)
    visit_type_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_visit_type_concept_set",
    )
    provider: Provider = models.ForeignKey(Provider, models.DO_NOTHING, blank=True, null=True)
    care_site: CareSite = models.ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    visit_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    visit_source_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_visit_source_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_admitted_from_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    discharged_to_concept: Concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_discharged_to_concept_set",
        blank=True,
        null=True,
    )
    discharged_to_source_value: str = models.CharField(max_length=50, blank=True, null=True)
    preceding_visit_occurrence: VisitOccurrence = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "visit_occurrence"


class Vocabulary(Record, CanValidate):
    """Vocabularies collected from various sources or created de novo by the OMOP community.
    
    Populated with a single record for each Vocabulary source and includes a descriptive name and other associated attributes for the Vocabulary.
    """
    vocabulary_id: str = models.CharField(primary_key=True, max_length=20)
    vocabulary_name: str = models.CharField(max_length=255)
    vocabulary_reference: str = models.CharField(max_length=255, blank=True, null=True)
    vocabulary_version: str = models.CharField(max_length=255, blank=True, null=True)
    vocabulary_concept: Concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "vocabulary"
