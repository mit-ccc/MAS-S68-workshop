
# MAS.S68 Python workshop 1

([Zoom Recording](https://us02web.zoom.us/rec/play/BKzMuph7VR1jHHa3XuC8opeLiS1vmO7DhiFcgEXBGYBwf7AHIxVU2CWPiQqqQWm51Fi3GY2XprjCF3Fw.KABKHlCX3W8gfCQo?continueMode=true&_x_zm_rtaid=HHGod3FxRc6tbq58z9razA.1676939169419.ac4f84a2caac62e0f284604eccefc662&_x_zm_rhtaid=369))



**Note**:  This workshop assumes that you have a basic understanding of Python, and have written and run Python programs on your computer before.   If you're brand new to Python, please see [Python for Beginners](https://www.python.org/about/gettingstarted/) first.

## 1.  Some preliminaries

  - Be sure you have your Python environment and editor ready
  - Be sure you have already signed up for the [OpenAI API](https://openai.com/api/)
  - Open a Terminal window on your laptop
  - Install the openai Python library and streamlit (``pip install openai streamlit``)
  - (Optional for today)  [Install git](https://github.com/git-guides/install-git) and [clone our repo](https://github.com/mit-ccc/MAS-S68-workshop)
  - (Optional for today)   Run from within a virtual environment   (see [here](https://towardsdatascience.com/virtual-environments-104c62d48c54#:~:text=A%20virtual%20environment%20is%20a,a%20system%2Dwide%20Python))
  - Find your API key
    - Get it from [here](https://platform.openai.com/account/api-keys)
    - For convenience, set the OPENAI_API_KEY environment variable (see [OpenAI's tips](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety))
    - Don't ever check it into a git repository or put it in user-visible code (e.g., Javascript)

## 2.  Running basic completion queries

  Our goal today:  Let's make an application that lets you describe an English word and then guesses the word that you mean!
  Such a tool could be used as a writing aid or by people who want to expand their vocabulary.  This is called the "reverse dictionary" problem.
  (Here are [100 examples of this task](https://github.com/mit-ccc/MAS-S68-workshop/blob/main/data/train.jsonl) from a research data set.)
  
  - First, go to the [OpenAI Playground page](https://platform.openai.com/playground)
  - How well does GPT-3 work for this with a straightforward "zero-shot" prompt?    Type ``What are some words that mean "clothing that you wear on your head?"`` into the input box and hit Submit.
  - You can see the corresponding API code for the query, in Python, by pressing the "View code" button above the playground
  - Copy this code and run it in a [Google Colab](https://colab.research.google.com/) session.   (Add ``print(response)`` to see the output)
    - Note that you will need to specify your API key in the cell;  below ``import openai``, put ``openai.api_key = "<your_key>``
  - Now let's run the query in a standalone python script on your computer
    - Copy the code you have in Colab to a new python file, say ``reverse_dictionary.py``
    - Run ``python3 ./reverse_dictionary.py`` from the command line

## 3.  Understanding the input parameters ([doc](https://platform.openai.com/docs/api-reference/completions/create))
  - ``n``:   Number of completions to generate.  (Not useful to override if temperature is zero -- you'll just get repeats)
  - ``stop``:   A list of sequences of characters that indicate generation should stop.
    If it's omitted, generation will occur until max_tokens is reached.  ("\n\n" is a good-enough choice for many tasks in which the output is a list or a paragraph.)
  - ``max_tokens``  Max tokens to generate;  note these do not correspond 1-1 with words.  See below. 
  - ``logprobs``  Set to 1 to see the log probability (aka logprob) assigned to the most likely token, which can be useful for gauging the level of surprise at a given point of the text.
     Set to > 1, to see the next-most-likely alternatives (conditioned on the prompt and the already-generated to the left.)
     Pair with ``echo`` parameter if you want to see logprobs for your prompt as well.
  - ``temperature``   Informally, this is the "level of randomness".  0 is (intended to be) deterministic  ([blog post](https://algowriting.medium.com/gpt-3-temperature-setting-101-41200ff0d0be))
  - frequency_penalty, presence_penalty

## 4.  Understanding the output
  - choices array:  (will contain ``n`` elements)
     - choices[].text:  The completion text iself.
     - choices[].finish_reason:   ``stop`` or ``length`` depending on whether it hit a stop sequence or not.
     - choices[].logprobs:   If logprobs is set, this will be an object containing several arrays, each with length equal to the number of tokens generated (and also in the prompt, if "echo" was set).  The arrays are:
         - ``token_logprobs``:  The log probabilities for the generated tokens ("token_logprobs")
	 - ``top_logprobs``:  The log probabilities for the top-logprobs predicted tokens.     (Discussion question:  In what situation might the tokens in "top_logprobs" **not** contain the generated token, from "token_logprobs") 
	 - ``token``:  The selected tokens
	 - ``text_offset``:  Tells you how the tokens map into the words in the text
  - usage:  Summarizes how many tokens you used in this query.  (See below).
  - Parsing the response for what you care about


## 5.  Models
  - [Understand which models are available](https://platform.openai.com/docs/models/gpt-3)
  - Try your query in different models by changing the "model" parameter.

## 6.  Iterating on your prompt
  - Back in the Playground, try a few variations of zero-shot prompts.  Notice any differences in the results?
  - Is the output format consistent across different inputs for the same zero-shot prompting template?
  - Zero-shot vs. few-shot.  Try adding some examples to the prompt.  How to pick these?
  - Prompt guidlines.   [Basic tips from OpenAI](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)


## 7.  Operational considerations
  - Limits:
    - Token limits
      - 4096 for davinci, 2048 for curie
      - On average ~1.3 tokens per English word.
      - The limit includes both prompt and completion
      - Actual number used is reported in API response.
      - [How to count tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
      - Advanced:  count them exactly in python with the [transformers GPT2 tokenizer](https://huggingface.co/docs/transformers/model_doc/gpt2#transformers.GPT2TokenizerFast)
      - Consider "graceful truncation" strategies if your task needs long prompts
    - [Rate limit](https://platform.openai.com/docs/guides/rate-limits)
      - Only 20 queries per minute in free tier, 3000 after 48 hours of adding payment method.
    - Monthly quota
      - $18 credit when you sign up, $120 default quota when you add a payment method
      - [How to increase](https://help.openai.com/en/articles/6643435-how-do-i-get-more-tokens-or-increase-my-monthly-usage-limits)
  - [OpenAI Status page](https://status.openai.com/) Subscribe to this to stay abreast of operational problems with the API.  (These have been more frequent lately, especially for davinci models.)
  - Tracking costs:  Be aware of the [pricing](https://openai.com/api/pricing/) page and the [usage](https://platform.openai.com/account/usage) page.
  - Error codes:  The most common Python exceptions you'll hit are RateLimitError (you've gone over the rate limit) and APIError or ServiceUnavailableError
    (due to problems on OpenAI's end).   In the latter case, check the [status page](https://status.openai.com/).   ([More info](https://platform.openai.com/docs/guides/error-codes/python-library-error-types))
  - Adding retry logic to the Python API call to guard against these problems.

## 8.   Make the script into an interactive dashboard
  - Intro to streamlit:   https://streamlit.io/
  - Let's turn our command-line script into a simple Streamlit dashboard.
    - Import streamlitm, and add a streamlit_app() method that lays out:
      - A text input box to capture the user's query (See [st.text_input](https://docs.streamlit.io/library/api-reference/widgets/st.text_input))
      - A select box to control the number of alternatives generated (See [st.selectbox](https://docs.streamlit.io/library/api-reference/widgets/st.selectbox))
      - A form wrapping these two elements with a submit button (See [st.form](https://docs.streamlit.io/library/api-reference/control-flow/st.form)) 
    - Start your dashboard from the command line with ``streamlit run reverse_dictionary.py``.  It will open a browser window.
  - Use caching (@st.cache_data decorations) to save API queries ([Streamlit caching](https://docs.streamlit.io/library/advanced-features/caching))

## 9. Evaluating our system
  - First let's make training / validation sets for our task.
  - As we are not (yet) doing fine-tuning of the model, the train set is solely for identifying prompt examples.
  - There are a few data sets of (description, word) pairs out there already,  and we'll use one from a research paper by Hill et al originally published back in 2016 (https://arxiv.org/abs/1504.00548).
  - Note that having just a train/validation split is just a shortcut for today's exercise.   For better
    machine learning hygiene, we'd have a test set as well, and never look at it
    -- see https://towardsdatascience.com/train-validation-and-test-sets-72cb40cba9e7 -- and then evaluate our best configuration on it.
    That's because if we've tried a variety of configurations (number of prompt examples, model type, instruction wording), the one with the
    best performance on the validation set may not be the one with the best performance on new data.
  - Next we update the code to run in batches.  Here it may be important to pay attention to your rate limit.
  - Evaluation metrics:   For our task, we can compute raw accuracy by counting the rate at which GPT-3's best guess is equal to the labeled guess.  (Discussion:  What shortcomings
    does this have as an evaluation metric?)
  - Keep a notebook  ([example](https://github.com/mit-ccc/MAS-S68-workshop/blob/main/experiments.md))

## 10.  Useful resources
  - Other tutorials that are good:
    - OpenAI's official quickstart:  https://platform.openai.com/docs/quickstart
    - For journalists:  https://colab.research.google.com/drive/1rr0dxKpwK5zjch1V4eKjwwyVW-AzuDTw?utm_source=puntofisso&utm_medium=email
  - Prompt engineering stuff
    - [Prompt Engineering Guide from DAIR](https://github.com/dair-ai/Prompt-Engineering-Guide)
    - Prompt generation libraries -- https://github.com/microsoft/prompt-engine
    - [GPT-3 Parameters and Prompt Design](https://towardsdatascience.com/gpt-3-parameters-and-prompt-design-1a595dc5b405)

