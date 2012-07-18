from dingus import Dingus
from datetime import datetime
from django.test import TestCase

from devilry.apps.core.testhelper import TestHelper
from devilry.apps.core.models import AssignmentGroup
from devilry.apps.core.models import Candidate
from devilry.apps.core.models import Examiner
from devilry.apps.core.models import AssignmentGroupTag
from devilry.apps.core.models import Deadline
from devilry.utils.rest_testclient import RestClient

from devilry_subjectadmin.rest.errors import PermissionDeniedError
from devilry_subjectadmin.rest.group import GroupCreator


class TestListGroupRest(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.client = RestClient()

    def _geturl(self, assignment_id):
        assignment_id = assignment_id or self.testhelper.sub_p1_a1.id
        return '/devilry_subjectadmin/rest/group/{0}/'.format(assignment_id)

    def _getas(self, username, assignment_id, **data):
        self.client.login(username=username, password='test')
        return self.client.rest_get(self._geturl(assignment_id), **data)

    def _create_testassignments(self):
        self.testhelper.add(nodes='uni',
                       subjects=['duck1010'],
                       periods=['firstsem'],
                       assignments=['a1:admin(a1admin)', 'a2'])

    def _create_testdata(self):
        self._create_testassignments()
        for num in xrange(3):
            path = 'uni;duck1010.firstsem.a1.g{num}:candidate(student{num},extrastudent):examiner(examiner1,extraexaminer).d1'
            self.testhelper.add_to_path(path.format(**vars()))
            group = getattr(self.testhelper, 'duck1010_firstsem_a1_g{0}'.format(num))
            group.tags.create(tag="stuff")
            group.tags.create(tag="lownumber")
            delivery = self.testhelper.add_delivery(group)
            if num != 2:
                self.testhelper.add_feedback(delivery,
                                             verdict=dict(grade='A', points=100,
                                                          is_passing_grade=True))

    def test_list_permissiondenied(self):
        self.testhelper.create_user('nobody')
        self._create_testassignments()
        a1 = self.testhelper.duck1010_firstsem_a1
        content, response = self._getas('nobody', a1.id)
        self.assertEquals(response.status_code, 403)


    def _test_list_as(self, username):
        self._create_testdata()
        a1 = self.testhelper.duck1010_firstsem_a1
        content, response = self._getas(username, a1.id)
        #from pprint import pprint
        #pprint(content)

        self.assertEquals(len(content), 3)
        self.assertEquals(set(content[0].keys()),
                          set(['name', 'feedback', 'deadlines', 'id', 'etag',
                               'is_open', 'parentnode', 'candidates',
                               'examiners', 'num_deliveries']))

        # Properties directly from group
        self.assertEquals(AssignmentGroup.objects.get(id=content[0]['id']).parentnode_id,
                          a1.id)
        self.assertEquals(content[0]['is_open'], False)
        self.assertEquals(content[0]['name'], 'g0')
        self.assertEquals(content[0]['num_deliveries'], 1)
        self.assertEquals(content[0]['parentnode'], a1.id)

        # Feedback
        feedback = content[0]['feedback']
        self.assertEquals(set(feedback.keys()),
                          set(['id', 'grade', 'is_passing_grade', 'points', 'save_timestamp']))
        self.assertEquals(feedback['grade'], 'A')
        self.assertEquals(feedback['is_passing_grade'], True)
        self.assertEquals(feedback['points'], 100)

        # NULL feedback
        self.assertEquals(content[2]['feedback'], None)

        # Canididates
        def get_usernames(users):
            return [user['user']['username'] for user in users]
        self.assertEquals(len(content[0]['candidates']), 2)
        self.assertEquals(set(get_usernames(content[0]['candidates'])),
                          set(['student0', 'extrastudent']))
        self.assertEquals(set(content[0]['candidates'][0].keys()),
                          set(['id', 'candidate_id', 'user']))
        self.assertEquals(set(content[0]['candidates'][0]['user'].keys()),
                          set(['email', 'full_name', 'id', 'username']))

        # Examiners
        self.assertEquals(len(content[0]['examiners']), 2)
        self.assertEquals(set(get_usernames(content[0]['examiners'])),
                          set(['examiner1', 'extraexaminer']))
        self.assertEquals(set(content[0]['examiners'][0].keys()),
                          set(['id', 'user']))
        self.assertEquals(set(content[0]['examiners'][0]['user'].keys()),
                          set(['email', 'full_name', 'id', 'username']))

        # Deadlines
        self.assertEquals(len(content[0]['deadlines']), 1)
        deadline = content[0]['deadlines'][0]
        self.assertEquals(set(deadline.keys()),
                          set(['id', 'deadline']))


    def test_list(self):
        self._test_list_as('a1admin')

    def test_list_as_superuser(self):
        self.testhelper.create_superuser('superuser')
        self._test_list_as('superuser')


class TestGroupCreator(TestCase):
    def setUp(self):
        self.client = RestClient()
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                       subjects=['sub'],
                       periods=['p1'],
                       assignments=['a1'])
        self.a1id = self.testhelper.sub_p1_a1.id

    def test_update_group(self):
        self.assertEquals(AssignmentGroup.objects.all().count(), 0)
        creator = GroupCreator(self.a1id)
        self.assertEquals(creator.group.id, None)
        creator.update_group(name='Nametest', is_open=False)
        self.assertIsNotNone(creator.group.id)
        self.assertEquals(creator.group.name, 'Nametest')
        self.assertEquals(creator.group.is_open, False)
        self.assertEquals(AssignmentGroup.objects.all().count(), 1)



