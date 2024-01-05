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
            return self.client.add_table(generator_id=self.id, **kwargs)

    def add_table_by_upload(self, **kwargs) -> "Table":
        if self.client and hasattr(self.client, "add_table_by_upload"):
            return self.client.add_table_by_upload(generator_id=self.id, **kwargs)

    def add_table_from_df_by_upload(self, **kwargs) -> "Table":
        if self.client and hasattr(self.client, "add_table_from_df_by_upload"):
            return self.client.add_table_from_df_by_upload(
                generator_id=self.id, **kwargs
            )
