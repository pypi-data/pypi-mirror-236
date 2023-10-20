# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import logging
import sys
import traceback
from datetime import timedelta
from io import StringIO
from django.conf import settings
from django.utils import timezone
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from lino.api import dd, rt, _
from lino.core.roles import SiteStaff
from lino import logger
from lino.mixins import Sequenced
from lino.modlib.checkdata.choicelists import Checker
from lino.modlib.system.mixins import RecurrenceSet
from .choicelists import Procedures, LogLevels



# VERBOSITY_CHOICES = [
#    (0, _("silent")),
#    (1, _("normal")),
#    (2, _("verbose")),
#    (3, _("very verbose"))
# ]



# class SetupTasks(dd.Action):
#     """Run this only in development environment."""
#     label = _("Setup tasks")
#     help_text = _("Run this action only in development environment (not designed for production environment).")
#     select_rows = False
#
#     def run_from_ui(self, ar, **kwargs):
#         if not settings.SITE.is_demo_site:
#             ar.error(message="Action is not allowed in production site.")
#             return
#         from lino.modlib.linod.tasks import Tasks
#         Tasks().setup()
#         ar.success(refresh_all=True)


class RunNow(dd.Action):
    label = _("Run now")
    select_rows = True
    # icon_name = 'bell'
    # icon_name = 'lightning'

    def run_from_ui(self, ar, **kwargs):
        for obj in ar.selected_rows:
            assert isinstance(obj, rt.models.linod.JobRule)
            obj.start_job(ar)
        ar.set_response(refresh_all=True)


class JobRule(Sequenced, RecurrenceSet):
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'JobRule')
        app_label = 'linod'
        verbose_name = _("Background job")
        verbose_name_plural = _("Background jobs")

    # name = dd.CharField(max_length=50, default="", blank=True)
    procedure = Procedures.field(strict=False, unique=True)
    log_level = LogLevels.field(default='DEBUG')
    disabled = dd.BooleanField(default=False)
    # silent = dd.BooleanField(default=True)
    # verbosity = dd.IntegerField(_("Verbosity"), default=0, choices=VERBOSITY_CHOICES)
    last_start_time = dd.DateTimeField(_("Started at"), null=True, editable=False)
    last_end_time = dd.DateTimeField(_("Ended at"), null=True, editable=False)
    message = dd.RichTextField(format='plain', editable=False)

    # setup_tasks = SetupTasks()
    run_now = RunNow()

    def disabled_fields(self, ar):
        df = super().disabled_fields(ar)
        df.add('procedure')
        return df

    @classmethod
    async def run_them_all(cls, ar):
        # ar.debug("20231013 run_them_all()")
        now = timezone.now()
        next_time = now + timedelta(seconds=12)
        if False:  # both work
            rules = await sync_to_async(cls.objects.filter)(disabled=False)
        else:
            rules = cls.objects.filter(disabled=False)
        async for self in rules:
        # for jr in rules:
            # ar.info("20231010 start %s", jr)
            if self.last_start_time is None:
                await self.start_job(ar)
                assert self.last_end_time is not None
                nst = self.get_next_suggested_date(ar, self.last_end_time)
                next_time = min(next_time, nst)
            elif self.last_end_time is not None:
                nst = self.get_next_suggested_date(ar, self.last_end_time)
                if nst <= now:
                    await self.start_job(ar)
                    assert self.last_end_time is not None
                    nst = self.get_next_suggested_date(ar, self.last_end_time)
                # else:
                #     ar.debug("20231013 Skip %s for now", self)
                next_time = min(next_time, nst)

        return next_time

    async def start_job(self, ar):
        # ar.info("Start %s", self)
        if self.last_end_time is None and self.last_start_time is not None:
            raise Warning("{} is already running".format(self))
            # return
        self.last_start_time = timezone.now()
        # forget about any previous run:
        self.last_end_time = None
        self.message = ''
        await database_sync_to_async(self.full_clean)()
        await database_sync_to_async(self.save)()
        with ar.capture_logger(self.log_level.num_value) as out:
            ar.info("Start background job %s", self)
            try:
                await self.procedure.run(ar)
                # job.message = ar.response.get('info_message', '')
                self.message = out.getvalue()
            except Exception as e:
                self.message = out.getvalue()
                self.message += '\n' + ''.join(traceback.format_exception(e))
                self.disabled = True
        # ar.logger = logger  # restore default value
        self.last_end_time = timezone.now()
        self.message = "<pre>" + self.message + "</pre>"
        await database_sync_to_async(self.full_clean)()
        await database_sync_to_async(self.save)()

    def __str__(self):
        r = "{} #{} {}".format(
            self._meta.verbose_name, self.pk, self.procedure.value)
        # if self.disabled:
        #     r += " ('disabled')"
        return r



# class Jobs(dd.Table):
#     model = 'linod.Job'
#     required_roles = dd.login_required(SiteStaff)
#     column_names = "start_time end_time rule message *"
#     detail_layout = """
#     rule
#     start_time end_time
#     message
#     """


# class JobsByRule(Jobs):
#     master_key = 'rule'
#     column_names = "start_time end_time message *"
#

class JobRules(dd.Table):
    # label = _("System tasks")
    model = 'linod.JobRule'
    required_roles = dd.login_required(SiteStaff)
    column_names = "seqno procedure every every_unit log_level disabled last_start_time last_end_time *"
    detail_layout = """
    seqno procedure every every_unit
    log_level disabled
    last_start_time last_end_time
    message
    """
    insert_layout = """
    procedure
    every every_unit
    """


class JobsChecker(Checker):
    """

    Checks for procedures that do not yet have a background job database row.

    """
    verbose_name = _("Check for missing job rules")
    model = None

    def get_checkdata_problems(self, obj, fix=False):
        JobRule = rt.models.linod.JobRule

        for proc in Procedures.get_list_items():
            if JobRule.objects.filter(procedure=proc).count() == 0:
                msg = _("Missing background job for {}").format(proc)
                yield (True, msg)
                if fix:
                    logger.debug(f"Create job rule from {proc!r}")
                    jr = JobRule(procedure=proc,
                        every_unit=proc.every_unit, every=proc.every_value)
                    # if proc.every_unit.value in "sm":
                    #     jr.log_level = "ERROR"
                    # else:
                    #     jr.log_level = "INFO"
                    jr.full_clean()
                    jr.save()

JobsChecker.activate()
