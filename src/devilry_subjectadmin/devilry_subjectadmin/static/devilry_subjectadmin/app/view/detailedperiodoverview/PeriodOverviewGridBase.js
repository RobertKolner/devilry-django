/**
 * Base class for grids that needs an overview of an entire period.
 */
Ext.define('devilry_subjectadmin.view.detailedperiodoverview.PeriodOverviewGridBase', {
    extend: 'Ext.grid.Panel',
    cls: 'devilry_qualifiesforexam_previewgrid bootstrap',

    /**
     * @cfg {int} [firstAssignmentColumnIndex=1]
     * When rendering assignment result, we need to know the column index of the first assignment
     * to place the results in the correct column.
     */
    firstAssignmentColumnIndex: 1,

    requires: [
        'Ext.XTemplate',
        'Ext.grid.column.Column'
    ],

    studentColTpl: [
        '<div class="student" style="white-space: normal !important;">',
            '<div class="fullname"><strong>{full_name}</strong></div>',
            '<div class="username"><small class="muted">{username}</small></div>',
        '</div>'
    ],
    feedbackColTpl: [
        '<div class="feedback feedback_assignment_{assignmentid}" style="white-space: normal !important;">',
            '<tpl if="grouplist.length == 0">',
                '<small class="muted nofeedback">',
                    gettext('Not registered on assignment'),
                '</small>',
            '<tpl else>',
                '<tpl for="grouplist">',
                    '<div class="group-{id}">',
                        '<div class="status-{status}">',
                            '<tpl if="status === \'corrected\'">',
                                '<div class="{[this.getGradeClass(values.feedback.is_passing_grade)]}">',
                                    '<div class="passingstatus {[this.getTextClassForGrade(values.feedback.is_passing_grade)]}">',
                                        '{[this.getPassedOrFailedText(values.feedback.is_passing_grade)]}',
                                    '</div>',
                                    '<div class="gradedetails">',
                                        '<small class="grade muted">({feedback.grade})</small>',
                                        ' <small class="points muted">(',
                                            gettext('Points:'),
                                            '{feedback.points})',
                                        '</small>',
                                    '</div>',
                                '</div>',
                            '<tpl elseif="status === \'waiting-for-deliveries\'">',
                                '<em><small class="muted">', gettext('Waiting for deliveries'), '</small></em>',
                            '<tpl elseif="status === \'waiting-for-feedback\'">',
                                '<em><small class="muted">', gettext('Waiting for feedback'), '</small></em>',
                            '<tpl else>',
                                '<span class="label label-important">{status}</span>',
                            '</tpl>',
                        '</div>',
                    '</div>',
                '</tpl>',
            '</tpl>',
        '</div>', {
            getGradeClass: function(is_passing_grade) {
                return is_passing_grade? 'passinggrade': 'notpassinggrade';
            },
            getTextClassForGrade: function(is_passing_grade) {
                return is_passing_grade? 'text-success': 'text-warning';
            },
            getPassedOrFailedText: function(is_passing_grade) {
                return is_passing_grade? gettext('Passed'): gettext('Failed');
            }
        }
    ],

    initComponent: function() {
        this.studentColTplCompiled = Ext.create('Ext.XTemplate', this.studentColTpl);
        this.feedbackColTplCompiled = Ext.create('Ext.XTemplate', this.feedbackColTpl);
        this.columns = [{
            text: gettext('Student'),
            dataIndex: 'id',
            flex: 2,
            menuDisabled: true,
            sortable: false,
            renderer: this.renderStudentColumn
        }];
        this.setupColumns();
        this.setupToolbar();
        this.callParent(arguments);
    },

    renderStudentColumn: function(value, meta, record) {
        return this.studentColTplCompiled.apply(record.get('user'));
    },


    /**
     * Override to add custom columns. Make sure you adjust ``firstAssignmentColumnIndex`` accordingly.
     */
    setupColumns: function() {
    },

    /** Override to customize toolbar */
    setupToolbar: function() {
        this.tbar = [{
            xtype: 'button',
            text: gettext('Sort'),
            itemId: 'sortButton',
            menu: [{
                itemId: 'sortByFullname',
                text: gettext('Full name'),
                listeners: {
                    scope: this,
                    click: this._onSortByFullname
                }
            }, {
                itemId: 'sortByLastname',
                text: gettext('Last name'),
                listeners: {
                    scope: this,
                    click: this._onSortByLastname
                }
            }, {
                itemId: 'sortByUsername',
                text: gettext('Username'),
                listeners: {
                    scope: this,
                    click: this._onSortByUsername
                }
            }]
        }, '->', {
            xtype: 'textfield',
            width: 250,
            emptyText: gettext('Search for name or username ...'),
            listeners: {
                scope: this,
                change: this._onSearch
            }
        }];
    },

    /**
     * Add assignment column to the grid.
     * @param assignment An object with assignment details.
     *
     * NOTE: Remember to call ``getView().refresh()`` on the grid after adding new dynamic columns.
     */
    addAssignmentResultColumn: function(assignment) {
        var column = Ext.create('Ext.grid.column.Column', {
            text: assignment.short_name,
            flex: 1,
            dataIndex: 'id',
            menuDisabled: true,
            sortable: false,
            renderer: this._renderAssignmentResultColum
        });
        this.headerCt.insert(this.columns.length, column);
    },

    /**
     * Loops through the given array and uses ``this.addAssignmentResultColumn()`` to add columns.
     * */
    addColumnForEachAssignment:function (assignments) {
        Ext.Array.each(assignments, function(assignment) {
            this.addAssignmentResultColumn(assignment);
        }, this);
        this.getView().refresh();
    },


    _renderAssignmentResultColum: function(value, meta, record, rowIndex, colIndex) {
        var assignmentIndex = colIndex - this.firstAssignmentColumnIndex;
        var assignmentinfo = record.get('groups_by_assignment')[assignmentIndex];
        return this.feedbackColTplCompiled.apply({
            grouplist: assignmentinfo.grouplist,
            assignmentid: assignmentinfo.assignmentid
        });
    },

    /**
     * Add sorters for the given assignments.
     * @param assignments An array of assignment-objects. Each object
     *   must have the ``short_name``-attribute, and the array must be sorted
     *   in the same order as they are in the records in the store.
     * */
    addAssignmentSorters: function(assignments) {
        var menu = this.down('#sortButton').menu;
        Ext.Array.each(assignments, function(assignment, index) {
            menu.add({
                text: assignment.short_name,
                hideOnClick: false,
                menu: [{
                    text: gettext('Sort by points ascending'),
                    listeners: {
                        scope: this,
                        click: function() {
                            this._onSortByFeedback(index, this._sortByPointsAscending);
                        }
                    }
                }, {
                    text: gettext('Sort by points decending'),
                    listeners: {
                        scope: this,
                        click: function() {
                            this._onSortByFeedback(index, this._sortByPointsDecending);
                        }
                    }
                }]
            });
        }, this);
    },


    _onSearch: function(field, newValue) {
        if(!Ext.isEmpty(this.searchtask)) {
            this.searchtask.cancel();
        }
        this.searchtask = new Ext.util.DelayedTask(function() {
            this._search(newValue.toLocaleLowerCase());
        }, this);
        this.searchtask.delay(140);
    },
    _searchMatch: function(searchString, value) {
        if(value === null) {
            value = '';
        }
        return value.toLocaleLowerCase().indexOf(searchString) !== -1;
    },
    _search: function(searchString) {
        this.getStore().filterBy(function(record) {
            var user = record.get('user');
            return this._searchMatch(searchString, user.username) ||
                this._searchMatch(searchString, user.full_name);
        }, this);
    },


    _getBestFeedback: function(record, assignmentIndex) {
        var grouplist = record.get('groups_by_assignment')[assignmentIndex].grouplist;
        var bestFeedback = {
            points: -1,
            grade: '',
            is_passing_grade: false
        };
        for (var i = 0; i < grouplist.length; i++) {
            var group = grouplist[i];
            if(group.status === 'corrected' && group.feedback.points > bestFeedback.points) {
                bestFeedback = group.feedback;
            }
        }
        return bestFeedback;
    },
    _onSortByFeedback: function(assignmentIndex, sorter) {
        this.getStore().sort(Ext.create('Ext.util.Sorter', {
            sorterFn: Ext.bind(function(a, b) {
                var aFeedback = this._getBestFeedback(a, assignmentIndex);
                var bFeedback = this._getBestFeedback(b, assignmentIndex);
                return sorter(aFeedback, bFeedback);
            }, this)
        }));
    },
    _sortByPointsAscending: function(feedbackA, feedbackB) {
        return feedbackA.points - feedbackB.points;
    },
    _sortByPointsDecending: function(feedbackA, feedbackB) {
        return feedbackB.points - feedbackA.points;
    },


    _onSortByFullname: function() {
        this._sortByUser('fullname');
    },
    _onSortByLastname: function() {
        this._sortByUser('lastname');
    },
    _onSortByUsername: function() {
        this._sortByUser('username');
    },

    _sortByUser: function(sortby) {
        var sorter = null;
        if(sortby === 'username') {
            sorter = this._sortByUsername;
        } else if(sortby === 'fullname') {
            sorter = this._sortByFullname;
        } else if(sortby === 'lastname') {
            sorter = this._sortByLastname;
        } else {
            throw "Invalid sorter: " + sortby;
        }
        this.getStore().sort(Ext.create('Ext.util.Sorter', {
            sorterFn: Ext.bind(sorter, this)
        }));
    },

    _sortByUserProperty: function(a, b, property) {
        return a.get('user')[property].localeCompare(b.get('user')[property]);
    },
    _sortByUsername: function (a, b) {
        return this._sortByUserProperty(a, b, 'username');
    },

    _sortByFullname: function (a, b) {
        return this._sortByUserProperty(a, b, 'full_name');
    },

    _getLastname: function(record) {
        var splitted = record.get('user').full_name.split(/\s+/);
        return splitted[splitted.length-1];
    },
    _sortByLastname: function (a, b) {
        var aLastName = this._getLastname(a);
        var bLastName = this._getLastname(b);
        return aLastName.localeCompare(bLastName);
    }
});