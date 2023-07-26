odoo.define('sd_payaneh_import.sheet_names', function(require) {
    "use strict";

    const FormController = require('web.FormController');
    const FormView = require('web.FormView');
    const viewRegistry = require('web.view_registry');
    const Dialog = require('web.Dialog');

    const core = require('web.core');
    const _t = core._t;

    const HseImportFormController = FormController.extend({
        /**
         * @override
         * @private
         **/
    start: function () {
        let self = this;
        return this._super.apply(this, arguments).then(function(){
            let sheets_div = self.el.querySelectorAll('.sd_payaneh_import_sheet_names')[0];
            let sheet_list = self.el.querySelectorAll('input[name="sheet_list"]')[0];
            let excel_file = self.el.querySelectorAll('input[name="excel_file"]')[0];
//                console.log('sheets_div,sheet_list',sheets_div,sheet_list)
            if(sheets_div != undefined){
                sheets_div.parentElement.style.width =  '';
                let sheets_select = self.el.querySelector('.sd_payaneh_import_sheet_select');
                while (sheets_select.hasChildNodes()) {
                    sheets_select.removeChild(sheets_select.firstChild);
                }
                // todo: It is needed to to know if the sheets_list is changed. then update the selection input.
                sheet_list.addEventListener('input', e => {
                    console.log(e)
                })

            }



        });
    },

    });

    var HseImportFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: HseImportFormController,
        }),
    });

    viewRegistry.add('sheet_names', HseImportFormView);

    return HseImportFormView;
});
