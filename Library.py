#Parent class library item
class LibraryItem:

    def __init__(self, library_item_id, title):
        self ._library_item_id = library_item_id
        self ._title = title
        self ._checked_out_by = None
        self ._requested_by = None
        self ._location = 'ON_SHELF'
        self ._date_checked_out = 0

    #Functions to both get and set almost every parameter
    def get_library_item_id(self):
        return self ._library_item_id

    def get_title(self):
        return self ._title

    def get_checked_out_by(self):
        return self ._checked_out_by

    def get_requested_by(self):
        return self ._requested_by

    def get_location(self):
        return self ._location

    def get_date_checked_out(self):
        return self ._date_checked_out

    def set_date_checked_out(self, checked_out):
        self ._date_checked_out = checked_out

    def set_location(self, location):
        self ._location = location

    def set_checked_out_by(self, checked_out_by):
        self ._checked_out_by = checked_out_by

    def set_requested_by(self, requested_by):
        self ._requested_by = requested_by


#Book class inherits from LibraryItem, has an author parameter
class Book(LibraryItem):

    def __init__(self, library_item_id, title, author):
        super(). __init__(library_item_id, title)
        self ._author = author
        self ._check_out_length = 21

    def get_check_out_length(self):
        return self ._check_out_length

    def get_author(self):
        return self ._author


#Book class inherits from LibraryItem, has an artist parameter
class Album(LibraryItem):

    def __init__(self, library_item_id, title, artist):
        super(). __init__(library_item_id, title, )
        self ._artist = artist
        self ._check_out_length = 14

    def get_check_out_length(self):
        return self ._check_out_length

    def get_artist(self):
        return self ._artist


#Book class inherits from LibraryItem, has a director parameter
class Movie(LibraryItem):

    def __init__(self, library_item_id, title, director):
        super(). __init__(library_item_id, title)
        self ._director = director
        self ._check_out_length = 7

    def get_check_out_length(self):
        return self ._check_out_length

    def get_director(self):
        return self ._director


#Patron class is used in Library like the previous classes
class Patron:

    def __init__(self, patron_id, name):
        self ._patron_id = patron_id
        self ._name = name
        self ._checked_out_items = []
        self ._fine_amount = 0

    #get functions for all parameters, as well as 2 functions to add and remove from the _checked_out_items and a function to add to fines
    def get_patron_id(self):
        return self ._patron_id

    def get_name(self):
        return self ._name

    def get_checked_out_items(self):
        return self ._checked_out_items

    def get_fine_amount(self):
        return self ._fine_amount

    def add_library_item(self, library_item):
        self ._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        for i in self ._checked_out_items:
            if i == self ._checked_out_items:
                self ._checked_out_items.remove(library_item)

    def amend_fine(self, fine):
        self ._fine_amount -= fine


#Primary class of the program, calls upon all other classes
class Library:

    def __init__(self):
        self ._current_day = 0
        self ._holdings = []
        self ._members = []

    def add_library_item(self, library_item):
        self ._holdings.append(library_item)

    def add_patron(self, patron):
        self ._members.append(patron)

    #The look up methods are used in following methods as a way to initialize a variable into a LibraryItem or Patron
    def look_up_library_id(self, item_id):
        for i in self ._holdings:
            if i.get_library_item_id() == item_id:
                return i
        else:
            return None

    def look_up_patron_id(self, patron_id):
        for i in self ._members:
            if i.get_patron_id() == patron_id:
                return i
        else:
            return None

    def check_out_library_item(self, patron_id, item_id):
        #initializing two local variables for ease
        item = self.look_up_library_id(item_id)
        patron = self.look_up_patron_id(patron_id)

        #If either the patron or item ids don't exist, they return these statements
        if patron is None:
            return 'patron not found'
        elif item is None:
            return 'item not found'

        #This code first checks if the library item is checked out. If not, it checks if it's requested. If it is, it checks to see
        #if the Patron is the requester. If so, it updates the LibraryItems location, check out date, check-out status, and clears the
        #Patron from the requester area. If they weren't the requester but the LibraryItem wasn't on hold, the same code plays out,
        #excluding the updating of the requester. In any other scenario, a fail return statement is given.
        if item.get_checked_out_by() is None:
            if item.get_requested_by() is None:
                item.set_location('CHECKED_OUT')
                item.set_date_checked_out(self._current_day)
                patron.add_library_item(item)
                item.set_checked_out_by(patron)
                return 'check out successful'
            elif item.get_requested_by() == patron:
                item.set_location('CHECKED_OUT')
                item.set_date_checked_out(self._current_day)
                item.set_requested_by(None)
                patron.add_library_item(item)
                item.set_checked_out_by(patron)
                return 'check out successful'
            else:
                return 'item on hold by other patron'
        else:
            return 'item already checked out'

    def return_library_item(self, item_id):
        item = self.look_up_library_id(item_id)
        if item is not None:
            patron = item.get_checked_out_by()
        elif item is None:
            return 'item not found'

        #This section ensures that the item will be returned only if the item exists and was checked out. It removes the item from the
        #patron who current has it checked out, sets who it is checked out by to None, sets it checked_out_by to the current date (which
        #doesn't matter as when it is checked out later, the date will be updated again), and puts it on either the regular shelf or hold
        #shelf depending on if it is requested or not.
        if patron is None:
            return 'item already in library'
        else:
            patron.remove_library_item(item)
            if item.get_requested_by is None:
                item.set_location('ON_SHELF')
            elif item.get_requested_by is not None:
                item.set_location('ON_HOLD_SHELF')
            item.set_checked_out_by(None)
            item.set_date_checked_out(self ._current_day)
            return 'return successful'

    #This function adds a patron to the request list if the item is not already requested
    def request_library_item(self, patron_id, item_id):
        item = self.look_up_library_id(item_id)
        patron = self.look_up_patron_id(patron_id)

        if patron is None:
            return 'patron not found'
        elif item is None:
            return 'item not found'

        if item.get_requested_by() is None:
            item.set_requested_by(patron)
            if item.get_location == 'ON_SHELF':
                item.set_location('ON_HOLD_SHELF')
            return 'request successful'
        else:
            return 'item already on hold'

    #This will subtract from the fine by the amount paid. Notably, amend is actually a subtraction method because of this function
    def pay_fine(self, patron_id, amount_paid):
        patron = self.look_up_patron_id(patron_id)

        if patron is None:
            return 'patron not found'

        patron.amend_fine(amount_paid)

    #Increment the day and increase the fine by 10 cents if the patron has held it for longer than the check out length. Notably, the fine
    #appears to be negative 10 cents in this function, but it will become positive as it is amend_fine uses subtraction rather than addition
    def increment_current_date(self):
        self ._current_day = self ._current_day + 1
        for i in self ._members:
            for j in i.get_checked_out_items():
                if (self ._current_day - j.get_date_checked_out()) > j.get_check_out_length():
                    i.amend_fine(-.10)
