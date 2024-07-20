# views for CRUD operations
# create
from .createbook import CreateBook
from .createlibrary import CreateLibrary
from .createhosts import CreateHosts
from .createvote import CreateVote
# create + update READ
from .managereaduser2book import ManageReadUser2Book
# create + delete RESERVE
from .managereserveuser2book import ManageReserveUser2Book
# create + update User
from .manageuser import ManageUser

# read
from .readbook import ReadBook
from .readbooklend import ReadBookLend
from .readbooksearch import ReadBookSearch
from .readlists import ReadLists
from .readsuggestion import ReadSuggestion
from .readhistory import ReadHistory

# update
from .updateauthor import UpdateAuthor
from .updatebook import UpdateBook


'''

# create
from .managebook.createbook import CreateBook
from .managebook.createlibrary import CreateLibrary
from .managebook.createhosts import CreateHosts
from .manageuser.createvote import CreateVote
# create + update READ
from .manageuser.managereaduser2book import ManageReadUser2Book
# create + delete RESERVE
from .manageuser.managereserveuser2book import ManageReserveUser2Book
# create + update User
from .manageuser.manageuser import ManageUser

# read
from .managebook.readbook import ReadBook
from .managebook.readbooklend import ReadBookLend
from .managebook.readbooksearch import ReadBookSearch
from .readlists import ReadLists
from .manageuser.readsuggestion import ReadSuggestion
from .manageuser.readhistory import ReadHistory

# update
from .managebook.updateauthor import UpdateAuthor
from .managebook.updatebook import UpdateBook

'''
