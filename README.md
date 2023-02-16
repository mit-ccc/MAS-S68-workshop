
# MAS.S68 Python workshop 1

1.  Some preliminaries

- Be sure you have your python environment and editor ready
- Open a Terminal window on your laptop
- Install openai Python library  (``pip install openai``)
- (Optional for today)  Install git and download our repo  [Install](https://github.com/git-guides/install-git)
- (Optional for today)   Run from a virtual environment   ([Link](https://towardsdatascience.com/virtual-environments-104c62d48c54#:~:text=A%20virtual%20environment%20is%20a,a%20system%2Dwide%20Python))
- Understand your API key
  - For convenience, set the OPENAI_API_KEY environment variable (see [OpenAI's tips](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety))
  - Don't ever check it into a git repository or put it in user-visible code (e.g., Javascript)

2.  Running basic completion queries

- First, go to the [OpenAI Playground page](https://platform.openai.com/playground)
- Type *What are some words that mean "clothing that you wear on your head"** into the input box and hit Submit.
- Translate the query to Python (press the "View code" button above the playground)
- Run the query in [Google Colab](https://colab.research.google.com/).   (Add ``print(response)``
- Run the query in a standalone python script on your computer
  - Copy the code you have in Colab to a new python file, say ``reverse_dictionary.py``
  - Run ``python3 ./reverse_dictionary.py`` from the command line

3.  Understanding the output
- choices array
- finish_reason
- parsing the response for what you care about

4.  Understanding the input parameters
- Stop sequence.   \n\n
- Max words
- Temperature
- Getting logprobs
- Topn

5.  Models
- [Understand which models are available](https://platform.openai.com/docs/models/gpt-3)
- Try your query in different models by changing the "model" parameter.

6.  Iterating on your idea
- Back in the playground, try a few variations of zero-shot prompts.  Notice any differences in the results?
- Is the output format consistent across different inputs for the same zero-shot prompting template?
- Zero-shot vs. few-shot.  Try adding some examples to the prompt.  How to pick these?
- Prompt guidlines.   [Basic tips from OpenAI](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)


7.  Operational considerations
- Limits:
  - Token limits
     - 4096 for davinci, 2048 for curie
     - Includes both prompt and completion
     - [How to count tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
  - [Rate limit](https://platform.openai.com/docs/guides/rate-limits)
  - Quota    ([How to increase](https://help.openai.com/en/articles/6643435-how-do-i-get-more-tokens-or-increase-my-monthly-usage-limits))
- [OpenAI Status page](https://status.openai.com/) Subscribe to this to stay abreast of operational problems with the API.  (These have been more frequent lately, especially for davinci models.)
- Tracking costs:  Be aware of the [pricing](https://openai.com/api/pricing/) page and the [usage](https://platform.openai.com/account/usage) page.
- Adding retry logic

8.   Make it interactive
- Intro to streamlit   https://streamlit.io/
- Turning this into a simple streamlit dashboard
- Add a text input box
- Add a select box
- Using caching to save queries

9. Toward evaluation
- Make a training / test set
- Updating the code to run in batches
- For better hygiene, do a train/validation/test split.  https://towardsdatascience.com/train-validation-and-test-sets-72cb40cba9e7
- Evaluation metrics
- Keep a notebook!

10.  Useful resources
- Other tutorials that are good:
   - OpenAI's official quickstart:  https://platform.openai.com/docs/quickstart
   - For journalists:  https://colab.research.google.com/drive/1rr0dxKpwK5zjch1V4eKjwwyVW-AzuDTw?utm_source=puntofisso&utm_medium=email
   - Prompt generation libraries -- https://github.com/microsoft/prompt-engine
   - [GPT-3 Parameters and Prompt Design](https://towardsdatascience.com/gpt-3-parameters-and-prompt-design-1a595dc5b405)

