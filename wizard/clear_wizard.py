# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
import jdatetime
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
import pandas as pd
import base64
from lxml import etree
import openpyxl
import io
# from tabulate import tabulate
# from prettytable import PrettyTable
from . import get_calendare as gc
import warnings

# #############################################################################
class SdPayanehImportClearWizard(models.TransientModel):
    _name = 'sd_payaneh_import.clear.wizard'
    _description = 'Database Clear Wizard'

    data_type = fields.Selection(selection=[('inputs', 'Inputs'),
                                            ('registrations', 'Registrations'),

                                            ], default='inputs')

    count = fields.Integer(default=1000)

    def process_clear(self):
        error_index = 0
        if self.data_type == 'inputs':
            input_recs = self.env['sd_payaneh_nafti.input_info'].search([], limit=self.count)
            if len(input_recs) > 0:
                for input_rec in input_recs:
                    try:
                        input_rec.unlink()
                    except Exception as e:
                        error_index += 1
                        logging.error(f'[process_clear]: {e}')
                        if error_index > 5:
                            logging.error(f'[process_clear]: More than 5 errors')
                            break