class TestListOrCreateGroupRest(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1'],
                            assignments=['a1:admin(a1admin)'])
        self.client = RestClient()
        self.testhelper.create_user('student0')
        self.a1url = '/devilry_subjectadmin/rest/group/{0}/'.format(self.testhelper.sub_p1_a1.id)

    def test_list(self):
        self.client.login(username='a1admin', password='test')
        for studentNum in xrange(3):
            path = 'uni;sub.p1.a1.g{studentNum}:candidate(stud{studentNum})'.format(studentNum=studentNum)
            self.testhelper.add_to_path(path)
        content, response = self.client.rest_get(self.a1url)
        self.assertEquals(len(content), 3)
        self.assertEquals(set(content[0].keys()),
                          set([u'name', u'tags', u'students',
                               u'feedback__is_passing_grade', u'deadlines',
                               u'id', u'feedback__points', u'feedback__grade',
                               u'is_open', u'num_deliveries',
                               u'feedback__save_timestamp', u'examiners']))

    def test_create(self):
        self.client.login(username='a1admin', password='test')
        data = dict(
                    students=[dict(candidate_id=u'candid334',
                                   student__username=u'student0',
                                   student__email=u'myemail2',
                                   student__devilryuserprofile__full_name=u'Somename2')],
                    tags=[dict(tag='group1')],
                    deadlines=[dict(deadline=u'2011-01-02 03:04:05')]
                   )
        content, response = self.client.rest_post(self.a1url, data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(content.keys(), ['id'])
        groups = self.testhelper.sub_p1_a1.assignmentgroups.all()
        self.assertEquals(len(groups), 1)
        self.assertEquals(content['id'], groups[0].id)

    def test_noperm(self):
        self.client.login(username='student0', password='test')
        content, response = self.client.rest_post(self.a1url, {})
        self.assertEquals(response.status_code, 403)
        self.assertEquals(content, {u'detail': u'Permission denied'})


class TestInstanceGroupRest(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1'],
                            assignments=['a1:admin(a1admin)'])
        self.client = RestClient()
        self.testhelper.create_user('student0')

    def _geturl(self, group_id, assignment_id=None):
        assignment_id = assignment_id or self.testhelper.sub_p1_a1.id
        return '/devilry_subjectadmin/rest/group/{0}/{1}'.format(assignment_id, group_id)

    def _putas(self, username, group_id, assignment_id=None, data={}):
        self.client.login(username=username, password='test')
        return self.client.rest_put(self._geturl(assignment_id, group_id), data)

    def _add_group(self, name, candidates, examiners):
        self.testhelper.add_to_path('uni;sub.p1.a1.g1:candidate({candidates}):examiner({examiners})'.format(**vars()))
        return getattr(self.testhelper, 'sub_p1_a1_' + name)

    def test_put(self):
        g1 = self._add_group('g1', 'student0', 'examiner0')
        content, response = self._putas('a1admin', g1.id)
        print response
        #print content
