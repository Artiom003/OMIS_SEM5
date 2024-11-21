from ..base_default_settings_service import BaseDefaultSettingsService


class DefaultSettingsService(BaseDefaultSettingsService):
    def __init__(self):
        from factories.model_factory import ModelFactory
        self.work_schedule_repository = ModelFactory.create_work_schedule_repository(self.FILE)
        self.default_settings_repository = ModelFactory.create_default_settings_repository(self.FILE)

    def set_default_settings(self):
        self.default_settings_repository.create_tables()
        if not self.work_schedule_repository.check_exists("08:00", "18:00",
                                                          "08:00", "18:00",
                                                          "08:00", "18:00",
                                                          "08:00", "18:00",
                                                          "08:00", "18:00",
                                                          "08:00", "18:00",
                                                          "-", "-"):
            self.work_schedule_repository.add_work_schedule("08:00", "18:00",
                                                            "08:00", "18:00",
                                                            "08:00", "18:00",
                                                            "08:00", "18:00",
                                                            "08:00", "18:00",
                                                            "08:00", "18:00",
                                                            "-", "-")
