# -*- coding: utf-8 -*-
import datetime
from datetime import  timedelta
# import random

from odoo import models, fields, api
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError

from colorama import Fore
import random
import logging
import traceback

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

