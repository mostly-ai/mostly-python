class TestMostlyClient:
    def test_temp_get_token(self, mostly):
        token = mostly._temp_get_token()
        assert len(token) > 20
