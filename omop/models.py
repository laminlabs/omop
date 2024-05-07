# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from lnschema_core.models import Registry


class CareSite(Registry):
    care_site_id = models.IntegerField(primary_key=True)
    care_site_name = models.CharField(max_length=255, blank=True, null=True)
    place_of_service_concept = models.ForeignKey(
        "Concept", models.DO_NOTHING, blank=True, null=True
    )
    location = models.ForeignKey("Location", models.DO_NOTHING, blank=True, null=True)
    care_site_source_value = models.CharField(max_length=50, blank=True, null=True)
    place_of_service_source_value = models.CharField(
        max_length=50, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "care_site"


class CdmSource(Registry):
    cdm_source_name = models.CharField(max_length=255)
    cdm_source_abbreviation = models.CharField(max_length=25)
    cdm_holder = models.CharField(max_length=255)
    source_description = models.TextField(blank=True, null=True)
    source_documentation_reference = models.CharField(
        max_length=255, blank=True, null=True
    )
    cdm_etl_reference = models.CharField(max_length=255, blank=True, null=True)
    source_release_date = models.DateField()
    cdm_release_date = models.DateField()
    cdm_version = models.CharField(max_length=10, blank=True, null=True)
    cdm_version_concept = models.ForeignKey("Concept", models.DO_NOTHING)
    vocabulary_version = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = "cdm_source"


class Cohort(Registry):
    cohort_definition_id = models.IntegerField()
    subject_id = models.IntegerField()
    cohort_start_date = models.DateField()
    cohort_end_date = models.DateField()

    class Meta:
        managed = True
        db_table = "cohort"


class CohortDefinition(Registry):
    cohort_definition_id = models.IntegerField()
    cohort_definition_name = models.CharField(max_length=255)
    cohort_definition_description = models.TextField(blank=True, null=True)
    definition_type_concept = models.ForeignKey("Concept", models.DO_NOTHING)
    cohort_definition_syntax = models.TextField(blank=True, null=True)
    subject_concept = models.ForeignKey(
        "Concept",
        models.DO_NOTHING,
        related_name="cohortdefinition_subject_concept_set",
    )
    cohort_initiation_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cohort_definition"


class Concept(Registry):
    concept_id = models.IntegerField(primary_key=True)
    concept_name = models.CharField(max_length=255)
    domain = models.ForeignKey("Domain", models.DO_NOTHING)
    vocabulary = models.ForeignKey("Vocabulary", models.DO_NOTHING)
    concept_class = models.ForeignKey("ConceptClass", models.DO_NOTHING)
    standard_concept = models.CharField(max_length=1, blank=True, null=True)
    concept_code = models.CharField(max_length=50)
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "concept"


class ConceptAncestor(Registry):
    ancestor_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    descendant_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conceptancestor_descendant_concept_set",
    )
    min_levels_of_separation = models.IntegerField()
    max_levels_of_separation = models.IntegerField()

    class Meta:
        managed = True
        db_table = "concept_ancestor"


class ConceptClass(Registry):
    concept_class_id = models.CharField(primary_key=True, max_length=20)
    concept_class_name = models.CharField(max_length=255)
    concept_class_concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "concept_class"


class ConceptRelationship(Registry):
    concept_id_1 = models.ForeignKey(
        Concept, models.DO_NOTHING, db_column="concept_id_1"
    )
    concept_id_2 = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        db_column="concept_id_2",
        related_name="conceptrelationship_concept_id_2_set",
    )
    relationship = models.ForeignKey("Relationship", models.DO_NOTHING)
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "concept_relationship"


class ConceptSynonym(Registry):
    concept = models.ForeignKey(Concept, models.DO_NOTHING)
    concept_synonym_name = models.CharField(max_length=1000)
    language_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="conceptsynonym_language_concept_set"
    )

    class Meta:
        managed = True
        db_table = "concept_synonym"


class ConditionEra(Registry):
    condition_era_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    condition_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    condition_era_start_date = models.DateField()
    condition_era_end_date = models.DateField()
    condition_occurrence_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "condition_era"


