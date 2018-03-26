from celery.result import AsyncResult

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

from polyaxon.celery_api import app as celery_app
from polyaxon.settings import Intervals

from libs.models import DiffModel, DescribableModel
from pipelines.constants import OperationStatus, TriggerRule


class Schedule(DiffModel):
    """A model that represents the scheduling behaviour of an operation or a pipeline."""
    frequency = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Defines how often to run, "
                  "this timedelta object gets added to your latest operation instance's "
                  "execution_date to figure out the next schedule", )
    start_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this instance should run, "
                  "default is None which translate to now.")
    end_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this instance should stop running, "
                  "default is None which translate to open ended.")
    depends_on_past = models.BooleanField(
        default=False,
        help_text="when set to true, the instances will run "
                  "sequentially while relying on the previous instances' schedule to succeed.")


class ExecutableModel(models.Model):
    """A model that represents an execution behaviour of an operation or a pipeline."""
    EXECUTABLE_RELATED_NAME = ''

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=EXECUTABLE_RELATED_NAME)
    schedule = models.OneToOneField(
        Schedule,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    execute_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this instance should be executed. "
                  "default None which translate to now")
    timeout = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="specify how long this instance should be up "
                  "before timing out in seconds.")


class Pipeline(DiffModel, DescribableModel, ExecutableModel):
    """A model that represents a pipeline (DAG - directed acyclic graph).

    A Pipeline is a collection / namespace of operations with directional dependencies.
    A Pipeline can optionally have
     * a schedule (e.g. daily, hourly, ...)
     * a start end an end date

    Every operation has dependencies, and can only run when all the dependencies are met.

    Certain operations can depend on their own past, i.e that they can't run
    until their previous schedule (and upstream operations) are completed.

    A pipeline can also have dependencies/upstream pipelines/operations.
    """
    EXECUTABLE_RELATED_NAME = 'pipelines'

    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of operation instances allowed to run concurrently")

    @property
    def dag(self):
        """Construct the DAG of this pipeline based on the its operations and their downstream."""
        dag = {}
        ops = {}
        operations = self.operations.all()
        operations = operations.prefetch_related('downstream_operations')

        for operation in operations:
            downstream_ops = operation.downstream_operations.values_list('id', flat=True)
            dag[operation.id] = set(downstream_ops)
            ops[operation.id] = operation

        return dag, ops


class Operation(DiffModel, DescribableModel, ExecutableModel):
    """ Base class for all Operations.

    To derive this class, you are expected to override
    the constructor as well as the 'execute' method.

    Operations derived from this class should perform or trigger certain behaviour
    synchronously (wait for completion).

    Instantiating a class derived from this one results in the creation of a operation object,
    which ultimately could run independently or becomes a node in DAG objects.

    N.B.1: The `start_date` for the operation, determines
        the `execution_date` for the first operation instance. The best practice
        is to have the start_date rounded
        to your DAG's `schedule`. Daily jobs have their `start_date`
        some day at 00:00:00, hourly jobs have their start_date at 00:00
        of a specific hour. Note that Polyaxon simply looks at the latest
        `execution_date` and adds the `schedule_interval` to determine
        the next `execution_date`. It is also very important
        to note that different operations' dependencies
        need to line up in time. If operation A depends on operation B and their
        `start_date` are offset in a way that their execution_date don't line
        up, A's dependencies will never be met.

    Add for wait for downstream `wait_for_downstream` of upstream operations before running.
    """
    EXECUTABLE_RELATED_NAME = 'operations'

    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='operations')
    upstream_operations = models.ManyToManyField(
        "self",
        blank=True,
        null=True,
        related_name='downstream_operations')
    trigger_rule = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=TriggerRule.ALL_SUCCESS,
        choices=TriggerRule.CHOICES,
        help_text="defines the rule by which dependencies are applied, "
                  "default is `all_success`.")
    max_retries = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of retries that should be performed before failing the operation.")
    retry_delay = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=Intervals.DEFAULT_RETRY_DELAY,
        help_text="The delay between retries.")
    retry_exponential_backoff = models.BooleanField(
        default=False,
        help_text="allow progressive longer waits between "
                  "retries by using exponential backoff algorithm on retry delay.")
    max_retry_delay = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=Intervals.MAX_RETRY_DELAY,
        help_text="maximum delay interval between retries.")
    n_retries = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of retries that performed so far by the operations.")
    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="When set, a operation will be able to limit the concurrent "
                  "runs across execution_dates")
    run_as_user = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="unix username to impersonate while running the operation.")
    resources = models.OneToOneField(
        'jobs.JobResources',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    celery_task = models.CharField(
        max_length=128,
        help_text="The celery task name to execute.")
    celery_queue = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="The celery queue name to use for the executing this task. "
                  "If provided, it will override the queue provided in CELERY_TASK_ROUTES.")

    @property
    def independent(self):
        return self.pipeline is None

    def get_countdown(self, retries):
        """Calculate the countdown for a celery task retry."""
        retry_delay = self.retry_delay
        if self.retry_exponential_backoff:
            return min(
                max(2 ** retries, retry_delay),  # Exp. backoff
                self.max_retry_delay  # The countdown should be more the max allowed
            )
        else:
            return retry_delay

    def get_run_kwargs(self):
        kwargs = {}
        if self.celery_queue:
            kwargs['queue'] = self.celery_queue

        if self.timeout:
            kwargs['soft_time_limit'] = self.timeout
            # We set also a hard time limit that will send sig 9
            # This hard time limit should not happened, as it will set inconsistent state
            kwargs['time_limit'] = self.timeout + settings.CELERY_HARD_TIME_LIMIT_DELAY

        if self.execute_at:
            kwargs['eta'] = self.execute_at

        return kwargs


