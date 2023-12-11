import logging

from django.conf import settings

from huey.contrib.djhuey import on_startup, pre_execute, task
from huey.exceptions import CancelExecution


@on_startup()
def setup_slack_logging():
    """
    On startup, add a handler (e.g. a Slack handler) for logging
    in the 'huey' namespace. Ensure module containing this
    method is included in settings.INSTALLED_APPS .e.g.:

    INSTALLED_APPS = [
        # ...misc installed apps...
        'utils.huey',
    ]

    """
    LOGGING = settings.LOGGING
    slack_handler = LOGGING['handlers']['slack']  # could be any handler...
    logging.getLogger('huey').addHandler(slack_handler)


@pre_execute()
def inspect_huey_allowed_tasks_registry(task):
    """
    Before executing a task, check whether the task is registered in
    settings.HUEY_ALLOWED_TASKS_REGISTRY. Ensure module containing this
    method is included in settings.INSTALLED_APPS .e.g.:

    INSTALLED_APPS = [
        # ...misc installed apps...
        'utils.huey',
    ]

    """
    if f"{task.__module__}.{task.name}" not in settings.HUEY_ALLOWED_TASKS_REGISTRY:
        # cancel execution
        raise CancelExecution()


@task()
def test_task_exception_handling():
    raise Exception()
