from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    location = 'static/assets/files'