class RunModel(DiffModel):
    """
    A model that represents an execution behaviour of instance/run of a operation or a pipeline.
    """
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the instance started.")
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the instance finished.")
    status = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=OperationStatus.CREATED,
        choices=OperationStatus.CHOICES)

    class Meta:
        abstract = True

    def on_run(self):
        self.status = OperationStatus.RUNNING
        self.save()

    def on_timeout(self):
        self.status = OperationStatus.FAILED
        self.save()

    def on_failure(self):
        self.status = OperationStatus.FAILED
        self.save()

    def on_success(self):
        self.status = OperationStatus.SUCCESS
        self.save()

    def on_stop(self):
        self.status = OperationStatus.STOPPED
        self.save()


class PipelineRun(RunModel):
    """A model that represents an execution behaviour/run of instance of a pipeline.

    Since this is an instance of known Pipeline,
    we can store the sorted topology of the dag,
    which should should not change during the execution time.
    """
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        related_name='runs')


class OperationRun(RunModel):
    """A model that represents an execution behaviour/run of instance of an operation."""
    operation = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        related_name='runs')
    pipeline_run = models.ForeignKey(
        PipelineRun,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='operation_runs')
    upstream_runs = models.ManyToManyField(
        'self',
        blank=True,
        null=True,
        related_name='downstream_runs')
    retried_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the instance last retried.")
    celery_task_context = JSONField(
        blank=True,
        null=True,
        help_text='The kwargs required to execute the celery task.')
    celery_task_id = models.UUIDField(null=False, blank=True)

    def can_start(self):
        """Checks the upstream and the trigger rule."""
        if self.operation.trigger_rule == TriggerRule.ONE_DONE:
            return self.upstream_runs.filter(
                status__in=OperationStatus.DONE_STATUS).exists()
        if self.operation.trigger_rule == TriggerRule.ONE_SUCCESS:
            return self.upstream_runs.filter(
                status=OperationStatus.SUCCESS).exists()
        if self.operation.trigger_rule == TriggerRule.ONE_FAILED:
            return self.upstream_runs.filter(
                status=OperationStatus.FAILED).exists()
        if self.operation.trigger_rule == TriggerRule.ALL_DONE:
            return self.upstream_runs.exclude(
                status__in=OperationStatus.DONE_STATUS).exists()
        if self.operation.trigger_rule == TriggerRule.ALL_SUCCESS:
            return self.upstream_runs.exclude(
                status=OperationStatus.SUCCESS).exists()
        if self.operation.trigger_rule == TriggerRule.ALL_FAILED:
            return self.upstream_runs.exclude(
                status=OperationStatus.FAILED).exists()

    def notify_downstream(self):
        """Notify downstream that this instance is done, and that its dependency can start."""
        for pipeline in self.downstream_operations.filter(status=OperationStatus.CREATED):
            pipeline.check_and_start()

    def schedule(self):
        """Schedule the task: check first if the task is startable and then start it"""
        if self.status != OperationStatus.CREATED:
            return
        self.status = OperationStatus.SCHEDULED
        self.save()
        if self.can_start():
            self.start()

    def start(self):
        """Start the celery task of this operation."""
        async_result = celery_app.send_task(
            self.operation.celery_task,
            kwargs=self.celery_task_context,
            **self.operation.get_run_kwargs())
        self.celery_task_id = async_result.id
        self.started_at = timezone.now()
        self.status = OperationStatus.STARTED
        self.save()

    def stop(self):
        self.task = AsyncResult(self.celery_task_id)
        self.task.revoke(terminate=True, signal='SIGKILL')
        self.status = OperationStatus.STOPPED
        self.save()

    def on_retry(self):
        self.status = OperationStatus.RETRYING
        self.save()