class ConditionOccurrence(Registry):
    condition_occurrence_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    condition_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    condition_start_date = models.DateField()
    condition_start_datetime = models.DateTimeField(blank=True, null=True)
    condition_end_date = models.DateField(blank=True, null=True)
    condition_end_datetime = models.DateTimeField(blank=True, null=True)
    condition_type_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_type_concept_set",
    )
    condition_status_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_status_concept_set",
        blank=True,
        null=True,
    )
    stop_reason = models.CharField(max_length=20, blank=True, null=True)
    provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    condition_source_value = models.CharField(max_length=50, blank=True, null=True)
    condition_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="conditionoccurrence_condition_source_concept_set",
        blank=True,
        null=True,
    )
    condition_status_source_value = models.CharField(
        max_length=50, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "condition_occurrence"


class Cost(Registry):
    cost_id = models.IntegerField(primary_key=True)
    cost_event_id = models.IntegerField()
    cost_domain = models.ForeignKey("Domain", models.DO_NOTHING)
    cost_type_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    currency_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_currency_concept_set",
        blank=True,
        null=True,
    )
    total_charge = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    total_cost = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    total_paid = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    paid_by_payer = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    paid_by_patient = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    paid_patient_copay = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    paid_patient_coinsurance = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    paid_patient_deductible = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    paid_by_primary = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    paid_ingredient_cost = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    paid_dispensing_fee = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    payer_plan_period_id = models.IntegerField(blank=True, null=True)
    amount_allowed = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    revenue_code_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_revenue_code_concept_set",
        blank=True,
        null=True,
    )
    revenue_code_source_value = models.CharField(max_length=50, blank=True, null=True)
    drg_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="cost_drg_concept_set",
        blank=True,
        null=True,
    )
    drg_source_value = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cost"


class Death(Registry):
    person = models.ForeignKey("Person", models.DO_NOTHING)
    death_date = models.DateField()
    death_datetime = models.DateTimeField(blank=True, null=True)
    death_type_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    cause_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="death_cause_concept_set",
        blank=True,
        null=True,
    )
    cause_source_value = models.CharField(max_length=50, blank=True, null=True)
    cause_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="death_cause_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "death"


class DeviceExposure(Registry):
    device_exposure_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    device_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    device_exposure_start_date = models.DateField()
    device_exposure_start_datetime = models.DateTimeField(blank=True, null=True)
    device_exposure_end_date = models.DateField(blank=True, null=True)
    device_exposure_end_datetime = models.DateTimeField(blank=True, null=True)
    device_type_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_device_type_concept_set",
    )
    unique_device_id = models.CharField(max_length=255, blank=True, null=True)
    production_id = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    device_source_value = models.CharField(max_length=50, blank=True, null=True)
    device_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_device_source_concept_set",
        blank=True,
        null=True,
    )
    unit_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_unit_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value = models.CharField(max_length=50, blank=True, null=True)
    unit_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="deviceexposure_unit_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "device_exposure"


class Domain(Registry):
    domain_id = models.CharField(primary_key=True, max_length=20)
    domain_name = models.CharField(max_length=255)
    domain_concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "domain"


class DoseEra(Registry):
    dose_era_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    drug_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    unit_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="doseera_unit_concept_set"
    )
    dose_value = models.DecimalField(max_digits=65535, decimal_places=65535)
    dose_era_start_date = models.DateField()
    dose_era_end_date = models.DateField()

    class Meta:
        managed = True
        db_table = "dose_era"


class DrugEra(Registry):
    drug_era_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    drug_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    drug_era_start_date = models.DateField()
    drug_era_end_date = models.DateField()
    drug_exposure_count = models.IntegerField(blank=True, null=True)
    gap_days = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "drug_era"


