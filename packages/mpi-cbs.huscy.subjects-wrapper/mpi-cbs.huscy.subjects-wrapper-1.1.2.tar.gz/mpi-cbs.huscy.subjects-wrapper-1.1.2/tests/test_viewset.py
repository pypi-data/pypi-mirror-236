import pytest
from model_bakery import baker
from pytest_bdd import given, parsers, scenarios, then, when

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from huscy.subjects.serializers import SubjectSerializer
from mpi_cbs.huscy.subjects_wrapper.models import WrappedSubject

pytestmark = pytest.mark.django_db


scenarios(
    'viewsets/create_subjects.feature',
    'viewsets/delete_subjects.feature',
    'viewsets/update_subjects.feature',
    'viewsets/view_subjects.feature',
)


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='user', password='password',
                                                 first_name='Phil', last_name='Stift')


@pytest.fixture
def subject():
    return baker.make('subjects.Subject')


@pytest.fixture
def wrapped_subject(subject):
    return baker.make(WrappedSubject, pseudonym='123abc.0f', subject=subject)


@given(parsers.parse('I am {huscy_user}'), target_fixture='client')
def client(admin_user, user, huscy_user):
    assert huscy_user in ['admin user', 'normal user', 'anonymous user']
    api_client = APIClient()
    if huscy_user == 'admin user':
        api_client.login(username=admin_user.username, password='password')
    elif huscy_user == 'normal user':
        api_client.login(username=user.username, password='password')
    elif huscy_user == 'anonymous user':
        pass
    return api_client


@given(parsers.parse('I have {codename} permission'), target_fixture='codename')
def assign_permission(user, codename):
    permission = Permission.objects.get(codename=codename)
    user.user_permissions.add(permission)


@when('I try to create a subject', target_fixture='request_result')
def create_subject(client, subject):
    data = dict(
        pseudonym='123abc.0f',
        subject=SubjectSerializer(subject).data,
    )
    return client.post(reverse('wrappedsubject-list'), data=data, format='json')


@when('I try to delete a subject', target_fixture='request_result')
def delete_subject(client, wrapped_subject):
    return client.delete(f'/api/wrappedsubjects/{wrapped_subject.pk}')


@when('I try to list subjects', target_fixture='request_result')
def list_subjects(client):
    return client.get(reverse('wrappedsubject-list'))


@when('I try to partial update the subject', target_fixture='request_result')
def partial_update_subject(client, wrapped_subject):
    return client.patch(
        f'/api/wrappedsubjects/{wrapped_subject.pk}',
        data={
            'subject': {
                'contact': {'first_name': 'Antonia'}
            }
        },
        format='json'
    )


@when('I try to retrieve a subject', target_fixture='request_result')
def retrieve_subject(client, wrapped_subject):
    return client.get(f'/api/wrappedsubjects/{wrapped_subject.pk}')


@when('I try to update the subject', target_fixture='request_result')
def update_subject(client, wrapped_subject):
    subject = SubjectSerializer(wrapped_subject.subject).data
    subject['contact']['first_name'] = 'Antonia'
    return client.put(
        f'/api/wrappedsubjects/{wrapped_subject.pk}',
        data=dict(pseudonym='123456.ab', subject=subject),
        format='json'
    )


@then(parsers.parse('I get status code {status_code:d}'))
def assert_status_code(request_result, status_code):
    assert request_result.status_code == status_code, request_result.content


@then('the subject was created')
def subject_created():
    assert WrappedSubject.objects.filter(pseudonym='123abc.0f').count() == 1
