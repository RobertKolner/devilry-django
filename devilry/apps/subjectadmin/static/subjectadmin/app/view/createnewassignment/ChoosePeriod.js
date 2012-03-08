Ext.define('subjectadmin.view.createnewassignment.ChoosePeriod' ,{
    extend: 'Ext.panel.Panel',
    alias: 'widget.chooseperiod',
    requires: [
        'themebase.form.Help'
    ],

    border: 0,
    bodyPadding: 40,
    autoScroll: true,

    items: [{
        xtype: 'panel',
        title: dtranslate('subjectadmin.createnewassignment.title'),
        ui: 'inset-header-strong-panel',
        items: { // Note: We wrap this in an extra container to avoid that the Next button ends up at the bottom of the screen
            xtype: 'form',
            region: 'center',
            ui: 'transparentpanel',
            cls: 'centerbody',
            fieldDefaults: {
                labelAlign: 'top',
                labelStyle: 'font-weight: bold'
            },
            items: [{
                margin: {top: 0, bottom: 20},
                xtype: 'alertmessagelist'

                // Active period
            }, {
                xtype: 'activeperiodslist',
                name: 'activeperiod',
                fieldLabel: dtranslate('subjectadmin.assignment.activeperiod.label')
            }, {
                xtype: 'formhelp',
                margin: {top: 5},
                html: dtranslate('subjectadmin.assignment.activeperiod.help')

                // How do students add deliveries
            }, {
                margin: {top: 20},
                fieldLabel: dtranslate('subjectadmin.assignment.delivery_types.label'),
                xtype: 'radiogroup',
                vertical: true,
                itemId: 'deliveryTypesRadioGroup',
                cls: 'delivery_types-radiogroup',
                columns: 1,
                items: [{
                    boxLabel: dtranslate('subjectadmin.assignment.delivery_types.electronic'),
                    name: 'delivery_types',
                    inputValue: 0,
                    checked: true
                }, {
                    boxLabel: dtranslate('subjectadmin.assignment.delivery_types.nonelectronic'),
                    name: 'delivery_types',
                    inputValue: 1
                }]
            }, {
                xtype: 'formhelp',
                margin: {top: 5},
                html: dtranslate('subjectadmin.assignment.delivery_types.help')
            }],
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'bottom',
                ui: 'footer',
                padding: 0,
                margin: {top: 20, bottom: 0},
                items: [{
                    xtype: 'nextbutton'
                }]
            }]
        }
    }]
});