class DrugExposure(Registry):
    drug_exposure_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    drug_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    drug_exposure_start_date = models.DateField()
    drug_exposure_start_datetime = models.DateTimeField(blank=True, null=True)
    drug_exposure_end_date = models.DateField()
    drug_exposure_end_datetime = models.DateTimeField(blank=True, null=True)
    verbatim_end_date = models.DateField(blank=True, null=True)
    drug_type_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="drugexposure_drug_type_concept_set"
    )
    stop_reason = models.CharField(max_length=20, blank=True, null=True)
    refills = models.IntegerField(blank=True, null=True)
    quantity = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    days_supply = models.IntegerField(blank=True, null=True)
    sig = models.TextField(blank=True, null=True)
    route_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugexposure_route_concept_set",
        blank=True,
        null=True,
    )
    lot_number = models.CharField(max_length=50, blank=True, null=True)
    provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    drug_source_value = models.CharField(max_length=50, blank=True, null=True)
    drug_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugexposure_drug_source_concept_set",
        blank=True,
        null=True,
    )
    route_source_value = models.CharField(max_length=50, blank=True, null=True)
    dose_unit_source_value = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "drug_exposure"


class DrugStrength(Registry):
    drug_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    ingredient_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="drugstrength_ingredient_concept_set"
    )
    amount_value = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    amount_unit_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_amount_unit_concept_set",
        blank=True,
        null=True,
    )
    numerator_value = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    numerator_unit_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_numerator_unit_concept_set",
        blank=True,
        null=True,
    )
    denominator_value = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    denominator_unit_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="drugstrength_denominator_unit_concept_set",
        blank=True,
        null=True,
    )
    box_size = models.IntegerField(blank=True, null=True)
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "drug_strength"


class Episode(Registry):
    episode_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    episode_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    episode_start_date = models.DateField()
    episode_start_datetime = models.DateTimeField(blank=True, null=True)
    episode_end_date = models.DateField(blank=True, null=True)
    episode_end_datetime = models.DateTimeField(blank=True, null=True)
    episode_parent_id = models.IntegerField(blank=True, null=True)
    episode_number = models.IntegerField(blank=True, null=True)
    episode_object_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="episode_episode_object_concept_set"
    )
    episode_type_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="episode_episode_type_concept_set"
    )
    episode_source_value = models.CharField(max_length=50, blank=True, null=True)
    episode_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="episode_episode_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "episode"


class EpisodeEvent(Registry):
    episode = models.ForeignKey(Episode, models.DO_NOTHING)
    event_id = models.IntegerField()
    episode_event_field_concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "episode_event"


class FactRelationship(Registry):
    domain_concept_id_1 = models.ForeignKey(
        Concept, models.DO_NOTHING, db_column="domain_concept_id_1"
    )
    fact_id_1 = models.IntegerField()
    domain_concept_id_2 = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        db_column="domain_concept_id_2",
        related_name="factrelationship_domain_concept_id_2_set",
    )
    fact_id_2 = models.IntegerField()
    relationship_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="factrelationship_relationship_concept_set",
    )

    class Meta:
        managed = True
        db_table = "fact_relationship"


class Location(Registry):
    location_id = models.IntegerField(primary_key=True)
    address_1 = models.CharField(max_length=50, blank=True, null=True)
    address_2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=9, blank=True, null=True)
    county = models.CharField(max_length=20, blank=True, null=True)
    location_source_value = models.CharField(max_length=50, blank=True, null=True)
    country_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    country_source_value = models.CharField(max_length=80, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "location"


class Measurement(Registry):
    measurement_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    measurement_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    measurement_date = models.DateField()
    measurement_datetime = models.DateTimeField(blank=True, null=True)
    measurement_time = models.CharField(max_length=10, blank=True, null=True)
    measurement_type_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_measurement_type_concept_set",
    )
    operator_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_operator_concept_set",
        blank=True,
        null=True,
    )
    value_as_number = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    value_as_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_value_as_concept_set",
        blank=True,
        null=True,
    )
    unit_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_unit_concept_set",
        blank=True,
        null=True,
    )
    range_low = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    range_high = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    measurement_source_value = models.CharField(max_length=50, blank=True, null=True)
    measurement_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_measurement_source_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value = models.CharField(max_length=50, blank=True, null=True)
    unit_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_unit_source_concept_set",
        blank=True,
        null=True,
    )
    value_source_value = models.CharField(max_length=50, blank=True, null=True)
    measurement_event_id = models.IntegerField(blank=True, null=True)
    meas_event_field_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="measurement_meas_event_field_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "measurement"


