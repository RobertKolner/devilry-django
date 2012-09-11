Ext.define('devilry_subjectadmin.view.allwhereisadmin.AllWhereIsAdminList' ,{
    extend: 'Ext.Component',
    alias: 'widget.allwhereisadminlist',
    cls: 'devilry_subjectadmin_allwhereisadminlist bootstrap',
    tpl: [
        '<tpl if="loadingtext">',
            '<h2>{loadingtext}</h2>',
        '<tpl else>',
            '<h1>',
                interpolate(gettext('All %(subjects_term)s'), {
                    subjects_term: gettext('subjects')
                }, true),
            '</h1>',
            '<p class="muted">',
                interpolate(gettext('These are all %(subjects_term)s where you are administrator.'), {
                    subjects_term: gettext('subjects')
                }, true),
            '</p>',
            '<ul class="unstyled">',
            '<tpl for="subjects">',
                '<h3 class="subject subject_{data.short_name}">',
                    '<tpl if="data.can_administer">',
                        '<a href="#/subject/{data.id}/">',
                            '{data.long_name}',
                        '</a>',
                    '<tpl else>',
                        '{data.long_name}',
                    '</tpl>',
                '</h3>',
                '<tpl for="data.periods">',
                    '<li>',
                        '<tpl if="can_administer">',
                            '<p><strong><a href="#/period/{id}/">',
                                '{[Ext.String.ellipsis(values.long_name, 40)]}',
                            '</a></strong></p>',
                        '<tpl else>',
                            '<tpl for="assignments">',
                                '<li><p><strong><a href="#/assignment/{id}/">',
                                    '{parent.short_name} - ',
                                    '{[Ext.String.ellipsis(values.long_name, 40)]}',
                                '</a></strong></p></li>',
                            '</tpl>',
                        '</tpl>',
                    '</li>',
                '</tpl>',
                '</ul>',
            '</tpl>',
            '</ul>',
        '</tpl>'
    ],

    data: {
        loadingtext: gettext('Loading') + ' ...'
    }
});