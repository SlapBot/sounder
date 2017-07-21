# Sounder API

This section is dedicated to the Sounder Library API, which is an abstraction of the [Sounder Algorithm](https://slapbot.github.io/documentation/resources/algorithm), To read the full paper explaining how Sounder works and can be incoporated in the project as well as where it can be used at, kindly refer here: [Sounder Explained](https://slapbot.github.io/documentation/resources/algorithm), [PDF version](https://slapbot.github.io/documentation/resources/algorithm/sounder.pdf)

- [Installation](#installation)
- [Instantiate Class](#instantiate)
- [Search Method](#search)
- [Probability Method](#probability)
- [Filter Method](#filter)
- [Practical Usage](#practical-usage)

<hr>

<a name="installation">

## Installation

Installing Sounder library into your application is easy as pie with `pip` package manager, allowing you to do a simple command from your favorite command line as follows:

	pip install sounder

<hr>

<a name="instantiate">

## Instantiate Class

The first and the foremost thing to do is to import the class like so.

	from sounder import Sounder

And then simply instantiating the class.

	sounder = Sounder([['facebook', 'notifications'], ['twitter', 'notifications']])

You can pass dataset as a positional argument(optional) to the Sounder constructor, or set it later down the line using 
`set_module()` method which returns self.

	sounder.set_dataset([['facebook', 'notifications'], ['twitter', 'notifications']])

As you can already notice, in order to use `search` method, the `dataset` needs to be `2 dimensional list`, containing string elements.

<hr>

<a name="search">

## Search Method

`search(query, dataset=None, metaphone=False)` method takes a positional argument(compulsory), a query which needs to be a list composed of string that needs to be searched through the dataset, like so.

	sounder = Sounder([['facebook', 'notifications'], ['twitter', 'notifications'], ['note', 'something']])
	index = sounder.search(['trackbook', 'notifs'])

`search` method always returns back the index which it found to be most probable to be identical for your given set of data. In this case index will equate to 0.

This method take other optional arguments as follows:

- **dataset :** It's simply the dataset, in case you don't want set dataset while instantiating the class, no problem just pass it as a another argument. Though again it needs to be a double dimensional list.

- **metaphone :** It defaults to False, resonating to the fact that you don't want to use metaphones in addition to the master algorithm. On True state, all the dataset and query is first transformed to metaphones and then inputted to the algorithm increasing efficiency in cases where input data is quite randomized or uses generic terms.

<hr>

<a name="probability">

## Probability Method

`probability(query, dataset=None, metaphone=False, detailed=False, prediction=False)` method takes again a single positional argument which is the query that needs to be compared with the dataset. (A list composed of strings.), like so.

	sounder = Sounder([['facebook', 'notifications'], ['twitter', 'notifications'], ['note', 'something']])
	chances = sounder.probabiltiy(['trackbook', 'notifs'])

`probability` method returns result depending on the optional parameters under given cases:

- **No optional argument passed :** It returns the list the size of the dataset, composed of probability that the query list is most probable to the dataset, resulting from a value between 0.0 to 1.0 where 0.0 refers to nothing matches, and 1.0 to everything matches.

- **detailed :** If detailed argument is set to True, then it returns back the size of the dataset in a nested list format, where the first element is the probability that the query list is most probable to the dataset, while the second element is an another list the size of the ith data of dataset, consisting the probabiltiy that jth word of the ith data was found on the query by solving assignment problem, resulting from a value between 0.0 to 1.0 where 0.0 refers to nothing matches.

- **prediction :** If set to True, it returns back a dict, with keys `chances` and `index` suggesting which index of the dataset is most probable to the the given query in terms of similarity while chances denoting to a value between 0.0 to 1.0 where 0.0 refers to nothing matches.

Two other arguments that can be set are :

- **dataset :** Again, in case you didn't set the dataset on the instantiation, fear not, just pass it as an argument. One more thing, this time it doesn't necessarily needs to be a double dimensional list if you're just comparing two lists of string elements. like so.
	
		information = sounder.probability(['trackbook'], dataset=['facebook'])

Sounder basically internally map it into double dimensional list automatically, giving you the leverage to compare any two lists of words.

- **metaphones :** Again, it's exactly the same as for search method.

<hr>

<a name="filter">

## Filter Method

`filter(query, reserved_sub_words=None)` is basically a utility provided you to filter the stop words out of your string, for instance, `"Hey Stephanie, what is the time right now?"` would filter away `['hey', 'what', 'is', 'the']` since they don't hold higher meaning, leaving behind key_words like `['stephanie', 'time', 'right', 'now']`

This method is just a utility to help you do the entire intent recognization from single library, but you're free to use any kind of system. It returns back a dictionary with keys such as `sub_words` and `key_words`, resonating to stop words found in the string and keywords found in it in a list form respectively.

- **reserved_sub_words :** is the filter that is used to filter out the stop words, you can pass your own filter in the method itself or through using `set_filter(reserved_sub_words)` method which returns the self instance. **Note :** make sure the filter is a dictionary of all the words that you consider as stop words. Default is as follows:

		{
	        "what", "where", "which", "how", "when", "who",
	        "is", "are", "makes", "made", "make", "did", "do",
	        "to", "the", "of", "from", "against", "and", "or",
	        "you", "me", "we", "us", "your", "my", "mine", 'yours',
	        "could", "would", "may", "might", "let", "possibly",
	        'tell', "give", "told", "gave", "know", "knew",
	        'a', 'am', 'an', 'i', 'like', 'has', 'have', 'need',
	        'will', 'be', "this", 'that', "for"
		}

<hr>

<a name="practical-usage">

## Practical Usage

This algorithm is the brain of [Stephanie](https://slapbot.github.io), an open-source platform built specifically for voice-controlled application as well as to automate daily tasks imitating much of an virtual assistant's work.
