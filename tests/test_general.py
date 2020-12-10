def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'St. Bakhita Catholic Church' in res.data


def test_checkin(app, client):
    res = client.post('/checkin', data=dict(
        number="020"
    ), follow_redirects=True)
    assert res.status_code == 200
    assert b'St. Bakhita Catholic Church' in res.data