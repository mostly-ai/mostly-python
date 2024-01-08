class TestMostlyClient:
    def test_temp_get_token(self, mostly_client):
        token = mostly_client._temp_get_token()
        assert len(token) > 20
