from django.apps import AppConfig
import os

class RoomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "room"
    
    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            # This ensures the code inside runs only in the main process
            print('ready...')
            from room import tasks
            tasks.start()