First, you need to import the modules from the package:

.. code:: ipython3

    import tidyX.TextPreprocessor as tp
    import tidyX.WordNormalization as wn
    import tidyX.SpacyVisualizer as tv

``remove_repetitions``
-------------------------

**Description of the function**

This function deletes any consecutive repetition of characters in a
string. For example, the string ‘coooroosooo’ will be changed to
‘coroso’. As in many languages it’s common to have some special
characters that can be repeated, for example the ‘l’ in spanish to form
‘ll’, the exception argument could be used to specify which characters
are allowed to repeat once.

**When is it useful to use it?**

In social media, it is common for people to repeat certain characters of
a word in order to add more emotion to a sentence. However, when we
attempt to count the occurrences of a word, the various ways in which a
word can be written make it difficult to uniquely identify each
instance. One simple solution to this issue is to use the
``remove_repetitions`` function. Let’s consider the following tweet:

.. raw:: html

    <center>
    <img src="https://raw.githubusercontent.com/lgomezt/tidyX/main/docs/source/examples/remove_repetitions1.png" alt="remove_repetitions1" height=300px />
    </center>


In this particular case, the author writes “Goooal” and “Goal.”
Consequently, it becomes necessary for us to eliminate the repeated “o”s
in the first word in order to make both words equal.

.. code:: ipython3

    string_example = "Goooal ⚽️⚽️⚽️ Christiano Ronaldo Amazing Goal Juventus vs Real Madrid 1-3 Champions League Final #JUVRMA #UCLFinal2017 #JuventusRealMadrid"
    print("Before:", string_example)

.. parsed-literal::

    Before: Goooal ⚽️⚽️⚽️ Christiano Ronaldo Amazing Goal Juventus vs Real Madrid 1-3 Champions League Final #JUVRMA #UCLFinal2017 #JuventusRealMadrid
    
.. code:: ipython3

    string_without_repetitions = tp.remove_repetitions(string = string_example, exceptions = None)
    print("After:", string_without_repetitions)


.. parsed-literal::

    After: Goal ⚽️⚽️⚽️ Christiano Ronaldo Amazing Goal Juventus vs Real Madrid 1-3 Champions League Final #JUVRMA #UCLFinal2017 #JuventusRealMadrid
    

However, it’s worth noting that there exist numerous words that feature
the repetition of a single character. To address this, the
``remove_repetitions`` function incorporates the ``exceptions``
parameter, which allows for specifying a list of characters that are
permitted to appear twice. For instance, if we set
``exceptions = ['p']``, words such as ‘happpy’ will be cleaned and
transformed into ‘happy’. The default value for this parameter is
``['r', 'l', 'n', 'c', 'a', 'e', 'o']``. Let’s see another example:

.. raw:: html

    <center>
    <img src="https://raw.githubusercontent.com/lgomezt/tidyX/main/docs/source/examples/remove_repetitions2.png" alt="remove_repetitions2" height=300px />
    </center>


.. code:: ipython3

    string_example = "HAPPPYYYYY GRADUATION TO US!! THANKYOUUUU LORD!!! 🫶🤍"
    print("Before:", string_example)

.. parsed-literal::

    Before: HAPPPYYYYY GRADUATION TO US!! THANKYOUUUU LORD!!! 🫶🤍
    

.. code:: ipython3

    string_without_repetitions = tp.remove_repetitions(string = string_example, 
        exceptions = ["P"])
    print("After:", string_without_repetitions)


.. parsed-literal::

    After: HAPPY GRADUATION TO US! THANKYOU LORD! 🫶🤍
    

``remove_last_repetition``
-----------------------------

**Description of the function**

The ``remove_last_repetition`` function is designed to remove the
repetition of the last character in each word of a given string. It’s
particularly useful when dealing with text that contains repeated
characters at the end of words, a common occurrence in social media
posts where users emphasize words for expression. This function helps
clean and standardize the text by eliminating these last-character
repetitions.

**When is it useful to use it?**

Suppose you're analyzing text data from social media platforms, and you aim 
to maintain consistency in your analysis by eliminating repetitive characters 
at the ends of words. In Spanish, for instance, words usually don't conclude 
with repeated characters. However, social media users frequently emphasize 
words by duplicating the last letter. Let's delve into a practical example 
using a tweet:

.. code:: ipython3

    # Original tweet with last-character repetitions
    string_example = "Holaaaa amigooo"
    print("Before:", string_example)
    
    # Apply remove_last_repetition function to clean the text
    string_without_last_repetitions = tp.remove_last_repetition(string = string_example)
    print("After:", string_without_last_repetitions)


.. parsed-literal::

    Before: Holaaaa amigooo
    After: Hola amigo
    

In this case, the input string contains repeated characters at the end
of words, like “Holaaaa” and “amigooo.” To ensure consistent analysis,
you can use the ``remove_last_repetition`` function, which removes the
last-character repetitions and transforms the text into “Hola amigo.”

``remove_urls``
------------------

**Description of the function**

The ``remove_urls`` function is designed to remove all URLs that start
with “http” from a given string. It’s a handy tool for text processing
when you want to eliminate URLs from a text dataset, making it cleaner
and more focused on textual content. This function scans the entire
string, identifies any sequences of characters that start with “http”
and continue until a space or end of the line, and removes them.

**When is it useful to use it?**

You may encounter situations where you want to analyze or visualize the
textual content of a dataset, but the presence of URLs can clutter the
text and skew your analysis. This is especially common in social media
data, chat messages, or web scraping scenarios. Let’s explore a
practical use case with a sample text containing URLs:

