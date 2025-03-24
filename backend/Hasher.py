import regex as re


class hasher():
	def __init__(self):

		self.keys = {
			"A":"##z",
			"B":"#z#",
			"C":"z##",
			"D":"##a",
			"E":"#a#",
			"F":"a##",
			"G":"##y",
			"H":"#y#",
			"I":"y##",
			"J":"##b",
			"K":"#b#",
			"L":"b##",
			"M":"##x",
			"N":"#x#",
			"O":"x##",
			"P":"##c",
			"Q":"#c#",
			"R":"c##",
			"S":"##w",
			"T":"#w#",
			"U":"w##",
			"V":"##d",
			"W":"#d#",
			"X":"d##",
			"Y":"##v",
			"Z":"#v#",
			"a":"##q",
			"b":"#q#",
			"c":"q##",
			"d":"##e",
			"e":"#e#",
			"f":"e##",
			"g":"##s",
			"h":"#s#",
			"i":"s##",
			"j":"##f",
			"k":"#f#",
			"l":"f##",
			"m":"##u",
			"n":"#u#",
			"o":"u##",
			"p":"##g",
			"q":"#g#",
			"r":"g##",
			"s":"##t",
			"t":"#t#",
			"u":"t##",
			"v":"h##",
			"w":"#h#",
			"x":"##h",
			"y":"##r",
			"z":"#r#"
		}

		self.Hashed = []
		self.Unhashed = []
		self.pattern1 = "[A-Z]"
		self.pattern2 = "[a-z]"
		self.pattern3 = "[0-9]"
		self.email_pattern = ".*@.*\\..*"

	def hash(self,password):
		for letter in password:
			try:
				rep = self.keys[letter]
			except:
				rep = str(letter)*3
			self.Hashed.append(rep)
		result = "".join(self.Hashed)
		self.Hashed = []
		return result

	def unhash(self,password):
		split_count = len(password)//3
		groups = []
		result = []
		start = 0
		for part in range(split_count):
			end = start+3
			part = password[start:end]
			groups.append(part)
			start=end
		
		all_keys = list(self.keys.keys())
		all_values = list(self.keys.values())
		for part in groups:
			try:
				position = all_values.index(part)
				character = all_keys[position]
				result.append(character)
			except:
				character = part[0]
				result.append(character)
		return "".join(result)

	def password_validity(self,password):
		check1 = re.findall(self.pattern1,password)
		if len(password) < 6:
			result = "Passwords cannot be less than 6 characters"
			return result
		elif len(check1) == 0:
			result = "Password must contain upper case character"
			return result
		else:
			check2 = re.findall(self.pattern2,password)
			if len(check2) == 0:
				result = "Password must contain lower case character"
				return result
			else:
				check3 = re.findall(self.pattern3,password)
				if len(check3) == 0:
					result = "Password must contain an Integer"
					return result
				else:
					result = True
					return result

	def email_validity(self,email):
		result = re.findall(self.email_pattern,email)
		if len(result) == 0:
			return False
		else:
			return True

			