from contextlib import contextmanager

from netbox.context import current_request, events_queue
from .events import flush_events


@contextmanager
def event_tracking(request):
    """
    Queue interesting events in memory while processing a request, then flush that queue for processing by the
    events pipline before returning the response.

    :param request: WSGIRequest object with a unique `id` set
    """
    current_request.set(request)
    events_queue.set([])

    yield

    # Flush queued webhooks to RQ
    flush_events(events_queue.get())

    # Clear context vars
    current_request.set(None)
    events_queue.set([])
