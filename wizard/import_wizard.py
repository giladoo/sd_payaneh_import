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


# #############################################################################
class SdPayanehImportImportWizard(models.TransientModel):
    _name = 'sd_payaneh_import.import.wizard'
    _description = 'Database Import Wizard'

    data_type = fields.Selection(selection=[('ثبت قرارداد', 'ثبت قرارداد'),
                                            ('اطلاعات ورودی ', 'اطلاعات ورودی '),], string='Data Type', default='اطلاعات ورودی ')

    excel_file = fields.Binary(required=True)
    excel_file_name = fields.Char()
    # sheet_names = fields.Selection(selection=sheet_list, string='Sheet Names', default='0')
    sheet_list = fields.Char()
    log_field = fields.Text()
    excel_file_rows = fields.Integer()
    start_row = fields.Integer(readonly=False, default=1)
    end_row = fields.Integer( readonly=False, default=10)

    # start_date = fields.Date(required=True, default=lambda self: date.today() )
    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    month = fields.Selection(lambda self: gc.get_months_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_months(),
                             string='Month', required=True,
                             default=lambda self: self._month_selector())
    year = fields.Selection(lambda self: gc.get_years_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_years(),
                            string='Year', required=True,
                            default=lambda self: self._year_selector())
    @api.onchange('excel_file', 'data_type')
    def _start_row(self):
        try:
            if self.excel_file:
                if self.excel_file and self.excel_file_name and (self.excel_file_name.split('.')[-1]).lower() in ['xlsx', 'xlsm']:
                    excel_file = base64.b64decode(self.excel_file)
                    excel_data = pd.read_excel(excel_file, sheet_name=self.data_type)
                    self.end_row = excel_data.index.stop + 1
                    self.excel_file_rows = excel_data.index.stop
        except Exception as e:
            raise ValidationError(_(e))

    @api.onchange('start_row', 'end_row')
    def _row_changed(self):
        if self.start_row < 1:
            self.start_row = 1
        elif self.start_row > self.excel_file_rows:
            self.start_row = self.excel_file_rows - 1

        if self.end_row < self.start_row:
            self.end_row = self.start_row + 1
        elif self.end_row > self.excel_file_rows:
            self.end_row = self.excel_file_rows

    # #############################################################################
    def hse_test_import(self):
        self.log_field = ''
        error_log = ''
        log_result = ''
        read_form = self.read()[0]
        data = {'form_data': read_form}
        data_type = read_form.get('data_type')
        registration_model = self.env['sd_payaneh_import.registration']
        all_registration_no = [rec.registration_no for rec in
                                    registration_model.search([('active', '=', True), ('active', '=', False)])]
        input_model = self.env['sd_payaneh_import.input']
        if read_form.get('excel_file'):
            if self.excel_file and self.excel_file_name and (self.excel_file_name.split('.')[-1]).lower() in ['xlsx', 'xlsm']:
                try:
                    # todo: persian and grogerian month
                    #   projec name
                    # sheet_data = [rec.sheet for rec in import_data]
                    excel_file = base64.b64decode(self.excel_file)
                    # bytestream = io.BytesIO(excel_file)
                    # bytestream.seek(0)
                    # wb = openpyxl.load_workbook(bytestream)
                    # sheets = wb.sheetnames
                    # # return
                    # if data_type not in sheets:
                    #     raise UserError(_(f'The file [{self.excel_file_name}] does not have a sheet of [{data_type}] '))

                    excel_data = pd.read_excel(excel_file, sheet_name=data_type)
                    print(f'\n{excel_data.iloc[0][3]}\n{excel_data.iloc[0]}\n')
                    if data_type == 'ثبت قرارداد':

                        for index in range(self.start_row -1, self.end_row):
                            if str(excel_data.iloc[index][0]) == '' or str(excel_data.iloc[index][0]).lower() == 'nan':
                                continue
                            if str(excel_data.iloc[index][0]) in all_registration_no:
                                continue

                            registration_model.create({'registration_no': excel_data.iloc[index][0] if str(excel_data.iloc[index][0]) != 'nan' else '',
                                                        'letter_no': excel_data.iloc[index][1] if str(excel_data.iloc[index][1]) != 'nan' else '',
                                                        'contract_no': excel_data.iloc[index][2] if str(excel_data.iloc[index][2]) != 'nan' else '',
                                                        'order_no': excel_data.iloc[index][3] if str(excel_data.iloc[index][3]) != 'nan' else '',
                                                        'buyer': excel_data.iloc[index][4].strip() if str(excel_data.iloc[index][4]) != 'nan' else '',
                                                        'amount': excel_data.iloc[index][5] if str(excel_data.iloc[index][5]) != 'nan' else '',
                                                        'unit': excel_data.iloc[index][6] if str(excel_data.iloc[index][6]) != 'nan' else '',
                                                        'contract_type': excel_data.iloc[index][7] if str(excel_data.iloc[index][7]) != 'nan' else '',
                                                        'loading_type': excel_data.iloc[index][8] if str(excel_data.iloc[index][8]) != 'nan' else '',
                                                        'start_date': excel_data.iloc[index][9] if str(excel_data.iloc[index][9]) != 'nan' else '',
                                                        'end_date': excel_data.iloc[index][10] if str(excel_data.iloc[index][10]) != 'nan' else '',
                                                        'destination': excel_data.iloc[index][11].strip() if str(excel_data.iloc[index][11]) != 'nan' else '',

                                                        'contractor1': excel_data.iloc[index][13].strip() if str(excel_data.iloc[index][13]) != 'nan' else '',
                                                        'contractor2': excel_data.iloc[index][14].strip() if str(excel_data.iloc[index][14]) != 'nan' else '',
                                                        'contractor3': excel_data.iloc[index][15].strip() if str(excel_data.iloc[index][15]) != 'nan' else '',
                                                        'contractor4': excel_data.iloc[index][16].strip() if str(excel_data.iloc[index][16]) != 'nan' else '',
                                                        'contractor5': excel_data.iloc[index][17].strip() if str(excel_data.iloc[index][17]) != 'nan' else '',

                                                        'first_extend_no': excel_data.iloc[index][18] if str(excel_data.iloc[index][18]) != 'nan' else '',
                                                        'first_extend_star_date': excel_data.iloc[index][19] if str(excel_data.iloc[index][19]) != 'nan' else '',
                                                        'first_extend_end_date': excel_data.iloc[index][20] if str(excel_data.iloc[index][20]) != 'nan' else '',

                                                        'second_extend_no': excel_data.iloc[index][21] if str(excel_data.iloc[index][21]) != 'nan' else '',
                                                        'second_extend_star_date': excel_data.iloc[index][22] if str(excel_data.iloc[index][22]) != 'nan' else '',
                                                        'second_extend_end_date': excel_data.iloc[index][23] if str(excel_data.iloc[index][23]) != 'nan' else '',})

                    if data_type == 'اطلاعات ورودی ':
                        for index in range(self.start_row -1, self.end_row):
                            if str(excel_data.iloc[index][0]) == '' or str(excel_data.iloc[index][0]).lower() == 'nan':
                                continue
                            input_model.create({'document_no': excel_data.iloc[index][1] if str(excel_data.iloc[index][1]) != 'nan' else '',
                                                       'loading_no': excel_data.iloc[index][2] if str(excel_data.iloc[index][2]) != 'nan' else '',
                                                       'loading_date': excel_data.iloc[index][3] if str(excel_data.iloc[index][3]) != 'nan' else '',
                                                       'registration_no': excel_data.iloc[index][4] if str(excel_data.iloc[index][4]) != 'nan' else '',
                                                       'contractor': excel_data.iloc[index][5].strip() if str(excel_data.iloc[index][5]) != 'nan' else '',
                                                       'buyer': excel_data.iloc[index][6].strip() if str(excel_data.iloc[index][6]) != 'nan' else '',
                                                       'driver': excel_data.iloc[index][7].strip() if str(excel_data.iloc[index][7]) != 'nan' else '',
                                                       'card_no': excel_data.iloc[index][8] if str(excel_data.iloc[index][8]) != 'nan' else '',
                                                       'plate_1': excel_data.iloc[index][9] if str(excel_data.iloc[index][9]) != 'nan' else '',
                                                       'plate_2': excel_data.iloc[index][10] if str(excel_data.iloc[index][10]) != 'nan' else '',
                                                       'plate_3': excel_data.iloc[index][11] if str(excel_data.iloc[index][11]) != 'nan' else '',
                                                       'plate_4': excel_data.iloc[index][12] if str(excel_data.iloc[index][12]) != 'nan' else '',

                                                       'front_container': excel_data.iloc[index][14] if str(excel_data.iloc[index][14]) != 'nan' else '',
                                                       'middle_container': excel_data.iloc[index][15] if str(excel_data.iloc[index][15]) != 'nan' else '',
                                                       'back_container': excel_data.iloc[index][16] if str(excel_data.iloc[index][16]) != 'nan' else '',

                                                       'centralized_container': excel_data.iloc[index][18] if str(excel_data.iloc[index][18]) != 'nan' else '',
                                                       'sp_gr': excel_data.iloc[index][19] if str(excel_data.iloc[index][19]) != 'nan' else '',
                                                       'temperature': excel_data.iloc[index][20] if str(excel_data.iloc[index][20]) != 'nan' else '',
                                                       'pressure': excel_data.iloc[index][21] if str(excel_data.iloc[index][21]) != 'nan' else '',

                                                       'weighbridge': excel_data.iloc[index][23] if str(excel_data.iloc[index][23]) != 'nan' else '',
                                                       'meter_no': excel_data.iloc[index][24] if str(excel_data.iloc[index][24]) != 'nan' else '',
                                                       'totalizer_start': excel_data.iloc[index][25] if str(excel_data.iloc[index][25]) != 'nan' else '',
                                                       'totalizer_end': excel_data.iloc[index][26] if str(excel_data.iloc[index][26]) != 'nan' else '',
                                                       'totalizer_difference': excel_data.iloc[index][27] if str(excel_data.iloc[index][27]) != 'nan' else '',
                                                       'tanker_empty_weight': excel_data.iloc[index][28] if str(excel_data.iloc[index][28]) != 'nan' else '',
                                                       'tanker_full_weight': excel_data.iloc[index][29] if str(excel_data.iloc[index][29]) != 'nan' else '',
                                                       'tanker_pure_weight': excel_data.iloc[index][30] if str(excel_data.iloc[index][30]) != 'nan' else '',
                                                       'evacuation_box_seal': excel_data.iloc[index][31] if str(excel_data.iloc[index][31]) != 'nan' else '',
                                                       'compartment_1': excel_data.iloc[index][32] if str(excel_data.iloc[index][32]) != 'nan' else '',
                                                       'compartment_2': excel_data.iloc[index][33] if str(excel_data.iloc[index][33]) != 'nan' else '',
                                                       'compartment_3': excel_data.iloc[index][34] if str(excel_data.iloc[index][34]) != 'nan' else '',
                                                       'correction_factor': excel_data.iloc[index][35] if str(excel_data.iloc[index][35]) != 'nan' else '',
                                                       'rec_api': excel_data.iloc[index][36] if str(excel_data.iloc[index][36]) != 'nan' else '',
                                                       'temperature_f': excel_data.iloc[index][37] if str(excel_data.iloc[index][37]) != 'nan' else '',
                                                       'pressure_psi': excel_data.iloc[index][38] if str(excel_data.iloc[index][38]) != 'nan' else '',
                                                       'ctl': excel_data.iloc[index][39] if str(excel_data.iloc[index][39]) != 'nan' else '',
                                                       'cpl': excel_data.iloc[index][40] if str(excel_data.iloc[index][40]) != 'nan' else '',
                                                       'tab_13': excel_data.iloc[index][41] if str(excel_data.iloc[index][41]) != 'nan' else '',
                                                       'meter_tov_l': excel_data.iloc[index][42] if str(excel_data.iloc[index][42]) != 'nan' else '',
                                                       'meter_gsv_l': excel_data.iloc[index][43] if str(excel_data.iloc[index][43]) != 'nan' else '',
                                                       'meter_gsv_b': excel_data.iloc[index][44] if str(excel_data.iloc[index][44]) != 'nan' else '',
                                                       'meter_mt': excel_data.iloc[index][45] if str(excel_data.iloc[index][45]) != 'nan' else '',
                                                       'wb_tov_l': excel_data.iloc[index][46] if str(excel_data.iloc[index][46]) != 'nan' else '',
                                                       'wb_gsv_l': excel_data.iloc[index][47] if str(excel_data.iloc[index][47]) != 'nan' else '',
                                                       'wb_gsv_b': excel_data.iloc[index][48] if str(excel_data.iloc[index][48]) != 'nan' else '',
                                                       'wb_mt': excel_data.iloc[index][49] if str(excel_data.iloc[index][49]) != 'nan' else '',
                                                       'final_tov_l': excel_data.iloc[index][50] if str(excel_data.iloc[index][50]) != 'nan' else '',
                                                       'final_gsv_l': excel_data.iloc[index][51] if str(excel_data.iloc[index][51]) != 'nan' else '',
                                                       'final_gsv_b': excel_data.iloc[index][52] if str(excel_data.iloc[index][52]) != 'nan' else '',
                                                       'final_mt': excel_data.iloc[index][53] if str(excel_data.iloc[index][53]) != 'nan' else '',
                                                       'jyear': int(self.year),
                                                        'jmonth': int(self.month),
                                                       })

                except Exception as e:
                    logging.error(f'hse_test_import: {e}')
                    raise UserError(_(f'File read Error: {e}'))
            elif self.excel_file_name:
                self.excel_file = ''
                self.excel_file_name = ''
                raise UserError(_(f'Try again! select a .xlsx file '))
        # self.log_field += tabulate(log_result, headers=['Project', 'Date', 'File', 'Sheet'],tablefmt='orgtbl')
        # t = PrettyTable(['Project', 'Date', 'File', 'Sheet'])
        # t.add_rows(log_result)
        # print(t)
        # self.log_field += str(t)
        self.log_field += 'Ignored Sheets:\n' + error_log
        self.log_field += '\n----------------------------------------------------\n'
        self.log_field += log_result

        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'sd_payaneh_import.import.wizard',
                'target': 'new',
                'res_id': self.id,
                }

    def hse_close(self):
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def _year_selector(self):
        # todo: timezone is needed to make sure date after 8 pm is correct
        this_date = datetime.now()
        if self.env.context.get('lang') == 'fa_IR':
            s_this_year = jdatetime.date.fromgregorian(date=this_date).strftime("%Y")
        else:
            s_this_year = this_date.strftime("%Y")
        return s_this_year
    def _month_selector(self):
        # todo: timezone is needed to make sure date after 8 pm is correct
        this_date = datetime.now()
        if self.env.context.get('lang') == 'fa_IR':
            s_this_month = jdatetime.date.fromgregorian(date=this_date).strftime("%m")
        else:
            s_this_month = this_date.strftime("%m")
        return s_this_month