class Metadata(Registry):
    metadata_id = models.IntegerField(primary_key=True)
    metadata_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    metadata_type_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="metadata_metadata_type_concept_set"
    )
    name = models.CharField(max_length=250)
    value_as_string = models.CharField(max_length=250, blank=True, null=True)
    value_as_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="metadata_value_as_concept_set",
        blank=True,
        null=True,
    )
    value_as_number = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    metadata_date = models.DateField(blank=True, null=True)
    metadata_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "metadata"


class Note(Registry):
    note_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    note_date = models.DateField()
    note_datetime = models.DateTimeField(blank=True, null=True)
    note_type_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    note_class_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_note_class_concept_set"
    )
    note_title = models.CharField(max_length=250, blank=True, null=True)
    note_text = models.TextField()
    encoding_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_encoding_concept_set"
    )
    language_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="note_language_concept_set"
    )
    provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    note_source_value = models.CharField(max_length=50, blank=True, null=True)
    note_event_id = models.IntegerField(blank=True, null=True)
    note_event_field_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="note_note_event_field_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "note"


class NoteNlp(Registry):
    note_nlp_id = models.IntegerField(primary_key=True)
    note_id = models.IntegerField()
    section_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    snippet = models.CharField(max_length=250, blank=True, null=True)
    offset = models.CharField(max_length=50, blank=True, null=True)
    lexical_variant = models.CharField(max_length=250)
    note_nlp_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="notenlp_note_nlp_concept_set",
        blank=True,
        null=True,
    )
    note_nlp_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="notenlp_note_nlp_source_concept_set",
        blank=True,
        null=True,
    )
    nlp_system = models.CharField(max_length=250, blank=True, null=True)
    nlp_date = models.DateField()
    nlp_datetime = models.DateTimeField(blank=True, null=True)
    term_exists = models.CharField(max_length=1, blank=True, null=True)
    term_temporal = models.CharField(max_length=50, blank=True, null=True)
    term_modifiers = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "note_nlp"


class Observation(Registry):
    observation_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    observation_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    observation_date = models.DateField()
    observation_datetime = models.DateTimeField(blank=True, null=True)
    observation_type_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_observation_type_concept_set",
    )
    value_as_number = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    value_as_string = models.CharField(max_length=60, blank=True, null=True)
    value_as_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_value_as_concept_set",
        blank=True,
        null=True,
    )
    qualifier_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_qualifier_concept_set",
        blank=True,
        null=True,
    )
    unit_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_unit_concept_set",
        blank=True,
        null=True,
    )
    provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    observation_source_value = models.CharField(max_length=50, blank=True, null=True)
    observation_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_observation_source_concept_set",
        blank=True,
        null=True,
    )
    unit_source_value = models.CharField(max_length=50, blank=True, null=True)
    qualifier_source_value = models.CharField(max_length=50, blank=True, null=True)
    value_source_value = models.CharField(max_length=50, blank=True, null=True)
    observation_event_id = models.IntegerField(blank=True, null=True)
    obs_event_field_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="observation_obs_event_field_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "observation"


class ObservationPeriod(Registry):
    observation_period_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    observation_period_start_date = models.DateField()
    observation_period_end_date = models.DateField()
    period_type_concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "observation_period"


