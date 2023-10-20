"""
Tests for SkylabStudio - Python Client
"""

import pytest
import requests
import uuid
import os
import skylab_studio

#pylint: disable=redefined-outer-name

job_id = 0
profile_id = 0
photo_id = 0

@pytest.fixture
def api_key():
    # Get desired api key
    return os.environ['PY_SDK_STAGING_KEY']

@pytest.fixture
def api_options():
    """ Returns an example dictionary configuration. """
    return {'debug': True}

@pytest.fixture
def api(api_key, api_options):
    """ Returns an instance of the API. """
    return skylab_studio.api(api_key, **api_options)

def test_api_no_key():
    """ Test api host setting. """
    with pytest.raises(Exception):
        skylab_studio.api(None)

def test_api_host():
    """ Test api host setting. """
    assert skylab_studio.api('KEY', api_host='test.com').api_host == 'test.com'

def test_api_proto():
    """ Test api proto setting. """
    assert skylab_studio.api('KEY', api_proto='http').api_proto == 'http'

def test_api_port():
    """ Test api port setting. """
    assert skylab_studio.api('KEY', api_port='80').api_port == '80'

def test_api_version():
    """ Test api version setting. """
    assert skylab_studio.api('KEY', api_version='2').api_version == '2'

def test_api_debug():
    """ Test api debug setting. """
    assert skylab_studio.api('KEY', debug=True).debug is True

def test_list_jobs(api):
    """ Test list jobs endpoint. """
    result = api.list_jobs()
    assert result.status_code == 200

def test_create_job(api):
    """ Test list jobs endpoint. """
    job_name = str(uuid.uuid4())
    job_payload = {
      'name': job_name,
      'profile_id': 24
    }

    result = api.create_job(payload=job_payload)
    global job_id

    job_id = result.json()['id']
    assert job_id is not None
    assert result.status_code == 201

def test_get_job(api):
    global job_id
    assert job_id is not 0

    result = api.get_job(job_id)
    assert result.status_code == 200

def test_update_job(api):
    global job_id
    new_job_name = str(uuid.uuid4())
    payload = {
        'name': new_job_name
    }
    result = api.update_job(job_id, payload=payload)
    assert result.status_code == 200

def test_cancel_job(api):
    job_name = str(uuid.uuid4())
    job_payload = {
      'name': job_name,
      'profile_id': 24
    }

    result = api.create_job(payload=job_payload)
    job_id = result.json()['id']
    job_cancel_result = api.cancel_job(job_id)
    assert job_cancel_result.status_code == 200

def test_delete_job(api):
    job_name = str(uuid.uuid4())
    job_payload = {
      'name': job_name,
      'profile_id': 24
    }

    result = api.create_job(payload=job_payload)
    job_id = result.json()['id']

    result = api.delete_job(job_id)
    assert result.status_code == 200


def test_list_profiles(api):
    result = api.list_profiles()
    assert result.status_code == 200

def test_create_profile(api):
    global profile_id
    profile_name = str(uuid.uuid4())
    payload = {
        'name': profile_name,
        'enable_crop': False
    }
    result = api.create_profile(payload=payload)
    profile_id = result.json()['id']

    assert profile_id is not None
    assert result.status_code == 201

def test_get_profile(api):
    global profile_id
    result = api.get_profile(profile_id)
    assert result.status_code == 200

def test_update_profile(api):
    global profile_id
    payload = {
        'description': 'a description!'
    }
    result = api.update_profile(profile_id, payload=payload)
    assert result.status_code == 200

def test_list_photos(api):
    result = api.list_photos()
    assert result.status_code == 200

def test_create_photo(api):
    global photo_id
    global profile_id

    job_name = str(uuid.uuid4())
    job_payload = {
      'name': job_name,
      'profile_id': 24
    }

    result = api.create_job(payload=job_payload)
    job_id = result.json()['id']

    photo_name = str(uuid.uuid4())
    payload = {
        "job_id": job_id,
        "name": photo_name,
        "use_cache_upload": False
    }

    photo_result = api.create_photo(payload=payload)
    photo_id = photo_result.json()['id']

    assert photo_id is not 0
    assert result.status_code == 201

def test_get_photo(api):
    global photo_id
    result = api.get_photo(photo_id)
    assert result.status_code == 200

def test_delete_photo(api):
    global photo_id
    result = api.delete_photo(photo_id)
    assert result.status_code == 200
