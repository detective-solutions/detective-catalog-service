# import third party module
from pydantic import Field

# import project related module
from detective_catalog_service.service.models.connector.main import PropertyModel

# TODO: Checkout
#  https://arsenvlad.medium.com/presto-querying-data-in-azure-blob-storage-and-azure-data-lake-store-99149c8c796
# Hive configuration needs a special hive meta store


class AzureDataLakeStorageGen2(PropertyModel):
    connectorName: str = "hive"
    storageAccountName: str = Field(title="storage account name", description="The name of the ADLS Gen2"
                                                                              "storage account")
    accessKey: str = Field(title="storage account name", description="The decrypted access key for the ADLS Gen2 "
                                                                     "storage account")

    def as_properties(self):
        config = {
            "connector.name": self.connectorName,
            "hive.azure.abfs": self.storageAccountName,
            "hive.azure.abfs-access-key": self.accessKey

        }

        auto_default_fields = {
            "connector.name": "hive"
        }

        for key, value in auto_default_fields.items():
            if value is not None:
                config[key] = value
        return config
