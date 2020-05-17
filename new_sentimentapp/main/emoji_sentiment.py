import emoji
import regex
from bs4 import BeautifulSoup
import requests

# url of a dataset
url = "http://kt.ijs.si/data/Emoji_sentiment_ranking/"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")

# extract emojis from given message
def split_text(text):
    emojis = []
    data = regex.findall(r'\X', text)
    for x in data:
        if any(char in emoji.UNICODE_EMOJI for char in x):
            emojis.append(x)
    return emojis

# get final pos, neg, neutr scores for all emojis
def emoji_sentiment(message = [], *args):
	# local variables
	emoji_map = {}
	text = split_text(message[0])
	count_of_emojis = 0
	total_positivity = 0.0
	total_negatitivity = 0.0
	total_neutrality = 0.0
	total_sentiment_score = 0.0

	for x in text:
		for row in soup.find('tbody').find_all('tr'):
			cols = row.find_all('td')
			firstUnicode = cols[2].string
			secondUnicode = 'U+{:X}'.format(ord(x)).lower()
			if firstUnicode[-3:] == secondUnicode[-3:]:
				count_of_emojis += 1
				total_positivity += float(cols[7].string)
				total_negatitivity += float(cols[5].string)
				total_neutrality += float(cols[6].string)
				total_sentiment_score += float(cols[8].string)
	if count_of_emojis!=0:
		final_positivity = total_positivity / count_of_emojis
		final_negatitivity = total_negatitivity / count_of_emojis
		final_neutrality = total_neutrality / count_of_emojis
		final_sentiment_score = total_sentiment_score / count_of_emojis
		return final_positivity, final_neutrality, final_negatitivity, final_sentiment_score
	else:
		return None

# print(emoji_sentiment(["🤣жалко Алматушечку горы наши, что имеем не ценим и не бережём, последнее уничтожаем. А ведь это наше достояние, красота, свежий воздух"]))
