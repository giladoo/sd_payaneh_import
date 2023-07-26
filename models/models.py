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

class SdHseImpoertData(models.Model):
    _name = 'sd_payaneh_import.data'
    _description = 'sd_payaneh_import.data'

    active = fields.Boolean(default=True)




