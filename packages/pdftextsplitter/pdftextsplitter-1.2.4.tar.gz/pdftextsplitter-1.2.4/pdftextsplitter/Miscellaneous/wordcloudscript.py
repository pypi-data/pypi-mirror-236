from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Load the text file
text_file = open("testdocument.txt", "r")
text = text_file.read()

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=800,
                        max_words=20,
                        background_color='white',
                        stopwords=set(STOPWORDS),
                        min_font_size=10).generate(text)

# Plot the WordCloud image
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

# Show the plot
plt.show()