.. code:: ipython3

    # Original text with URLs
    string_example = "Check out our website: http://example.com. For more info, visit http://example2.com"
    print("Before:", string_example)
    
    # Apply remove_urls function to clean the text
    string_without_urls = tp.remove_urls(string = string_example)
    print("After:", string_without_urls)


.. parsed-literal::

    Before: Check out our website: http://example.com. For more info, visit http://example2.com
    After: Check out our website:  For more info, visit 
    

In this case, the input string contains two URLs, “http://example.com”
and “http://example2.com.” To focus on the textual content without the
distraction of URLs, you can use the ``remove_urls`` function, which
removes them and results in cleaner text.

``remove_RT``
----------------

**Description of the function**

The ``remove_RT`` function is designed to remove the “RT” prefix from
tweets. In the context of social media, “RT” typically stands for
“Retweet” and is often used as a prefix when users share or retweet
content. This function is useful for cleaning and standardizing tweet
text data by removing the “RT” prefix, accounting for varying amounts of
white space after “RT.”

**When is it useful to use it?**

When you’re working with tweet data and you want to analyze or visualize
the content of tweets without the distraction of the “RT” prefix, the
remove_RT function comes in handy. Retweets often have the “RT” prefix
at the beginning, but the amount of white space after “RT” can vary.
Let’s explore a practical use case:

.. code:: ipython3

    # Original tweet with "RT" prefix
    string_example = "RT     @username: Check out this amazing article!"
    print("Before:", string_example)
    
    # Apply remove_RT function to clean the tweet
    cleaned_tweet = tp.remove_RT(string = string_example)
    print("After:", cleaned_tweet)


.. parsed-literal::

    Before: RT     @username: Check out this amazing article!
    After: @username: Check out this amazing article!
    

In this case, the input tweet contains the “RT” prefix followed by
varying amounts of white space before the actual content of the tweet.
To focus on the tweet’s content and remove the “RT” prefix, you can use
the ``remove_RT`` function, which standardizes the text and results in a
tweet without the “RT” prefix.

``remove_accents``
---------------------

**Description of the function**

The ``remove_accents`` function serves two purposes: it removes accent
marks from characters in a given string and can optionally remove
emojis. Accent marks can be common in languages like French or Spanish
(this specific use case), and removing them can be helpful for text
processing tasks. This function provides flexibility by allowing you to
choose whether to remove emojis as well.

**When is it useful to use it?**

The ``remove_accents`` function is particularly useful when working with
text data that contains accented characters, and you want to simplify
the text for analysis or comparison. Additionally, if your text data
includes emojis that are not relevant to your analysis, you can choose
to remove them as well. Let’s explore a practical use case:

.. code:: ipython3

    # Original text with accents and emojis
    string_example = "Café ☕️ à côté de l'hôtel. 😃"
    print("Before:", string_example)
    
    # Apply remove_accents function to clean the text (removing emojis)
    cleaned_text = tp.remove_accents(string = string_example, delete_emojis = True)
    print("After:", cleaned_text)


.. parsed-literal::

    Before: Café ☕️ à côté de l'hôtel. 😃
    After: Cafe  a cote de l'hotel. 
    

In this case, the input text contains accented characters (e.g., “é”)
and emojis (e.g., “☕️” and “😃”). To simplify the text for analysis and
remove emojis, you can use the ``remove_accents`` function with the
``delete_emojis`` option set to True, resulting in cleaned text without
accents or emojis.

This method is flexible over the total number of followed emojis on a
text, let’s process a Spanish common example:

.. raw:: html

    <center>
    <img src="https://raw.githubusercontent.com/lgomezt/tidyX/main/docs/source/examples/remove_accents.png" alt="remove_accents" height=300px />
    </center>


.. code:: ipython3

    # Original text with accents and emojis
    string_example = "‼️ La función de traductor no funciona así que este tweet es solo para nuestros seguidores hispanohablantes, siempre van a ser nuestros favoritos y ahora vamos a poner emojis tristes para que los que no hablan español se preocupen 😭  y también esta foto fuera de contexto 😔💔"
    print("Before:", string_example)
    
    # Apply remove_accents function to clean the text (removing emojis)
    cleaned_text = tp.remove_accents(string = string_example, delete_emojis = True)
    print("After:", cleaned_text)


.. parsed-literal::

    Before: ‼️ La función de traductor no funciona así que este tweet es solo para nuestros seguidores hispanohablantes, siempre van a ser nuestros favoritos y ahora vamos a poner emojis tristes para que los que no hablan español se preocupen 😭  y también esta foto fuera de contexto 😔💔
    After: !! La funcion de traductor no funciona asi que este tweet es solo para nuestros seguidores hispanohablantes, siempre van a ser nuestros favoritos y ahora vamos a poner emojis tristes para que los que no hablan espanol se preocupen   y tambien esta foto fuera de contexto 
    

