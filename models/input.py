# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
import jdatetime
import logging
import sys, traceback

class SdPaynehImpoertInput(models.Model):
    _name = 'sd_payaneh_import.input'
    _description = 'sd_payaneh_import.input'

    active = fields.Boolean(default=True)
    document_no = fields.Char()
    loading_no = fields.Char()
    loading_date = fields.Char()
    registration_no = fields.Char()
    buyer = fields.Char()
    contractor = fields.Char()
    driver = fields.Char()
    card_no = fields.Char()
    plate_1 = fields.Char()
    plate_2 = fields.Char()
    plate_3 = fields.Char()
    plate_4 = fields.Char()
    front_container = fields.Char()
    middle_container = fields.Char()
    back_container = fields.Char()
    total = fields.Char()

    centralized_container = fields.Char()
    sp_gr = fields.Char()
    temperature = fields.Char()
    pressure = fields.Char()
    meter_no = fields.Char()
    totalizer_start = fields.Char()
    totalizer_end = fields.Char()
    totalizer_difference = fields.Char()
    weighbridge = fields.Char()
    tanker_empty_weight = fields.Char()
    tanker_full_weight = fields.Char()
    tanker_pure_weight = fields.Char()
    evacuation_box_seal = fields.Char()
    compartment_1 = fields.Char()
    compartment_2 = fields.Char()
    compartment_3 = fields.Char()
    correction_factor = fields.Char()
    rec_api = fields.Char()
    temperature_f = fields.Char()
    pressure_psi = fields.Char()
    ctl = fields.Char()
    cpl = fields.Char()
    tab_13 = fields.Char()
    meter_tov_l = fields.Char()
    meter_gsv_l = fields.Char()
    meter_gsv_b = fields.Char()
    meter_mt = fields.Char()
    wb_tov_l = fields.Char()
    wb_gsv_l = fields.Char()
    wb_gsv_b = fields.Char()
    wb_mt = fields.Char()
    final_tov_l = fields.Char()
    final_gsv_l = fields.Char()
    final_gsv_b = fields.Char()
    final_mt = fields.Char()
    description = fields.Char()


    def process_records(self):
        active_ids = self.env.context.get('active_ids')
        print(f'\n {active_ids}')
        jyear = 1402
        jmonth = 4
        data_model = self.browse(active_ids)
        payaneh_data_model = self.env['sd_payaneh_nafti.input_info']
        payaneh_buyers_model = self.env['sd_payaneh_nafti.buyers'].search([])
        payaneh_destinations_model = self.env['sd_payaneh_nafti.destinations'].search([])
        payaneh_contractors_model = self.env['sd_payaneh_nafti.contractors'].search([])
        payaneh_registration_model = self.env['sd_payaneh_nafti.contract_registration'].search([])
        buyers = [(b.name, b.id) for b in payaneh_buyers_model]
        destinations = [(d.name, d.id) for d in payaneh_destinations_model]
        contractors = [(c.name, c.id) for c in payaneh_contractors_model]
        registrations = [(reg.registration_no, reg.id) for reg in payaneh_registration_model]
        for data in data_model:
            try:
                if not data.document_no.isdigit():
                    data.write({'description': f'document_no is not a number: [{data.document_no}]'})
                    continue

                if data.loading_date.isdigit():
                    loading_date = jdatetime.date(jyear, jmonth, int(data.loading_date)).togregorian()
                else:
                    data.write({'description': f'loading_date is not a number: [{data.loading_date}]'})
                    continue

                # if data.registration_no.isdigit():
                #     registration_no = int(data.registration_no)
                # else:
                #     data.write({'description': f'registration_no is not a number: [{data.registration_no}]'})
                #     continue

                registration = list(filter(lambda d: d[0] == data.registration_no, registrations))
                if len(registration) == 0:
                    data.write({'description': _(f'There is no registration found\n {registration}')})
                    continue
                elif len(registration) > 1:
                    data.write({'description': _(f'There are multiple registration found \n {registration}')})
                    continue

                contractor = list(filter(lambda d: d[0] == data.contractor, contractors))
                if len(contractor) == 0:
                    data.write({'description': _(f'There is no destination found\n {contractor}')})
                    continue
                elif len(contractor) > 1:
                    data.write({'description': _(f'There are multiple destinations found \n {contractor}')})
                    continue
                # save new record
            except Exception as e:
                data.write({'description': f'calculations: {e}'})
                continue
            try:
                payaneh_data_model.create({'document_no': data.document_no,
                                           'loading_no': data.loading_no,
                                           'loading_date': loading_date,
                                           'registration_no': registration[0][1],
                                           'contractor': contractor[0][1],
                                           'driver': data.driver,
                                           'card_no': data.card_no,
                                           'plate_1': data.plate_1.split('.')[0],
                                           'plate_2': data.plate_2.split('.')[0],
                                           'plate_3': data.plate_3,
                                           'plate_4': data.plate_4.split('.')[0],
                                           'front_container': int(float(data.front_container)) if data.front_container.isdigit() else 0,
                                           'middle_container': int(float(data.middle_container)) if data.middle_container.isdigit() else 0,
                                           'back_container': int(float(data.back_container)) if data.back_container.isdigit() else 0,
                                           'centralized_container': data.centralized_container.lower(),
                                           'sp_gr': data.sp_gr,
                                           'temperature': int(float(data.temperature)) if data.temperature.isdigit() else False,
                                           'pressure': data.pressure,
                                           'meter_no': data.meter_no,
                                           'totalizer_start': data.totalizer_start,
                                           'totalizer_end': data.totalizer_end,
                                           'weighbridge': 'no' if data.weighbridge == 'خیر' else 'yes',
                                           'tanker_empty_weight': data.tanker_empty_weight,
                                           'tanker_full_weight': data.tanker_full_weight,
                                           'evacuation_box_seal': data.evacuation_box_seal,
                                           'compartment_1': data.compartment_1,
                                           'compartment_2': data.compartment_2,
                                           'compartment_3': data.compartment_3,
                                           'correction_factor': data.correction_factor,

                                           })
                data.write({'active': False, 'description': ''})
            except Exception as e:
                data.write({'description': f'save: {e}'})
                logging.error(f'save: {e}')
                print("-" * 60)
                print(traceback.format_exc())
                continue


class SdPayanehNaftiInputInfoInherit(models.Model):
    _inherit = 'sd_payaneh_nafti.input_info'

    def process_records(self):
        active_ids = self.env.context.get('active_ids')
        print(active_ids)
        records = self.browse(active_ids)
        for record in records:
            record.plate_1 = record.plate_1.split('.')[0]
            record.plate_2 = record.plate_2.split('.')[0]
            record.plate_4 = record.plate_4.split('.')[0]
