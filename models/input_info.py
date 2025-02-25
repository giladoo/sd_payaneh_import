# -*- coding: utf-8 -*-
import datetime
from datetime import  timedelta
from time import time

from odoo import models, fields, api
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError

from colorama import Fore
import random
import logging
import traceback
from icecream import ic

class SdPayanehNaftiInputInfoAmount(models.Model):
    _inherit = 'sd_payaneh_nafti.input_info'

    remain_amount_old = fields.Float()

    def make_done(self):
        active_ids = self.env.context.get('active_ids')
        # print(f'--------> active_ids: {active_ids}')
        selected = self.browse(active_ids)
        new_data = {}
        for rec in selected:
            if rec.state != 'done':
                new_data['state'] = 'done'
                rec.write(new_data)

    def make_finished(self):
        active_ids = self.env.context.get('active_ids')
        # print(f'--------> active_ids: {active_ids}')
        selected = filter(lambda x: x.state != 'finished',  self.browse(active_ids))
        print(f'''
            selected: {selected}
''')
        new_data = {}
        for rec in selected:
            new_data['state'] = 'finished'
            rec.write(new_data)
    def update_loading_info_date(self):
        active_ids = self.env.context.get('active_ids')
        # print(f'--------> active_ids: {active_ids}')
        selected = self.browse(active_ids)
        new_data = {}
        for rec in selected:
            new_data['loading_date'] = rec.request_date
            new_data['loading_info_date'] = rec.request_date
            rec.write(new_data)


    def update_loading_info_date_all(self):
        # active_ids = self.env.context.get('active_ids')
        # print(f'--------> active_ids: {active_ids}')
        selected = self.search([])
        new_data = {}
        for rec in selected:
            new_data['loading_date'] = rec.request_date
            new_data['loading_info_date'] = rec.request_date
            rec.write(new_data)


    def set_master_meter(self):
        active_ids = self.env.context.get('active_ids')
        # print(f'--------> active_ids: {active_ids}')
        selected = self.browse(active_ids)
        new_data = {}
        for rec in selected:
            print(f''' >>>>>>>>>>>>>>>>>>>>>>>>>>
                rec.meter_no: {rec.meter_no}
                rec.totalizer_start: {rec.totalizer_start}
''')
            if not rec.meter_no and rec.totalizer_start:
                new_data['meter_no'] = '0'
                rec.write(new_data)


    def update_lockers(self, active_ids=[]):
        lockers_model = self.env['sd_payaneh_nafti.lockers']
        lcoker_types = self.env['sd_payaneh_nafti.locker_type'].search([])
        locer_types_dict = dict({rec.name: rec.id for rec in lcoker_types})

        input_locker_list = ['evacuation_box_seal', 'compartment_1', 'compartment_2', 'compartment_3', ]
        input_locker_dict = {'evacuation_box_seal': locer_types_dict.get('Evacuation Box'),
                             'compartment_1': locer_types_dict.get('Compartment 1'),
                             'compartment_2': locer_types_dict.get('Compartment 2'),
                             'compartment_3': locer_types_dict.get('Compartment 3'), }
        # ic(locer_types_dict)

        # return
        active_ids = active_ids if active_ids else self.env.context.get('active_ids')
        limit_time_cpu = self.env['ir.config_parameter'].sudo().get_param('limit_time_cpu') or 180

        chunk_list = 500
        total_time = 0
        total_count = 0
        active_ids_lists = [active_ids[i:i + chunk_list] for i in range(0, len(active_ids), chunk_list)]
        # old_lockers = lockers_model.search_read([], ['locker_no'])
        # old_lockers_list = list([rec.get('locker_no').upper() for rec in old_lockers])
        logging.info(f"\n [TOTAL] active_ids: {len(active_ids)} \n")
        st = time()
        for active_id_list in active_ids_lists:
            st1 = time()
            input_infos = self.search_read([
                ('id', 'in', active_id_list),
                ('evacuation_box_seal', 'not in', ['', ' '])
            ], ['document_no'] + input_locker_list)
            # TODO: A report of empty lockers needed.

            # logging.info(f"\n len(active_id_list): {len(active_id_list)} input_infos[0]: {input_infos[0]}")

            for input_info in input_infos:
                for locker_name in input_locker_list:
                    if input_info.get(locker_name) :
                        locker_no = (input_info.get(locker_name)).upper()
                        locker_exists = lockers_model.search_count([('locker_no', '=', locker_no), ('input_info', '=', input_info.get('id'))])
                        if locker_exists:
                            continue
                        lockers_model.create({
                            'locker_no': locker_no,
                            'input_info': input_info.get('id'),
                            'locker_type': input_locker_dict.get(locker_name),
                        })
                        # old_lockers_list.append(input_info.get(locker_name))
            total_count += len(active_id_list)
            total_time += round(time() - st1, 0)
            time_rate = round(total_time / limit_time_cpu, 2)
            logging.info(f"\n [TOTAL] total_count: {total_count}  total_time: {total_time} limit_time_cpu: {limit_time_cpu} time_rate: {time_rate}\n")
            if time_rate > .85:
                break

    def update_all_lockers(self):
        lockers = self.env['sd_payaneh_nafti.lockers'].search_read([], ['input_info'],)
        lockers_ids = list(set([rec.get('input_info')[0] for rec in lockers if rec.get('input_info')])) if lockers else []
        all_records = self.search_count([('id', 'not in', lockers_ids), ('evacuation_box_seal', 'not in', ['', ' ']), ])
        logging.info(f"\n================= lockers: {len(lockers)}  all_records: {all_records} \n {lockers[:5]}\n ")
        self.update_lockers(self.search([('id', 'not in', lockers_ids), ('evacuation_box_seal', 'not in', ['', ' ']), ], limit=10000).ids)