As we saw, the method removed continuously repeated emojis, but passes
over “!!” v2 class emojis (Link to the emoji:
https://abs-0.twimg.com/emoji/v2/svg/203c.svg). This is due to the fact
that it is considered an expression, rather not a direct emoji, when you
type double exclamation on Twitter. You can see a full list of this
wildcard emoji converter expressions on X’s documentation in
https://twemoji.twitter.com/ and some examples in
https://twitter.com/FakeUnicode/status/1251505174348095488

``remove_hashtags``
----------------------

**Description of the function**

The ``remove_hashtags`` function is designed to remove hashtags from a
given string. In social media and text data, hashtags are often used to
categorize or highlight content. This function scans the input string
and removes any text that starts with a ‘#’ and is followed by
alphanumeric characters, effectively removing hashtags from the text.

**When is it useful to use it?**

You might encounter situations where you want to analyze or visualize
text data without the presence of hashtags. Hashtags can be prevalent in
social media posts and may not be relevant to your analysis. Let’s
explore a practical use case:

.. code:: ipython3

    # Original text with hashtags
    string_example = "Exploring the beauty of #nature in #springtime. #NaturePhotography 🌼"
    print("Before:", string_example)
    
    # Apply remove_hashtags function to clean the text
    cleaned_text = tp.remove_hashtags(string = string_example)
    print("After:", cleaned_text)


.. parsed-literal::

    Before: Exploring the beauty of #nature in #springtime. #NaturePhotography 🌼
    After: Exploring the beauty of  in .  🌼
    

In this case, the input text contains hashtags such as “#nature,”
“#springtime,” and “#NaturePhotography.” To focus on the textual content
without the distraction of hashtags, you can use the ``remove_hashtags``
function, which removes them and results in a cleaner text.

``remove_mentions``
----------------------

**Description of the function**

The ``remove_mentions`` function is designed to remove mentions (e.g.,
@username) from a given tweet string. In the context of social media,
mentions are often used to reference or tag other users. This function
scans the input tweet string and removes any text that starts with ‘@’
followed by a username. Optionally, it can also return a list of unique
mentions found in the tweet.

**When is it useful to use it?**

You may encounter situations where you want to analyze or visualize
tweet text data without the presence of mentions. Mentions can be common
in social media posts and may not be relevant to your analysis.
Additionally, you might want to extract and track mentioned accounts
separately. Let’s explore a practical use case:

.. code:: ipython3

    # Original tweet with mentions
    string_example = "Exploring the beauty of nature with @NatureExplorer and @WildlifeEnthusiast. #NaturePhotography 🌼"
    print("Before:", string_example)
    
    # Apply remove_mentions function to clean the tweet and extract mentions
    cleaned_text, extracted_mentions = tp.remove_mentions(string=string_example, extract = True)
    print("After:", cleaned_text)
    print("Extracted Mentions:", extracted_mentions)


.. parsed-literal::

    Before: Exploring the beauty of nature with @NatureExplorer and @WildlifeEnthusiast. #NaturePhotography 🌼
    After: Exploring the beauty of nature with  and . #NaturePhotography 🌼
    Extracted Mentions: ['@WildlifeEnthusiast', '@NatureExplorer']
    

In this case, the input tweet text contains mentions such as
“@NatureExplorer” and “@WildlifeEnthusiast.” To focus on the textual
content without the distraction of mentions and to extract mentioned
accounts, you can use the ``remove_mentions`` function, which removes
mentions and provides a list of unique mentions found in the tweet.

``remove_special_characters``
--------------------------------

**Description of the function**

The ``remove_special_characters`` function is designed to remove all
characters from a string except for lowercase letters and spaces. It’s a
useful tool for cleaning text data when you want to focus on the textual
content while excluding punctuation marks, exclamation marks, special
characters, numbers, and uppercase letters. This function scans the
input string and removes any character that does not match the criteria.

**When is it useful to use it?**

You may encounter situations where you want to preprocess text data and
eliminate special characters and non-lowercase characters to make it
more suitable for natural language processing tasks. Cleaning text in
this way can help improve text analysis, topic modeling, or sentiment
analysis. Let’s explore a practical use case:

.. code:: ipython3

    string_example = "This is an example text! It contains special characters. 123"
    print("Before:", string_example)
    
    # Apply remove_special_characters function to clean the text
    cleaned_text = tp.remove_special_characters(string = string_example)
    print("After:", cleaned_text)


.. parsed-literal::

    Before: This is an example text! It contains special characters. 123
    After: his is an example text t contains special characters
    

In this case, the input text contains special characters, punctuation
marks, numbers, and uppercase letters. To focus on the textual content
with lowercase letters and spaces only, you can use the
``remove_special_characters`` function, which removes the undesired
characters and results in a cleaner text. Beware to lowercase your text
before applying this method over your corpus, as you can see on the past
example, it can remove useful strings.

``remove_extra_spaces``
--------------------------

**Description of the function**

The ``remove_extra_spaces`` function is designed to remove extra spaces
within and surrounding a given string. It’s a valuable tool for cleaning
text data when you want to standardize spaces, trim leading and trailing
spaces, and replace consecutive spaces between words with a single
space. This function helps improve the consistency and readability of
text.

**When is it useful to use it?**

You may encounter situations where you want to preprocess text data and
ensure consistent spacing for better readability and analysis. Extra
spaces can be common in unstructured text, and cleaning them can enhance
text analysis, especially when dealing with natural language processing
tasks. Let’s explore a practical use case:

.. code:: ipython3

    # Original text with extra spaces
    string_example = "This is    an   example  text with extra   spaces.     "
    print("Before:", string_example)
    
    # Apply remove_extra_spaces function to clean the text
    cleaned_text = tp.remove_extra_spaces(string = string_example)
    print("After:", cleaned_text)


.. parsed-literal::

    Before: This is    an   example  text with extra   spaces.     
    After: This is an example text with extra spaces.
    

In this case, the input text contains extra spaces between words and
leading/trailing spaces. To standardize the spacing and remove the extra
spaces, you can use the ``remove_extra_spaces`` function, which trims
leading/trailing spaces and replaces consecutive spaces with a single
space.

``space_between_emojis``
----------------------------

**Description of the function**

The ``space_between_emojis`` function is designed to insert spaces
around emojis within a given string. It ensures that emojis are
separated from other text or emojis in the string. This function is
helpful for improving the readability of text containing emojis and
ensuring proper spacing. It also removes any extra spaces resulting from
the insertion of spaces around emojis.

**When is it useful to use it?**

This function is particularly useful when you’re working with text data
that includes emojis and you want to enhance the visual presentation of
the text. Emojis are often used for expressing emotions or conveying
messages, and proper spacing ensures that emojis are distinct and do not
run together. Let’s explore a practical use case:

.. code:: ipython3

    # Original text with emojis
    string_example = "I love😍this place🌴It's amazing!👏"
    print("Before:", string_example)
    
    # Apply space_between_emojis function to add spaces around emojis
    cleaned_text = tp.space_between_emojis(string = string_example)
    print("After:", cleaned_text)


.. parsed-literal::

    Before: I love😍this place🌴It's amazing!👏
    After: I love 😍 this place 🌴 It's amazing! 👏
    

In this case, the input text contains emojis such as “😍,” “🌴,” and
“👏” mixed with regular text. To ensure that emojis are separated from
other text and from each other, you can use the ``space_between_emojis``
function, which inserts spaces around emojis and removes any extra
spaces resulting from the insertion.

``preprocess``
------------------

**Description of the function**

The ``preprocess`` function is a comprehensive text preprocessing tool
designed to clean and standardize tweet text. It applies a series of
cleaning functions to perform tasks such as removing retweet prefixes,
converting text to lowercase, removing accents and emojis, extracting or
removing mentions, removing URLs, hashtags, special characters, extra
spaces, and consecutive repeated characters with specified exceptions.
This function offers extensive text cleaning capabilities and prepares
tweet text for analysis or visualization.

**When is it useful to use it?**

The ``preprocess`` function is particularly useful when you’re working
with tweet data and need to clean and standardize the text for various
text analysis tasks. Tweet text can be messy and contain various
elements such as mentions, URLs, emojis, and special characters that may
need to be processed and standardized. Let’s explore a practical use
case:

.. code:: ipython3

    # Original tweet with various elements
    string_example = "RT @user1: I love this place! 😍 Check out the link: https://example.com #travel #vacation!!!"
    print("Before:", string_example)
    
    # Apply preprocess function to clean and preprocess the tweet
    cleaned_text, extracted_mentions = tp.preprocess(string = string_example, delete_emojis = True)
    print("After:", cleaned_text)
    print("Extracted Mentions:", extracted_mentions)


.. parsed-literal::

    Before: RT @user1: I love this place! 😍 Check out the link: https://example.com #travel #vacation!!!
    After: i love this place check out the link
    Extracted Mentions: ['@user1']
    

In this case, the input tweet text contains retweet prefixes, mentions,
emojis, URLs, hashtags, and special characters. To standardize the tweet
text for analysis, you can use the ``preprocess`` function, which
performs a series of cleaning operations to remove or extract various
elements and return cleaned text and mentions.

``remove_words``
--------------------

**Description of the function**

The ``remove_words`` function is designed to remove all occurrences of
specific words listed in the ``bag_of_words`` parameter from a given
string. This function is particularly useful for removing stopwords or
any other set of unwanted words from text data. It performs an exact
match, meaning it will remove only the exact words listed in the
``bag_of_words`` and won’t remove variations of those words that are not
in the list.

**When is it useful to use it?**

This function is valuable when you want to clean text data by removing
specific words that are not relevant to your analysis or that you
consider stopwords. It’s commonly used in natural language processing
tasks to improve the quality of text analysis, topic modeling, or
sentiment analysis. Let’s explore a practical use case:

.. code:: ipython3

    # Original text with stopwords
    string_example = "This is an example sentence with some unnecessary words like 'the', 'is', and 'with'."
    print("Before:", string_example)
    
    # List of stopwords to remove
    stopwords = ["the", "is", "and", "with"]
    print("Stopwords to Remove:", stopwords)
    
    # Apply remove_words function to clean the text
    cleaned_text = tp.remove_words(string = string_example, bag_of_words = stopwords)
    print("After:", cleaned_text)


.. parsed-literal::

    Before: This is an example sentence with some unnecessary words like 'the', 'is', and 'with'.
    Stopwords to Remove: ['the', 'is', 'and', 'with']
    After: This an example sentence some unnecessary words like '', '', ''.
    

In this case, the input text contains stopwords such as “the,” “is,” and
“with.” To clean the text by removing these stopwords, you can use the
``remove_words`` function, which removes the specified words from the
text.

``unnest_tokens``
---------------------

**Description of the function**

The ``unnest_tokens`` function is designed to flatten a pandas DataFrame
by tokenizing a specified column. It takes a pandas DataFrame, the name
of the column to tokenize, and an optional flag to create an “id” column
based on the DataFrame’s index. Each token in the specified column
becomes a separate row in the resulting DataFrame, effectively
“exploding” the data into a long format.

**When is it useful to use it?**

This function is useful when you have text data stored in a DataFrame,
and you want to transform it into a format that is more suitable for
certain text analysis or modeling tasks. For instance, when working with
natural language processing or text mining, you may need to tokenize
text data and represent it in a format where each token corresponds to a
separate row. Let’s explore a practical use case:

.. code:: ipython3

    import pandas as pd
    # Create a sample DataFrame with a text column
    data = {'text_column': ["This is a sample sentence.",
                            "Another sentence with tokens.",
                            "Text analysis is interesting."]}
    df = pd.DataFrame(data)
    print("Original DataFrame:")
    print(df)
    
    # Apply unnest_tokens function to tokenize the text column
    tokenized_df = tp.unnest_tokens(df=df, input_column='text_column')
    print("\nTokenized DataFrame:")
    print(tokenized_df)


.. parsed-literal::

    Original DataFrame:
                         text_column
    0     This is a sample sentence.
    1  Another sentence with tokens.
    2  Text analysis is interesting.
    
    Tokenized DataFrame:
       id   text_column
    0   0          This
    0   0            is
    0   0             a
    0   0        sample
    0   0     sentence.
    1   1       Another
    1   1      sentence
    1   1          with
    1   1       tokens.
    2   2          Text
    2   2      analysis
    2   2            is
    2   2  interesting.
    

In this case, the input DataFrame contains a column named ‘text_column’
with sentences. To tokenize the text and transform it into a long format
where each token is a separate row, you can use the ``unnest_tokens``
function.

``spanish_lemmatizer``
--------------------------

**Description of the function**

The ``spanish_lemmatizer`` function is designed to lemmatize a given
Spanish language token using Spacy’s Spanish language model. It takes a
token (word) and a Spacy language model object as input and returns the
lemmatized version of the token with accents removed. This function is
valuable for text analysis tasks where you need to reduce words to their
base or dictionary form.

**When is it useful to use it?**

This function is useful when you’re working with text data in Spanish
and want to perform text analysis tasks such as sentiment analysis,
topic modeling, or text classification. Lemmatization helps standardize
words to their base form, reducing the complexity of text data. Let’s
explore a practical use case:

.. code:: ipython3

    import spacy

.. code:: ipython3

    !python -m spacy download es_core_news_sm

.. code:: ipython3

    # Load Spacy's Spanish language model (you should have this model downloaded)
    nlp = spacy.load("es_core_news_sm")
    
    # Input token to lemmatize
    token = "corriendo"  # Example token in Spanish
    print("Original Token:", token)
    
    # Apply spanish_lemmatizer function to lemmatize the token
    lemmatized_token = tp.spanish_lemmatizer(token = token, model = nlp)
    print("Lemmatized Token:", lemmatized_token)


.. parsed-literal::

    Original Token: corriendo
    Lemmatized Token: correr
    

In this case, we have an input token, “corriendo,” in Spanish that we
want to lemmatize to its base form. We use the ``spanish_lemmatizer``
function to perform the lemmatization.

``create_bol``
------------------

**Description of the function**

The ``create_bol`` function is designed to group lemmas based on
Levenshtein distance to handle misspelled words in social media data. It
takes a numpy array containing lemmas and an optional verbose flag for
progress reporting. The function groups similar lemmas into bags of
lemmas based on their Levenshtein distance. The result is a pandas
DataFrame that contains information about the bags of lemmas, including
their IDs, names, associated lemmas, and the similarity threshold used
for grouping.

**When is it useful to use it?**

This function is useful when you’re dealing with text data, especially
social media data, where misspelled or variations of words are common.
Grouping similar lemmas together can help clean and organize text data
for analysis, improving the accuracy of text-based tasks like sentiment
analysis or topic modeling. Let’s explore a practical use case:

.. code:: ipython3

    import pandas as pd
    import numpy as np
    
    # Create a numpy array of lemmas
    lemmas = np.array(['apple', 'aple', 'apples', 'banana', 'banan', 'bananas', 'cherry', 'cheri', 'cherries'])
    print("Original Lemmas:")
    print(lemmas)
    
    # Apply create_bol function to group similar lemmas
    bol_df = tp.create_bol(lemmas=lemmas, verbose=True)
    print("\nBags of Lemmas DataFrame:")
    print(bol_df)


.. parsed-literal::

    Original Lemmas:
    ['apple' 'aple' 'apples' 'banana' 'banan' 'bananas' 'cherry' 'cheri'
     'cherries']
    An error occurred: integer division or modulo by zero
    
    Bags of Lemmas DataFrame:
       bow_id bow_name   lemma  similarity  threshold
    0       1    apple   apple         100         86
    1       1    apple    aple          89         86
    2       1    apple  apples          91         86
    

In this case, we have an array of lemmas representing fruits, but some
of the lemmas are misspelled or have variations. We want to group
similar lemmas together into bags of lemmas using the ``create_bol``
function.

``get_most_common_strings``
-------------------------------

**Description of the function**

The ``get_most_common_strings`` function is designed to identify and
retrieve the most common strings in a list of texts. It takes two
arguments: a list of texts and an integer specifying the number of most
common words to return. The function calculates word frequencies across
the texts and returns a list of the most frequently occurring words
along with their respective counts.

**When is it useful to use it?**

This function is particularly useful when you want to gain insights into
the content of a collection of texts. It helps you identify which words
or strings are the most prevalent within the text data. You can use this
information for various purposes, including data validation, descriptive
analysis, or identifying significant terms in text data. Let’s explore a
practical use case:

.. code:: ipython3

    # List of example texts
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "A quick brown dog jumps over a lazy fox.",
        "The quick brown dog jumps over the quick lazy fox."
    ]
    
    # Number of most common strings to retrieve
    num_strings = 5
    
    # Apply get_most_common_strings function to find the most common words
    most_common_words = tp.get_most_common_strings(texts = texts, num_strings = num_strings)
    print("Most Common Strings:")
    print(most_common_words)


