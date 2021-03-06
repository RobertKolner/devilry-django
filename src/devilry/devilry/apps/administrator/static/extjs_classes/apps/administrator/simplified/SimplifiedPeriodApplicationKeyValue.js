// Autogenerated by the dev_coreextjsmodels script. DO NOT CHANGE MANUALLY

/*******************************************************************************
 * NOTE: You will need to add the following before your application code:
 *
 *    Ext.Loader.setConfig({
 *        enabled: true,
 *        paths: {
 *            'devilry': DevilrySettings.DEVILRY_STATIC_URL + '/extjs_classes'
 *        }
 *    });
 *    Ext.syncRequire('devilry.extjshelpers.RestProxy');
 ******************************************************************************/
Ext.define('devilry.apps.administrator.simplified.SimplifiedPeriodApplicationKeyValue', {
    extend: 'Ext.data.Model',
    requires: ['devilry.extjshelpers.RestProxy'],
    fields: [
        {
            "type": "auto", 
            "name": "period"
        }, 
        {
            "type": "int", 
            "name": "id"
        }, 
        {
            "type": "auto", 
            "name": "application"
        }, 
        {
            "type": "auto", 
            "name": "key"
        }, 
        {
            "type": "auto", 
            "name": "value"
        }
    ],
    idProperty: 'id',
    proxy: {
        type: 'devilryrestproxy',
        url: '/administrator/restfulsimplifiedperiodapplicationkeyvalue/',
        headers: {
            'X_DEVILRY_USE_EXTJS': true
        },
        extraParams: {
            getdata_in_qrystring: true,
            result_fieldgroups: '[]'
        },
        reader: {
            type: 'json',
            root: 'items',
            totalProperty: 'total'
        },
        writer: {
            type: 'json'
        }
    }
});