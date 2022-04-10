import uuid


def generate_task_id() -> str:
    """
    Return unique string for task id.
    """
    return uuid.uuid4().hex