.. parsed-literal::

    Most Common Strings:
    [('quick', 4), ('brown', 3), ('jumps', 3), ('over', 3), ('lazy', 3)]
    

In this case, we have a list of example texts, and we want to find the
most common words within these texts using the
``get_most_common_strings`` function.

``spacy_pipeline``
----------------------

**Description of the function**

The ``spacy_pipeline`` function is a comprehensive text preprocessing
tool that leverages spaCy’s capabilities to process a list of documents.
It allows you to customize the spaCy pipeline, including options such as
using a custom lemmatizer for Spanish, specifying stopwords language,
choosing a spaCy model, and retrieving the most common words after
preprocessing.

The function takes several arguments, including a list of documents, a
custom lemmatizer flag, pipeline components, stopwords language, spaCy
model, and the number of most common words to return. It processes the
documents by tokenizing, lemmatizing, and removing stopwords, providing
you with well-preprocessed documents and a list of the most common words
within them.

**When is it useful to use it?**

This function is highly useful when you need to preprocess a collection
of text documents for natural language processing tasks. It offers
flexibility by allowing you to configure the spaCy pipeline according to
your specific requirements. Additionally, it provides insights into the
most common words in the preprocessed documents, which can be valuable
for data validation or descriptive analysis. Let’s explore a practical
use case:

