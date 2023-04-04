import signal
import time

from django import db
from django.core.management.base import BaseCommand
from django.utils import timezone

from drf_anonymous_login.models import AnonymousLogin


class Command(BaseCommand):
    help = "Cleanup (remove) any expired AnonymousLogin instances"

    def _handle_options(self, options):
        self.tick = options["tick"]

    def _handle_termination(self, sig, frame):
        self._running = False

    def handle(self, *args, **options):
        # Load given options.
        self._handle_options(options)

        while self._running:
            time.sleep(self.tick)

            try:
                self.handle_tick()

            except Exception as exc:
                self.stdout.write(
                    "%s exception occurred ... " % (exc.__class__.__name__,), ending=""
                )
                self.stdout.flush()
                self.stdout.write(self.style.ERROR("FATAL"))
                self.stdout.flush()

                # As the database connection might have failed, we discard it here, so django will
                # create a new one on the next database access.
                db.close_old_connections()

    @staticmethod
    def handle_tick():
        # get all AnonymousLogin that already expired and delete them
        AnonymousLogin.objects.filter(
            expiration_datetime__isnull=False,
            expiration_datetime__lte=timezone.now(),
        ).delete()

    def add_arguments(self, parser):
        # Optional argument for setting the sleep time in seconds after each
        # iteration (a.k.a. tick time).
        parser.add_argument(
            "--tick",
            action="store",
            dest="tick",
            type=int,
            default=1,
            help="Sleep time after each iteration in seconds.",
        )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        # The command will run as long as the `_running` attribute is
        # set to `True`. To safely quit the command, just set this attribute to `False` and the
        # command will finish a running tick and quit afterwards.
        self._running = True

        self.tick = 1  # every second

        # Register system signal handler to gracefully quit the service when
        # getting a `SIGINT` or `SIGTERM` signal (e.g. by CTRL+C).
        signal.signal(signal.SIGINT, self._handle_termination)
        signal.signal(signal.SIGTERM, self._handle_termination)
