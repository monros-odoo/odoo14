odoo.define('kp_stock_custom.makescraptransfer_button', function (require) {
"use strict";
var ListController = require('web.ListController');
var ListView = require('web.ListView');
var viewRegistry = require('web.view_registry');
var StockLotTreeButton = ListController.extend({
   buttons_template: 'LotMakeTransferButton.buttons',
   events: _.extend({}, ListController.prototype.events, {
       'click .maketransfer_action': '_onClickMakeTransfer',
   }),
   _onClickMakeTransfer: function () {
       var self = this;

       console.log("resid",this.renderer.state['res_ids'])
       console.log("rsss",this.model.localIdsToResIds(this.selectedRecords))
       var rcds = this.model.localIdsToResIds(this.selectedRecords)
        this._rpc({
            model: 'stock.production.lot',
            method: 'make_lotscrap_transfer',
            args: [rcds],
        }).then(function (result) {
//        self.do_action(result);
            console.log("resultt",result)
        })

   }
    });

var StockLotListView = ListView.extend({
   config: _.extend({}, ListView.prototype.config, {
       Controller: StockLotTreeButton,
   }),
});

viewRegistry.add('lotmaketransfer_in_tree', StockLotListView);
});