.. code:: ipython3

    # List of example documents
    documents = [
        "El rápido zorro marrón salta sobre el perro perezoso.",
        "Un veloz perro marrón salta sobre un zorro perezoso.",
        "El rápido perro marrón salta sobre el veloz zorro perezoso."
    ]
    
    # Specify preprocessing options
    custom_lemmatizer = False
    pipeline = ['tokenize', 'lemmatizer']
    stopwords_language = 'spanish'
    model = 'es_core_news_sm'
    num_strings = 5
    
    # Apply spacy_pipeline function to preprocess documents
    processed_documents, most_common_words = tp.spacy_pipeline(
        documents=documents,
        custom_lemmatizer=custom_lemmatizer,
        pipeline=pipeline,
        stopwords_language=stopwords_language,
        model=model,
        num_strings=num_strings
    )
    
    print("Processed Documents:")
    for i, doc in enumerate(processed_documents):
        print(f"Document {i + 1}: {' '.join(doc)}")
    
    print("\nMost Common Words:")
    print(most_common_words)

``dependency_parse_visualizer_text``
----------------------------------------

**Description of the function**

The ``dependency_parse_visualizer_text`` function is designed to
visualize the dependency parsing or named entity recognition (NER) of a
single text document. It leverages spaCy’s visualization tool, DisplaCy,
to render a graphical representation of linguistic features. The
function is configurable, allowing you to specify the visualization
style, whether you’re working within a Jupyter notebook environment, and
which spaCy model to use for parsing.

