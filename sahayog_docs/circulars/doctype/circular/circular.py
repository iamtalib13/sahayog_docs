# Copyright (c) 2024, Talib Sheikh and contributors
# For license information, please see license.txt
import re
import frappe
from frappe.model.document import Document

class Circular(Document):
	pass
def before_insert(self):
        file = self.circular_doc
        if file:
            # Define a regular expression to extract the required components
            regex = r'Circular No\. (\d+) \((\d{4}-\d{2})\) (.+) Date (\d{2}-\d{2}-\d{4})\.pdf'
            match = re.match(regex, file)

            if match:
                id = f'Circular No. {match.group(1)}'
                year = match.group(2)
                file_name = match.group(3)
                date = match.group(4)

                self.date = date
                self.circular_id = id
                self.year = year
                self.circular_name = file_name
                self.name=file_name
            else:
                frappe.logger().debug('Filename does not match the expected pattern')