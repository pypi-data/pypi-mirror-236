# -*- coding: utf-8 -*-
import pytest
from _pytest.terminal import TerminalReporter

from . import models
from .wrappers import OutcomeCharacters, UnicodeWrapper

_PSPEC_OPTIONS = [
    ('pspec_passed', 'passed',
     'prefix strings for passed tests, you may use unicodeescape here',),
    ('pspec_failed', 'failed',
     'prefix strings for failed tests, you may use unicodeescape here',),
    ('pspec_skipped', 'skipped',
     'prefix strings for skipped tests, you may use unicodeescape here',),
    ('pspec_default', 'default',
     'prefix strings for other tests, you may use unicodeescape here',),
]


def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting', 'reporting', after='general')
    group.addoption(
        '--pspec', action='store_true', dest='pspec', default=False,
        help='Report test progress in pspec format'
    )
    for x, _, help_message in _PSPEC_OPTIONS:
        parser.addini(
            x,
            help=help_message,
            default=None
        )


@pytest.mark.trylast
def pytest_configure(config):
    if config.option.pspec:
        # Get the standard terminal reporter plugin and replace it with ours
        standard_reporter = config.pluginmanager.getplugin('terminalreporter')
        pspec_reporter = PspecTerminalReporter(standard_reporter.config)
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(pspec_reporter, 'terminalreporter')


def pytest_collection_modifyitems(config, items):
    if not config.option.pspec:
        return

    for item in items:
        node = item.obj
        parent = item.parent.obj
        node_parts = item.nodeid.split('::')
        node_str = node.__doc__ or node_parts[-1]

        if hasattr(item, "callspec"):
            node_str = node_str.format(**item.callspec.params)

        mode_str = node_parts[0]
        klas_str = ''
        node_parts_length = len(node_parts)

        if node_parts_length > 3:
            klas_str = parent.__doc__ or node_parts[-3]
        elif node_parts_length > 2:
            klas_str = parent.__doc__ or node_parts[-2]

        item._nodeid = '::'.join([mode_str, klas_str, node_str])


class PspecTerminalReporter(TerminalReporter):

    def __init__(self, config, file=None):
        TerminalReporter.__init__(self, config, file)
        self._last_header = None
        self.pattern_config = models.PatternConfig(
            files=self.config.getini('python_files'),
            functions=self.config.getini('python_functions'),
            classes=self.config.getini('python_classes')
        )
        self.result_wrappers = []
        self.result_wrappers.append(UnicodeWrapper)
        for option_name, attr_name, _ in _PSPEC_OPTIONS:
            value = config.getini(option_name)
            if value:
                try:
                    value = eval(f"'{value}'")
                except:
                    pass
                setattr(OutcomeCharacters, attr_name, value)

    def _register_stats(self, report):
        """
        This method is not created for this plugin, but it is needed in order
        to the reporter display the tests summary at the end.

        Originally from:
        https://github.com/pytest-dev/pytest/blob/47a2a77/_pytest/terminal.py#L198-L201
        """
        res = self.config.hook.pytest_report_teststatus(
            report=report,
            config=self.config)
        category = res[0]
        self.stats.setdefault(category, []).append(report)
        self._tests_ran = True

    def pytest_runtest_logreport(self, report):
        self._register_stats(report)

        if report.when != 'call' and not report.skipped:
            return

        result = models.Result.create(report, self.pattern_config)

        for wrapper in self.result_wrappers:
            result = wrapper(result)

        self._last_header = result.header
        self._tw.sep(' ')
        self._tw.line(result.header)
        self._tw.line(str(result))