**When is it Useful to Use this Function?**

This function is beneficial in multiple scenarios:

1. **Exploratory Data Analysis (EDA):** During the initial stages of
   text analysis, understanding the syntactic structure of your
   documents can be crucial. The visualization helps you to quickly
   grasp the relationships between words in a sentence or identify named
   entities.

2. **Debugging NLP Pipelines:** If you’re building an NLP pipeline that
   includes dependency parsing or named entity recognition, this
   function serves as a helpful debugging tool. You can visually confirm
   whether the spaCy model is interpreting the text as expected.

3. **Educational Purposes:** If you’re learning about dependency parsing
   or named entity recognition, visual representations can significantly
   aid your understanding of these complex linguistic features.

4. **Reporting and Presentation:** You can use this function to generate
   visualizations for reports or presentations, making your findings
   more accessible to those without a technical background in
   linguistics or NLP.

Here a practical dependency example:

.. code:: ipython3

    # Example document in Spanish
    document = "El perro saltó sobre el gato."
    
    # Visualizing the dependency parse
    tp.dependency_parse_visualizer_text(document, style='dep', jupyter=True, model='es_core_news_sm')

Now let’s visualize the named entities instead

.. code:: ipython3

    # Example document in Spanish
    document = "El Banco Mundial decidió contactar al gobierno de Argentina para ofrecerle ayuda. Varios países como Estados Unidos, China y Rusia también ofrecieron su ayuda."
    
    # Visualizing the named entities
    tp.dependency_parse_visualizer_text(document, style='ent', jupyter=True, model='es_core_news_sm')

In this example, we have a list of Spanish documents, and we want to
preprocess them using the ``spacy_pipeline`` function with specific
configuration options.

Tutorial: Topic Modelling
-----------------------------

**Introduction**

In the age of social media, Twitter has become a fertile ground for data
mining, sentiment analysis, and various other natural language
processing (NLP) tasks. However, dealing with Spanish tweets adds
another layer of complexity due to language-specific nuances, slang,
abbreviations, and other colloquial expressions. ‘tidyX’ aims to
streamline the preprocessing pipeline for Spanish tweets, making them
ready for various NLP tasks such as text classification, topic modeling,
sentiment analysis, and more. In this tutorial, we will focus on a
classification task based on Topic Modelling, showing preprocessing,
modeling and results with real data snippets.

**Context**