class PayerPlanPeriod(Registry):
    payer_plan_period_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey("Person", models.DO_NOTHING)
    payer_plan_period_start_date = models.DateField()
    payer_plan_period_end_date = models.DateField()
    payer_concept = models.ForeignKey(Concept, models.DO_NOTHING, blank=True, null=True)
    payer_source_value = models.CharField(max_length=50, blank=True, null=True)
    payer_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_payer_source_concept_set",
        blank=True,
        null=True,
    )
    plan_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_plan_concept_set",
        blank=True,
        null=True,
    )
    plan_source_value = models.CharField(max_length=50, blank=True, null=True)
    plan_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_plan_source_concept_set",
        blank=True,
        null=True,
    )
    sponsor_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_sponsor_concept_set",
        blank=True,
        null=True,
    )
    sponsor_source_value = models.CharField(max_length=50, blank=True, null=True)
    sponsor_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_sponsor_source_concept_set",
        blank=True,
        null=True,
    )
    family_source_value = models.CharField(max_length=50, blank=True, null=True)
    stop_reason_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_stop_reason_concept_set",
        blank=True,
        null=True,
    )
    stop_reason_source_value = models.CharField(max_length=50, blank=True, null=True)
    stop_reason_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="payerplanperiod_stop_reason_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "payer_plan_period"


class Person(Registry):
    person_id = models.IntegerField(primary_key=True)
    gender_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    year_of_birth = models.IntegerField()
    month_of_birth = models.IntegerField(blank=True, null=True)
    day_of_birth = models.IntegerField(blank=True, null=True)
    birth_datetime = models.DateTimeField(blank=True, null=True)
    race_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="person_race_concept_set"
    )
    ethnicity_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="person_ethnicity_concept_set"
    )
    location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    care_site = models.ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    person_source_value = models.CharField(max_length=50, blank=True, null=True)
    gender_source_value = models.CharField(max_length=50, blank=True, null=True)
    gender_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_gender_source_concept_set",
        blank=True,
        null=True,
    )
    race_source_value = models.CharField(max_length=50, blank=True, null=True)
    race_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_race_source_concept_set",
        blank=True,
        null=True,
    )
    ethnicity_source_value = models.CharField(max_length=50, blank=True, null=True)
    ethnicity_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="person_ethnicity_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "person"


class ProcedureOccurrence(Registry):
    procedure_occurrence_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    procedure_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    procedure_date = models.DateField()
    procedure_datetime = models.DateTimeField(blank=True, null=True)
    procedure_end_date = models.DateField(blank=True, null=True)
    procedure_end_datetime = models.DateTimeField(blank=True, null=True)
    procedure_type_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_procedure_type_concept_set",
    )
    modifier_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_modifier_concept_set",
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(blank=True, null=True)
    provider = models.ForeignKey("Provider", models.DO_NOTHING, blank=True, null=True)
    visit_occurrence = models.ForeignKey(
        "VisitOccurrence", models.DO_NOTHING, blank=True, null=True
    )
    visit_detail = models.ForeignKey(
        "VisitDetail", models.DO_NOTHING, blank=True, null=True
    )
    procedure_source_value = models.CharField(max_length=50, blank=True, null=True)
    procedure_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="procedureoccurrence_procedure_source_concept_set",
        blank=True,
        null=True,
    )
    modifier_source_value = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "procedure_occurrence"


class Provider(Registry):
    provider_id = models.IntegerField(primary_key=True)
    provider_name = models.CharField(max_length=255, blank=True, null=True)
    npi = models.CharField(max_length=20, blank=True, null=True)
    dea = models.CharField(max_length=20, blank=True, null=True)
    specialty_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, blank=True, null=True
    )
    care_site = models.ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    year_of_birth = models.IntegerField(blank=True, null=True)
    gender_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_gender_concept_set",
        blank=True,
        null=True,
    )
    provider_source_value = models.CharField(max_length=50, blank=True, null=True)
    specialty_source_value = models.CharField(max_length=50, blank=True, null=True)
    specialty_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_specialty_source_concept_set",
        blank=True,
        null=True,
    )
    gender_source_value = models.CharField(max_length=50, blank=True, null=True)
    gender_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="provider_gender_source_concept_set",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "provider"


class Relationship(Registry):
    relationship_id = models.CharField(primary_key=True, max_length=20)
    relationship_name = models.CharField(max_length=255)
    is_hierarchical = models.CharField(max_length=1)
    defines_ancestry = models.CharField(max_length=1)
    reverse_relationship_id = models.CharField(max_length=20)
    relationship_concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "relationship"


