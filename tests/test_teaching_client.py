"""Offline tests for unauthenticated Apps Script teaching-plan client."""
import pytest
from professorx import teaching_client as client

@pytest.fixture(autouse=True)
def clean_cache():
    client._PLAN_CACHE.clear()
    yield
    client._PLAN_CACHE.clear()

def test_reject_non_google_endpoint(monkeypatch):
    for url in ['http://script.google.com/macros/s/test/exec',
                'https://evil.example/macros/s/test/exec',
                'https://script.google.com.evil.example/macros/s/test/exec',
                'https://script.google.com/macros/s/test/exec?x=1']:
        monkeypatch.setenv('PROFESSORX_APPS_SCRIPT_URL',url)
        with pytest.raises(RuntimeError, match='HTTPS'):
            client._endpoint()

def test_validate_subject_before_network(monkeypatch):
    monkeypatch.setattr(client.httpx,'Client',lambda **kw: pytest.fail('Should not make network request'))
    with pytest.raises(ValueError,match='Subject'):
        client.request_teaching_plan('private-file-id','LEARN')

def test_cached_request_contains_no_student_identity(monkeypatch):
    monkeypatch.setenv('PROFESSORX_APPS_SCRIPT_URL','https://script.google.com/macros/s/test/exec')
    sent=[]
    class Response:
        status_code=200
        def raise_for_status(self): pass
        def json(self):
            return {'ok':True,'subject':'RTES','mode':'LEARN','cache_seconds':900,
                    'policy_version':'beta-1','plan':{'sections':['Concept']}}
    class FakeHTTP:
        def __init__(self,**kwargs):
            assert kwargs['follow_redirects'] is False
        def __enter__(self): return self
        def __exit__(self,*_): pass
        def post(self,url,json,headers):
            sent.append((url,json,headers))
            return Response()
    monkeypatch.setattr(client.httpx,'Client',FakeHTTP)
    assert client.request_teaching_plan('rtes','learn')['plan']['sections']==['Concept']
    assert client.request_teaching_plan('RTES','LEARN')['plan']['sections']==['Concept']
    assert len(sent)==1
    assert set(sent[0][1])=={'action','subject','mode'}
    client.request_teaching_plan('RTES','LEARN',force_refresh=True)
    assert len(sent)==2

def test_gateway_errors_not_ignored(monkeypatch):
    monkeypatch.setenv('PROFESSORX_APPS_SCRIPT_URL','https://script.google.com/macros/s/test/exec')
    class Response:
        status_code=200
        def raise_for_status(self): pass
        def json(self):return {'ok':False,'error':'INVALID_ACTION'}
    class FakeHTTP:
        def __init__(self,**kwargs):pass
        def __enter__(self):return self
        def __exit__(self,*_):pass
        def post(self,*args,**kwargs):return Response()
    monkeypatch.setattr(client.httpx,'Client',FakeHTTP)
    with pytest.raises(RuntimeError,match='INVALID_ACTION'):
        client.request_teaching_plan('PAD','EXAM')

def test_only_google_content_redirect_allowed(monkeypatch):
    monkeypatch.setenv('PROFESSORX_APPS_SCRIPT_URL','https://script.google.com/macros/s/test/exec')
    class Response:
        status_code=302
        headers={'location':'https://attacker.example/steal'}
    class FakeHTTP:
        def __init__(self,**kwargs):pass
        def __enter__(self):return self
        def __exit__(self,*_):pass
        def post(self,*args,**kwargs):return Response()
        def get(self,url):pytest.fail('Must never request attacker redirect')
    monkeypatch.setattr(client.httpx,'Client',FakeHTTP)
    with pytest.raises(RuntimeError,match='Unexpected redirect'):
        client.request_teaching_plan('ESD','LEARN')

def test_public_skill_copies_are_identical_and_private_catalog_absent():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    copies=[root/'SKILL.md',root/'skills/professorx/SKILL.md']
    assert len({p.read_text(encoding='utf-8') for p in copies})==1
    assert not (root/'references/source-catalog.json').exists()
    assert 'LectureNotes_RTA.pdf' not in copies[0].read_text(encoding='utf-8')


def test_unexpected_gateway_fields_are_dropped(monkeypatch):
    monkeypatch.setenv('PROFESSORX_APPS_SCRIPT_URL','https://script.google.com/macros/s/test/exec')
    class Response:
        status_code=200
        def raise_for_status(self): pass
        def json(self):
            return {'ok':True,'subject':'SES','mode':'LEARN', 'private_policy':'never return',
                    'plan':{'sections':['A'], 'owner_notes':'private', 'checks':[],
                            'source_guidance':[], 'interaction':[]}}
    class FakeHTTP:
        def __init__(self,**kw):pass
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def post(self,*args,**kw):return Response()
    monkeypatch.setattr(client.httpx,'Client',FakeHTTP)
    result=client.request_teaching_plan('SES','LEARN')
    assert 'private_policy' not in result
    assert 'owner_notes' not in result['plan']
    assert result['plan']['sections']==['A']