Using data provided by `Barómetro de
Xenofobia <https://barometrodexenofobia.org/>`, a non-profit organization that 
quantifies the amount of hate speech against migrants on social media, we aim to 
classify the overall conversation related to migrants. This is a **common NLP task** that
involves preprocessing poorly-written social media posts. Subsequently,
these processed posts are fed into an unsupervised Topic Classification
Model (LDA) to identify an optimal number of cluster topics. This helps
reveal the main discussion points concerning Venezuelan migrants in
Colombia.

.. code:: ipython3

    # PREPARATIONS
    # Environment set-up
    import sys
    sys.path.insert(1, r'C:\Users\JOSE\Desktop\Trabajo\Paper_no_supervisado\Tidytweets')
    from tidyX import TextPreprocessor as tt
    import pandas as pd
    import random
    # Getting the data:
    # In this tutorial, we use a sample dataset of 799053 tweets related to Venezuelan migrants in Colombia.
    # The dataset is available in the data folder of the repository.
    # For efficiency we will only use a random sample of 1000 tweets
    n = 799053 #number of records in file
    s = 1000 #desired sample size
    skip = sorted(random.sample(range(n),n-s))
    tweets = pd.read_excel(r"C:\Users\JOSE\Desktop\Trabajo\Paper_no_supervisado\Tidytweets\data\Base_Para_Labels.xlsx", skiprows=skip, header=None, names=['Snippet'])
    tweets.head()

**Preprocessing Tweets**

We will then use ``preprocess`` function to clean the sample and prepare
it for modelling

.. code:: ipython3

    cleaning_process = lambda x: tp.preprocess(x, delete_emojis=True, extract=False)
    tweets['Clean_tweets'] = tweets['Snippet'].apply(cleaning_process)

Here is a random sample of the before and after with specific Tweets

.. code:: ipython3

    sample_tweets = tweets.sample(5, random_state=1)  # You can change the random_state for different samples
    print("Before and After Text Cleaning:")
    print('-' * 40)
    for index, row in sample_tweets.iterrows():
        print(f"Original: {row['Snippet']}")
        print(f"Cleaned: {row['Clean_tweets']}")
        print('-' * 40)

**Tokenize the dataset**

This representation of the dataset will return a list of tokens per
document. ``spacy_pipeline`` function returns a list of lists of
processed lemmatized and stopword absent tweets.

.. code:: ipython3

    tokenized_cleaned_tweets = tp.spacy_pipeline(tweets['Clean_tweets'].to_list(), custom_lemmatizer=True, pipeline=['tokenize', 'lemmatizer'], stopwords_language='spanish', model='es_core_news_sm', num_strings=0)

Here is a random sample of the before and after with specific Tweets

.. code:: ipython3

    tweets['lemmatized_tweets'] = tokenized_cleaned_tweets
    sample_tweets = tweets.sample(5, random_state=1)  # You can change the random_state for different samples
    print("Before and After Text Cleaning:")
    print('-' * 40)
    for index, row in sample_tweets.iterrows():
        print(f"Original: {row['Snippet']}")
        print(f"Cleaned: {row['lemmatized_tweets']}")
        print('-' * 40)

**Seemingly used words and social media bad writting addressing**

May you saw in the previous proccesed tweets that there are seemingly
used or Out-of-Vocabulary (OOV) words that became evident after
processing and cleaning the tweets showed. This words can be a result of
bad spelling, common in social media, abbreviations, or other language
rules.

Here we propose a method to handle this limitations, some research
related to this topic establishes local solutions to this condition, we
invite the user to try this approach and also find some other resources
to proccess the resulted lemmas. Some additional research to handle OOV
words can be found in:

1. `FastText <https://github.com/facebookresearch/fastText>`__
2. `Kaggle NER
   Bi-LSTM <https://www.kaggle.com/code/jatinmittal0001/ner-bi-lstm-dealing-with-oov-words>`__
3. `Contextual Spell
   Check <https://github.com/R1j1t/contextualSpellCheck>`__

We use our ``create_bol`` function to find distances between lemmas, we
are based on the premise that seemingly used lemmas ar far away from the
original corpus and don’t have a big apperance on it. Warning: Expect
long kernel runs, this method evaluates each distance from a lemma N-1
times.

.. code:: ipython3

    import numpy as np
    import itertools
    from collections import Counter
    # We take our list of lists and convert it to a list of strings
    flattened_list = list(itertools.chain.from_iterable(tokenized_cleaned_tweets))
    # Now we count the number of times each lemma appears in the list and sort the list in descending order
    word_count = Counter(flattened_list)
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    sorted_words_only = [word for word, count in sorted_words]
    numpy_array = np.array(sorted_words_only)
    # Now we create our bag of lemmas
    bol_df = tp.create_bol(numpy_array, verbose=True)
    bol_df.head(10)

Now we want to select a specific subset of words that does not include
our probable OOV or NEW words in the text processing. We will replace
words using 85% confidence treshold soo we can infer what was intended
to be written.

.. code:: ipython3

    # Replace each lemma in the original list of lists with its bow_name
    lemma_to_bow = dict(zip(bol_df['lemma'], bol_df['bow_name']))
    replaced_lemmas = [[lemma_to_bow.get(lemma, lemma) for lemma in doc] for doc in tokenized_cleaned_tweets]

Here some random examples with the new mapping, you can inspect the
differences in lemmas:

.. code:: ipython3

    tweets['new_clean_lemmas'] = replaced_lemmas
    sample_tweets = tweets.sample(10, random_state=1)  # You can change the random_state for different samples
    print("Before and After Text Cleaning:")
    print('-' * 40)
    for index, row in sample_tweets.iterrows():
        print(f"Original: {row['Snippet']}")
        print(f"Cleaned: {row['new_clean_lemmas']}")
        print('-' * 40)

