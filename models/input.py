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
    remain_amount = fields.Char()
    loading_date = fields.Char()
    registration_no = fields.Char()
    buyer = fields.Char()
    contractor = fields.Char()
    driver = fields.Char()
    driver_m = fields.Many2one('sd_payaneh_nafti.drivers')
    card_no = fields.Char()
    truck_plate = fields.Char()
    truck = fields.Many2one('sd_payaneh_nafti.trucks')
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
    jyear = fields.Integer()
    jmonth = fields.Integer()

    def process_bunch(self):
        self.process_drivers(True)
        self.process_trucks(True)
        self.process_records(True)

    def process_drivers(self, bunch=False):
        active_ids = self.env.context.get('active_ids')
        if bunch:
            records = self.search([], limit=1000)
        else:
            records = self.browse(active_ids)
        drivers_model = self.env['sd_payaneh_nafti.drivers']
        for rec in records:
            if not drivers_model.search([('card_no', '=', rec.card_no)]):
                drivers_model.create({'name': rec.driver, 'card_no': rec.card_no})
            drivers = drivers_model.search([('card_no', '=', rec.card_no)])
            if len(drivers) == 1:
                rec.write({'driver_m': drivers.id, 'description': f'' })
            elif len(drivers) == 0:
                rec.write({'description': f'No driver: [{rec.card_no}]'})
            else:
                rec.write({'description': f'Multiple drivers: [{rec.card_no}]'})
    def process_trucks(self, bunch=False):
        active_ids = self.env.context.get('active_ids')
        if bunch:
            records = self.search([], limit=2000)
        else:
            records = self.browse(active_ids)
        trucks_model = self.env['sd_payaneh_nafti.trucks']
        trucks_all = self.env['sd_payaneh_nafti.trucks'].search([])
        records_trucks = set()

        # create a list of unique plate numbers
        for rec in records:
            if not (rec.plate_1).isdigit():
                continue
            plate_1 = str(int(float(rec.plate_1)))
            plate_2 = str(int(float(rec.plate_2)))
            plate_3 = str(rec.plate_3)
            plate_4 = str(int(float(rec.plate_4)))
            records_trucks.add((plate_1, plate_2, plate_3, plate_4, ))
            rec.truck_plate = f'[ {plate_4}  {plate_3}  {plate_2} ]  [ {plate_1} ]'

        # create new truck if there is no plane
        for records_truck in records_trucks:
            truck = [trk.id for trk in trucks_all
                     if records_truck[0] == trk.plate_1
                     and records_truck[1] == trk.plate_2
                     and records_truck[2] == trk.plate_3
                     and records_truck[3] == trk.plate_4]
            if len(truck) == 0:
                new_truck = trucks_model.create({'plate_1': records_truck[0],
                                                 'plate_2': records_truck[1],
                                                 'plate_3': records_truck[2],
                                                 'plate_4': records_truck[3],})
            else:
                pass

        # link the plate to the input data
        trucks_all = self.env['sd_payaneh_nafti.trucks'].search([])
        for rec in records:
            if not (rec.plate_1).isdigit():
                continue
            plate_1 = str(int(float(rec.plate_1)))
            plate_2 = str(int(float(rec.plate_2)))
            plate_3 = str(rec.plate_3)
            plate_4 = str(int(float(rec.plate_4)))
            truck = [trk.id for trk in trucks_all
                     if plate_1 == trk.plate_1
                     and plate_2 == trk.plate_2
                     and plate_3 == trk.plate_3
                     and plate_4 == trk.plate_4]
            if len(truck) == 1:
                rec.write({'truck': truck[0], 'description': 'Truck Linked', })
            if len(truck) > 1:
                rec.write({'truck': truck[0], 'description': 'Truck multi', })
            else:
                rec.write({'description': 'Truck mismatch', })


    def process_records(self, bunch=False):
        active_ids = self.env.context.get('active_ids')
        # print(f'\n {active_ids}')
        # jyear = 1402
        # jmonth = 4
        # data_model = self.browse(active_ids)
        if bunch:
            data_model = self.search([], limit=2000)
        else:
            data_model = self.browse(active_ids)

        payaneh_data_model = self.env['sd_payaneh_nafti.input_info'].search([])
        payaneh_buyers_model = self.env['sd_payaneh_nafti.buyers'].search([])
        payaneh_destinations_model = self.env['sd_payaneh_nafti.destinations'].search([])
        payaneh_contractors_model = self.env['sd_payaneh_nafti.contractors'].search([])
        payaneh_drivers_model = self.env['sd_payaneh_nafti.drivers'].search([])
        payaneh_registration_model = self.env['sd_payaneh_nafti.contract_registration'].search([])
        buyers = [(b.name, b.id) for b in payaneh_buyers_model]
        destinations = [(d.name, d.id) for d in payaneh_destinations_model]
        contractors = [(c.name, c.id) for c in payaneh_contractors_model]
        drivers = [(c.card_no, c.id) for c in payaneh_drivers_model]
        registrations = [(reg.registration_no, reg.id) for reg in payaneh_registration_model]
        input_infos = [(info.document_no, info.id) for info in payaneh_data_model]
        for data in data_model:
            try:
                if not data.document_no.isdigit():
                    data.write({'description': f'document_no is not a number: [{data.document_no}]'})
                    continue
                info_record = list(filter(lambda r: r.document_no == int(data.document_no), payaneh_data_model))
                if len(info_record) != 0:
                    if len(info_record) == 1 and info_record[0].totalizer_start > 0:
                        data.write({'active': False, 'description': f'document_no is exist: [{data.document_no}]'})
                    elif len(info_record) == 1 and info_record[0].totalizer_start == 0:
                        data.write({'description': f'document_no is exist: update needed'})

                    elif len(info_record) > 1:
                        data.write({'description': f'Multiple of document_no exist: [{data.document_no}]'})

                    continue

                if data.loading_date.isdigit():
                    loading_date = jdatetime.date(data.jyear, data.jmonth, int(data.loading_date)).togregorian()
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
                    data.write({'description': _(f'There is no contractor found\n {contractor}')})
                    continue
                elif len(contractor) > 1:
                    data.write({'description': _(f'There are multiple contractor found \n {contractor}')})
                    continue

                driver = list(filter(lambda d: d[0] == data.driver_m.card_no, drivers))
                if len(driver) == 0:
                    data.write({'description': _(f'There is no driver found\n {driver}')})
                    continue
                elif len(driver) > 1:
                    data.write({'description': _(f'There are multiple driver found \n {driver}')})
                    continue
                if not data.truck.id > 0:
                    data.write({'description': _(f'Truck No Empty')})
                    continue
                # save new record
            except Exception as e:
                data.write({'description': f'calculations: {e}'})
                continue
            try:
                input_id = payaneh_data_model.create({'document_no': int(data.document_no),
                                           'remain_amount_old': data.remain_amount,
                                           'loading_no': data.loading_no,
                                           'request_date': loading_date,
                                           'loading_date': loading_date,
                                           'registration_no': registration[0][1],
                                           'contractor': contractor[0][1],
                                           # 'driver': driver[0][1],
                                           'driver': data.driver_m.id,
                                           'truck_no': data.truck.id,
                                           # 'plate_1': data.plate_1.split('.')[0],
                                           # 'plate_2': data.plate_2.split('.')[0],
                                           # 'plate_3': data.plate_3,
                                           # 'plate_4': data.plate_4.split('.')[0],
                                           'front_container': int(float(data.front_container)) if data.front_container and data.front_container.isdigit() else 0,
                                           'middle_container': int(float(data.middle_container)) if data.middle_container and data.middle_container.isdigit() else 0,
                                           'back_container': int(float(data.back_container)) if data.back_container and data.back_container.isdigit() else 0,
                                           'centralized_container': data.centralized_container.lower(),
                                           'sp_gr': data.sp_gr,
                                           'temperature': int(float(data.temperature)) if data.temperature and data.temperature.isdigit() else False,
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
                input_id.write({'sp_gr': data.sp_gr})
                data.write({'active': False, 'description': ''})
            except Exception as e:
                data.write({'description': f'save: {e}'})
                logging.error(f'save: {e}')
                print("-" * 60)
                print(traceback.format_exc())
                continue

    def process_contractors(self):
        active_ids = self.env.context.get('active_ids')
        records = self.browse(active_ids)
        payaneh_contractors_model = self.env['sd_payaneh_nafti.contractors'].search([])
        contractors = list([(c.name.strip(), c.id) for c in payaneh_contractors_model if c.name.strip() != '']) if len(
            payaneh_contractors_model) > 0 else []
        for rec in records:
            rec_item = rec.contractor.strip()
            # if not payaneh_contractors_model.search([('name', '=', rec_item)]):
            if rec_item == '':
                continue
            if len(contractors) == 0 or len(list(filter(lambda x: x[0] == rec_item, contractors))) == 0:
                try:
                    new_rec = payaneh_contractors_model.create({'name': rec_item})
                    contractors.append((rec_item, new_rec.id))
                    rec.write({'description': _(f'CREATED')})
                except Exception as er:
                    rec.write({'description': _(f'ERROR: {er}')})
            else:
                rec.write({'description': _(f'EXISTS')})

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
