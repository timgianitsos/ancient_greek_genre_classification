import os
import sys
from cltk.tokenize.sentence import TokenizeSentence

class Features:
	def freq_interrogatives(file):
		num_interrogative = 0

		for line in file:
			num_interrogative += line.count(";")

		return num_interrogative / len(file)

	def freq_conditional_characters(file):
		num_conditional_characters = 0
		num_characters = 0

		for line in file:
			num_conditional_characters += line.count("εἲ") + line.count("ἐάν") + line.count("εἰ")
			num_characters += len(line)

		return num_conditional_characters / num_characters

tesserae_clone_command = "git clone https://github.com/tesserae/tesserae.git"
greek_text_dir = "tesserae/texts/grc"

def main():
	global greek_text_dir

	#Associates files names to their respective features
	text_to_features = {}

	file_names = None
	if len(sys.argv) > 1:
		if sys.argv[1] == "debug": #if debug, just scan pre-selected corpus
			file_names = ["tesserae/texts/grc/polybius.histories.tess"]
		else: #Allows user to select custom path other than tesserae
			greek_text_dir = sys.argv[1]

	#Download corpus if non-existent
	if not os.path.isdir(greek_text_dir):
		print("Corpus at " + greek_text_dir + " does not exist - attempting to clone repository...")
		os.system(tesserae_clone_command)

	#Obtain all the files to parse by traversing through the directory
	if file_names is None:
		file_names = [current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
		os.walk(greek_text_dir) for current_file_name in current_file_names if current_file_name.endswith(".tess")]

	#Feature extraction
	for file_name in file_names:
		text_to_features[file_name] = {}

		#Store each line of file in a list
		file_text = []
		with open(file_name, "r") as file:
			for line in file:
				#Ignore lines without tess tags, or parse the tag out and strip whitespace
				if not line.startswith("<"):
					continue
				assert ">" in line
				line = line[line.index(">") + 1:].strip()
				file_text.append(line)

		#Convert list of strings into a single string, then break that into sentences using cltk tokenizer
		file_text = " ".join(file_text)
		tokenizer = TokenizeSentence("greek")
		file_text = tokenizer.tokenize_sentences(file_text)

		#Invoke those values of the Feature class which are functions
		for feature in Features.__dict__.values():
			if callable(feature):
				score = feature(file_text)
				text_to_features[file_name][feature] = score
				print(file_name + ", " + str(feature) + ", " + str(score))

if __name__ == "__main__":
	main()