From here, you can use this processed tweets to train different models
and make your own empirical applications of NLP using social media data.
However, we will show you a simple application of Topic Modelling using
the data we processed. For more information about this methodology, we
deliver some links to help understanding this type of unsupervised
classification.

Now we can plug this processed documents in a toy model to see some
topics about Venezuelan migrants in Colombia:

This model resolves in some steps: 1. We iterate over the best
combination of hyperparameters alpha, beta, and number of topics. 2. We
filter the results and pick the model with best coherence. We calculate
Coherence Score and Perplexity of each LDA Topic Modeling
implementation. 3. We display a visualization of the topics found in the
toy model.

.. code:: ipython3

    # Now we create our initial variables for Topic Modeling
    import gensim
    from gensim import corpora 
    import tqdm
    from gensim.models import CoherenceModel
    # Create Dictionary
    dictionary = corpora.Dictionary(replaced_lemmas)
    corpus = [dictionary.doc2bow(text) for text in replaced_lemmas]
    # A function that resolves our hyperparameters using a corpus and a dictionary
    def compute_coherence_perplexity_values(corpus, dictionary, k, a, b):
        
        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                               id2word=dictionary,
                                               num_topics=k, 
                                               random_state=100,
                                               chunksize=100,
                                               passes=10,
                                               alpha=a,
                                               eta=b,
                                               workers=7)
        
        coherence_model_lda = CoherenceModel(model=lda_model, texts=replaced_lemmas, dictionary=dictionary, coherence='c_v')
        
        return (coherence_model_lda.get_coherence(),lda_model.log_perplexity(corpus))
    grid = {}
    grid['Validation_Set'] = {}
    # Topics range
    min_topics = 2
    max_topics = 11
    step_size = 1
    topics_range = range(min_topics, max_topics, step_size)
    # Alpha parameter
    alpha = list(np.arange(0.01, 1, 0.3))
    alpha.append('symmetric')
    alpha.append('asymmetric')
    # Beta parameter
    beta = list(np.arange(0.01, 1, 0.3))
    beta.append('symmetric')
    # Validation sets
    num_of_docs = len(corpus)
    corpus_sets = [# gensim.utils.ClippedCorpus(corpus, num_of_docs*0.25), 
                   # gensim.utils.ClippedCorpus(corpus, num_of_docs*0.5), 
                   gensim.utils.ClippedCorpus(corpus, int(num_of_docs*0.75)), 
                   corpus]
    corpus_title = ['75% Corpus', '100% Corpus']
    model_results = {'Validation_Set': [],
                     'Topics': [],
                     'Alpha': [],
                     'Beta': [],
                     'Coherence': [],
                     'Perplexity': []
                    }
    # Can take a long time to run
    if 1 == 1:
        # This is the number of times we want to iterate to find optimal hyperparameters
        pbar = tqdm.tqdm(total=20)
        
        # iterate through validation corpuses
        for i in range(len(corpus_sets)):
            # iterate through number of topics
            for k in topics_range:
                # iterate through alpha values
                for a in alpha:
                    # iterare through beta values
                    for b in beta:
                        # get the coherence score for the given parameters
                        (cv, pp) = compute_coherence_perplexity_values(corpus=corpus_sets[i], dictionary=dictionary, 
                                                      k=k, a=a, b=b)
                        # Save the model results
                        model_results['Validation_Set'].append(corpus_title[i])
                        model_results['Topics'].append(k)
                        model_results['Alpha'].append(a)
                        model_results['Beta'].append(b)
                        model_results['Coherence'].append(cv)
                        model_results['Perplexity'].append(pp)
                        pbar.update(1)
        pd.DataFrame(model_results).to_csv(r"C:\Users\JOSE\Desktop\Trabajo\Paper_no_supervisado\Tidytweets\data\lda_tuning_results.csv", index=False)
        pbar.close()

Now we want to find the optimal model to train, let’s see the results of
our trainning pocess:

.. code:: ipython3

    tabla_tunning = pd.read_csv(r"C:\Users\JOSE\Desktop\Trabajo\Paper_no_supervisado\Tidytweets\data\lda_tuning_results.csv")
    tabla_tunning = tabla_tunning.sort_values(by = 'Coherence', ascending = False)
    tabla_tunning

Let’s train the model! We now pick the best result from the validation
table created on the last step

.. code:: ipython3

    import pprint
    import pyLDAvis
    pyLDAvis.enable_notebook()
    import pyLDAvis.gensim_models
    lda_final_model = gensim.models.LdaMulticore(corpus=corpus,
                                                 id2word=dictionary,
                                                 num_topics=9,
                                                 random_state=100,
                                                 chunksize=100,
                                                 passes=30,
                                                 alpha='asymmetric',
                                                 eta=0.61,
                                                 workers=7)

Now that we have trained an optimized version of our toy model, we want
to visually inspect the derived topics and see if we find some
interesting patterns giving information related to the way people speaks
about Venezuelan migrants in Colombia.

.. code:: ipython3

    [[(dictionary[id], freq) for id, freq in cp] for cp in corpus[:1]]
    
    pprint(lda_final_model.print_topics())
    doc_lda = lda_final_model[corpus]
    
    visxx = pyLDAvis.gensim_models.prepare(topic_model=lda_final_model, corpus=corpus, dictionary=dictionary)
    pyLDAvis.display(visxx)
