'''
Before running this module, Run the below commands in CMD.

pip install fire
pip install tabulate
'''

import fire
import datetime

from tabulate import tabulate

class BookLibrary(object):
	'''
	Class to maintain the books in a Library.
	'''
	# Dictionary to store the Books information.
	books = {'Book1': {'author': 'Author1', 'assigned': False},
			 'Book2': {'author': 'Author2', 'assigned': True},
			 'Book3': {'author': 'Author3', 'assigned': False}
			 }
	# List to store Student Names.
	customers = ['Cus1', 'Cus2', 'Cus3', 'Cus4']

	# Dictionaty to store the Assigned Books.
	assigned_history = {}

	def show_books(self):
		'''
		Method to display the available books in Library.

		Args:
			None

		Returns:
			Books Information in tabular format.

		Command: python book_library.py show_books
		'''
		# Fetch all the books
		data = [[book, details['author'], details['assigned']] for book, details in self.books.items()]
		# Printing in tabular format.
		print(tabulate(data, headers=["Book Name", "Author", "Status"]))

	def show_book(self, book_name):
		'''
		Method to display specific book information.

		Args:
			book_name: <string>

		Returns:
			Specific Book Information from Library.

		Command: python book_library.py show_book <book_name>
		'''
		# Check if book is available in Library
		if book_name in self.books:
			# Print book info..
			return f"{book_name} \t {self.books[book_name]['author']} \t {self.books[book_name]['assigned']}"
		else:
			return f"{book_name} is not available in Library."

	def assign_book(self, book_name, customer_name, duration=14):
		'''
		Method to assign a specific book to Student.

		Args:
			book_name: <string>
			customer_name: <string>
			duration: <int> (Limited to 14 days)

		Returns:
			Assigned book info along with all books information.

		Command: python book_library.py assign_book <book_name> <customer_name> <duration>
		'''
		# Check if the book is avialable
		if book_name and customer_name:
			# Don't assign if the book is already assigned.
			if self.books[book_name]['assigned']:
				return f"{book_name} is already assigned." 
			# Check if the the customer is available
			if str(customer_name) in self.customers:
				# Get current date
				cur_date = datetime.datetime.now().date()
				# Duration should not be more that 14 days.
				if duration <= 14:
					till = cur_date + datetime.timedelta(duration)
				else:
					return "Book can't assigned for more than two weeks."
				# Update Assignment Hisory.
				self.assigned_history[book_name] = {
					'customer': customer_name,
					'start': cur_date,
					'to': till}
				self.books[book_name]['assigned'] = True
				# Display all the books with status.
				self.show_books()
				return f"{book_name} is assigned to {customer_name}, It should be returned on or before {str(till)}"
			else:
				return f"{customer_name} is not available. Check the name"
		else:
			return f"{book_name} is not available in Library."


	def add_book(self, book_name, author_name, assigned=False):
		'''
		Method to add a book to Library.

		Args:
			book_name: <string>
			author_name: <string>
			assigned: <boolean>

		Returns:
			Added book info along with all books information.

		Command: python book_library.py add_book <book_name> <author_name> <assigned>
		'''
		# Check if the book is available in Library.
		if book_name not in self.books:
			# Add book info.
			self.books[book_name] = {'author': author_name, 'assigned': assigned}
			print(f'{book_name} is added to Library.')
			# Display all books for confirmation.
			self.show_books()
		else:
			return f"{book_name} already exist in Library, Can't be added."

	def delete_book(self, book_name):
		'''
		Method to delete a specific book from Library.

		Args:
			book_name: <string>

		Returns:
			Deleted book info along with all books information.

		Command: python book_library.py delete_book <book_name>
		'''
		# Check if the book is available in Library.
		if book_name in self.books:
			if self.books[book_name]['assigned']:
				return "Book is assigned, First collect the book and the try removing.. "
			else:
				# Delete book from Library
				self.books.pop(book_name)
				# Display remaining books.
				self.show_books()
				return f"{book_name} has been removed from Library"
		else:
			return f"{book_name} doesn't exist in Library.. Can't be deleted."

	def update_book(self, book_name, author_name='', status=False):
		'''
		Method to update a specific book in Library.

		Args:
			book_name: <string>
			author_name: <string>
			status: <boolean>

		Returns:
			Updated book info along with all books information.

		Command: python book_library.py update_book <book_name> <author_name> <status>
		'''
		# Check if the book is available in Library.
		if book_name in self.books:
			# If the book is already assigned and if the status \
			# is False then remove book from assignment_history
			if book_name in self.assigned_history and not status:
				self.assigned_history.pop(book_name)
			# Dictionary to update book info.
			data = {'author': author_name if author_name else self.books[
					 book_name]['author'],
					'assigned': status if status != self.books[
					book_name]['assigned'] else self.books[book_name]['assigned']}
			# Update book info.
			self.books[book_name] = data
			# Display updated book info
			print(self.show_book(book_name))
			return f"{book_name} info has been updated..."
			
		else:
			return f"{book_name} is not in Library."

if __name__ == '__main__':
	fire.Fire(BookLibrary)