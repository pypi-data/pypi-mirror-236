# -*- coding: utf-8 -*-
import pytest
from .wrappers import OutcomeCharacters

_PSPEC_OPTIONS = [
    ('pspec_passed', 'passed',
     'prefix strings for passed tests, you may use unicodeescape here',),
    ('pspec_failed', 'failed',
     'prefix strings for failed tests, you may use unicodeescape here',),
    ('pspec_skipped', 'skipped',
     'prefix strings for skipped tests, you may use unicodeescape here',),
    ('pspec_default', 'default',
     'prefix strings for other tests, you may use unicodeescape here',),
    ('pspec_short_passed', 'short_passed',
     'short status for passed tests, you may use unicodeescape here',),
    ('pspec_short_failed', 'short_failed',
     'short status for failed tests, you may use unicodeescape here',),
    ('pspec_short_skipped', 'short_skipped',
     'short status for skipped tests, you may use unicodeescape here',),
    ('pspec_short_default', 'short_default',
     'short status for other tests, you may use unicodeescape here',),
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
    parser.addini(
        'pspec_show_header',
        help='displays the header at the start of report output',
        default='false'
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    for option_name, attr_name, _ in _PSPEC_OPTIONS:
        value = config.getini(option_name)
        if value:
            try:
                value = eval(f"'{value}'")
            except:  # pragma: nocover
                pass
            setattr(OutcomeCharacters, attr_name, value)


def pytest_collection_modifyitems(config, items):
    if not config.option.pspec:
        return
    if config.option.verbose == 0:
        return

    last_mode_str = None
    for item in items:
        node = item.obj
        node_parts = item.nodeid.split('::')
        node_str = node.__doc__ or node_parts[-1]
        node_str = node_str.strip()

        mode_str = node_parts[0]
        if mode_str != last_mode_str:
            last_mode_str = mode_str
            item._nodeid = f'{mode_str}\n  {node_str}'
        else:
            item._nodeid = f'  {node_str}'


@pytest.hookimpl()
def pytest_report_teststatus(report, config):
    boo = report.when == 'call'
    boo = boo or report.when == 'setup' and report.outcome == 'skipped'
    if config.option.pspec and boo:
        if config.option.verbose:
            emoji = OutcomeCharacters.get_outcome(report)
        else:
            emoji = OutcomeCharacters.get_short_outcome(report)
        spaces = '.' * 80
        node_len = len(report.nodeid.rsplit('\n', 1)[-1].strip())
        suffix = ''
        if config.option.verbose > 0:
            suffix = f' [{report.duration:7.2f}s]'
        result = f'{spaces[:75 - node_len]}{emoji}{suffix}'
        return report.outcome, emoji, (result, {})
