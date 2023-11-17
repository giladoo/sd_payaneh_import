# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import jdatetime
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
import logging
import re

class SdPaynehImpoertRegistration(models.Model):
    _name = 'sd_payaneh_import.registration'
    _description = 'sd_payaneh_import.registration'

    active = fields.Boolean(default=True)
    registration_no = fields.Char()
    letter_no = fields.Char()
    contract_no = fields.Char()
    order_no = fields.Char()
    buyer = fields.Char()
    amount = fields.Char()
    unit = fields.Char()
    contract_type = fields.Char()
    loading_type = fields.Char()
    start_date = fields.Char()
    end_date = fields.Char()
    destination = fields.Char()
    contractor1 = fields.Char()
    contractor2 = fields.Char()
    contractor3 = fields.Char()
    contractor4 = fields.Char()
    contractor5 = fields.Char()

    first_extend_no = fields.Char()
    first_extend_star_date = fields.Char()
    first_extend_end_date = fields.Char()

    second_extend_no = fields.Char()
    second_extend_star_date = fields.Char()
    second_extend_end_date = fields.Char()

    description = fields.Char()

    def process_buyers(self):
        active_ids = self.env.context.get('active_ids')
        # print(f'\n {active_ids}')
        data_model = self.browse(active_ids)
        payaneh_data_model = self.env['sd_payaneh_nafti.contract_registration']
        payaneh_buyers_model = self.env['sd_payaneh_nafti.buyers'].search([])
        payaneh_destinations_model = self.env['sd_payaneh_nafti.destinations'].search([])
        payaneh_contractors_model = self.env['sd_payaneh_nafti.contractors'].search([])
        for rec in data_model:
            rec_item = rec.buyer.strip()
            if not payaneh_buyers_model.search([('name', '=', rec_item)]):
                try:
                    payaneh_buyers_model.create({'name': rec_item})
                    rec.write({'description': _(f'CREATED')})
                except Exception as er:
                    rec.write({'description': _(f'ERROR: {er}')})
            else:
                rec.write({'description': _(f'EXISTS')})

    def process_contractors(self):
        active_ids = self.env.context.get('active_ids')
        # print(f'\n {active_ids}')
        data_model = self.browse(active_ids)
        payaneh_data_model = self.env['sd_payaneh_nafti.contract_registration']
        payaneh_buyers_model = self.env['sd_payaneh_nafti.buyers'].search([])
        payaneh_destinations_model = self.env['sd_payaneh_nafti.destinations'].search([])
        payaneh_contractors_model = self.env['sd_payaneh_nafti.contractors'].search([])
        for rec in data_model:
            for cont in [rec.contractor1, rec.contractor2, rec.contractor3, rec.contractor4, rec.contractor5, ]:
                rec_item = cont.strip()
                if not payaneh_contractors_model.search([('name', '=', rec_item)]):
                    try:
                        payaneh_contractors_model.create({'name': rec_item})
                        rec.write({'description': _(f'CREATED')})
                    except Exception as er:
                        rec.write({'description': _(f'ERROR: {er}')})
                else:
                    rec.write({'description': _(f'EXISTS')})

    def process_destinations(self):
        active_ids = self.env.context.get('active_ids')
        # print(f'\n {active_ids}')
        data_model = self.browse(active_ids)
        payaneh_data_model = self.env['sd_payaneh_nafti.contract_registration']
        payaneh_buyers_model = self.env['sd_payaneh_nafti.buyers'].search([])
        payaneh_destinations_model = self.env['sd_payaneh_nafti.destinations'].search([])
        payaneh_contractors_model = self.env['sd_payaneh_nafti.contractors'].search([])
        for rec in data_model:
            rec_item = rec.destination.strip()
            if not payaneh_destinations_model.search([('name', '=', rec_item)]):
                try:
                    payaneh_destinations_model.create({'name': rec_item})
                    rec.write({'description': _(f'CREATED')})
                except Exception as er:
                    rec.write({'description': _(f'ERROR: {er}')})
            else:
                rec.write({'description': _(f'EXISTS')})
    def process_registrations(self):
        active_ids = self.env.context.get('active_ids')
        # print(f'\nactive_ids {active_ids}')
        data_model = self.browse(active_ids)
        registration_no_list = ()
        registration_id_list = ()
        data_model_ids = dict(((rec.registration_no, rec.id) for rec in data_model))
        # print(f'\ndata_model_ids: {data_model_ids}')

        # for key, value in data_model_ids.items():
        #     if key not in registration_no_list:
        #         registration_no_list.append(key)
        #         registration_id_list.append(value)
        data_model = self.browse(data_model_ids.values())
        # print(f'\ndata_model: {data_model}')

        payaneh_data_model = self.env['sd_payaneh_nafti.contract_registration']
        payaneh_buyers_model = self.env['sd_payaneh_nafti.buyers'].search([])
        payaneh_destinations_model = self.env['sd_payaneh_nafti.destinations'].search([])
        payaneh_contractors_model = self.env['sd_payaneh_nafti.contractors'].search([])
        registrations = ([(r.registration_no, r.id) for r in payaneh_data_model.search([])])
        buyers = [(b.name, b.id) for b in payaneh_buyers_model]
        destinations = [(d.name, d.id) for d in payaneh_destinations_model]
        contractors = [(c.name, c.id) for c in payaneh_contractors_model]

        for data in data_model:
            # buyer
            logging.error(f'\n buyer:')
            if len(list((r[0] for r in registrations if r[0] == str(data.registration_no).split('.')[0]))) != 0:
                data.write({'active': False, 'description': f'registration_no is exist: [{data.registration_no}]'})
                continue

            buyer = list(filter(lambda b: b[0] == data.buyer, buyers))
            if len(buyer) == 0:
                data.write({'description': _('There is no buyer found')})
                continue
            if len(buyer) > 1:
                data.write({'description': _(f'There are multiple buyers found \n {buyer}')})
                continue
            # destination
            logging.error(f'\n destination:')
            destination = list(filter(lambda d: d[0] == data.destination, destinations))
            if len(destination) == 0:
                data.write({'description': _('There is no destination found')})
                continue
            if len(destination) > 1:
                data.write({'description': _(f'There are multiple destinations found \n {destination}')})
                continue

            # contractors
            logging.error(f'\n contractors:')
            contractors_list = []
            contractor_error = False
            for data_contractor in [data.contractor1, data.contractor2, data.contractor3, data.contractor4, data.contractor5]:
                if data_contractor == '':
                    continue
                contractor = list(filter(lambda d: d[0] == data_contractor, contractors))
                if len(contractor) == 0:
                    data.write({'description': _(f'There is no contractor found\n {data_contractor}')})
                    contractor_error = True
                    break
                elif len(contractor) > 1:
                    data.write({'description': _(f'There are multiple contractors found \n {contractor}')})
                    contractor_error = True
                    break
                else:
                    contractors_list.append(contractor[0][1])
            if contractor_error:
                continue
            # print(f'\n int(float(data.registration_no)): {int(float(data.registration_no))}')

            try:
                # datetime
                logging.error(f'\n datetime:')
                dt = re.findall( '([\d]{4})/([\d]{1,2})/([\d]{1,2})', data.start_date)
                if dt:
                    start_date = jdatetime.date(int(dt[0][0]), int(dt[0][1]), int(dt[0][2])).togregorian()
                else:
                    data.write({'description': f'start date error: {data.start_date}'})
                    continue
                dt = re.findall( '([\d]{4})/([\d]{1,2})/([\d]{1,2})', data.end_date)
                if dt:
                    end_date = jdatetime.date(int(dt[0][0]), int(dt[0][1]), int(dt[0][2])).togregorian()
                else:
                    data.write({'description': f'start date error: {data.end_date}'})
                    continue

                dt = re.findall( '([\d]{4})/([\d]{1,2})/([\d]{1,2})', data.first_extend_star_date)
                # print(f'\n first_extend_star_date: {dt}')
                first_extend_star_date = jdatetime.date(int(dt[0][0]), int(dt[0][1]), int(dt[0][2])).togregorian() if len(dt) == 1 else False
                dt = re.findall( '([\d]{4})/([\d]{1,2})/([\d]{1,2})', data.first_extend_end_date)
                first_extend_end_date = jdatetime.date(int(dt[0][0]), int(dt[0][1]), int(dt[0][2])).togregorian() if len(dt) == 1 else False
                dt = re.findall( '([\d]{4})/([\d]{1,2})/([\d]{1,2})', data.second_extend_star_date)
                second_extend_star_date = jdatetime.date(int(dt[0][0]), int(dt[0][1]), int(dt[0][2])).togregorian() if len(dt) == 1 else False
                dt = re.findall( '([\d]{4})/([\d]{1,2})/([\d]{1,2})', data.second_extend_end_date)
                second_extend_end_date = jdatetime.date(int(dt[0][0]), int(dt[0][1]), int(dt[0][2])).togregorian() if len(dt) == 1 else False



                # save new record
                logging.error(f'\n save new record:')
                payaneh_data_model.create({'registration_no': str(data.registration_no).split('.')[0],
                                           'letter_no': data.letter_no,
                                           'contract_no': data.contract_no,
                                           'order_no': str(data.order_no).split('.')[0],
                                           'buyer': buyer[0][1],
                                           'amount': int(float(data.amount)),
                                           'unit': 'barrel' if data.unit == 'بشکه' else 'metric_ton',
                                           'contract_type': 'stock' if data.contract_type == 'بورس' else 'general',
                                           'loading_type': 'internal' if data.loading_type == 'داخلی' else 'export',
                                           'cargo_type': 1,
                                           'start_date': start_date,
                                           'end_date': end_date,
                                           'destination': destination[0][1],
                                           'contractors': contractors_list,
                                           'first_extend_no': data.first_extend_no,
                                           'first_extend_star_date': first_extend_star_date,
                                           'first_extend_end_date': first_extend_end_date,
                                           'second_extend_no': data.second_extend_no,
                                           'second_extend_star_date': second_extend_star_date,
                                           'second_extend_end_date': second_extend_end_date,
                                           })
                logging.error('\n  data.write ')
                data.write({'active': False, 'description': 'Done'})

            except Exception as e:
                data.write({'description': e})
                logging.error(f'\n process_records: {e}')
                continue
