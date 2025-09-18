# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActionEmailMapping(models.Model):
    action_email_mapping_id = models.AutoField(primary_key=True)
    action_master_id = models.IntegerField(blank=True, null=True)
    from_email_id = models.CharField(max_length=100, blank=True, null=True)
    to_email_id = models.CharField(max_length=100, blank=True, null=True)
    cc_email_id = models.CharField(max_length=100, blank=True, null=True)
    bcc_email_id = models.CharField(max_length=100, blank=True, null=True)
    template_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action_email_mapping'


class ActionMaster(models.Model):
    action_master_id = models.AutoField(primary_key=True)
    action_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action_master'


class AgencyCodeDetails(models.Model):
    agency_code_id = models.AutoField(primary_key=True)
    agency_code = models.CharField(max_length=30, blank=True, null=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    airline_code = models.CharField(max_length=2)
    code_type = models.CharField(max_length=2)
    status = models.CharField(max_length=10, blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agency_code_details'


class AgencyCodeHistory(models.Model):
    agency_code_history_id = models.AutoField(primary_key=True)
    agency_code_id = models.IntegerField(blank=True, null=True)
    agency_code = models.CharField(max_length=30, blank=True, null=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    airline_code = models.CharField(max_length=2)
    code_type = models.CharField(max_length=2)
    status = models.CharField(max_length=10, blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agency_code_history'


class AgencyCodeUserMapping(models.Model):
    agency_code_user_mapping_id = models.AutoField(primary_key=True)
    agency_code_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agency_code_user_mapping'


class AgencyPaymentFailedHistory(models.Model):
    agency_payment_failed_id = models.AutoField(primary_key=True)
    payment_master_id = models.IntegerField(blank=True, null=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    payment_type_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=10, blank=True, null=True)
    amount_to_pay = models.FloatField(blank=True, null=True)
    paid_by = models.IntegerField(blank=True, null=True)
    agent_id = models.CharField(max_length=200, blank=True, null=True)
    pnr_status = models.CharField(max_length=20, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    card_authorization = models.CharField(max_length=20, blank=True, null=True)
    error = models.CharField(max_length=300, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agency_payment_failed_history'


class AirlinesRequestMapping(models.Model):
    airlines_request_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    current_status = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    request_upload_batch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airlines_request_mapping'


class AirportDetails(models.Model):
    airport_id = models.AutoField(primary_key=True)
    airport_code = models.CharField(unique=True, max_length=3)
    airport_name = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=2)
    display_status = models.CharField(max_length=1)
    user_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airport_details'


class AlternateSeriesRequestDetails(models.Model):
    alternate_series_request_id = models.AutoField(primary_key=True)
    transaction_master_id = models.IntegerField(blank=True, null=True)
    series_request_id = models.IntegerField(blank=True, null=True)
    request_id = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=3, blank=True, null=True)
    destination = models.CharField(max_length=3, blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    number_of_passenger = models.IntegerField(blank=True, null=True)
    number_of_adult = models.IntegerField(blank=True, null=True)
    number_of_child = models.IntegerField(blank=True, null=True)
    number_of_infant = models.IntegerField(blank=True, null=True)
    cabin = models.CharField(max_length=20, blank=True, null=True)
    start_time = models.CharField(max_length=20, blank=True, null=True)
    end_time = models.CharField(max_length=5, blank=True, null=True)
    baggage_allowance = models.CharField(max_length=250, blank=True, null=True)
    ancillary = models.CharField(max_length=5, blank=True, null=True)
    meals_code = models.CharField(max_length=5, blank=True, null=True)
    pnr = models.CharField(max_length=25, blank=True, null=True)
    expected_fare = models.FloatField(blank=True, null=True)
    group_category_id = models.IntegerField(blank=True, null=True)
    flight_status = models.CharField(max_length=5, blank=True, null=True)
    response_id = models.IntegerField(blank=True, null=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    mapped_series_request_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alternate_series_request_details'


class AttachmentDetails(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    attachment_type_id = models.IntegerField()
    attachment_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    file_szie = models.CharField(max_length=64)
    meta_info = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'attachment_details'


class AttachmentLog(models.Model):
    attachment_log_id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=8)
    attachment_id = models.IntegerField()
    user_id = models.IntegerField()
    create_datetime = models.DateTimeField()
    update_timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'attachment_log'


class AttachmentMapping(models.Model):
    attachment_mapping_id = models.AutoField(primary_key=True)
    attachment_type_id = models.IntegerField()
    attachment_id = models.IntegerField()
    id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'attachment_mapping'


class AttachmentTypeMaster(models.Model):
    attachment_type_id = models.AutoField(primary_key=True)
    attachment_type = models.CharField(max_length=64)
    attachment_folder = models.CharField(max_length=64)
    mapping_ref_table = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'attachment_type_master'


class AttachmentUserMapping(models.Model):
    attachment_mapping_id = models.AutoField(primary_key=True)
    attachment_id = models.IntegerField()
    level = models.CharField(max_length=5)
    id = models.IntegerField()
    status = models.CharField(max_length=1)
    create_timestamp = models.DateTimeField()
    update_timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'attachment_user_mapping'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField('SystemTUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class AutoPilotCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    negotiation_auto_pilot_display_status = models.CharField(max_length=1, blank=True, null=True)
    criteria_logical_id = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auto_pilot_criteria_master'


class AutoPilotPolicyDetails(models.Model):
    policy_details_id = models.AutoField(primary_key=True)
    policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField()
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auto_pilot_policy_details'


class AutoPilotPolicyMaster(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=100, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    process_type = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    policy_type = models.CharField(max_length=1, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auto_pilot_policy_master'


class BaggageDetails(models.Model):
    baggage_id = models.AutoField(primary_key=True)
    baggage_name = models.CharField(max_length=250, blank=True, null=True)
    baggage_code = models.CharField(max_length=5)
    baggage_cabin = models.CharField(max_length=25)
    baggage_market = models.CharField(max_length=25)
    pax_type = models.CharField(max_length=10)
    baggage_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'baggage_details'


class BaggageMapping(models.Model):
    baggage_mapping_id = models.AutoField(primary_key=True)
    baggage_matrix_id = models.IntegerField(blank=True, null=True)
    days_to_departure = models.IntegerField(blank=True, null=True)
    booked_load_factor = models.IntegerField(blank=True, null=True)
    forecast_load_factor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baggage_mapping'


class BaggageMatrix(models.Model):
    baggage_matrix_id = models.AutoField(primary_key=True)
    baggage_matrix_name = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baggage_matrix'


class BaggageValueMapping(models.Model):
    baggage_value_mapping_id = models.AutoField(primary_key=True)
    baggage_mapping_id = models.IntegerField(blank=True, null=True)
    group_size = models.IntegerField(blank=True, null=True)
    baggage_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baggage_value_mapping'


class BankDetails(models.Model):
    bank_details_id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=70, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    branch_code = models.CharField(max_length=50, blank=True, null=True)
    beneficiary_name = models.CharField(max_length=50, blank=True, null=True)
    additional_data = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bank_details'


class BankPosMapping(models.Model):
    bank_mapping_id = models.AutoField(primary_key=True)
    bank_details_id = models.IntegerField(blank=True, null=True)
    pos_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bank_pos_mapping'


class BatchDetails(models.Model):
    batch_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    initiated_by = models.IntegerField(blank=True, null=True)
    batch_date = models.DateTimeField()
    batch_status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'batch_details'


class BidPriceDetails(models.Model):
    bid_price_id = models.AutoField(primary_key=True)
    request_approved_flight_id = models.IntegerField(blank=True, null=True)
    via_flight_id = models.IntegerField(blank=True, null=True)
    bid_fare = models.FloatField(blank=True, null=True)
    sold = models.IntegerField(blank=True, null=True)
    seat_taken = models.IntegerField(blank=True, null=True)
    bid_price_values = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bid_price_details'


class BillingDetails(models.Model):
    payment_id = models.IntegerField(blank=True, null=True)
    address_one = models.CharField(max_length=40, blank=True, null=True)
    address_two = models.CharField(max_length=40, blank=True, null=True)
    address_three = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    area_code = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    email_id = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'billing_details'


class BookingProfileDetails(models.Model):
    booking_profile_id = models.AutoField(primary_key=True)
    booking_profile_name = models.CharField(max_length=100, blank=True, null=True)
    booking_profile_type = models.CharField(max_length=5, blank=True, null=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)
    currency_type = models.CharField(max_length=3, blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking_profile_details'


class CabinDetails(models.Model):
    cabin_id = models.AutoField(primary_key=True)
    cabin_name = models.CharField(max_length=250, blank=True, null=True)
    cabin_status = models.CharField(max_length=1, blank=True, null=True)
    cabin_value = models.CharField(max_length=25, blank=True, null=True)
    pnr_blocking_class = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cabin_details'


class CancelPnrDetails(models.Model):
    cancel_pnr_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    request_approved_flight_id = models.IntegerField()
    request_group_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=7)
    cancelled_by = models.IntegerField()
    status = models.CharField(max_length=20)
    cancelled_date = models.DateTimeField()
    cancel_remarks = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cancel_pnr_details'


class CancelPolicyCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100)
    criteria_type = models.CharField(max_length=3)
    display_status = models.CharField(max_length=1)
    criteria_logical_id = models.CharField(max_length=100)
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cancel_policy_criteria_master'


class CancelPolicyDetails(models.Model):
    cancel_policy_id = models.AutoField(primary_key=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    cancel_policy_name = models.CharField(max_length=150, blank=True, null=True)
    cancel_policy_description = models.TextField(blank=True, null=True)
    activation_status = models.CharField(max_length=1, blank=True, null=True)
    default_status = models.CharField(max_length=1, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cancel_policy_details'


class CancelPolicyMatrixDetails(models.Model):
    cancel_policy_matrix_detail_id = models.AutoField(primary_key=True)
    cancel_policy_matrix_master_id = models.IntegerField()
    criteria_id = models.IntegerField()
    loop_value = models.IntegerField()
    operator_id = models.IntegerField()
    policy_value = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'cancel_policy_matrix_details'


class CancelPolicyMatrixMaster(models.Model):
    cancel_policy_matrix_master_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=100)
    cancel_policy_id = models.IntegerField()
    priority = models.IntegerField()
    active_status = models.CharField(max_length=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField()
    policy_dow = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cancel_policy_matrix_master'


class CardDetails(models.Model):
    payment_id = models.IntegerField(blank=True, null=True)
    card_type = models.CharField(max_length=5, blank=True, null=True)
    card_number = models.CharField(max_length=30, blank=True, null=True)
    cvv_number = models.CharField(max_length=30, blank=True, null=True)
    expdate_year = models.CharField(max_length=5, blank=True, null=True)
    expdate_mon = models.CharField(max_length=2, blank=True, null=True)
    name_on_card = models.CharField(max_length=40, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'card_details'


class CardDetailsHistory(models.Model):
    card_history_id = models.AutoField(primary_key=True)
    payment_id = models.IntegerField(blank=True, null=True)
    card_type = models.CharField(max_length=5, blank=True, null=True)
    card_number = models.CharField(max_length=100, blank=True, null=True)
    cvv_number = models.CharField(max_length=30, blank=True, null=True)
    expdate_year = models.CharField(max_length=30, blank=True, null=True)
    expdate_mon = models.CharField(max_length=30, blank=True, null=True)
    name_on_card = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'card_details_history'


class CategorySubcategoryAccessMapping(models.Model):
    issue_category_id = models.IntegerField(blank=True, null=True)
    issue_subcategory_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_subcategory_access_mapping'


class CitizenshipDetails(models.Model):
    citizenship_id = models.AutoField(primary_key=True)
    citizenship_name = models.CharField(max_length=100, blank=True, null=True)
    citizen_code = models.CharField(unique=True, max_length=3, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    currency_code = models.CharField(max_length=5)
    phone_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'citizenship_details'


class CityMaster(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=40, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    pos_code = models.CharField(max_length=5)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city_master'


class CommonPolicyDetails(models.Model):
    policy_details_id = models.AutoField(primary_key=True)
    policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)
    loop_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'common_policy_details'


class CommonPolicyMaster(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_type_id = models.IntegerField(blank=True, null=True)
    policy_name = models.CharField(max_length=100, blank=True, null=True)
    matrix_id = models.IntegerField(blank=True, null=True)
    matrix_type = models.CharField(max_length=5, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    active_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    negotiation_status = models.CharField(max_length=1, blank=True, null=True)
    negotiation_limit = models.CharField(max_length=10, blank=True, null=True)
    materialization_rate = models.FloatField(blank=True, null=True)
    conversion_rate = models.CharField(max_length=1, blank=True, null=True)
    prediction_type = models.CharField(max_length=5, blank=True, null=True)
    process_type = models.CharField(max_length=2, blank=True, null=True)
    spl_fare_type = models.CharField(max_length=100, blank=True, null=True)
    additional_discount = models.CharField(max_length=1, blank=True, null=True)
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    policy_string = models.TextField()
    fare_range = models.TextField(blank=True, null=True)
    additional_details = models.TextField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_policy_master'


class CompetitorFareBatchDetails(models.Model):
    batch_id = models.AutoField(primary_key=True)
    folder_name = models.CharField(max_length=200, blank=True, null=True)
    file_count = models.IntegerField(blank=True, null=True)
    processed_file_count = models.IntegerField(blank=True, null=True)
    backup_zip_file_name = models.CharField(max_length=200, blank=True, null=True)
    batch_type = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    batch_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_fare_batch_details'


class CompetitorFareBatchFileDetails(models.Model):
    batch_file_id = models.AutoField(primary_key=True)
    batch_id = models.IntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    status_msg = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    moved_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_fare_batch_file_details'


class CompetitorFlightDetails(models.Model):
    competitor_flight_id = models.AutoField(primary_key=True)
    batch_id = models.IntegerField(blank=True, null=True)
    batch_file_id = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=3, blank=True, null=True)
    destination = models.CharField(max_length=3, blank=True, null=True)
    carrier = models.CharField(max_length=5, blank=True, null=True)
    trip_type = models.CharField(max_length=1, blank=True, null=True)
    onward_departure_date = models.DateField(blank=True, null=True)
    onward_departure_time = models.TimeField(blank=True, null=True)
    onward_arrival_date = models.DateField(blank=True, null=True)
    onward_arrival_time = models.TimeField(blank=True, null=True)
    return_departure_date = models.DateField(blank=True, null=True)
    return_departure_time = models.TimeField(blank=True, null=True)
    return_arrival_date = models.DateField(blank=True, null=True)
    return_arrival_time = models.TimeField(blank=True, null=True)
    onward_stop = models.IntegerField(blank=True, null=True)
    onward_flight = models.CharField(max_length=20, blank=True, null=True)
    onward_class = models.CharField(max_length=20, blank=True, null=True)
    return_stop = models.IntegerField(blank=True, null=True)
    return_flight = models.CharField(max_length=20, blank=True, null=True)
    return_class = models.CharField(max_length=20, blank=True, null=True)
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    base_fare = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    total_fare = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_flight_details'


class CompetitorFlightDetailsTemp(models.Model):
    competitor_flight_id = models.AutoField(primary_key=True)
    batch_id = models.IntegerField(blank=True, null=True)
    batch_file_id = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=3, blank=True, null=True)
    destination = models.CharField(max_length=3, blank=True, null=True)
    carrier = models.CharField(max_length=5, blank=True, null=True)
    trip_type = models.CharField(max_length=1, blank=True, null=True)
    onward_departure_date = models.DateField(blank=True, null=True)
    onward_departure_time = models.TimeField(blank=True, null=True)
    onward_arrival_date = models.DateField(blank=True, null=True)
    onward_arrival_time = models.TimeField(blank=True, null=True)
    return_departure_date = models.DateField(blank=True, null=True)
    return_departure_time = models.TimeField(blank=True, null=True)
    return_arrival_date = models.DateField(blank=True, null=True)
    return_arrival_time = models.TimeField(blank=True, null=True)
    onward_stop = models.IntegerField(blank=True, null=True)
    onward_flight = models.CharField(max_length=20, blank=True, null=True)
    onward_class = models.CharField(max_length=20, blank=True, null=True)
    return_stop = models.IntegerField(blank=True, null=True)
    return_flight = models.CharField(max_length=20, blank=True, null=True)
    return_class = models.CharField(max_length=20, blank=True, null=True)
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    base_fare = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    total_fare = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_flight_details_temp'


class CompetitorPolicyCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    logical_name = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_policy_criteria_master'


class CompetitorPolicyDetails(models.Model):
    policy_details_id = models.AutoField(primary_key=True)
    policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_policy_details'


class CompetitorPolicyMaster(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=100, blank=True, null=True)
    competitor_rule_master_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_policy_master'


class CompetitorRuleAirlineDetails(models.Model):
    competitor_rule_airline_id = models.AutoField(primary_key=True)
    competitor_rule_master_id = models.IntegerField(blank=True, null=True)
    airline_code = models.CharField(max_length=7, blank=True, null=True)
    flight_number = models.CharField(max_length=7, blank=True, null=True)
    departure_operator = models.CharField(max_length=15, blank=True, null=True)
    depart_time_range = models.CharField(max_length=15, blank=True, null=True)
    depart_fare_validity_type_id = models.CharField(max_length=15, blank=True, null=True)
    arrival_operator = models.CharField(max_length=15, blank=True, null=True)
    arrival_time_range = models.CharField(max_length=15, blank=True, null=True)
    arrival_fare_validity_type_id = models.CharField(max_length=15, blank=True, null=True)
    additive_factor = models.FloatField(blank=True, null=True)
    multiplicative_factor = models.FloatField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_rule_airline_details'


class CompetitorRuleCriteriaMaster(models.Model):
    competitor_criteria_id = models.AutoField(primary_key=True)
    competitor_criteria_name = models.CharField(max_length=50, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    show_status = models.CharField(max_length=1, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    criteria_logic_name = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_rule_criteria_master'


class CompetitorRuleDetails(models.Model):
    competitor_rule_id = models.AutoField(primary_key=True)
    competitor_rule_master_id = models.IntegerField(blank=True, null=True)
    competitor_criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    competitor_criteria_value = models.CharField(max_length=200, blank=True, null=True)
    fare_validity_type_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_rule_details'


class CompetitorRuleMaster(models.Model):
    competitor_rule_master_id = models.AutoField(primary_key=True)
    competitor_rule_name = models.CharField(max_length=20, blank=True, null=True)
    minimum_fare = models.FloatField(blank=True, null=True)
    maximum_fare = models.FloatField(blank=True, null=True)
    calculate_using = models.CharField(max_length=1, blank=True, null=True)
    include_connecting_flights = models.CharField(max_length=1, blank=True, null=True)
    include_hub = models.CharField(max_length=1, blank=True, null=True)
    fare_taken = models.CharField(max_length=3)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_rule_master'


class CompetitorTimeFrameDetails(models.Model):
    competitor_time_frame_id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=3, blank=True, null=True)
    destination = models.CharField(max_length=3, blank=True, null=True)
    carrier = models.CharField(max_length=5, blank=True, null=True)
    interval_value = models.IntegerField(blank=True, null=True)
    interval_type = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_time_frame_details'


class CompetitorViaFlightDetails(models.Model):
    competitor_via_flight_id = models.AutoField(primary_key=True)
    competitor_flight_id = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=3, blank=True, null=True)
    destination = models.CharField(max_length=3, blank=True, null=True)
    carrier = models.CharField(max_length=5, blank=True, null=True)
    flight = models.CharField(max_length=20, blank=True, null=True)
    travel_type = models.CharField(max_length=1, blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=20, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    base_fare = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    total_fare = models.FloatField(blank=True, null=True)
    segment_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitor_via_flight_details'


class ContractManagerDetails(models.Model):
    contract_detail_id = models.AutoField(primary_key=True)
    contract_manager_master_id = models.IntegerField(blank=True, null=True)
    contract_type = models.CharField(max_length=25)
    contract_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_manager_details'


class ContractManagerMaster(models.Model):
    contract_manager_master_id = models.AutoField(primary_key=True)
    contract_manager_name = models.CharField(max_length=100, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    activation_status = models.CharField(max_length=1, blank=True, null=True)
    default_status = models.CharField(max_length=1, blank=True, null=True)
    created_by = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField()
    updated_date = models.DateTimeField(blank=True, null=True)
    history_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'contract_manager_master'


class CorporateDetails(models.Model):
    corporate_id = models.AutoField(primary_key=True)
    corporate_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    corporate_name = models.CharField(max_length=100, blank=True, null=True)
    agent_name = models.CharField(max_length=52, blank=True, null=True)
    iata_code = models.CharField(max_length=36, blank=True, null=True)
    pcc_code = models.CharField(max_length=36, blank=True, null=True)
    airlines_code = models.CharField(max_length=3, blank=True, null=True)
    corporate_address = models.CharField(max_length=256, blank=True, null=True)
    fax = models.CharField(max_length=32, blank=True, null=True)
    office_number = models.CharField(max_length=32, blank=True, null=True)
    corporate_status = models.CharField(max_length=1)
    created_date = models.DateTimeField(blank=True, null=True)
    time_zone_interval = models.CharField(max_length=40, blank=True, null=True)
    time_zone_key = models.CharField(max_length=352, blank=True, null=True)
    pos_code = models.CharField(max_length=32, blank=True, null=True)
    customer_category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporate_details'


class CorporateExtjsReports(models.Model):
    report_id = models.SmallAutoField(primary_key=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    report_name = models.CharField(max_length=100, blank=True, null=True)
    report_file_name = models.CharField(max_length=100, blank=True, null=True)
    view_name = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.PositiveIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'corporate_extjs_reports'


class CorporateHomePageDetails(models.Model):
    corporate_id = models.IntegerField(blank=True, null=True)
    header_tpl_name = models.CharField(max_length=50, blank=True, null=True)
    footer_tpl_name = models.CharField(max_length=50, blank=True, null=True)
    landing_status = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporate_home_page_details'


class CorporateModuleSettings(models.Model):
    corporate_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    template_id = models.IntegerField(blank=True, null=True)
    target_template_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporate_module_settings'


class CorporateSalespersonMapping(models.Model):
    salesperson_mapping_id = models.AutoField(primary_key=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporate_salesperson_mapping'


class CorporateSubmenuSettings(models.Model):
    corporate_submenu_settings_id = models.AutoField(primary_key=True)
    corporate_id = models.IntegerField()
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    submenu_id = models.IntegerField()
    submenu_name = models.CharField(max_length=50, blank=True, null=True)
    submenu_link = models.CharField(max_length=100, blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)
    display_status = models.CharField(max_length=3, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporate_submenu_settings'


class CorporateTypeDetails(models.Model):
    corporate_type_id = models.AutoField(primary_key=True)
    corporate_type_name = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporate_type_details'


class CriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    criteria_logical_id = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    surcharge_status = models.CharField(max_length=1, blank=True, null=True)
    farerequote = models.CharField(max_length=1, blank=True, null=True)
    negotiateautopilot = models.CharField(db_column='negotiateAutoPilot', max_length=1, blank=True, null=True)  # Field name made lowercase.
    aggregatefunction = models.CharField(db_column='aggregateFunction', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autopilotpolicy = models.CharField(db_column='autoPilotPolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cancelpolicy = models.CharField(db_column='cancelPolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    timelinepolicy = models.CharField(db_column='timeLinePolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    negotiationpolicy = models.CharField(db_column='negotiationPolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nameupdatepolicy = models.CharField(db_column='nameUpdatePolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    farepolicy = models.CharField(db_column='farePolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    predictionpolicy = models.CharField(db_column='predictionPolicy', max_length=1)  # Field name made lowercase.
    fareclasspolicy = models.CharField(db_column='fareClassPolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    farebasispolicy = models.CharField(db_column='fareBasisPolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contractmanager = models.CharField(db_column='contractManager', max_length=1, blank=True, null=True)  # Field name made lowercase.
    baggagepolicy = models.CharField(db_column='baggagePolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.
    farerangepolicy = models.CharField(db_column='fareRangePolicy', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'criteria_master'


class CronEmailDetails(models.Model):
    cron_email_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    email_type = models.IntegerField()
    email_subject = models.CharField(max_length=50)
    sent_to = models.CharField(max_length=70)
    expiry_date = models.CharField(max_length=20)
    sent_date = models.DateTimeField()
    pnr = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cron_email_details'


class CronUpdatePnrDetails(models.Model):
    cron_update_pnr_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    series_request_id = models.IntegerField()
    pnr_updated_status = models.CharField(max_length=15)
    pnr_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cron_update_pnr_details'


class CronjobJobprogress(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_id = models.CharField(unique=True, max_length=150)
    task_id = models.CharField(max_length=150, blank=True, null=True)
    progress_percent = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    checkpoint_data = models.JSONField(blank=True, null=True)
    last_step = models.CharField(max_length=50, blank=True, null=True)
    last_processed_line = models.IntegerField()
    total_lines = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cronjob_jobprogress'


class CronjobScheduledtask(models.Model):
    id = models.BigAutoField(primary_key=True)
    enabled = models.IntegerField()
    crontab = models.ForeignKey('DjangoCeleryBeatCrontabschedule', models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey('DjangoCeleryBeatIntervalschedule', models.DO_NOTHING, blank=True, null=True)
    job = models.OneToOneField(CronjobJobprogress, models.DO_NOTHING)
    periodic_task = models.OneToOneField('DjangoCeleryBeatPeriodictask', models.DO_NOTHING, blank=True, null=True)
    task_path = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'cronjob_scheduledtask'


class CronjobTasklog(models.Model):
    id = models.BigAutoField(primary_key=True)
    task_id = models.CharField(max_length=150)
    message = models.TextField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    job = models.ForeignKey(CronjobJobprogress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cronjob_tasklog'


class CurrencyDetails(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_type = models.CharField(unique=True, max_length=3, blank=True, null=True)
    currency_symbol = models.CharField(max_length=5)
    exchange_rate = models.FloatField()
    decimal_precision = models.IntegerField()
    display_order = models.IntegerField()
    created_date = models.DateField()
    currency_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'currency_details'


class CurrencyMapping(models.Model):
    currency_mapping_id = models.AutoField(primary_key=True)
    pos_id = models.IntegerField()
    currency_id = models.IntegerField()
    country_code = models.CharField(max_length=3)
    display_in_request = models.CharField(max_length=1)
    display_in_payment = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'currency_mapping'


class CustomReportDetails(models.Model):
    custom_report_id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=30)
    report_type_language = models.CharField(max_length=100)
    based_on = models.CharField(max_length=100, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    display_status = models.CharField(max_length=1)
    default_selected = models.CharField(max_length=1)
    menu_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'custom_report_details'


class CustomReportValues(models.Model):
    custom_report_values_id = models.AutoField(primary_key=True)
    values_name = models.CharField(max_length=300)
    values_language = models.CharField(max_length=300)
    service_name = models.CharField(max_length=300)
    values_functionality = models.CharField(max_length=2)
    values_type = models.CharField(max_length=1)
    display_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'custom_report_values'


class CustomReportValuesMapping(models.Model):
    custom_report_values_mapping_id = models.AutoField(primary_key=True)
    custom_report_values_id = models.IntegerField()
    custom_report_id = models.IntegerField()
    header_id = models.IntegerField()
    parent_id = models.IntegerField(blank=True, null=True)
    corporate_id = models.IntegerField()
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    display_status = models.CharField(max_length=1)
    menu_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'custom_report_values_mapping'


class CustomerCategory(models.Model):
    customer_category_id = models.AutoField(primary_key=True)
    customer_category_name = models.CharField(max_length=10)
    status = models.CharField(max_length=1)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_category'


class CustomerInsightMaster(models.Model):
    customer_insight_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=6, blank=True, null=True)
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    login_id = models.CharField(max_length=100, blank=True, null=True)
    account_password = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_insight_master'


class DailyProductDetails(models.Model):
    daily_product_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(blank=True, null=True)
    booking_profile_id = models.IntegerField(blank=True, null=True)
    cabin_code = models.CharField(max_length=1, blank=True, null=True)
    date_departure = models.DateField(blank=True, null=True)
    time_departure = models.CharField(max_length=5, blank=True, null=True)
    time_arrival = models.CharField(max_length=5, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    current_bookings = models.IntegerField(blank=True, null=True)
    booking_fare = models.FloatField(blank=True, null=True)
    last_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_product_details'


class DiscountFareMapping(models.Model):
    discount_fare_id = models.AutoField(primary_key=True)
    discount_mapping_id = models.IntegerField(blank=True, null=True)
    group_size = models.IntegerField(blank=True, null=True)
    discount_fare = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discount_fare_mapping'


class DiscountMappingDetails(models.Model):
    discount_mapping_id = models.AutoField(primary_key=True)
    discount_matrix_id = models.IntegerField(blank=True, null=True)
    days_to_departure = models.IntegerField(blank=True, null=True)
    booked_load_factor = models.IntegerField(blank=True, null=True)
    forecast_load_factor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discount_mapping_details'


class DiscountMatrix(models.Model):
    discount_matrix_id = models.AutoField(primary_key=True)
    discount_matrix_name = models.CharField(max_length=50, blank=True, null=True)
    discount_matrix_type = models.CharField(max_length=5, blank=True, null=True)
    currency_type = models.CharField(max_length=5, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discount_matrix'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('SystemTUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoApschedulerDjangojob(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    next_run_time = models.DateTimeField(blank=True, null=True)
    job_state = models.TextField()

    class Meta:
        managed = False
        db_table = 'django_apscheduler_djangojob'


class DjangoApschedulerDjangojobexecution(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=50)
    run_time = models.DateTimeField()
    duration = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    finished = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    exception = models.CharField(max_length=1000, blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    job = models.ForeignKey(DjangoApschedulerDjangojob, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_apscheduler_djangojobexecution'
        unique_together = (('job', 'run_time'),)


class DjangoCeleryBeatClockedschedule(models.Model):
    clocked_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'


class DjangoCeleryBeatCrontabschedule(models.Model):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'


class DjangoCeleryBeatIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'


class DjangoCeleryBeatPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.IntegerField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.PositiveIntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, blank=True, null=True)
    one_off = models.IntegerField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.DO_NOTHING, blank=True, null=True)
    expire_seconds = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'


class DjangoCeleryBeatPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'


class DjangoCeleryBeatSolarschedule(models.Model):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)


class DjangoCeleryResultsChordcounter(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    sub_tasks = models.TextField()
    count = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'django_celery_results_chordcounter'


class DjangoCeleryResultsGroupresult(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    date_created = models.DateTimeField()
    date_done = models.DateTimeField()
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_groupresult'


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    worker = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField()
    periodic_task_name = models.CharField(max_length=255, blank=True, null=True)
    date_started = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoCronCronjoblock(models.Model):
    job_name = models.CharField(unique=True, max_length=200)
    locked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_cron_cronjoblock'


class DjangoCronCronjoblog(models.Model):
    code = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_success = models.IntegerField()
    message = models.TextField()
    ran_at_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_cron_cronjoblog'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EditUserHistory(models.Model):
    edit_user_history_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    updated_by = models.IntegerField()
    previous_user_details = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    user_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'edit_user_history'


class EmailSetting(models.Model):
    email_setting_id = models.AutoField(primary_key=True)
    email_type = models.CharField(max_length=200, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    setting_status = models.CharField(max_length=1, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_setting'


class EmailTemplateDetails(models.Model):
    email_template_id = models.AutoField(primary_key=True)
    corporate_id = models.IntegerField()
    group_id = models.IntegerField()
    email_setting_id = models.IntegerField()
    template_id = models.IntegerField()
    display_status = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_template_details'


class EmailTrackingDetails(models.Model):
    tracking_id = models.AutoField(primary_key=True)
    group_request_id = models.CharField(max_length=25, blank=True, null=True)
    email_type = models.IntegerField(blank=True, null=True)
    from_email_id = models.CharField(max_length=200, blank=True, null=True)
    to_email_id = models.CharField(max_length=200, blank=True, null=True)
    to_user_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_tracking_details'


class EmdDetails(models.Model):
    emd_id = models.AutoField(primary_key=True)
    pnr_payment_id = models.IntegerField()
    issued_document_number = models.CharField(max_length=25, blank=True, null=True)
    emd_amount = models.FloatField()
    issued_date = models.DateTimeField()
    emd_type = models.CharField(max_length=3, blank=True, null=True)
    emd_status = models.IntegerField()
    passenger_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emd_details'


class ExpiryTypeMaster(models.Model):
    expiry_type_id = models.AutoField(primary_key=True)
    expiry_type_name = models.CharField(max_length=20)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expiry_type_master'


class ExternalDataBatchDetails(models.Model):
    extenal_data_batch_id = models.AutoField(primary_key=True)
    external_data_type = models.CharField(max_length=2)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    data_count = models.IntegerField(blank=True, null=True)
    inserted_data_count = models.IntegerField(blank=True, null=True)
    file_uploaded_date = models.DateTimeField(blank=True, null=True)
    batch_date = models.DateTimeField(blank=True, null=True)
    batch_updated_date = models.DateTimeField(blank=True, null=True)
    batch_file_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'external_data_batch_details'


class FareClassCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    criteria_logical_id = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_class_criteria_master'


class FareClassMaster(models.Model):
    fare_class_id = models.AutoField(primary_key=True)
    policy_type_code = models.CharField(max_length=100, blank=True, null=True)
    fare_class_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_class_master'


class FareClassPolicyDetails(models.Model):
    fare_class_policy_details_id = models.AutoField(primary_key=True)
    fare_class_policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_class_policy_details'


class FareClassPolicyMaster(models.Model):
    fare_class_policy_id = models.AutoField(primary_key=True)
    fare_class_policy_name = models.CharField(max_length=100, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    discount_status = models.CharField(max_length=1, blank=True, null=True)
    surcharge_status = models.CharField(max_length=1)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_class_policy_master'


class FareDetails(models.Model):
    fare_id = models.AutoField(primary_key=True)
    series_flight_schedule_id = models.IntegerField(blank=True, null=True)
    series_via_flight_id = models.IntegerField(blank=True, null=True)
    adult_base_fare = models.FloatField()
    adult_tax = models.FloatField(blank=True, null=True)
    adult_discount = models.FloatField(blank=True, null=True)
    child_base_fare = models.FloatField()
    child_tax = models.FloatField(blank=True, null=True)
    child_discount = models.FloatField(blank=True, null=True)
    infant_base_fare = models.FloatField()
    infant_tax = models.FloatField(blank=True, null=True)
    meals_fare = models.FloatField()
    baggage_fare = models.FloatField()
    tiger_connect_fare = models.FloatField()
    baggage_code = models.CharField(max_length=5)
    fare_basis_code = models.CharField(max_length=15, blank=True, null=True)
    rule_number = models.CharField(max_length=4)
    fare_sequence = models.CharField(max_length=250, blank=True, null=True)
    journey_sell_key = models.TextField(blank=True, null=True)
    class_of_service = models.CharField(max_length=3, blank=True, null=True)
    fare_application_type = models.CharField(max_length=10)
    seat_availability = models.IntegerField()
    capacity = models.IntegerField()
    sold = models.IntegerField()
    seat_taken = models.IntegerField()
    service_adult_base_fare = models.FloatField(blank=True, null=True)
    service_adult_tax = models.FloatField(blank=True, null=True)
    service_child_base_fare = models.FloatField(blank=True, null=True)
    service_child_tax = models.FloatField(blank=True, null=True)
    service_infant_base_fare = models.FloatField(blank=True, null=True)
    service_infant_tax = models.FloatField(blank=True, null=True)
    ssi_seats_availability = models.IntegerField(blank=True, null=True)
    fare_type = models.CharField(max_length=5)
    chd_inf_basis_code = models.TextField()
    actual_fare = models.FloatField()
    fare_policy_details = models.TextField(blank=True, null=True)
    single_bid_price = models.IntegerField(blank=True, null=True)
    bid_price_seat_taken = models.IntegerField(blank=True, null=True)
    child_seat_taken = models.IntegerField(blank=True, null=True)
    group_booking_counter = models.IntegerField(blank=True, null=True)
    gst_data = models.CharField(max_length=60, blank=True, null=True)
    class_fare_type = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_details'


class FarePolicyDetails(models.Model):
    fare_policy_details_id = models.AutoField(primary_key=True)
    fare_policy_type = models.CharField(max_length=25)
    fare_policy_details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_policy_details'


class FareSuggestedMatrix(models.Model):
    fare_suggested_id = models.AutoField(primary_key=True)
    booking_profile_id = models.IntegerField(blank=True, null=True)
    days_to_departure = models.IntegerField(blank=True, null=True)
    booking_capacity = models.FloatField(blank=True, null=True)
    forecast_load_factor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_suggested_matrix'


class FareSuggestedMatrixValue(models.Model):
    fare_suggested_matrix_value_id = models.AutoField(primary_key=True)
    fare_suggested_id = models.IntegerField(blank=True, null=True)
    group_size = models.IntegerField(blank=True, null=True)
    static_fare = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_suggested_matrix_value'


class FareTypeMappingDetails(models.Model):
    fare_type_mapping_id = models.AutoField(primary_key=True)
    fare_type_matrix_id = models.IntegerField(blank=True, null=True)
    days_to_departure = models.IntegerField(blank=True, null=True)
    booked_load_factor = models.IntegerField(blank=True, null=True)
    forecast_load_factor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_type_mapping_details'


class FareTypeMaster(models.Model):
    fare_type_master_id = models.AutoField(primary_key=True)
    fare_type_name = models.CharField(max_length=50, blank=True, null=True)
    fare_type_alias = models.CharField(max_length=10, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_type_master'


class FareTypeMatrix(models.Model):
    fare_type_matrix_id = models.AutoField(primary_key=True)
    fare_type_matrix_name = models.CharField(max_length=100, blank=True, null=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_type_matrix'


class FareTypePolicyCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    criteria_logical_id = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_type_policy_criteria_master'


class FareTypePolicyDetails(models.Model):
    fare_type_policy_details_id = models.AutoField(primary_key=True)
    fare_type_policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField()
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_type_policy_details'


class FareTypePolicyMaster(models.Model):
    fare_type_policy_id = models.AutoField(primary_key=True)
    fare_type_policy_name = models.CharField(max_length=100, blank=True, null=True)
    fare_type_matrix_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    active_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_type_policy_master'


class FareTypeValueMapping(models.Model):
    fare_type_value_id = models.AutoField(primary_key=True)
    fare_type_mapping_id = models.IntegerField(blank=True, null=True)
    group_size = models.IntegerField(blank=True, null=True)
    fare_type_alias = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_type_value_mapping'


class FareValidityTypeDetails(models.Model):
    fare_validity_type_id = models.AutoField(primary_key=True)
    fare_validity_type = models.CharField(max_length=30, blank=True, null=True)
    fare_validity_values = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fare_validity_type_details'


class FieldTypeDetails(models.Model):
    field_type_id = models.AutoField(primary_key=True)
    condition_id = models.IntegerField()
    field_type_value = models.CharField(unique=True, max_length=15)
    field_type_name = models.CharField(max_length=20)
    field_type_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'field_type_details'


class FileProcessDataDetails(models.Model):
    file_process_data_id = models.AutoField(primary_key=True)
    request_info = models.JSONField(blank=True, null=True)
    unique_string = models.TextField()
    upload_request_type = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'file_process_data_details'


class FileProcessDetails(models.Model):
    file_process_id = models.AutoField(primary_key=True)
    file_upload_batch_id = models.IntegerField()
    upload_file_type = models.CharField(max_length=15)
    process_status = models.CharField(max_length=2)
    request_info = models.TextField()
    request_master_id = models.IntegerField()
    remarks = models.TextField()
    file_process_data_id = models.IntegerField()
    sheet_row = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'file_process_details'


class FileUploadBatchDetails(models.Model):
    file_upload_batch_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    uploaded_date = models.DateTimeField(blank=True, null=True)
    processed_date = models.DateTimeField(blank=True, null=True)
    process_type = models.CharField(max_length=2, blank=True, null=True)
    file_status = models.CharField(max_length=2, blank=True, null=True)
    uploaded_by = models.IntegerField(blank=True, null=True)
    backend_file_name = models.CharField(max_length=200, blank=True, null=True)
    parent_file_id = models.IntegerField(blank=True, null=True)
    requested_user_id = models.IntegerField(blank=True, null=True)
    additional_details = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file_upload_batch_details'


class FlightCabinMappingDetails(models.Model):
    flight_cabin_mapping_id = models.AutoField(primary_key=True)
    request_approved_flight_id = models.IntegerField(blank=True, null=True)
    via_flight_id = models.IntegerField(blank=True, null=True)
    fare_basis_code = models.CharField(max_length=20, blank=True, null=True)
    rule_number = models.CharField(max_length=10, blank=True, null=True)
    fare_sequence = models.CharField(max_length=50, blank=True, null=True)
    journey_sell_key = models.TextField(blank=True, null=True)
    class_of_service = models.CharField(max_length=5, blank=True, null=True)
    seat_availability = models.IntegerField(blank=True, null=True)
    seat_taken = models.IntegerField(blank=True, null=True)
    cabin_base_fare = models.FloatField(blank=True, null=True)
    adult_base_fare = models.FloatField(blank=True, null=True)
    adult_tax = models.FloatField(blank=True, null=True)
    adult_total_fare = models.FloatField(blank=True, null=True)
    child_base_fare = models.FloatField(blank=True, null=True)
    child_tax = models.FloatField(blank=True, null=True)
    child_total_fare = models.FloatField(blank=True, null=True)
    infant_base_fare = models.FloatField(blank=True, null=True)
    infant_tax = models.FloatField(blank=True, null=True)
    infant_total_fare = models.FloatField(blank=True, null=True)
    fare_type = models.CharField(max_length=5)
    chd_inf_basis_code = models.TextField()
    actual_fare = models.FloatField()
    cabin_child_fare = models.FloatField(blank=True, null=True)
    child_seat_taken = models.IntegerField(blank=True, null=True)
    class_fare_type = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight_cabin_mapping_details'


class FlightDiscountMappingDetails(models.Model):
    flight_discount_mapping_id = models.AutoField(primary_key=True)
    request_approved_flight_id = models.IntegerField(blank=True, null=True)
    via_flight_id = models.IntegerField()
    policy_id = models.IntegerField(blank=True, null=True)
    matrix_id = models.IntegerField(blank=True, null=True)
    matrix_type = models.CharField(max_length=5, blank=True, null=True)
    discount_fare = models.FloatField(blank=True, null=True)
    days_to_departure = models.IntegerField(blank=True, null=True)
    booked_load_factor = models.IntegerField(blank=True, null=True)
    policy_currency_type = models.CharField(max_length=5, blank=True, null=True)
    existing_adult_base_fare = models.FloatField(blank=True, null=True)
    existing_adult_tax = models.FloatField(blank=True, null=True)
    existing_adult_total_fare = models.FloatField(blank=True, null=True)
    existing_child_base_fare = models.FloatField(blank=True, null=True)
    existing_child_tax = models.FloatField(blank=True, null=True)
    existing_child_total_fare = models.FloatField(blank=True, null=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)
    forecast_load_factor = models.IntegerField(blank=True, null=True)
    child_discount_fare = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight_discount_mapping_details'


class FlightSalesPromoMapping(models.Model):
    flight_sales_promo_mapping_id = models.AutoField(primary_key=True)
    request_approved_flight_id = models.IntegerField()
    via_flight_id = models.IntegerField()
    sales_promo_policy_id = models.IntegerField()
    sales_promo_matrix_id = models.IntegerField()
    sales_promo_matrix_type = models.CharField(max_length=5)
    sales_promo_discount_percentage = models.FloatField()
    sales_promo_discount_fare = models.FloatField()
    sales_promo_currency_type = models.CharField(max_length=5)
    original_base_fare = models.FloatField()

    class Meta:
        managed = False
        db_table = 'flight_sales_promo_mapping'


class FlightScheduleDetails(models.Model):
    flight_schedule_id = models.AutoField(primary_key=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    origin_airport_code = models.CharField(max_length=3, blank=True, null=True)
    dest_airport_code = models.CharField(max_length=3, blank=True, null=True)
    airlines_code = models.CharField(max_length=7, blank=True, null=True)
    cabin = models.CharField(max_length=5, blank=True, null=True)
    arrival_time = models.CharField(max_length=5, blank=True, null=True)
    departure_time = models.CharField(max_length=5, blank=True, null=True)
    flight_number = models.CharField(max_length=5, blank=True, null=True)
    flight_jounary_time = models.CharField(max_length=5, blank=True, null=True)
    leg_count = models.IntegerField(blank=True, null=True)
    routing = models.CharField(max_length=11, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    series_weekdays = models.CharField(max_length=13, blank=True, null=True)
    displacement_fare = models.IntegerField(blank=True, null=True)
    booking_profile_fare = models.IntegerField(blank=True, null=True)
    competetor_fare = models.IntegerField(blank=True, null=True)
    base_fare = models.IntegerField(blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True)
    currency_type = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight_schedule_details'


class ForecastBatchDetails(models.Model):
    forecast_batch_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    data_count = models.IntegerField(blank=True, null=True)
    inserted_data_count = models.IntegerField(blank=True, null=True)
    file_uploaded_date = models.DateTimeField(blank=True, null=True)
    batch_date = models.DateTimeField(blank=True, null=True)
    batch_updated_date = models.DateTimeField(blank=True, null=True)
    batch_file_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forecast_batch_details'


class ForecastDataDetails(models.Model):
    forecast_data_id = models.AutoField(primary_key=True)
    forecast_batch_id = models.IntegerField(blank=True, null=True)
    carrier = models.CharField(max_length=5, blank=True, null=True)
    flight_number = models.CharField(max_length=20, blank=True, null=True)
    origin = models.CharField(max_length=3, blank=True, null=True)
    destination = models.CharField(max_length=3, blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    depature_time = models.TimeField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    cabin = models.CharField(max_length=2, blank=True, null=True)
    authorized_capacity = models.IntegerField(blank=True, null=True)
    forecasted_demand = models.IntegerField(blank=True, null=True)
    groups_booked = models.IntegerField(blank=True, null=True)
    stand_deviation = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=5, blank=True, null=True)
    avg_fare = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    forecasted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forecast_data_details'


class ForecastDataDetailsTemp(models.Model):
    forecast_data_id = models.AutoField(primary_key=True)
    forecast_batch_id = models.IntegerField()
    carrier = models.CharField(max_length=5, blank=True, null=True)
    flight_number = models.CharField(max_length=20, blank=True, null=True)
    origin = models.CharField(max_length=3, blank=True, null=True)
    destination = models.CharField(max_length=3, blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    depature_time = models.TimeField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    cabin = models.CharField(max_length=2, blank=True, null=True)
    authorized_capacity = models.IntegerField(blank=True, null=True)
    forecasted_demand = models.FloatField(blank=True, null=True)
    groups_booked = models.FloatField(blank=True, null=True)
    stand_deviation = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=5, blank=True, null=True)
    avg_fare = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    forecasted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forecast_data_details_temp'


class GenderTitleDetails(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender_type = models.CharField(max_length=20)
    gender_title_value = models.CharField(max_length=10)
    display_value = models.CharField(max_length=30, blank=True, null=True)
    view_status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'gender_title_details'


class GrmMenuDetails(models.Model):
    menu_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=100)
    menu_link = models.CharField(max_length=100)
    menu_status = models.CharField(max_length=1)
    created_date = models.DateField()
    updated_date = models.DateField()
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grm_menu_details'


class GrmMenuMappingDetails(models.Model):
    menu_mapping_id = models.AutoField(primary_key=True)
    parent_id = models.PositiveIntegerField()
    child_id = models.PositiveIntegerField()
    display_order = models.PositiveIntegerField()
    display_status = models.CharField(max_length=1)
    group_id = models.IntegerField()
    created_date = models.DateField()
    updated_date = models.DateField()
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grm_menu_mapping_details'


class GroupAllocationProfileDetails(models.Model):
    profile_id = models.AutoField(primary_key=True)
    profile_name = models.CharField(max_length=100, blank=True, null=True)
    profile_type = models.CharField(max_length=2, blank=True, null=True)
    currency_type = models.CharField(max_length=3, blank=True, null=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_allocation_profile_details'


class GroupAllocationSuggestedMatrix(models.Model):
    suggested_matrix_id = models.AutoField(primary_key=True)
    profile_id = models.IntegerField()
    group_start_pax = models.IntegerField()
    group_end_pax = models.IntegerField()
    group_pax_fare = models.FloatField()
    days_to_departure = models.IntegerField()
    booking_capacity = models.FloatField()
    forecast_load_factor = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'group_allocation_suggested_matrix'


class GroupCategoryList(models.Model):
    group_category_id = models.AutoField(primary_key=True)
    group_category_name = models.CharField(max_length=30, blank=True, null=True)
    group_category_code = models.CharField(max_length=2, blank=True, null=True)
    category_type = models.CharField(max_length=1, db_collation='utf8mb3_general_ci')
    group_category_status = models.CharField(max_length=1)
    display_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'group_category_list'


class GroupContractDetails(models.Model):
    group_contract_id = models.AutoField(primary_key=True)
    request_group_id = models.IntegerField()
    contract_manager_master_id = models.IntegerField()
    reference_id = models.IntegerField()
    updated_contract = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_contract_details'


class GroupDetails(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=30, blank=True, null=True)
    group_alias_name = models.CharField(unique=True, max_length=3, blank=True, null=True)
    corporate_type_id = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1)
    access_group_id = models.CharField(max_length=50)
    default_module = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'group_details'


class GroupchangeRequestDetails(models.Model):
    groupchange_request_id = models.AutoField(primary_key=True)
    groupchange_master_id = models.IntegerField(blank=True, null=True)
    request_id = models.IntegerField(blank=True, null=True)
    series_request_id = models.IntegerField(blank=True, null=True)
    parent_series_request_id = models.IntegerField(blank=True, null=True)
    request_approved_flight_id = models.IntegerField()
    current_no_of_adult = models.IntegerField(blank=True, null=True)
    current_no_of_child = models.IntegerField(blank=True, null=True)
    current_no_of_infant = models.IntegerField(blank=True, null=True)
    current_no_of_foc = models.IntegerField(blank=True, null=True)
    requested_no_of_adult = models.IntegerField(blank=True, null=True)
    requested_no_of_child = models.IntegerField(blank=True, null=True)
    requested_no_of_infant = models.IntegerField(blank=True, null=True)
    requested_no_of_foc = models.IntegerField(blank=True, null=True)
    approved_no_of_adult = models.IntegerField(blank=True, null=True)
    approved_no_of_child = models.IntegerField(blank=True, null=True)
    approved_no_of_infant = models.IntegerField(blank=True, null=True)
    approved_no_of_foc = models.IntegerField(blank=True, null=True)
    changed_no_of_adult = models.IntegerField(blank=True, null=True)
    changed_no_of_child = models.IntegerField(blank=True, null=True)
    changed_no_of_infant = models.IntegerField(blank=True, null=True)
    changed_no_of_foc = models.IntegerField(blank=True, null=True)
    infant_basefare = models.FloatField()
    infant_tax = models.FloatField()
    infant_taxbreakup = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groupchange_request_details'


class GroupchangeRequestMaster(models.Model):
    groupchange_master_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    parent_request_master_id = models.IntegerField(blank=True, null=True)
    resize_type_id = models.IntegerField()
    trip_type = models.CharField(max_length=5)
    pnr = models.CharField(max_length=11)
    request_user_id = models.IntegerField(blank=True, null=True)
    request_status = models.CharField(max_length=1, blank=True, null=True)
    user_remarks = models.TextField(blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)
    requested_date = models.DateTimeField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)
    responded_user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groupchange_request_master'


class HistoryDetails(models.Model):
    history_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    child_id = models.IntegerField()
    actioned_name = models.CharField(max_length=50)
    actioned_details = models.TextField()
    actioned_date = models.DateTimeField()
    actioned_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'history_details'


class HolidayList(models.Model):
    holiday_list_id = models.AutoField(primary_key=True)
    holiday_list_name = models.TextField(blank=True, null=True)
    non_business_days_list = models.CharField(max_length=30, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    country_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.CharField(max_length=1)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    enable_status = models.CharField(max_length=1)
    created_by = models.IntegerField()
    created_date = models.DateTimeField()
    roll_on = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'holiday_list'


class HolidayMappingList(models.Model):
    holiday_mapping_id = models.AutoField(primary_key=True)
    holiday_list_id = models.IntegerField(blank=True, null=True)
    holiday_date = models.DateField(blank=True, null=True)
    holiday_desc = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=1)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'holiday_mapping_list'


class HubAirportDetails(models.Model):
    hub_airport_id = models.AutoField(primary_key=True)
    airport_code = models.CharField(max_length=3, blank=True, null=True)
    mapped_airport_code = models.CharField(max_length=3, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hub_airport_details'


class IpRestrictionDetails(models.Model):
    restriction_id = models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=40, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=4, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    history_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ip_restriction_details'


class IssueCategoryDetails(models.Model):
    issue_category_id = models.AutoField(primary_key=True)
    issue_category_name = models.CharField(max_length=200, blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    parent_category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue_category_details'


class IssueCronEmailDetails(models.Model):
    issue_cron_email_id = models.AutoField(primary_key=True)
    issue_id = models.IntegerField()
    issue_type = models.IntegerField()
    email_subject = models.CharField(max_length=50)
    sent_to = models.CharField(max_length=70)
    sent_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'issue_cron_email_details'


class IssueDetails(models.Model):
    issue_details_id = models.AutoField(primary_key=True)
    issue_category_id = models.IntegerField(blank=True, null=True)
    issue_subcategory_id = models.IntegerField(blank=True, null=True)
    severity_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    issue_status_id = models.IntegerField(blank=True, null=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=25, blank=True, null=True)
    last_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue_details'


class IssueSeverityDetails(models.Model):
    severity_id = models.AutoField(primary_key=True)
    severity_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue_severity_details'


class IssueStatusDetails(models.Model):
    issue_status_id = models.AutoField(primary_key=True)
    issue_status_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue_status_details'


class IssueSubcategoryDetails(models.Model):
    issue_subcategory_id = models.AutoField(primary_key=True)
    issue_subcategory_name = models.CharField(max_length=200, blank=True, null=True)
    issue_category_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    parent_category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue_subcategory_details'


class LoadFactorTypeDetails(models.Model):
    load_factor_type_id = models.AutoField(primary_key=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)
    load_factor_type_name = models.CharField(max_length=100, blank=True, null=True)
    discount_status = models.CharField(max_length=1, blank=True, null=True)
    static_fare_status = models.CharField(max_length=1, blank=True, null=True)
    fare_type_status = models.CharField(max_length=1, blank=True, null=True)
    surcharge_status = models.CharField(max_length=1, blank=True, null=True)
    group_allocation_fare_matrix = models.CharField(max_length=1)
    baggage_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'load_factor_type_details'


class LoginVerification(models.Model):
    login_verification_id = models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    email_id = models.CharField(max_length=100, blank=True, null=True)
    requested_date = models.DateTimeField(blank=True, null=True)
    verification_status = models.CharField(max_length=2, blank=True, null=True)
    additional_info = models.TextField()

    class Meta:
        managed = False
        db_table = 'login_verification'


class ManipulateHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    module_id = models.IntegerField()
    history_type = models.CharField(max_length=50)
    history_type_id = models.IntegerField()
    user_id = models.IntegerField()
    ip_address = models.CharField(max_length=40)
    date = models.DateTimeField()
    history_value = models.TextField()
    action_type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'manipulate_history'


class MealCodeDetails(models.Model):
    meal_id = models.AutoField(primary_key=True)
    meal_description = models.CharField(max_length=250, blank=True, null=True)
    meal_code = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'meal_code_details'


class MenuMAppDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    app_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'menu_m_app_details'


class MenuMComponents(models.Model):
    id = models.BigAutoField(primary_key=True)
    component = models.CharField(max_length=50)
    r_app = models.ForeignKey(MenuMAppDetails, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menu_m_components'


class MenuMLayouts(models.Model):
    id = models.BigAutoField(primary_key=True)
    layout = models.CharField(max_length=50)
    r_app = models.ForeignKey(MenuMAppDetails, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menu_m_layouts'


class MenuMMenu(models.Model):
    id = models.BigAutoField(primary_key=True)
    menu_code = models.CharField(max_length=50)
    path = models.CharField(max_length=200)
    icon_name = models.CharField(max_length=100)
    r_app = models.ForeignKey(MenuMAppDetails, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menu_m_menu'


class MenuMRouteMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    default = models.IntegerField()
    display_status = models.CharField(max_length=1)
    r_component = models.ForeignKey(MenuMComponents, models.DO_NOTHING)
    r_group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    r_layout = models.ForeignKey(MenuMLayouts, models.DO_NOTHING)
    r_route = models.ForeignKey('MenuMRoutes', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menu_m_route_mapping'


class MenuMRoutes(models.Model):
    id = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=200)
    permission_id = models.CharField(max_length=50, blank=True, null=True)
    r_app = models.ForeignKey(MenuMAppDetails, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menu_m_routes'


class MenuTMenuMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    display_order = models.IntegerField()
    r_child = models.ForeignKey(MenuMMenu, models.DO_NOTHING,        related_name='parent_mappings'  # <-- Add this unique name
, blank=True, null=True)
    r_group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    r_parent = models.ForeignKey(MenuMMenu, models.DO_NOTHING,        related_name='child_mappings'   # <-- Add this unique name
)

    class Meta:
        managed = False
        db_table = 'menu_t_menu_mapping'


class MessageAttachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    message_id = models.IntegerField(blank=True, null=True)
    attachment_name = models.CharField(max_length=200, blank=True, null=True)
    attachment_path = models.CharField(max_length=200, blank=True, null=True)
    upload_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_attachment'


class MessageDetails(models.Model):
    message_id = models.AutoField(primary_key=True)
    reference_id = models.IntegerField(blank=True, null=True)
    support_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    status_id = models.IntegerField(blank=True, null=True)
    message_subject = models.TextField(db_collation='utf8mb3_general_ci', blank=True, null=True)
    message_content = models.TextField(db_collation='utf8mb3_general_ci', blank=True, null=True)
    attachment = models.CharField(max_length=1, blank=True, null=True)
    base_message_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    satisfaction_status = models.CharField(max_length=1, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_details'


class ModuleDetails(models.Model):
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'module_details'


class ModuleGroupMapping(models.Model):
    module_group_id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    template_id = models.IntegerField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    display_status = models.CharField(max_length=3, blank=True, null=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'module_group_mapping'


class ModuleGroupStdtplMapping(models.Model):
    module_id = models.IntegerField(blank=True, null=True)
    std_tpl_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    class_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'module_group_stdtpl_mapping'


class NegotiationCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    criteria_logical_id = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'negotiation_criteria_master'


class NegotiationPolicyDetails(models.Model):
    negotiation_policy_details_id = models.AutoField(primary_key=True)
    negotiation_policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'negotiation_policy_details'


class NegotiationPolicyMaster(models.Model):
    negotiation_policy_id = models.AutoField(primary_key=True)
    negotiation_policy_name = models.CharField(max_length=100, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    negotiation_status = models.CharField(max_length=1, blank=True, null=True)
    negotiation_limit = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'negotiation_policy_master'


class NegotiationRequestDetails(models.Model):
    negotiation_details_id = models.AutoField(primary_key=True)
    negotiation_fileupload_id = models.IntegerField(blank=True, null=True)
    request_master_id = models.IntegerField()
    transaction_id = models.IntegerField()
    pax_count = models.IntegerField(blank=True, null=True)
    total_base_fare = models.FloatField(blank=True, null=True)
    mr_rate = models.IntegerField(blank=True, null=True)
    tandc_type = models.CharField(max_length=3, blank=True, null=True)
    analyst_comments = models.TextField(blank=True, null=True)
    fare_status = models.CharField(max_length=1, blank=True, null=True)
    process_status = models.CharField(max_length=1, blank=True, null=True)
    processed_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'negotiation_request_details'


class NoteDetails(models.Model):
    note_details_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    message = models.TextField()
    posted_by = models.IntegerField(blank=True, null=True)
    posted_on = models.DateTimeField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'note_details'


class NoteReadStatusDetails(models.Model):
    note_read_status_id = models.AutoField(primary_key=True)
    note_details_id = models.IntegerField()
    note_user_mapping_id = models.IntegerField()
    user_id = models.IntegerField()
    read_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'note_read_status_details'


class NoteUserMappingDetails(models.Model):
    note_user_mapping_id = models.AutoField(primary_key=True)
    note_details_id = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'note_user_mapping_details'


class OperatorMaster(models.Model):
    operator_id = models.AutoField(primary_key=True)
    operator_name = models.CharField(max_length=15, blank=True, null=True)
    logical_value = models.CharField(max_length=15, blank=True, null=True)
    operator_type = models.CharField(max_length=3, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operator_master'


class OtherCodeDetails(models.Model):
    other_id = models.AutoField(primary_key=True)
    other_description = models.CharField(max_length=250, db_collation='latin1_swedish_ci')
    other_code = models.CharField(max_length=250, db_collation='latin1_swedish_ci')

    class Meta:
        managed = False
        db_table = 'other_code_details'


class PackageDetails(models.Model):
    package_id = models.AutoField(primary_key=True)
    pnr_blocking_id = models.IntegerField()
    adult = models.IntegerField()
    child = models.IntegerField()
    infant = models.IntegerField()
    status = models.CharField(max_length=1)
    parent_package_id = models.IntegerField()
    ref_package_id = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.IntegerField()
    passenger_mapping = models.JSONField()

    class Meta:
        managed = False
        db_table = 'package_details'


class PassengerDetails(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    request_approved_flight_id = models.IntegerField(blank=True, null=True)
    series_request_id = models.IntegerField(blank=True, null=True)
    name_number = models.CharField(max_length=10, blank=True, null=True)
    pnr = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=16, blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    middle_name = models.CharField(max_length=35, blank=True, null=True)
    age = models.CharField(max_length=16, blank=True, null=True)
    pax_email_id = models.CharField(max_length=32, blank=True, null=True)
    pax_mobile_number = models.CharField(max_length=16, blank=True, null=True)
    pax_employee_code = models.CharField(max_length=16, blank=True, null=True)
    pax_employee_id = models.CharField(max_length=16, blank=True, null=True)
    passenger_type = models.CharField(max_length=10, blank=True, null=True)
    id_proof = models.CharField(max_length=16, blank=True, null=True)
    id_proof_number = models.CharField(max_length=16, blank=True, null=True)
    sex = models.CharField(max_length=16, blank=True, null=True)
    dob = models.CharField(max_length=16, blank=True, null=True)
    citizenship = models.CharField(max_length=16, blank=True, null=True)
    passport_no = models.CharField(max_length=16, blank=True, null=True)
    date_of_issue = models.CharField(max_length=256, blank=True, null=True)
    date_of_expiry = models.CharField(max_length=256, blank=True, null=True)
    submitted_date = models.DateTimeField(blank=True, null=True)
    traveller_number = models.CharField(max_length=16, blank=True, null=True)
    frequent_flyer_number = models.CharField(max_length=16, blank=True, null=True)
    passport_issued_place = models.CharField(max_length=80, blank=True, null=True)
    meal_code = models.CharField(max_length=6, blank=True, null=True)
    place_of_birth = models.CharField(max_length=40, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    additional_details = models.TextField()
    passenger_status = models.CharField(max_length=2)
    foc_status = models.CharField(max_length=1)
    parent_pax_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger_details'


class PassengerMaster(models.Model):
    passenger_master_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=10)
    time_validity = models.DateTimeField(blank=True, null=True)
    passenger_status = models.IntegerField(blank=True, null=True)
    requested_date = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    passenger_remarks = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger_master'


class PassengerPnrMapping(models.Model):
    passenger_pnr_id = models.AutoField(primary_key=True)
    pnr_id = models.IntegerField(blank=True, null=True)
    passenger_id = models.IntegerField(blank=True, null=True)
    ticketing_id = models.IntegerField()
    submitted_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger_pnr_mapping'


class PassengerTemplateConditionDetails(models.Model):
    template_condition_id = models.AutoField(primary_key=True)
    condition_name = models.CharField(max_length=20, db_collation='utf8mb3_general_ci', blank=True, null=True)
    condition_type = models.CharField(max_length=20, db_collation='utf8mb3_general_ci', blank=True, null=True)
    display_status = models.CharField(max_length=5, db_collation='utf8mb3_general_ci', blank=True, null=True)
    condition_logical_name = models.CharField(max_length=20, db_collation='utf8mb3_general_ci', blank=True, null=True)
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'passenger_template_condition_details'


class PassengerTemplateConditionMapping(models.Model):
    passenger_template_condition_mapping_id = models.AutoField(primary_key=True)
    passenger_template_field_mapping_id = models.IntegerField()
    template_condition_id = models.IntegerField()
    template_condition_value = models.CharField(max_length=20, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger_template_condition_mapping'


class PassengerTemplateCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    criteria_type = models.CharField(max_length=3, db_collation='utf8mb3_general_ci')
    display_status = models.CharField(max_length=1, db_collation='utf8mb3_general_ci', blank=True, null=True)
    criteria_logical_id = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger_template_criteria_master'


class PassengerTemplateDetails(models.Model):
    passenger_template_id = models.AutoField(primary_key=True)
    passenger_template_name = models.CharField(max_length=50, db_collation='utf8mb3_general_ci', blank=True, null=True)
    status = models.CharField(max_length=5, db_collation='utf8mb3_general_ci', blank=True, null=True)
    created_by = models.IntegerField()
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'passenger_template_details'


class PassengerTemplateFieldConditionMapping(models.Model):
    passenger_template_field_condition_mapping_id = models.AutoField(primary_key=True)
    template_field_id = models.IntegerField()
    template_condition_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'passenger_template_field_condition_mapping'


class PassengerTemplateFieldDetails(models.Model):
    template_field_id = models.AutoField(primary_key=True)
    template_field_name = models.CharField(max_length=25, blank=True, null=True)
    template_field_type = models.CharField(max_length=10, db_collation='utf8mb3_general_ci', blank=True, null=True)
    display_status = models.CharField(max_length=5, db_collation='utf8mb3_general_ci', blank=True, null=True)
    template_logical_name = models.CharField(max_length=25, blank=True, null=True)
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'passenger_template_field_details'


class PassengerTemplateFieldMapping(models.Model):
    passenger_template_field_mapping_id = models.AutoField(primary_key=True)
    passenger_template_id = models.IntegerField()
    template_field_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'passenger_template_field_mapping'


class PassengerTemplatePolicyDetails(models.Model):
    policy_details_id = models.AutoField(primary_key=True)
    policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger_template_policy_details'


class PassengerTemplatePolicyMaster(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    passenger_template_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField()
    created_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'passenger_template_policy_master'


class PaxTypeDetails(models.Model):
    pax_type_id = models.AutoField(primary_key=True)
    pax_type_value = models.CharField(max_length=10)
    display_value = models.CharField(max_length=50, blank=True, null=True)
    view_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'pax_type_details'


class PaymentAdditionalChargeDetails(models.Model):
    payment_charge_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    ssr_list_id = models.IntegerField()
    ssr_master_id = models.IntegerField(blank=True, null=True)
    pnr_blocking_id = models.IntegerField()
    additional_amount = models.FloatField()
    pnr_payment_id = models.IntegerField(blank=True, null=True)
    paid_status = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    modified_details = models.TextField(blank=True, null=True)
    series_group_id = models.IntegerField(blank=True, null=True)
    ssr_status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'payment_additional_charge_details'


class PaymentDetails(models.Model):
    payment_id = models.AutoField(primary_key=True)
    response_code = models.IntegerField(blank=True, null=True)
    response_message = models.CharField(max_length=64, blank=True, null=True)
    transaction_type_id = models.IntegerField(blank=True, null=True)
    request_source = models.CharField(max_length=25, blank=True, null=True)
    request_source_id = models.IntegerField(blank=True, null=True)
    payment_amount = models.FloatField(blank=True, null=True)
    payment_status = models.CharField(max_length=3, blank=True, null=True)
    payment_mode = models.CharField(max_length=25, blank=True, null=True)
    paid_by = models.IntegerField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_details'


class PaymentFailedHistory(models.Model):
    payment_failed_id = models.AutoField(primary_key=True)
    payment_master_id = models.IntegerField(blank=True, null=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=10, blank=True, null=True)
    amount_to_pay = models.FloatField(blank=True, null=True)
    paid_by = models.IntegerField(blank=True, null=True)
    card_type = models.CharField(max_length=6, blank=True, null=True)
    card_number = models.CharField(max_length=200, blank=True, null=True)
    cvv_number = models.CharField(max_length=50, blank=True, null=True)
    card_name_holder = models.CharField(max_length=150, blank=True, null=True)
    expirydate_year = models.CharField(max_length=25, blank=True, null=True)
    expirydate_month = models.CharField(max_length=25, blank=True, null=True)
    pnr_status = models.CharField(max_length=20, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    card_authorization = models.CharField(max_length=20, blank=True, null=True)
    error = models.CharField(max_length=300, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_failed_history'


class PaymentMaster(models.Model):
    payment_master_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    payment_percentage = models.FloatField(blank=True, null=True)
    percentage_amount = models.FloatField(blank=True, null=True)
    exchange_rate = models.FloatField()
    payment_validity_date = models.DateTimeField(blank=True, null=True)
    payment_requested_date = models.DateTimeField(blank=True, null=True)
    payment_remarks = models.CharField(max_length=300, db_collation='utf8mb3_general_ci', blank=True, null=True)
    payment_status = models.IntegerField(blank=True, null=True)
    paid_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_master'


class PaymentPendingHistory(models.Model):
    payment_pending_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    payment_master_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=10, blank=True, null=True)
    payment_requested_amount = models.FloatField(blank=True, null=True)
    card_type = models.CharField(max_length=10, blank=True, null=True)
    card_last_digit = models.CharField(max_length=6, blank=True, null=True)
    corn_count = models.IntegerField(blank=True, null=True)
    paid_by = models.IntegerField(blank=True, null=True)
    payment_status = models.CharField(max_length=15, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    last_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_pending_history'


class PaymentRequestDetails(models.Model):
    payment_request_id = models.AutoField(primary_key=True)
    transaction_id = models.IntegerField()
    payment_validity = models.IntegerField()
    payment_validity_type = models.IntegerField()
    payment_expiry_type = models.IntegerField()
    payment_expiry_date = models.DateTimeField()
    payment_percentage = models.FloatField()
    paid_status = models.CharField(max_length=20)
    payment_absolute_amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'payment_request_details'


class PaymentRequestDetailsHistory(models.Model):
    payment_request_history_id = models.AutoField(primary_key=True)
    payment_request_id = models.IntegerField(blank=True, null=True)
    transaction_id = models.IntegerField()
    payment_validity = models.IntegerField()
    payment_validity_type = models.IntegerField()
    payment_expiry_type = models.IntegerField()
    payment_expiry_date = models.DateTimeField()
    payment_percentage = models.FloatField()
    paid_status = models.CharField(max_length=20)
    payment_absolute_amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'payment_request_details_history'


class PaymentTransactionDetails(models.Model):
    payment_transaction_id = models.AutoField(primary_key=True)
    payment_master_id = models.IntegerField(blank=True, null=True)
    payment_type_id = models.IntegerField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.IntegerField(blank=True, null=True)
    paid_date = models.DateField(blank=True, null=True)
    payment_received_by = models.IntegerField(blank=True, null=True)
    payment_transaction_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_transaction_details'


class PaymentTypeDetails(models.Model):
    payment_type_id = models.AutoField(primary_key=True)
    payment_type_code = models.CharField(max_length=10, blank=True, null=True)
    payment_type_description = models.CharField(max_length=25, blank=True, null=True)
    parent_payment_type_id = models.IntegerField()
    display_status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'payment_type_details'


class PenalityTypeMaster(models.Model):
    penality_type_id = models.AutoField(primary_key=True)
    penality_type_code = models.CharField(max_length=5, blank=True, null=True)
    penality_type_name = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=40, blank=True, null=True)
    config = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'penality_type_master'


class PnrBlockingDetails(models.Model):
    pnr_blocking_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    request_approved_flight_id = models.IntegerField()
    via_flight_id = models.IntegerField()
    pnr = models.CharField(max_length=10)
    no_of_adult = models.IntegerField()
    no_of_child = models.IntegerField()
    no_of_infant = models.IntegerField()
    no_of_foc = models.IntegerField()
    pnr_amount = models.FloatField()
    price_quote_at = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pnr_blocking_details'


class PnrDetails(models.Model):
    pnr_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    request_id = models.IntegerField(blank=True, null=True)
    series_request_id = models.IntegerField(blank=True, null=True)
    pnr_number = models.CharField(max_length=50, blank=True, null=True)
    pnr_status = models.IntegerField(blank=True, null=True)
    ticket_type = models.CharField(max_length=10)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pnr_details'


class PnrPaymentDetails(models.Model):
    pnr_payment_id = models.AutoField(primary_key=True)
    payment_master_id = models.IntegerField()
    pnr = models.CharField(max_length=10)
    paid_amount = models.FloatField()
    paid_date = models.DateTimeField()
    group_pax_paid = models.CharField(max_length=100, blank=True, null=True)
    group_pax_percent = models.FloatField(blank=True, null=True)
    payment_status = models.CharField(max_length=20)
    payment_service_id = models.CharField(max_length=100)
    topup_id = models.IntegerField(blank=True, null=True)
    pnr_payment_validity_date = models.DateTimeField(blank=True, null=True)
    request_timeline_id = models.IntegerField(blank=True, null=True)
    pnr_percentage_amount = models.FloatField(blank=True, null=True)
    convinence_charge = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pnr_payment_details'


class PnrPaymentTransactions(models.Model):
    pnr_payment_transaction_id = models.AutoField(primary_key=True)
    pnr_payment_id = models.IntegerField(blank=True, null=True)
    payment_transaction_id = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    exchange_rate = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    original_requested_amount = models.FloatField()
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pnr_payment_transactions'


class PnrRemainderMailDetails(models.Model):
    pnr_remainder_mail_id = models.AutoField(primary_key=True)
    pnr = models.CharField(max_length=7, blank=True, null=True)
    pnr_action = models.CharField(max_length=10, blank=True, null=True)
    to_mail_id = models.CharField(max_length=400, blank=True, null=True)
    cc_mail_id = models.CharField(max_length=400, blank=True, null=True)
    from_queue_no = models.IntegerField()
    to_queue_no = models.IntegerField()
    user_remark = models.CharField(max_length=500, blank=True, null=True)
    pnr_remarks = models.CharField(max_length=200, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    action_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    action_by = models.IntegerField(blank=True, null=True)
    pos = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pnr_remainder_mail_details'


class PolicyDetails(models.Model):
    policy_details_id = models.AutoField(primary_key=True)
    policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField()
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_details'


class PolicyGroupMapping(models.Model):
    policy_group_mapping_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    series_group_id = models.IntegerField(blank=True, null=True)
    request_approved_flight_id = models.IntegerField(blank=True, null=True)
    via_flight_id = models.IntegerField(blank=True, null=True)
    request_master_history_id = models.IntegerField(blank=True, null=True)
    policy_mapping_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_group_mapping'


class PolicyMapping(models.Model):
    policy_mapping_id = models.AutoField(primary_key=True)
    policy_type_id = models.IntegerField(blank=True, null=True)
    policy_id = models.IntegerField(blank=True, null=True)
    matrix_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_mapping'


class PolicyMaster(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=100, blank=True, null=True)
    discount_matrix_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    active_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_master'


class PolicyTypeDetails(models.Model):
    policy_type_id = models.AutoField(primary_key=True)
    policy_type_code = models.CharField(max_length=5, blank=True, null=True)
    policy_type_name = models.CharField(max_length=100, blank=True, null=True)
    policy_type_value = models.CharField(max_length=100, blank=True, null=True)
    matrix_table_name = models.CharField(max_length=100, blank=True, null=True)
    policy_type_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'policy_type_details'


class PosDetails(models.Model):
    pos_id = models.AutoField(primary_key=True)
    pos_code = models.CharField(max_length=8, blank=True, null=True)
    pos_city = models.CharField(max_length=40, blank=True, null=True)
    pos_country = models.CharField(max_length=2, blank=True, null=True)
    pos_region = models.CharField(max_length=40, blank=True, null=True)
    pos_office_id = models.CharField(max_length=20, blank=True, null=True)
    station_number = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pos_details'


class PosUserMapping(models.Model):
    pos_user_id = models.AutoField(primary_key=True)
    pos_code = models.CharField(max_length=8, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    active_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'pos_user_mapping'


class ProductDetails(models.Model):
    product_id = models.AutoField(primary_key=True)
    booking_profile_id = models.IntegerField(blank=True, null=True)
    airline_code = models.CharField(max_length=2, blank=True, null=True)
    origin_airport_code = models.CharField(max_length=3, blank=True, null=True)
    dest_airport_code = models.CharField(max_length=3, blank=True, null=True)
    flight_number = models.CharField(max_length=8, blank=True, null=True)
    time_departure = models.CharField(max_length=5, blank=True, null=True)
    time_arrival = models.CharField(max_length=5, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    fare = models.FloatField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    day_preference = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_details'


class ProofDetails(models.Model):
    proof_id = models.AutoField(primary_key=True)
    proof_type = models.CharField(max_length=40, blank=True, null=True)
    adult_status = models.CharField(max_length=2, blank=True, null=True)
    child_status = models.CharField(max_length=2, blank=True, null=True)
    infant_status = models.CharField(max_length=2, blank=True, null=True)
    proof_code = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proof_details'


class PwdUpgrade(models.Model):
    pwd_upgrade_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    old_pwd = models.CharField(max_length=40)
    new_pwd = models.CharField(max_length=90)
    updated_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pwd_upgrade'


class QueueBatchDetails(models.Model):
    queue_batch_id = models.AutoField(primary_key=True)
    total_pnr_count = models.IntegerField(blank=True, null=True)
    processed_pnr_count = models.IntegerField(blank=True, null=True)
    batch_date = models.DateTimeField(blank=True, null=True)
    batch_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'queue_batch_details'


class QueuePnrDetails(models.Model):
    queue_pnr_id = models.AutoField(primary_key=True)
    queue_batch_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=10, blank=True, null=True)
    locator = models.CharField(max_length=5, blank=True, null=True)
    placed_by = models.CharField(max_length=5, blank=True, null=True)
    pnr_created_datetime = models.DateTimeField(blank=True, null=True)
    pnr_status = models.CharField(max_length=1, blank=True, null=True)
    pnr_remarks = models.CharField(max_length=300, blank=True, null=True)
    request_status = models.IntegerField(blank=True, null=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    queue_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'queue_pnr_details'


class RegistrationPaymentDetails(models.Model):
    registration_payment_id = models.AutoField(primary_key=True)
    corporate = models.ForeignKey(CorporateDetails, models.DO_NOTHING)
    user = models.ForeignKey('UserDetails', models.DO_NOTHING)
    currency = models.ForeignKey(CurrencyDetails, models.DO_NOTHING)
    amount = models.FloatField()
    payment_type_id = models.IntegerField()
    pnr_blocking_id = models.IntegerField()
    emd_id = models.IntegerField()
    status = models.ForeignKey('StatusDetails', models.DO_NOTHING)
    paid_on = models.DateTimeField()
    approved_by = models.IntegerField()
    approved_on = models.DateTimeField()
    other = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registration_payment_details'


class RemarksDetails(models.Model):
    remarks_id = models.AutoField(primary_key=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    remarks_source = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'remarks_details'


class ReportNavigation(models.Model):
    menu_id = models.AutoField(primary_key=True)
    menu_type = models.CharField(max_length=30)
    route = models.CharField(max_length=50, blank=True, null=True)
    display_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'report_navigation'


class RequestApprovedFareDetails(models.Model):
    request_approved_fare_id = models.AutoField(primary_key=True)
    request_approved_flight_id = models.IntegerField(blank=True, null=True)
    request_approved_flight_history_id = models.IntegerField(blank=True, null=True)
    approved_fare = models.CharField(max_length=60)
    approved_tax = models.TextField(blank=True, null=True)
    approved_discount = models.CharField(max_length=120, blank=True, null=True)
    approved_fare_details = models.TextField(blank=True, null=True)
    approved_policy_details = models.TextField(blank=True, null=True)
    via_flight_details = models.TextField(blank=True, null=True)
    fare_filter_method = models.CharField(max_length=5, blank=True, null=True)
    request_timeline_id = models.CharField(max_length=60)
    cancel_policy_id = models.CharField(max_length=60)
    fare_accepted_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'request_approved_fare_details'


class RequestApprovedFlightDetails(models.Model):
    request_approved_flight_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    transaction_master_id = models.IntegerField(blank=True, null=True)
    request_id = models.IntegerField()
    request_details_history_id = models.IntegerField(blank=True, null=True)
    series_request_id = models.IntegerField()
    series_request_history_id = models.IntegerField(blank=True, null=True)
    request_option_id = models.IntegerField(blank=True, null=True)
    airline_code = models.CharField(max_length=5, blank=True, null=True)
    flight_code = models.CharField(max_length=10, blank=True, null=True)
    flight_number = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(max_length=5, blank=True, null=True)
    destination = models.CharField(max_length=5, blank=True, null=True)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    dep_time = models.CharField(max_length=6)
    arr_time = models.CharField(max_length=6)
    journey_time = models.CharField(max_length=6)
    fare_filter_method = models.CharField(max_length=30, blank=True, null=True)
    no_of_adult = models.IntegerField(blank=True, null=True)
    no_of_child = models.IntegerField(blank=True, null=True)
    no_of_infant = models.IntegerField(blank=True, null=True)
    displacement_cost = models.FloatField()
    base_fare = models.FloatField()
    tax = models.FloatField()
    fare_passenger = models.FloatField()
    tax_breakup = models.CharField(max_length=300, blank=True, null=True)
    child_base_fare = models.FloatField()
    child_tax = models.FloatField()
    child_tax_breakup = models.CharField(max_length=300, blank=True, null=True)
    infant_base_fare = models.FloatField()
    infant_tax = models.FloatField()
    infant_tax_breakup = models.CharField(max_length=300, blank=True, null=True)
    baggauge_fare = models.FloatField(blank=True, null=True)
    meals_fare = models.FloatField(blank=True, null=True)
    baggage_code = models.CharField(max_length=5)
    meals_code = models.CharField(max_length=6, blank=True, null=True)
    stops = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField()
    sold = models.IntegerField()
    seat_availability = models.IntegerField()
    discount_fare = models.FloatField(blank=True, null=True)
    child_discount_fare = models.FloatField(blank=True, null=True)
    sales_promo_discount_fare = models.FloatField()
    adjusted_amount = models.FloatField(blank=True, null=True)
    accepted_flight_status = models.CharField(max_length=1)
    displacement_fare_remarks = models.TextField(blank=True, null=True)
    surcharge = models.FloatField(blank=True, null=True)
    ancillary_fare = models.TextField(blank=True, null=True)
    free_cost_count = models.IntegerField()
    foc_base_fare = models.FloatField()
    foc_tax = models.FloatField()
    foc_tax_breakup = models.CharField(max_length=300, blank=True, null=True)
    lfid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_approved_flight_details'


class RequestApprovedFlightHistory(models.Model):
    request_approved_flight_history_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    transaction_history_id = models.IntegerField(blank=True, null=True)
    request_id = models.IntegerField()
    request_details_history_id = models.IntegerField(blank=True, null=True)
    series_request_history_id = models.IntegerField(blank=True, null=True)
    series_request_id = models.IntegerField()
    request_option_id = models.IntegerField(blank=True, null=True)
    airline_code = models.CharField(max_length=5, db_collation='latin1_swedish_ci', blank=True, null=True)
    flight_code = models.CharField(max_length=10, db_collation='latin1_swedish_ci', blank=True, null=True)
    flight_number = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(max_length=5, db_collation='latin1_swedish_ci', blank=True, null=True)
    destination = models.CharField(max_length=5, db_collation='latin1_swedish_ci', blank=True, null=True)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    dep_time = models.CharField(max_length=6, db_collation='latin1_swedish_ci')
    arr_time = models.CharField(max_length=6, db_collation='latin1_swedish_ci')
    journey_time = models.CharField(max_length=6, db_collation='latin1_swedish_ci')
    fare_filter_method = models.CharField(max_length=30, blank=True, null=True)
    no_of_adult = models.IntegerField(blank=True, null=True)
    no_of_child = models.IntegerField(blank=True, null=True)
    no_of_infant = models.IntegerField(blank=True, null=True)
    displacement_cost = models.FloatField()
    booking_profile_fare = models.FloatField()
    competetor_fare = models.FloatField()
    base_fare = models.FloatField()
    tax = models.FloatField()
    fare_passenger = models.FloatField()
    tax_breakup = models.CharField(max_length=150)
    child_base_fare = models.FloatField()
    child_tax = models.FloatField()
    child_tax_breakup = models.CharField(max_length=150)
    infant_base_fare = models.FloatField()
    infant_tax = models.FloatField()
    infant_tax_breakup = models.CharField(max_length=150)
    baggauge_fare = models.FloatField(blank=True, null=True)
    meals_fare = models.FloatField(blank=True, null=True)
    tiger_connect_fare = models.FloatField()
    baggage_code = models.CharField(max_length=5)
    fare_type = models.CharField(max_length=3, db_collation='latin1_swedish_ci', blank=True, null=True)
    fare_class = models.CharField(max_length=3, db_collation='latin1_swedish_ci', blank=True, null=True)
    fare_basis_code = models.CharField(max_length=10, db_collation='latin1_swedish_ci')
    rule_number = models.CharField(max_length=10, db_collation='latin1_swedish_ci')
    fare_sequence = models.CharField(max_length=5, db_collation='latin1_swedish_ci')
    fare_application_type = models.CharField(max_length=15, db_collation='latin1_swedish_ci')
    stops = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField()
    sold = models.IntegerField()
    seat_availability = models.IntegerField()
    dep_terminal = models.CharField(max_length=100, db_collation='latin1_swedish_ci')
    arr_terminal = models.CharField(max_length=100, db_collation='latin1_swedish_ci')
    image_location = models.CharField(max_length=50, db_collation='latin1_swedish_ci', blank=True, null=True)
    discount_fare = models.FloatField(blank=True, null=True)
    child_discount_fare = models.FloatField(blank=True, null=True)
    sales_promo_discount_fare = models.FloatField()
    adjusted_amount = models.FloatField(blank=True, null=True)
    accepted_flight_status = models.CharField(max_length=1)
    displacement_fare_remarks = models.TextField(blank=True, null=True)
    surcharge = models.FloatField(blank=True, null=True)
    ancillary_fare = models.TextField(blank=True, null=True)
    free_cost_count = models.IntegerField()
    foc_base_fare = models.FloatField()
    foc_tax = models.FloatField()
    foc_tax_breakup = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_approved_flight_history'


class RequestBatchDetails(models.Model):
    request_batch_id = models.AutoField(primary_key=True)
    user_file_name = models.CharField(max_length=200, blank=True, null=True)
    backend_file_name = models.CharField(max_length=200, blank=True, null=True)
    total_request_count = models.IntegerField(blank=True, null=True)
    processed_request_count = models.IntegerField(blank=True, null=True)
    uploaded_date = models.DateTimeField(blank=True, null=True)
    processed_date = models.DateTimeField(blank=True, null=True)
    file_status = models.CharField(max_length=1, blank=True, null=True)
    uploaded_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'request_batch_details'


class RequestCriteriaDetails(models.Model):
    request_criteria_details_id = models.AutoField(primary_key=True)
    request_criteria_master_id = models.IntegerField()
    request_criteria_field_id = models.IntegerField()
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    criteria_value = models.CharField(max_length=200, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_criteria_details'


class RequestCriteriaFieldDetails(models.Model):
    request_criteria_field_id = models.AutoField(primary_key=True)
    field_parent_id = models.IntegerField()
    request_criteria_field_name = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    request_criteria_field_type = models.CharField(max_length=3, db_collation='utf8mb3_general_ci')
    display_status = models.CharField(max_length=1, db_collation='utf8mb3_general_ci', blank=True, null=True)
    ssr_display_status = models.CharField(max_length=1)
    request_criteria_field_logical_name = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_criteria_field_details'


class RequestCriteriaMaster(models.Model):
    request_criteria_master_id = models.AutoField(primary_key=True)
    request_criteria_master_name = models.CharField(max_length=50, db_collation='utf8mb3_general_ci', blank=True, null=True)
    status = models.CharField(max_length=5, db_collation='utf8mb3_general_ci', blank=True, null=True)
    created_by = models.IntegerField()
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    policy_type = models.CharField(max_length=20, blank=True, null=True)
    matrix_group_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_criteria_master'


class RequestCriteriaPassengercountDetails(models.Model):
    criteria_passenger_count_id = models.AutoField(primary_key=True)
    request_criteria_master_id = models.IntegerField()
    min_passenger = models.IntegerField()
    max_passenger = models.IntegerField()
    min_infant = models.IntegerField()
    max_infant = models.IntegerField()
    min_stops = models.IntegerField(blank=True, null=True)
    foc = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_criteria_passengercount_details'


class RequestDetails(models.Model):
    request_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    origin_airport_code = models.CharField(max_length=5, blank=True, null=True)
    dest_airport_code = models.CharField(max_length=5, blank=True, null=True)
    flight_number = models.CharField(max_length=200, blank=True, null=True)
    cabin = models.CharField(max_length=20, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    start_time = models.CharField(max_length=5, blank=True, null=True)
    end_time = models.CharField(max_length=5, blank=True, null=True)
    series_weekdays = models.CharField(max_length=50, blank=True, null=True)
    baggage_allowance = models.CharField(max_length=250, blank=True, null=True)
    ancillary = models.CharField(max_length=50, blank=True, null=True)
    meals_code = models.CharField(max_length=6, blank=True, null=True)
    pnr = models.CharField(max_length=25, blank=True, null=True)
    trip_name = models.IntegerField()
    trip_type = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'request_details'


class RequestDetailsHistory(models.Model):
    request_details_history_id = models.AutoField(primary_key=True)
    request_master_history_id = models.IntegerField()
    request_master_id = models.IntegerField()
    request_id = models.IntegerField(blank=True, null=True)
    origin_airport_code = models.CharField(max_length=5, blank=True, null=True)
    dest_airport_code = models.CharField(max_length=5, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    flight_number = models.CharField(max_length=200, blank=True, null=True)
    baggage_allowance = models.CharField(max_length=250, blank=True, null=True)
    ancillary = models.CharField(max_length=5, blank=True, null=True)
    meals_code = models.CharField(max_length=5)
    cabin = models.CharField(max_length=20, blank=True, null=True)
    trip_type = models.CharField(max_length=1)
    trip_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'request_details_history'


class RequestGroupDetails(models.Model):
    request_group_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    transaction_master_id = models.IntegerField(blank=True, null=True)
    request_master_history_id = models.IntegerField()
    series_group_id = models.IntegerField(blank=True, null=True)
    materialization = models.CharField(max_length=3, blank=True, null=True)
    policy = models.CharField(max_length=2, blank=True, null=True)
    response_fare = models.CharField(max_length=30, blank=True, null=True)
    theshold_policy_id = models.CharField(max_length=30, blank=True, null=True)
    threshold_fare = models.CharField(max_length=30, blank=True, null=True)
    remarks = models.CharField(max_length=150, blank=True, null=True)
    group_status = models.IntegerField(blank=True, null=True)
    group_contract = models.TextField()

    class Meta:
        managed = False
        db_table = 'request_group_details'


class RequestMaster(models.Model):
    request_master_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    request_type = models.CharField(max_length=20, blank=True, null=True)
    request_type_id = models.IntegerField()
    trip_type = models.CharField(max_length=1, blank=True, null=True)
    series_type = models.CharField(max_length=2, blank=True, null=True)
    user_currency = models.CharField(max_length=3)
    request_fare = models.FloatField()
    exchange_rate = models.FloatField()
    requested_date = models.DateTimeField(blank=True, null=True)
    number_of_passenger = models.IntegerField(blank=True, null=True)
    number_of_adult = models.IntegerField(blank=True, null=True)
    number_of_child = models.IntegerField(blank=True, null=True)
    number_of_infant = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(db_collation='utf8mb3_general_ci', blank=True, null=True)
    fare_acceptance_transaction_id = models.IntegerField(blank=True, null=True)
    request_source = models.CharField(max_length=100, blank=True, null=True)
    requested_corporate = models.CharField(max_length=100, blank=True, null=True)
    opened_by = models.IntegerField()
    opened_time = models.DateTimeField()
    view_status = models.CharField(max_length=10)
    request_raised_by = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    auto_pilot_policy_id = models.IntegerField(blank=True, null=True)
    auto_pilot_status = models.CharField(max_length=10, blank=True, null=True)
    reference_request_master_id = models.IntegerField()
    quote_type = models.CharField(max_length=2, blank=True, null=True)
    request_group_name = models.CharField(max_length=100)
    group_category_id = models.IntegerField(blank=True, null=True)
    flexible_on_dates = models.CharField(max_length=1, blank=True, null=True)
    pnr_ignore_status = models.CharField(max_length=1, blank=True, null=True)
    queue_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_master'


class RequestMasterHistory(models.Model):
    request_master_history_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    trip_type = models.CharField(max_length=1, blank=True, null=True)
    user_currency = models.CharField(max_length=3)
    request_fare = models.IntegerField(blank=True, null=True)
    exchange_rate = models.FloatField()
    requested_date = models.DateTimeField(blank=True, null=True)
    remarks = models.CharField(max_length=300, db_collation='utf8mb3_general_ci', blank=True, null=True)
    request_raised_by = models.IntegerField(blank=True, null=True)
    cabin = models.CharField(max_length=20, blank=True, null=True)
    series_weekdays = models.CharField(max_length=50, blank=True, null=True)
    group_category_id = models.IntegerField(blank=True, null=True)
    flexible_on_dates = models.CharField(max_length=1)
    modify_status = models.IntegerField(blank=True, null=True)
    actual_request_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_master_history'


class RequestOpenHistory(models.Model):
    request_open_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    opened_by = models.IntegerField()
    opened_time = models.DateTimeField()
    view_status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'request_open_history'


class RequestPolicyCriteriaMaster(models.Model):
    request_policy_criteria_id = models.AutoField(primary_key=True)
    request_policy_criteria_name = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    request_policy_criteria_type = models.CharField(max_length=3, db_collation='utf8mb3_general_ci')
    display_status = models.CharField(max_length=1, db_collation='utf8mb3_general_ci', blank=True, null=True)
    request_policy_criteria_logical_id = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_policy_criteria_master'


class RequestPolicyDetails(models.Model):
    request_policy_details_id = models.AutoField(primary_key=True)
    request_policy_id = models.IntegerField(blank=True, null=True)
    request_criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_policy_details'


class RequestPolicyMaster(models.Model):
    request_policy_id = models.AutoField(primary_key=True)
    request_policy_name = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    request_criteria_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField()
    created_by = models.IntegerField()
    policy_group_id = models.IntegerField(blank=True, null=True)
    policy_string = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_policy_master'


class RequestProbabilityDetails(models.Model):
    request_probability_details_id = models.AutoField(primary_key=True)
    request_probability_master = models.ForeignKey('RequestProbabilityMaster', models.DO_NOTHING)
    ml_category = models.CharField(max_length=2)
    ml_response = models.TextField()
    ml_value = models.FloatField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'request_probability_details'


class RequestProbabilityMaster(models.Model):
    request_probability_master_id = models.AutoField(primary_key=True)
    request_master = models.ForeignKey(RequestMaster, models.DO_NOTHING)
    series_request = models.ForeignKey('SeriesRequestDetails', models.DO_NOTHING)
    flt_num = models.CharField(max_length=10)
    value = models.IntegerField()
    response_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'request_probability_master'


class RequestQuoteDetails(models.Model):
    request_quote_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    series_request_id = models.IntegerField(blank=True, null=True)
    series_request_history_id = models.IntegerField(blank=True, null=True)
    flight_searched_date = models.DateField(blank=True, null=True)
    batch_start_date = models.DateField(blank=True, null=True)
    quote_type = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    modify_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_quote_details'


class RequestTimelineDetails(models.Model):
    request_timeline_id = models.AutoField(primary_key=True)
    transaction_id = models.IntegerField()
    pnr_blocking_id = models.IntegerField()
    series_group_id = models.IntegerField()
    policy_history_id = models.IntegerField(blank=True, null=True)
    time_line_id = models.IntegerField()
    timeline_type = models.CharField(max_length=10)
    validity = models.IntegerField()
    validity_type = models.IntegerField()
    expiry_type = models.IntegerField()
    expiry_date = models.DateTimeField()
    percentage_value = models.FloatField()
    absolute_amount = models.FloatField()
    status = models.CharField(max_length=30, blank=True, null=True)
    materialization = models.IntegerField(blank=True, null=True)
    policy = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_timeline_details'


class RequestTimelineDetailsHistory(models.Model):
    request_timeline_history_id = models.AutoField(primary_key=True)
    request_timeline_id = models.IntegerField()
    transaction_id = models.IntegerField()
    series_group_id = models.IntegerField()
    policy_history_id = models.IntegerField()
    time_line_id = models.IntegerField()
    timeline_type = models.CharField(max_length=10)
    validity = models.IntegerField()
    validity_type = models.IntegerField()
    expiry_type = models.IntegerField()
    expiry_date = models.DateTimeField()
    percentage_value = models.FloatField()
    absolute_amount = models.FloatField()
    status = models.CharField(max_length=10)
    materialization = models.IntegerField(blank=True, null=True)
    policy = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'request_timeline_details_history'


class RequestTypeMaster(models.Model):
    request_type_id = models.AutoField(primary_key=True)
    request_type_name = models.CharField(max_length=20)
    request_type_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'request_type_master'


class RequestViaFlightDetails(models.Model):
    request_via_flight_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    series_request_id = models.IntegerField(blank=True, null=True)
    request_details_history_id = models.IntegerField()
    series_request_history_id = models.IntegerField()
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    airline_code = models.CharField(max_length=2, blank=True, null=True)
    flight_number = models.CharField(max_length=10, blank=True, null=True)
    departure_date = models.DateTimeField(blank=True, null=True)
    arrival_date = models.DateTimeField(blank=True, null=True)
    flight_status = models.CharField(max_length=1)
    option_id = models.IntegerField()
    schedule_status = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'request_via_flight_details'


class ResetPassword(models.Model):
    reset_token_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    url_token = models.CharField(unique=True, max_length=200)
    used_status = models.CharField(max_length=1)
    reset_token_type = models.CharField(max_length=2)
    initiated_time = models.DateTimeField()
    expiry_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reset_password'


class ResponseDetails(models.Model):
    response_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    transaction_master_id = models.IntegerField(blank=True, null=True)
    response_fare = models.FloatField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    response_status = models.IntegerField(blank=True, null=True)
    response_user = models.IntegerField()
    negotiation_autopilot_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'response_details'


class ReviewStatus(models.Model):
    review_status_id = models.AutoField(primary_key=True)
    transaction_id = models.IntegerField(blank=True, null=True)
    response_person_id = models.IntegerField(blank=True, null=True)
    response_date = models.DateTimeField()
    response_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_status'


class SalesPromoCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    criteria_logical_id = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_promo_criteria_master'


class SalesPromoFareMapping(models.Model):
    sales_promo_fare_id = models.AutoField(primary_key=True)
    sales_promo_mapping_id = models.IntegerField(blank=True, null=True)
    group_size = models.IntegerField(blank=True, null=True)
    discount_fare = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_promo_fare_mapping'


class SalesPromoMappingDetails(models.Model):
    sales_promo_mapping_id = models.AutoField(primary_key=True)
    sales_promo_matrix_id = models.IntegerField(blank=True, null=True)
    days_to_departure = models.IntegerField(blank=True, null=True)
    booked_load_factor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_promo_mapping_details'


class SalesPromoMatrix(models.Model):
    sales_promo_matrix_id = models.AutoField(primary_key=True)
    sales_promo_matrix_name = models.CharField(max_length=50, blank=True, null=True)
    sales_promo_matrix_type = models.CharField(max_length=5, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_promo_matrix'


class SalesPromoPolicyDetails(models.Model):
    sales_promo_policy_details_id = models.AutoField(primary_key=True)
    sales_promo_policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_promo_policy_details'


class SalesPromoPolicyMaster(models.Model):
    sales_promo_policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=100, blank=True, null=True)
    sales_promo_matrix_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    active_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_promo_policy_master'


class SaveSearchDetails(models.Model):
    process_type = models.CharField(max_length=255, blank=True, null=True)
    value_type = models.CharField(max_length=2)
    value = models.TextField(blank=True, null=True)
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    active_status = models.CharField(max_length=1, blank=True, null=True)
    filter_name = models.CharField(max_length=50, blank=True, null=True)
    default_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'save_search_details'


class SavedReportDetails(models.Model):
    saved_report_id = models.AutoField(primary_key=True)
    report_name = models.CharField(max_length=25)
    report_type_id = models.IntegerField()
    available_fields = models.CharField(max_length=150)
    available_conditions = models.CharField(max_length=50)
    created_by = models.IntegerField()
    created_date = models.DateTimeField()
    updated_by = models.IntegerField()
    updated_date = models.DateTimeField()
    deleted_by = models.IntegerField()
    deleted_date = models.DateTimeField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'saved_report_details'


class SavedReports(models.Model):
    saved_report_id = models.AutoField(primary_key=True)
    saved_report_category = models.CharField(max_length=500)
    saved_report_name = models.CharField(max_length=50)
    report_additional_info = models.TextField()
    schedule_status = models.CharField(max_length=1)
    report_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'saved_reports'


class SavedReportsMapping(models.Model):
    saved_reports_mapping_id = models.AutoField(primary_key=True)
    saved_report_id = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'saved_reports_mapping'


class ScheduleChangePnrDetails(models.Model):
    schedule_change_pnr_id = models.AutoField(primary_key=True)
    schedule_change_batch_id = models.IntegerField(blank=True, null=True)
    pnr = models.CharField(max_length=10, blank=True, null=True)
    remarks = models.CharField(max_length=50, blank=True, null=True)
    pnr_status = models.CharField(max_length=1, blank=True, null=True)
    processed_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule_change_pnr_details'


class ScheduleLogDetails(models.Model):
    schedule_log_id = models.AutoField(primary_key=True)
    saved_report_id = models.IntegerField()
    mail_recipients = models.CharField(max_length=500)
    schedule_actual_datetime = models.DateTimeField()
    schedule_sent_datetime = models.DateTimeField(blank=True, null=True)
    schedule_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'schedule_log_details'


class ScheduleReportDetails(models.Model):
    schedule_report_id = models.SmallAutoField(primary_key=True)
    report_id = models.PositiveSmallIntegerField(blank=True, null=True)
    email_id = models.CharField(max_length=256)
    frequency = models.CharField(max_length=32)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    run_at = models.TimeField(blank=True, null=True)
    created_by = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_by = models.PositiveIntegerField()
    updated_at = models.DateTimeField()
    batch_run_date = models.DateTimeField()
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule_report_details'


class ScheduleReportMapping(models.Model):
    schedule_report_mapping_id = models.SmallAutoField(primary_key=True)
    schedule_report_id = models.PositiveSmallIntegerField(blank=True, null=True)
    condition_name = models.CharField(max_length=35, blank=True, null=True)
    condition_value = models.CharField(max_length=100, blank=True, null=True)
    rolling = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'schedule_report_mapping'


class SectorManagement(models.Model):
    sector_id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=3, blank=True, null=True)
    destination = models.CharField(max_length=3, blank=True, null=True)
    active_status = models.CharField(max_length=1, db_collation='keybcs2_bin', blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sector_management'


class SectorMapping(models.Model):
    sector_mapping_id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    operation_status = models.CharField(max_length=1, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sector_mapping'


class SectorThresholdLimit(models.Model):
    sector_threshold_id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=5, blank=True, null=True)
    destination = models.CharField(max_length=5, blank=True, null=True)
    threshold_limit = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sector_threshold_limit'


class SectorUserMapping(models.Model):
    sector_user_id = models.AutoField(primary_key=True)
    sector_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    primary_user = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sector_user_mapping'


class SelectedCompetitorFareHistory(models.Model):
    selected_competitor_fare_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    transaction_id = models.IntegerField(blank=True, null=True)
    transaction_history_id = models.IntegerField(blank=True, null=True)
    request_approved_flight_id = models.IntegerField(blank=True, null=True)
    request_approve_history_flight_id = models.IntegerField(blank=True, null=True)
    competitor_flight_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'selected_competitor_fare_history'


class SeriesFlightScheduleDetails(models.Model):
    series_flight_schedule_id = models.AutoField(primary_key=True)
    series_request_id = models.IntegerField()
    alternate_series_request_id = models.IntegerField(blank=True, null=True)
    request_id = models.IntegerField(blank=True, null=True)
    request_details_history_id = models.IntegerField(blank=True, null=True)
    series_request_history_id = models.IntegerField(blank=True, null=True)
    batch_id = models.IntegerField()
    origin_airport_code = models.CharField(max_length=3, blank=True, null=True)
    dest_airport_code = models.CharField(max_length=3, blank=True, null=True)
    airlines_code = models.CharField(max_length=7, blank=True, null=True)
    cabin = models.CharField(max_length=10, blank=True, null=True)
    arrival_time = models.CharField(max_length=5, blank=True, null=True)
    departure_time = models.CharField(max_length=5, blank=True, null=True)
    flight_number = models.CharField(max_length=5, blank=True, null=True)
    flight_jounary_time = models.CharField(max_length=5, blank=True, null=True)
    leg_count = models.IntegerField(blank=True, null=True)
    routing = models.CharField(max_length=11, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    series_weekdays = models.CharField(max_length=13, blank=True, null=True)
    fare_filter_method = models.CharField(max_length=30, blank=True, null=True)
    displacement_fare = models.FloatField(blank=True, null=True)
    booking_profile_fare = models.IntegerField(blank=True, null=True)
    competetor_fare = models.IntegerField(blank=True, null=True)
    base_fare = models.FloatField(blank=True, null=True)
    child_base_fare = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    new_tax = models.FloatField(blank=True, null=True)
    child_tax = models.FloatField(blank=True, null=True)
    new_child_tax = models.FloatField()
    currency_type = models.CharField(max_length=3, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    sold = models.IntegerField(blank=True, null=True)
    seat_availability = models.IntegerField(blank=True, null=True)
    policy_id = models.IntegerField(blank=True, null=True)
    policy_matrix_id = models.IntegerField(blank=True, null=True)
    policy_matrix_type = models.CharField(max_length=5, blank=True, null=True)
    policy_currency_type = models.CharField(max_length=5, blank=True, null=True)
    policy_days_to_departure = models.IntegerField(blank=True, null=True)
    booked_load_factor = models.IntegerField(blank=True, null=True)
    policy_value = models.FloatField(blank=True, null=True)
    policy_display_value = models.CharField(max_length=10, blank=True, null=True)
    policy_discount_fare = models.FloatField(blank=True, null=True)
    policy_child_discount_fare = models.FloatField(blank=True, null=True)
    existing_adult_base_fare = models.FloatField(blank=True, null=True)
    existing_adult_tax = models.FloatField(blank=True, null=True)
    existing_child_base_fare = models.FloatField(blank=True, null=True)
    existing_child_tax = models.FloatField(blank=True, null=True)
    competitor_status = models.CharField(max_length=1, blank=True, null=True)
    sales_promo_policy_matrix_type = models.CharField(max_length=5, blank=True, null=True)
    sales_promo_policy_value = models.FloatField(blank=True, null=True)
    sales_promo_policy_matrix_id = models.IntegerField(blank=True, null=True)
    sales_promo_policy_id = models.IntegerField(blank=True, null=True)
    sales_promo_policy_currency_type = models.CharField(max_length=5, blank=True, null=True)
    sales_promo_discount_fare = models.FloatField(blank=True, null=True)
    sales_promo_policy_display_value = models.CharField(max_length=10, blank=True, null=True)
    sales_promo_booked_factor = models.IntegerField(blank=True, null=True)
    original_base_fare = models.FloatField(blank=True, null=True)
    sales_promo_policy_days_to_departure = models.IntegerField(blank=True, null=True)
    surcharge = models.FloatField(blank=True, null=True)
    surcharge_details = models.TextField(blank=True, null=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)
    forecast_load_factor = models.IntegerField(blank=True, null=True)
    ancillary_fare = models.TextField(blank=True, null=True)
    special_fare_type = models.TextField(blank=True, null=True)
    approved_fare_details = models.TextField(blank=True, null=True)
    approved_policy_details = models.TextField(blank=True, null=True)
    lfid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series_flight_schedule_details'


class SeriesRequestDetails(models.Model):
    series_request_id = models.AutoField(primary_key=True)
    request_id = models.IntegerField(blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    number_of_passenger = models.IntegerField(blank=True, null=True)
    number_of_adult = models.IntegerField(blank=True, null=True)
    number_of_child = models.IntegerField(blank=True, null=True)
    number_of_infant = models.IntegerField(blank=True, null=True)
    cabin = models.CharField(max_length=20, blank=True, null=True)
    start_time = models.CharField(max_length=5, blank=True, null=True)
    end_time = models.CharField(max_length=5, blank=True, null=True)
    baggage_allowance = models.CharField(max_length=250, blank=True, null=True)
    ancillary = models.CharField(max_length=50, blank=True, null=True)
    meals_code = models.CharField(max_length=6, blank=True, null=True)
    pnr = models.CharField(max_length=25, blank=True, null=True)
    expected_fare = models.FloatField(blank=True, null=True)
    flexible_on_dates = models.CharField(max_length=1)
    group_category_id = models.IntegerField(blank=True, null=True)
    mapped_series_request_id = models.IntegerField(blank=True, null=True)
    series_group_id = models.IntegerField(blank=True, null=True)
    parent_series_group_id = models.IntegerField()
    flight_number = models.CharField(max_length=200, blank=True, null=True)
    current_load_factor = models.CharField(max_length=100, blank=True, null=True)
    forecast_load_factor = models.CharField(max_length=100, blank=True, null=True)
    future_load_factor = models.CharField(max_length=100, blank=True, null=True)
    parent_series_request_id = models.IntegerField()
    flight_status = models.CharField(max_length=2)
    foc_pax = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series_request_details'


class SeriesRequestDetailsHistory(models.Model):
    series_request_history_id = models.AutoField(primary_key=True)
    request_details_history_id = models.IntegerField()
    series_request_id = models.IntegerField(blank=True, null=True)
    request_id = models.IntegerField(blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    number_of_passenger = models.IntegerField(blank=True, null=True)
    number_of_adult = models.IntegerField(blank=True, null=True)
    number_of_child = models.IntegerField(blank=True, null=True)
    number_of_infant = models.IntegerField(blank=True, null=True)
    cabin = models.CharField(max_length=20, blank=True, null=True)
    baggage_allowance = models.CharField(max_length=250, blank=True, null=True)
    ancillary = models.CharField(max_length=5, blank=True, null=True)
    meals_code = models.CharField(max_length=5, blank=True, null=True)
    pnr = models.CharField(max_length=25, blank=True, null=True)
    expected_fare = models.FloatField(blank=True, null=True)
    flexible_on_date = models.CharField(max_length=1)
    group_category_id = models.IntegerField(blank=True, null=True)
    mapped_series_request_id = models.IntegerField(blank=True, null=True)
    series_group_id = models.IntegerField(blank=True, null=True)
    parent_series_group_id = models.IntegerField()
    flight_number = models.CharField(max_length=200, blank=True, null=True)
    current_load_factor = models.CharField(max_length=100, blank=True, null=True)
    forecast_load_factor = models.CharField(max_length=100, blank=True, null=True)
    future_load_factor = models.CharField(max_length=100, blank=True, null=True)
    parent_series_request_id = models.IntegerField()
    modify_status = models.CharField(max_length=1, blank=True, null=True)
    flight_status = models.CharField(max_length=2)
    foc_pax = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series_request_details_history'


class SeriesViaFlightDetails(models.Model):
    series_via_flight_id = models.AutoField(primary_key=True)
    series_flight_schedule_id = models.IntegerField(blank=True, null=True)
    origin_airport_code = models.CharField(max_length=3)
    dest_airport_code = models.CharField(max_length=3)
    airline_code = models.CharField(max_length=2)
    flight_number = models.CharField(max_length=5)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    time_departure = models.CharField(max_length=5)
    time_arrival = models.CharField(max_length=5)
    base_fare = models.FloatField(blank=True, null=True)
    baggage_fare = models.FloatField()
    meals_fare = models.FloatField()
    ancillary_fare = models.TextField(blank=True, null=True)
    capacity = models.IntegerField()
    sold = models.IntegerField()
    seat_availability = models.IntegerField()
    forecast_load_factor = models.IntegerField(blank=True, null=True)
    surcharge = models.FloatField(blank=True, null=True)
    discount_amount = models.FloatField()
    discount_details = models.TextField(blank=True, null=True)
    special_fare_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series_via_flight_details'


class ServiceTaxDetails(models.Model):
    service_tax_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    corporate_id = models.IntegerField()
    reference_number = models.CharField(max_length=16)
    agency_name = models.CharField(max_length=100, blank=True, null=True)
    agent_email_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=1)  # Field name made lowercase.
    reference_type = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'service_tax_details'
        unique_together = (('reference_number', 'request_master_id'),)


class SessionDetails(models.Model):
    session_details_id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=40)
    user_id = models.IntegerField(blank=True, null=True)
    last_active_time = models.PositiveIntegerField()
    expiry_time = models.PositiveIntegerField()
    useragent = models.TextField(blank=True, null=True)
    ipaddr = models.CharField(max_length=46, blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'session_details'


class SharedProcessingrecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shared_processingrecord'


class SharedScheduledjob(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_name = models.CharField(unique=True, max_length=100)
    job_func = models.CharField(max_length=200)
    cron_schedule = models.CharField(max_length=50)
    is_enabled = models.IntegerField()
    last_run = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shared_scheduledjob'


class SharedTaskprogress(models.Model):
    task_id = models.CharField(primary_key=True, max_length=255)
    task_name = models.CharField(max_length=255)
    last_processed_id = models.IntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shared_taskprogress'


class SsrCategoryDetails(models.Model):
    ssr_category_id = models.AutoField(primary_key=True)
    ssr_category_name = models.CharField(max_length=30)
    display_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ssr_category_details'


class SsrDetails(models.Model):
    ssr_details_id = models.AutoField(primary_key=True)
    ssr_master_id = models.IntegerField()
    ssr_pax_id = models.IntegerField()
    ssr_category_id = models.IntegerField()
    ssr_code = models.CharField(max_length=50)
    ssr_base_fare = models.FloatField()
    ssr_tax = models.FloatField()
    ssr_total_fare = models.FloatField()
    emd_id = models.IntegerField(blank=True, null=True)
    ssr_status = models.CharField(max_length=32)
    remarks = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssr_details'


class SsrList(models.Model):
    ssr_list_id = models.AutoField(primary_key=True)
    ssr_category_id = models.IntegerField()
    ssr_subcategory_id = models.IntegerField(blank=True, null=True)
    ssr_code = models.CharField(max_length=10)
    ssr_description = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    display_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ssr_list'


class SsrMaster(models.Model):
    ssr_master_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    pnr = models.CharField(max_length=10)
    ssr_amount = models.FloatField()
    updated_by = models.IntegerField()
    ssr_updated_date = models.DateTimeField()
    last_transaction = models.CharField(max_length=1)
    status = models.CharField(max_length=32)
    ssr_category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssr_master'


class SsrMatrixDetails(models.Model):
    matrix_details_id = models.AutoField(primary_key=True)
    matrix_master_id = models.IntegerField()
    request_criteria_field_id = models.IntegerField()
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    criteria_value = models.CharField(max_length=200, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssr_matrix_details'


class SsrMatrixMaster(models.Model):
    matrix_id = models.AutoField(primary_key=True)
    matrix_name = models.CharField(max_length=48, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssr_matrix_master'


class SsrPaxDetails(models.Model):
    ssr_pax_id = models.AutoField(primary_key=True)
    pnr_blocking_id = models.IntegerField()
    via_flight_id = models.IntegerField()
    pax_reference_id = models.CharField(max_length=200, blank=True, null=True)
    passenger_id = models.IntegerField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ssr_pax_details'


class SsrPaxGrouping(models.Model):
    ssr_pax_grouping_id = models.AutoField(primary_key=True)
    ssr_details_id = models.IntegerField()
    ssr_id = models.CharField(max_length=200, blank=True, null=True)
    ssr_weight = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'ssr_pax_grouping'


class SsrPolicyDetails(models.Model):
    policy_details_id = models.AutoField(primary_key=True)
    policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField()
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssr_policy_details'


class SsrPolicyMaster(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=100, blank=True, null=True)
    matrix_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    active_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    policy_string = models.TextField()
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssr_policy_master'


class SsrSubcategoryDetails(models.Model):
    ssr_subcategory_id = models.AutoField(primary_key=True)
    ssr_category_id = models.IntegerField()
    ssr_subcategory_name = models.CharField(max_length=30)
    display_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ssr_subcategory_details'


class SsrTemp(models.Model):
    ssr_temp_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    series_request_id = models.IntegerField()
    passenger_id = models.CharField(max_length=15)
    pnr = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=25)
    fare = models.FloatField()
    amount_diff = models.FloatField()
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ssr_temp'


class SsrTempMaster(models.Model):
    ssr_temp_master_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    request_master_id = models.IntegerField(blank=True, null=True)
    series_request_id = models.IntegerField(blank=True, null=True)
    current_status = models.CharField(max_length=15, blank=True, null=True)
    requested_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssr_temp_master'


class StaticFareCriteriaMaster(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)
    criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    criteria_logical_id = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'static_fare_criteria_master'


class StaticFareDetails(models.Model):
    static_fare_id = models.AutoField(primary_key=True)
    request_approved_flight_id = models.IntegerField()
    via_flight_id = models.IntegerField()
    fare_type_policy_id = models.IntegerField()
    fare_type_matrix_id = models.IntegerField()
    fare_policy_id = models.IntegerField()
    fare_matrix_id = models.IntegerField()
    days_to_departure = models.IntegerField()
    capacity = models.IntegerField()
    sold = models.IntegerField()
    seat_availability = models.IntegerField()
    booked_load = models.IntegerField()
    forecast_load = models.IntegerField(blank=True, null=True)
    current_group_count = models.IntegerField(blank=True, null=True)
    group_size = models.CharField(max_length=5)
    quoted_date = models.DateTimeField()
    fare_policy_details = models.TextField()

    class Meta:
        managed = False
        db_table = 'static_fare_details'


class StaticFarePolicyDetails(models.Model):
    policy_details_id = models.AutoField(primary_key=True)
    policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'static_fare_policy_details'


class StaticFarePolicyMaster(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=100, blank=True, null=True)
    booking_profile_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    matrix_type = models.CharField(max_length=5, blank=True, null=True)
    active_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'static_fare_policy_master'


class StatusDetails(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_code = models.CharField(max_length=5, blank=True, null=True)
    status_name = models.CharField(max_length=150, blank=True, null=True)
    front_end = models.CharField(max_length=1, blank=True, null=True)
    back_end = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status_details'


class StdTplDetails(models.Model):
    std_tpl_id = models.AutoField(primary_key=True)
    std_tpl_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'std_tpl_details'


class SubAgencyMappingDetails(models.Model):
    sub_agency_mapping_id = models.AutoField(primary_key=True)
    corporate_id = models.IntegerField()
    mapped_corporate_id = models.IntegerField()
    status = models.CharField(max_length=7)
    requested_by = models.IntegerField()
    requested_date = models.DateTimeField()
    responded_by = models.IntegerField()
    responded_date = models.DateTimeField()
    remarks = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = 'sub_agency_mapping_details'


class SupportTypeMaster(models.Model):
    support_type_id = models.AutoField(primary_key=True)
    support_type_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'support_type_master'


class SurchargeMappingDetails(models.Model):
    surcharge_mapping_id = models.AutoField(primary_key=True)
    surcharge_details_id = models.IntegerField(blank=True, null=True)
    group_size = models.IntegerField(blank=True, null=True)
    surcharge = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'surcharge_mapping_details'


class SurchargeMatrix(models.Model):
    surcharge_matrix_id = models.AutoField(primary_key=True)
    surcharge_matrix_name = models.CharField(max_length=50, blank=True, null=True)
    load_factor_type = models.CharField(max_length=5, blank=True, null=True)
    surcharge_matrix_type = models.CharField(max_length=5, blank=True, null=True)
    currency_type = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'surcharge_matrix'


class SurchargeMatrixDetails(models.Model):
    surcharge_details_id = models.AutoField(primary_key=True)
    surcharge_matrix_id = models.IntegerField(blank=True, null=True)
    days_to_departure = models.IntegerField(blank=True, null=True)
    booked_load_factor = models.IntegerField(blank=True, null=True)
    forecast_load_factor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'surcharge_matrix_details'


class SurchargePolicyDetails(models.Model):
    surcharge_policy_details_id = models.AutoField(primary_key=True)
    surcharge_policy_id = models.IntegerField(blank=True, null=True)
    criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'surcharge_policy_details'


class SurchargePolicyMaster(models.Model):
    surcharge_policy_id = models.AutoField(primary_key=True)
    surcharge_policy_name = models.CharField(max_length=100, blank=True, null=True)
    surcharge_matrix_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    active_status = models.CharField(max_length=1, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    policy_dow = models.CharField(max_length=100)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'surcharge_policy_master'


class SystemMStatus(models.Model):
    id = models.SmallAutoField(primary_key=True)
    status_name = models.CharField(unique=True, max_length=50)
    status_code = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'system_m_status'


class SystemMUserTypes(models.Model):
    id = models.SmallAutoField(primary_key=True)
    user_type = models.CharField(max_length=30)
    r_status = models.ForeignKey(SystemMStatus, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_m_user_types'


class SystemSettings(models.Model):
    key_id = models.AutoField(primary_key=True)
    key_index = models.CharField(max_length=100, blank=True, null=True)
    key_name = models.CharField(max_length=100, blank=True, null=True)
    extra_key_name = models.CharField(max_length=100, blank=True, null=True)
    key_value = models.TextField(blank=True, null=True)
    value_type = models.CharField(max_length=1, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    backend_status = models.CharField(max_length=1, blank=True, null=True)
    last_updated_by = models.IntegerField(blank=True, null=True)
    last_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_settings'


class SystemTResetPassword(models.Model):
    url_token = models.CharField(unique=True, max_length=200)
    used_status = models.CharField(max_length=1)
    reset_token_type = models.CharField(max_length=2)
    initiated_time = models.DateTimeField()
    expiry_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('SystemTUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_t_reset_password'


class SystemTUsers(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    email_id = models.CharField(unique=True, max_length=254)
    title = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=32)
    last_login_ip = models.CharField(max_length=40, blank=True, null=True)
    r_status = models.ForeignKey(SystemMStatus, models.DO_NOTHING)
    r_user_type = models.ForeignKey(SystemMUserTypes, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_t_users'


class SystemTUsersGroups(models.Model):
    user = models.ForeignKey(SystemTUsers, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_t_users_groups'
        unique_together = (('user', 'group'),)


class SystemTUsersUserPermissions(models.Model):
    user = models.ForeignKey(SystemTUsers, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_t_users_user_permissions'
        unique_together = (('user', 'permission'),)


class TakeControlDetails(models.Model):
    take_control_id = models.AutoField(primary_key=True)
    request_master_id = models.IntegerField()
    reference_id = models.IntegerField()
    process_type = models.CharField(max_length=25, blank=True, null=True)
    opened_by = models.IntegerField()
    opened_time = models.DateTimeField()
    control_status = models.CharField(max_length=15)
    unique_status = models.CharField(max_length=11, blank=True, null=True)
    action_pnr = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'take_control_details'
        unique_together = (('process_type', 'unique_status'),)


class TaxBreakupDetails(models.Model):
    tax_breakup_id = models.AutoField(primary_key=True)
    series_flight_schedule_id = models.IntegerField(blank=True, null=True)
    pax_type = models.CharField(max_length=10, blank=True, null=True)
    tax_index = models.CharField(max_length=10, blank=True, null=True)
    tax_code = models.CharField(max_length=30, blank=True, null=True)
    charge_code = models.CharField(max_length=10, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    tax_description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tax_breakup_details'


class TemplateDetails(models.Model):
    template_id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=50, blank=True, null=True)
    class_tpl_name = models.CharField(max_length=50, blank=True, null=True)
    template_type = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'template_details'


class TenderDetails(models.Model):
    tender_id = models.AutoField(primary_key=True)
    tender_name = models.CharField(max_length=60)
    organisation_name = models.CharField(max_length=60)
    source_information = models.CharField(max_length=60)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2)
    created_on = models.DateTimeField()
    created_by = models.IntegerField()
    responded_on = models.DateTimeField()
    responded_by = models.IntegerField()
    last_updated_on = models.DateTimeField()
    last_updated_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tender_details'


class TenderOptionDetails(models.Model):
    tender_option_id = models.AutoField(primary_key=True)
    tender_id = models.IntegerField()
    request_master_id = models.IntegerField()
    status = models.CharField(max_length=2)
    created_on = models.DateTimeField()
    created_by = models.IntegerField()
    created_for = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tender_option_details'


class TenderParticipantDetails(models.Model):
    tender_participant_id = models.AutoField(primary_key=True)
    tender_id = models.IntegerField()
    user_id = models.IntegerField()
    participated_date = models.DateTimeField()
    participation_status = models.CharField(max_length=2)
    participant_remarks = models.TextField()
    actioned_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tender_participant_details'


class TenderPnrDetails(models.Model):
    tender_pnr_id = models.AutoField(primary_key=True)
    tender_id = models.IntegerField()
    pnr = models.CharField(max_length=6)
    request_master_id = models.IntegerField()
    request_approved_flight_id = models.IntegerField()
    via_flight_id = models.IntegerField()
    status = models.CharField(max_length=10)
    created_date = models.DateTimeField()
    created_by = models.IntegerField()
    awarded_on = models.DateTimeField()
    awarded_by = models.IntegerField()
    awarded_participant_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tender_pnr_details'


class TenderStatusDetails(models.Model):
    tender_status_id = models.AutoField(primary_key=True)
    status_code = models.CharField(max_length=2)
    status_name = models.CharField(max_length=32)
    type = models.CharField(max_length=10)
    display_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tender_status_details'


class TicketingDetails(models.Model):
    ticketing_id = models.AutoField(primary_key=True)
    travel_bank_id = models.IntegerField(blank=True, null=True)
    ticket_number = models.CharField(max_length=100, blank=True, null=True)
    fare_basis_code = models.CharField(max_length=20, blank=True, null=True)
    promo_code = models.CharField(max_length=20, blank=True, null=True)
    ticketed_date = models.DateTimeField(blank=True, null=True)
    ticketed_by = models.IntegerField(blank=True, null=True)
    ticket_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ticketing_details'


class TimeLineMatrix(models.Model):
    time_line_id = models.AutoField(primary_key=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    days_to_departure = models.IntegerField(blank=True, null=True)
    payment_validity = models.IntegerField(blank=True, null=True)
    payment_type_id = models.IntegerField(blank=True, null=True)
    passenger_validity = models.IntegerField(blank=True, null=True)
    passenger_type_id = models.IntegerField(blank=True, null=True)
    fare_validity = models.IntegerField(blank=True, null=True)
    fare_type_id = models.IntegerField(blank=True, null=True)
    time_line_matrix_list_id = models.IntegerField()
    expiry_type_id = models.IntegerField(blank=True, null=True)
    payment_expiry_type_id = models.IntegerField(blank=True, null=True)
    passenger_expiry_type_id = models.IntegerField(blank=True, null=True)
    payment_percentage = models.FloatField(blank=True, null=True)
    payment_in_percent = models.CharField(max_length=3)
    payment_currency = models.CharField(max_length=5, blank=True, null=True)
    materialization = models.IntegerField(blank=True, null=True)
    policy = models.CharField(max_length=5, blank=True, null=True)
    penalty_value = models.IntegerField(blank=True, null=True)
    penalty_type_id = models.IntegerField(blank=True, null=True)
    penalty_expiry_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_line_matrix'


class TimeLineMatrixCriteriaMaster(models.Model):
    time_line_matrix_criteria_id = models.AutoField(primary_key=True)
    time_line_matrix_criteria_name = models.CharField(max_length=100, blank=True, null=True)
    time_line_matrix_criteria_type = models.CharField(max_length=3, blank=True, null=True)
    display_status = models.CharField(max_length=1, blank=True, null=True)
    time_line_matrix_criteria_logical_id = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_line_matrix_criteria_master'


class TimeLineMatrixDetails(models.Model):
    time_line_matrix_details_id = models.AutoField(primary_key=True)
    time_line_matrix_master_id = models.IntegerField(blank=True, null=True)
    time_line_matrix_criteria_id = models.IntegerField(blank=True, null=True)
    loop_value = models.IntegerField(blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    policy_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_line_matrix_details'


class TimeLineMatrixList(models.Model):
    time_line_matrix_list_id = models.AutoField(primary_key=True)
    time_line_matrix_name = models.CharField(max_length=48, blank=True, null=True)
    activation_status = models.CharField(max_length=1, blank=True, null=True)
    default_status = models.CharField(max_length=1, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_line_matrix_list'


class TimeLineMatrixMaster(models.Model):
    time_line_matrix_master_id = models.AutoField(primary_key=True)
    time_line_matrix_list_id = models.IntegerField(blank=True, null=True)
    time_line_policy_name = models.CharField(max_length=48, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    activation_status = models.CharField(max_length=1, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    policy_dow = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_line_matrix_master'


class TimeLinePaymentDetails(models.Model):
    time_line_payment_id = models.AutoField(primary_key=True)
    time_line_id = models.IntegerField(blank=True, null=True)
    payment_validity = models.IntegerField(blank=True, null=True)
    payment_validity_type = models.IntegerField(blank=True, null=True)
    payment_expiry_type = models.IntegerField(blank=True, null=True)
    payment_percentage = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_line_payment_details'


class TransactionHistory(models.Model):
    transaction_history_id = models.AutoField(primary_key=True)
    review_status_id = models.IntegerField()
    airlines_request_id = models.IntegerField(blank=True, null=True)
    transaction_id = models.IntegerField(blank=True, null=True)
    request_master_history_id = models.IntegerField(blank=True, null=True)
    fare_advised = models.FloatField()
    child_fare = models.FloatField()
    infant_fare = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    child_discount = models.FloatField(blank=True, null=True)
    infant_discount = models.FloatField(blank=True, null=True)
    evaluated_fare = models.FloatField()
    exchange_rate = models.FloatField()
    fare_negotiable = models.CharField(max_length=20, db_collation='latin1_swedish_ci', blank=True, null=True)
    auto_approval = models.CharField(max_length=1)
    fare_validity = models.IntegerField(blank=True, null=True)
    fare_validity_type_id = models.IntegerField(blank=True, null=True)
    fare_expiry_type = models.IntegerField()
    payment_validity = models.IntegerField()
    payment_validity_type = models.IntegerField()
    payment_expiry_type = models.IntegerField()
    passenger_validity = models.IntegerField()
    passenger_validity_type = models.IntegerField()
    passenger_expiry_date = models.DateTimeField()
    passenger_expiry_type = models.IntegerField()
    transaction_date = models.DateTimeField(blank=True, null=True)
    fare_expiry_date = models.CharField(max_length=25, db_collation='latin1_swedish_ci', blank=True, null=True)
    payment_expiry_date = models.DateTimeField()
    active_status = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    response_source = models.CharField(max_length=50, db_collation='latin1_swedish_ci', blank=True, null=True)
    cancel_policy_id = models.IntegerField()
    time_line_id = models.IntegerField()
    negotiation_policy_id = models.IntegerField()
    sales_promo_status = models.CharField(max_length=1)
    payment_in_percent = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'transaction_history'


class TransactionMaster(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    airlines_request_id = models.IntegerField(blank=True, null=True)
    request_master_history_id = models.IntegerField(blank=True, null=True)
    fare_advised = models.FloatField()
    child_fare = models.FloatField()
    infant_fare = models.FloatField()
    exchange_rate = models.FloatField()
    fare_negotiable = models.CharField(max_length=20, blank=True, null=True)
    auto_approval = models.CharField(max_length=1)
    transaction_fee = models.CharField(max_length=1, blank=True, null=True)
    fare_validity = models.IntegerField(blank=True, null=True)
    fare_validity_type_id = models.IntegerField(blank=True, null=True)
    fare_expiry_type = models.IntegerField()
    payment_validity = models.IntegerField()
    payment_validity_type = models.IntegerField()
    payment_expiry_type = models.IntegerField()
    passenger_validity = models.IntegerField()
    passenger_validity_type = models.IntegerField()
    passenger_expiry_type = models.IntegerField()
    transaction_date = models.DateTimeField(blank=True, null=True)
    fare_expiry_date = models.DateTimeField()
    payment_expiry_date = models.DateTimeField()
    passenger_expiry_date = models.DateTimeField()
    active_status = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    alternate_flight_remarks = models.TextField(blank=True, null=True)
    timelimit_remarks = models.TextField(blank=True, null=True)
    response_source = models.CharField(max_length=50, blank=True, null=True)
    cancel_policy_id = models.IntegerField()
    time_line_id = models.IntegerField()
    negotiation_policy_id = models.IntegerField()
    sales_promo_status = models.CharField(max_length=1)
    payment_in_percent = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'transaction_master'


class TravelBankMaster(models.Model):
    travel_bank_id = models.AutoField(primary_key=True)
    customer_insight_id = models.IntegerField(blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.CharField(max_length=100, blank=True, null=True)
    account_balance = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'travel_bank_master'


class TravelBankTransactionDetails(models.Model):
    travel_bank_transaction_id = models.AutoField(primary_key=True)
    travel_bank_id = models.IntegerField(blank=True, null=True)
    emd_id = models.IntegerField(blank=True, null=True)
    payment_type = models.CharField(max_length=5, blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'travel_bank_transaction_details'


class UserDetails(models.Model):
    user_id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(blank=True, null=True)
    corporate_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=16, blank=True, null=True)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    email_id = models.CharField(max_length=100, blank=True, null=True)
    user_password = models.CharField(max_length=90, blank=True, null=True)
    user_address = models.CharField(max_length=256, blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    approved_status = models.CharField(max_length=1)
    email_verification_status = models.CharField(max_length=1)
    confirm_code = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    time_zone_interval = models.CharField(max_length=40, blank=True, null=True)
    time_zone_key = models.CharField(max_length=352, blank=True, null=True)
    ip_address = models.CharField(max_length=40)
    country_code = models.CharField(max_length=16, blank=True, null=True)
    last_login_ip_address = models.CharField(max_length=40)
    last_login_date = models.DateTimeField()
    country_number = models.CharField(max_length=15, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    user_zip_code = models.CharField(max_length=36, blank=True, null=True)
    user_name = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_details'


class UserEmailMapping(models.Model):
    user_email_mapping_id = models.AutoField(primary_key=True)
    email_setting_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    email_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_email_mapping'


class UserGuideHistory(models.Model):
    user_guide_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    user_guide_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_guide_history'


class UserLevelSettings(models.Model):
    key_id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    key_name = models.CharField(max_length=100, blank=True, null=True)
    key_value = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    last_updated_by = models.IntegerField(blank=True, null=True)
    last_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_level_settings'


class UserPasswordMapping(models.Model):
    password_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    last_updated_password = models.CharField(max_length=40)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_password_mapping'


class UserTypeDetails(models.Model):
    user_type_id = models.AutoField(primary_key=True)
    user_type_name = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type_details'


class ViaFlightDetails(models.Model):
    via_flight_id = models.AutoField(primary_key=True)
    request_approved_flight_id = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=4, blank=True, null=True)
    destination = models.CharField(max_length=4, blank=True, null=True)
    airline_code = models.CharField(max_length=3, blank=True, null=True)
    flight_number = models.CharField(max_length=5, blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    displacement_fare = models.FloatField()
    discount_amount = models.FloatField()
    base_fare = models.FloatField()
    baggauge_fare = models.FloatField()
    meals_fare = models.FloatField()
    capacity = models.IntegerField()
    sold = models.IntegerField()
    seat_availability = models.IntegerField()
    surcharge = models.FloatField(blank=True, null=True)
    ancillary_fare = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'via_flight_details'


class ViaFlightHistory(models.Model):
    via_flight_history_id = models.AutoField(primary_key=True)
    request_approved_flight_history_id = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=4, db_collation='latin1_swedish_ci', blank=True, null=True)
    destination = models.CharField(max_length=4, db_collation='latin1_swedish_ci', blank=True, null=True)
    airline_code = models.CharField(max_length=3, db_collation='latin1_swedish_ci', blank=True, null=True)
    flight_number = models.CharField(max_length=5, db_collation='latin1_swedish_ci', blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    baggauge_fare = models.FloatField()
    meals_fare = models.FloatField()
    tiger_connect_fare = models.FloatField()
    capacity = models.IntegerField()
    sold = models.IntegerField()
    seat_availability = models.IntegerField()
    fare_type = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    fare_class = models.CharField(max_length=3, db_collation='latin1_swedish_ci')
    rule_number = models.CharField(max_length=10, db_collation='latin1_swedish_ci')
    fare_sequence = models.CharField(max_length=5, db_collation='latin1_swedish_ci')
    fare_application_type = models.CharField(max_length=15, db_collation='latin1_swedish_ci')
    origin_airport_name = models.CharField(max_length=200, db_collation='latin1_swedish_ci', blank=True, null=True)
    dest_airport_name = models.CharField(max_length=200, db_collation='latin1_swedish_ci', blank=True, null=True)
    surcharge = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'via_flight_history'


class WorkflowEngineEdge(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    from_node = models.ForeignKey('WorkflowEngineNode', models.DO_NOTHING,        related_name='engine_out_edges'  # <-- Add this unique name
)
    to_node = models.ForeignKey('WorkflowEngineNode', models.DO_NOTHING)
    workflow = models.ForeignKey('WorkflowEngineWorkflow', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'workflow_engine_edge'


class WorkflowEngineNode(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    type = models.CharField(max_length=50)
    config = models.JSONField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    workflow = models.ForeignKey('WorkflowEngineWorkflow', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'workflow_engine_node'


class WorkflowEngineWorkflow(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255)
    mode = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'workflow_engine_workflow'
