class OutcomeCharacters:
    passed = '\N{cherry blossom}'
    failed = '\N{wilted flower}'
    skipped = '\N{warning sign}\N{vs16}'
    default = '\N{warning sign}\N{vs16}'
    short_passed = '\N{cherry blossom}'
    short_failed = '\N{wilted flower}'
    short_skipped = 's'
    short_default = 's'

    @classmethod
    def get_outcome(cls, result):
        return getattr(cls, result.outcome, cls.default)

    @classmethod
    def get_short_outcome(cls, result):
        return getattr(cls, f'short_{result.outcome}', cls.default)