class SourceToConceptMap(Registry):
    source_code = models.CharField(max_length=50)
    source_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    source_vocabulary_id = models.CharField(max_length=20)
    source_code_description = models.CharField(max_length=255, blank=True, null=True)
    target_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="sourcetoconceptmap_target_concept_set"
    )
    target_vocabulary = models.ForeignKey("Vocabulary", models.DO_NOTHING)
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "source_to_concept_map"


class Specimen(Registry):
    specimen_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    specimen_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    specimen_type_concept = models.ForeignKey(
        Concept, models.DO_NOTHING, related_name="specimen_specimen_type_concept_set"
    )
    specimen_date = models.DateField()
    specimen_datetime = models.DateTimeField(blank=True, null=True)
    quantity = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    unit_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_unit_concept_set",
        blank=True,
        null=True,
    )
    anatomic_site_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_anatomic_site_concept_set",
        blank=True,
        null=True,
    )
    disease_status_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="specimen_disease_status_concept_set",
        blank=True,
        null=True,
    )
    specimen_source_id = models.CharField(max_length=50, blank=True, null=True)
    specimen_source_value = models.CharField(max_length=50, blank=True, null=True)
    unit_source_value = models.CharField(max_length=50, blank=True, null=True)
    anatomic_site_source_value = models.CharField(max_length=50, blank=True, null=True)
    disease_status_source_value = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "specimen"


class VisitDetail(Registry):
    visit_detail_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    visit_detail_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    visit_detail_start_date = models.DateField()
    visit_detail_start_datetime = models.DateTimeField(blank=True, null=True)
    visit_detail_end_date = models.DateField()
    visit_detail_end_datetime = models.DateTimeField(blank=True, null=True)
    visit_detail_type_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_visit_detail_type_concept_set",
    )
    provider = models.ForeignKey(Provider, models.DO_NOTHING, blank=True, null=True)
    care_site = models.ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    visit_detail_source_value = models.CharField(max_length=50, blank=True, null=True)
    visit_detail_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_visit_detail_source_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_admitted_from_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_source_value = models.CharField(max_length=50, blank=True, null=True)
    discharged_to_source_value = models.CharField(max_length=50, blank=True, null=True)
    discharged_to_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitdetail_discharged_to_concept_set",
        blank=True,
        null=True,
    )
    preceding_visit_detail = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )
    parent_visit_detail = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="visitdetail_parent_visit_detail_set",
        blank=True,
        null=True,
    )
    visit_occurrence = models.ForeignKey("VisitOccurrence", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "visit_detail"


class VisitOccurrence(Registry):
    visit_occurrence_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    visit_concept = models.ForeignKey(Concept, models.DO_NOTHING)
    visit_start_date = models.DateField()
    visit_start_datetime = models.DateTimeField(blank=True, null=True)
    visit_end_date = models.DateField()
    visit_end_datetime = models.DateTimeField(blank=True, null=True)
    visit_type_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_visit_type_concept_set",
    )
    provider = models.ForeignKey(Provider, models.DO_NOTHING, blank=True, null=True)
    care_site = models.ForeignKey(CareSite, models.DO_NOTHING, blank=True, null=True)
    visit_source_value = models.CharField(max_length=50, blank=True, null=True)
    visit_source_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_visit_source_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_admitted_from_concept_set",
        blank=True,
        null=True,
    )
    admitted_from_source_value = models.CharField(max_length=50, blank=True, null=True)
    discharged_to_concept = models.ForeignKey(
        Concept,
        models.DO_NOTHING,
        related_name="visitoccurrence_discharged_to_concept_set",
        blank=True,
        null=True,
    )
    discharged_to_source_value = models.CharField(max_length=50, blank=True, null=True)
    preceding_visit_occurrence = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "visit_occurrence"


class Vocabulary(Registry):
    vocabulary_id = models.CharField(primary_key=True, max_length=20)
    vocabulary_name = models.CharField(max_length=255)
    vocabulary_reference = models.CharField(max_length=255, blank=True, null=True)
    vocabulary_version = models.CharField(max_length=255, blank=True, null=True)
    vocabulary_concept = models.ForeignKey(Concept, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "vocabulary"
