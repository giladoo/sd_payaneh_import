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




