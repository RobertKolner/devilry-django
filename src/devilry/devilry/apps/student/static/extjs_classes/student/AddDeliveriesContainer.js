Ext.define('devilry.student.AddDeliveriesContainer', {
    extend: 'Ext.container.Container',
    alias: 'widget.add_deliveries_container',
    cls: 'widget-add_deliveries_container',
    border: false,
    requires: [
        'devilry.extjshelpers.SingleRecordContainer',
        'devilry.student.FileUploadPanel',
        'devilry.student.DeadlineTitle',
        'devilry.student.stores.UploadedFileStore',
        'devilry_header.Breadcrumbs'
    ],

    /**
     * @cfg {int} [assignmentgroupid]
     */

    /**
     * @cfg {int} [deadlineid]
     */

    /**
     * @cfg {string} [deliverymodelname]
     */

    /**
     * @cfg {Object} [latest_deadline]
     */

    /**
     * @cfg {string} [deadline_modelname]
     */

    /**
     * @cfg {string} [ag_modelname]
     */



    initComponent: function() {
        var agroup_recordcontainer = Ext.create('devilry.extjshelpers.SingleRecordContainer');
        Ext.ModelManager.getModel(this.ag_modelname).load(this.assignmentgroupid, {
            scope: this,
            success: function(record) {
                Ext.getBody().unmask();
                agroup_recordcontainer.setRecord(record);
                this._onLoadGroup(record);
            }
        });

        this.uploadedFilesStore = Ext.create('devilry.student.stores.UploadedFileStore', {
            listeners: {
                scope: this,
                add: this.onAddToUploadFilesStore
            }
        });

        this.sidebar = Ext.widget('panel', {
            layout: 'accordion',
            flex: 3,
            margin: '0 0 0 10',
            hidden: true,
            listeners: {
                scope: this,
                add: function(sidebar, component) {
                    sidebar.show();
                    //component.show();
                }
            }
        });
        this.center = Ext.widget('container', {
            flex: 1,
            layout: {
                type: 'hbox',
                align: 'stretchmax'
            },
            margin: '0 0 10 0',
            style: 'background-color: transparent',
            autoScroll: true,
            items: [{
                flex: 7,
                xtype: 'fileuploadpanel',
                height: 280,
                bodyPadding: 20,
                assignmentgroupid: this.assignmentgroupid,
                deadlineid: this.deadlineid,
                initialhelptext: interpolate(gettext('Upload files for your %(delivery)s. You can upload multiple files.'), {
                    delivery: gettext('delivery')
                }, true),
                deliverymodelname: this.deliverymodelname,
                agroup_recordcontainer: agroup_recordcontainer,
                uploadedFilesStore: this.uploadedFilesStore
            }, this.sidebar]
        });

        Ext.apply(this, {
            layout: {
                type: 'vbox',
                align: 'stretch'
            },
            items: [{
                xtype: 'deadlinetitle',
                singlerecordontainer: agroup_recordcontainer,
                extradata: {
                    latest_deadline: this.latest_deadline
                }
            }, this.center]
        });

        this.showDeadlineTextIfAny();
        this.callParent(arguments);
    },

    showDeadlineTextIfAny: function() {
        Ext.ModelManager.getModel(this.deadline_modelname).load(this.deadlineid, {
            scope: this,
            success: function(record) {
                if(record.data.text) {
                    this.aboutdeadline = this.sidebar.add({
                        xtype: 'panel',
                        title: gettext('About this deadline'),
                        html: record.data.text,
                        style: 'white-space: pre-line',
                        bodyPadding: 10
                    });
                }
            }
        });
    },

    onAddToUploadFilesStore: function(store, records, index) {
        if(index === 0) {
            this.sidebar.insert(0, {
                title: gettext('Uploaded files'),
                xtype: 'grid',
                store: this.uploadedFilesStore,
                hideHeaders: true,
                disableSelection: true,
                columns: [{header: 'Filename', flex: 1, dataIndex: 'filename'}]
            });
            if(this.aboutdeadline) {
                this.aboutdeadline.collapse();
            }
        }
    },

    _onLoadGroup: function(groupRecord) {
        var periodpath = [
            groupRecord.get('parentnode__parentnode__parentnode__short_name'),
            groupRecord.get('parentnode__parentnode__short_name')].join('.');
        var addDeliveryText = interpolate(gettext('Add %(delivery)s'), {
            delivery: gettext('delivery')
        }, true);
        devilry_header.Breadcrumbs.getInBody().set([{
            text: gettext('Browse'),
            url: Ext.String.format('{0}/devilry_student/#/browse/',
                DevilrySettings.DEVILRY_URLPATH_PREFIX)
        }, {
            text: periodpath,
            url: Ext.String.format('{0}/devilry_student/#/browse/{1}',
                DevilrySettings.DEVILRY_URLPATH_PREFIX,
                groupRecord.get('parentnode__parentnode'))
        }, {
            text: groupRecord.get('parentnode__short_name'),
            url: Ext.String.format('{0}/student/assignmentgroup/{1}',
                DevilrySettings.DEVILRY_URLPATH_PREFIX,
                groupRecord.get('id'))
        }], addDeliveryText);

        window.document.title = addDeliveryText + ' - Devilry';
    }
});
