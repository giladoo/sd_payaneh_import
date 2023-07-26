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


# #############################################################################
class SdHseImportClearWizard(models.TransientModel):
    _name = 'sd_payaneh_import.clear.wizard'
    _description = 'HSE Database clear Wizard'

    def _project_domain(self):
        partner_id = self.env.user.partner_id
        projects = self.env['sd_hse.project'].search(['|',
                                                      ('hse_managers', 'in', partner_id.id),
                                                      ('hse_officers', 'in', partner_id.id),])
        return [('id', 'in', projects.ids)]

    project = fields.Many2many('sd_hse.project', required=True,
                              domain=lambda self: self._project_domain(), tracking=True,
                              default=lambda self: self.project.search(
                                  ['|', ('hse_managers', 'in', self.env.user.partner_id.id),
                                   ('hse_officers', 'in', self.env.user.partner_id.id)], limit=1))
    clear_all = fields.Boolean()
    start_date = fields.Date()
    end_date = fields.Date()
    log_field = fields.Text()


    # start_date = fields.Date(required=True, default=lambda self: date.today() )
    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    # #############################################################################
    def hse_import_test(self,):
        self.hse_import_clear(True)
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'sd_payaneh_import.clear.wizard',
                'target': 'new',
                'res_id': self.id,
                }
    # #############################################################################
    def hse_import_clear(self, istest=False):
        self.log_field = ''
        error_log = ''
        log_result = ''
        read_form = self.read()[0]
        data = {'form_data': read_form}
        error_log = f'{read_form.get("project")} {read_form.get("start_date")}   {read_form.get("end_date")}'
        error_log += f'{read_form.get("project")} {type(read_form.get("start_date"))}   {type(read_form.get("end_date"))}'
        projects = read_form.get("project")
        clear_all = read_form.get("clear_all")
        start_date = read_form.get('start_date')
        end_date = read_form.get('end_date')

        project_model = self.env['sd_hse.project']
        personnel_model = self.env['sd_hse.personnel']
        weather_model = self.env['sd_hse.weather']
        incident_model = self.env['sd_hse.incident']
        training_model = self.env['sd_hse.training']
        drill_model = self.env['sd_hse.drill']
        anomaly_model = self.env['sd_hse.anomaly']
        permit_model = self.env['sd_hse.permit']
        actions_model = self.env['sd_hse.actions']
        for project_id in projects:
            report = ''
            search_domain = [('project', '=', project_id)] if clear_all else [('record_date', '>=', start_date),
                                                                                ('record_date', '<=', end_date),
                                                                                ('project', '=', project_id),]

            records = personnel_model.search(search_domain)
            report += f'Personnel: {len(records) if records else 0}\n'
            if records and not istest:
                records.unlink()

            records =weather_model.search(search_domain)
            report += f'weather: {len(records) if records else 0}\n'
            if records and not istest:
                records.unlink()

            records =incident_model.search(search_domain)
            report += f'Incident: {len(records) if records else 0}\n'
            if records and not istest:
                records.unlink()

            records =training_model.search(search_domain)
            report += f'Training: {len(records) if records else 0}\n'
            if records and not istest:
                records.unlink()

            records =drill_model.search(search_domain)
            report += f'Drill: {len(records)}\n'
            if records and not istest:
                records.unlink()

            records =anomaly_model.search(search_domain)
            report += f'Anomaly: {len(records) if records else 0}\n'
            if records and not istest:
                records.unlink()

            records =permit_model.search(search_domain)
            report += f'Permit: {len(records) if records else 0}\n'
            if records and not istest:
                records.unlink()

            records =actions_model.search(search_domain)
            report += f'Actions: {len(records) if records else 0}\n'
            if records and not istest:
                records.unlink()
            self.log_field += f'\n---------------------- {project_model.browse(project_id).name} ------------------------------\n'
            self.log_field += report


        self.log_field += 'Ignored Sheets:\n' + error_log


        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'sd_payaneh_import.clear.wizard',
                'target': 'new',
                'res_id': self.id,
                }

    def hse_close(self):
        return {'type': 'ir.actions.client', 'tag': 'reload'}

