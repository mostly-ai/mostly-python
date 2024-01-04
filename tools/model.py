class Connector:
    # skip
    # Those comments
    # will not be copied
    # /skip
    def locations(self, prefix: str = "") -> list:
        if self.client and hasattr(self.client, "locations"):
            return self.client.locations(connector_id=self.id, prefix=prefix)


class Generator:
    def add_table(self, **kwargs) -> "Table":
        if self.client and hasattr(self.client, "add_table"):
            return self.client.add_table(gnerator_id=self.id, **kwargs)
