class Connector:
    def locations(self, prefix: str = "") -> object:
        if self.client:
            # skip
            # Those comments
            # will not be copied
            # /skip
            return self.client.locations(connector_id=self.id, prefix=prefix)


class Generator:
    def tables(self) -> object:
        if self.client:
            return self.client.generator_tables(connector_id=self.id)
