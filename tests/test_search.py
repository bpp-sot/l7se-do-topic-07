"""
test_search.py
--------------
Automated test suite for the StudyTrack /students/search endpoint.

Run with:
    pytest -v
"""


def test_search_returns_results_for_known_surname(client):
    response = client.get('/students/search?surname=Smith')
    assert response.status_code == 200
    assert len(response.get_json()) > 0


def test_search_returns_empty_list_for_unknown_surname(client):
    response = client.get('/students/search?surname=Zzzznotaname')
    assert response.status_code == 200
    assert response.get_json() == []


def test_search_response_contains_expected_fields(client):
    response = client.get('/students/search?surname=Jones')
    data = response.get_json()
    assert 'student_id' in data[0]
    assert 'first_name' in data[0]
    assert 'last_name' in data[0]


def test_search_handles_empty_input(client):
    response = client.get('/students/search?surname=')
    assert response.status_code == 200
