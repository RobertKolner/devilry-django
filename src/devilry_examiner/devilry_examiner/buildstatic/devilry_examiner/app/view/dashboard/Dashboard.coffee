Ext.define('devilry_examiner.view.dashboard.Dashboard', {
    extend: 'Ext.container.Container'
    alias: 'widget.dashboard'
    cls: 'devilry_dashboard bootstrap'

    layout: 'fit'
    padding: '40'
    autoScroll: true

    items: [{
        xtype: 'box'
        html: '<h1>Your assignments</h1>'
    }]
})
