from neomodel import (
    StructuredRel,
    DateTimeProperty,
    IntegerProperty,
)
from datetime import datetime


class DateIntervalRelationship(StructuredRel):
    '''DateIntervalRelationship This class handles the relationship with date interval.

    This class sets up the attribute for a relationship that needs a datetime interval (such as READ).
    '''
    now = datetime.now()
    since = DateTimeProperty(
        default=now
    )
    to = DateTimeProperty()


class DateRelationship(StructuredRel):
    '''DateRelationship This class handles the relationship with a single date attribute.

    This class sets up the attribute for a relationship that needs a specific date (such as RESERVE).
    '''
    now = datetime.now()
    on = DateTimeProperty(
        default=now
    )


class VoteRelationship(StructuredRel):
    '''VoteRelationship This class handles the relationship with an integer.

    This class sets up the attribute for a relationship that needs an integer attribute (such as VOTE).
    '''
    star = IntegerProperty(
        default=1
    )
