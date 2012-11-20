#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import xml.etree.ElementTree as ET

# TODO:
# 1) Find out whether these patches are necessary
# 2) learn how to write and test patches properly


# I don't want to mess with ANYthing :)
def tostring(elem, enc, meth):
	return ET.tostring(elem, enc, meth)
def fromstring(text):
	return ET.fromstring(text)
def SubElement(parent, tag):
	return ET.SubElement(parent, tag)

class Element(ET.Element):
	
	# Replacement for ET's 'findtext' function, which has a bug
	# that will return empty string if text field contains integer with
	# value of zero (0); If there is no match, return None
	def findElementText(self, match):
		elt = self.find(match)
		if elt is not None:
			return(elt.text)
		else:
			return(None)


	def findAllText(self, match):
		# Searches element and returns list that contains 'Text' attribute
		# of all matching sub-elements. Returns empty list if element
		# does not exist
	
		try:
			return [result.text for result in self.findall(match)]
		except:
			return []

	
	def appendChildTagWithText(self, tag, text):
		# Append childnode with text
		
		el = ET.SubElement(self, tag)
		el.text = text
		
	def appendIfNotEmpty(self,subelement):
		# Append sub-element, but only if subelement is not empty
		
		if len(subelement) != 0:
			self.append(subelement)
	
	def toxml(self, indent = "  "):
		return(ET.tostring(self, 'UTF-8','xml'))
		
		# Disabled pretty-printing for now as minidom appears to choke on
		# entity references, i.e. code below will go wrong:
		#
		# return minidom.parseString(selfAsString).toprettyxml(indent)

