# -*- coding: utf-8 -*-
{
    'name': "sd_payaneh_import",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "Arash Homayounfar",
    'website': "https://gilaneh.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Service Desk/Service Desk',
    'application': True,
    'version': '1.1.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'sd_payaneh_nafti'],
    # pip install openpyxl

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/registration.xml',
        'views/input.xml',
        'views/payaneh_input_info.xml',
        'wizard/import_wizard.xml',
        # 'wizard/clear_wizard.xml',
    ],
    'assets': {
        # 'website.assets_editor': [
        #     'static/src/**/*',
        # ],

        'web.assets_frontend': [

            'sd_payaneh_import/static/src/css/style.scss',
            # 'sd_payaneh_import/static/src/js/website_form_sd_hse.js'
        ],
        'web.assets_backend': [

            'sd_payaneh_import/static/src/css/style.scss',
            # 'sd_payaneh_import/static/src/js/sd_payaneh_import_sheet_names.js'
        ],
        'web.report_assets_common': [

            'sd_payaneh_import/static/src/css/report_styles.css',
            # 'sd_payaneh_import/static/src/js/website_form_sd_hse.js'
        ],

    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',

}
