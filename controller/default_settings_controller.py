
class DefaultSettingsController:
    def __init__(self):
        from factories.model_factory import ModelFactory
        self.default_settings_service = ModelFactory.create_default_settings_service()

    def set_default_settings(self):
        self.default_settings_service.set_default_settings()
