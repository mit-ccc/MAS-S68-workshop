#!/usr/bin/env python3

"""
Generates a CSV file called congress_gpt3.csv that contains
contains real facts about all currently-serving US senators
and representatives, plus GPT3-synthesized answers to some configurable
policy questions.  (Note that, as the policy answers may not be accurate,
the generated CSV file should used for demo purposes only, not as primary
source material!)

To use this, first download the legislator data at: 
  https://github.com/unitedstates/congress-legislators/blob/main/legislators-current.yaml

Then copy it into this directory, and run this script to produce the demo CSV.
Change the _QUESTIONS below if you want to add more synthesized questions.
"""
import csv
from datetime import datetime
import json
import openai
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

_QUESTIONS = [
    {
        "csv_column": "What are your policy positions",
        "prompt": "How would [Name], [Office] from [State], describe their policy positions?",
    },
    {
        "csv_column": "What are your positions on education",
        "prompt": "How would [Name], [Office] from [State], describe their positions on education in one or two sentences?",
    },
]

_OFFICES = {"rep": "representative", "sen": "senator"}

_STATES = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming",
    "VI": "Virgin Islands",
    "MP": "MP",
    "AS": "American Samoa",
    "PR": "Puerto Rico",
    "GU": "Guam",
}


def run_completion_query(prompt, model="text-davinci-003", num_to_generate=1):
    tries = 0
    while tries < 3:
        try:
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=0.0,
                n=num_to_generate,
                stop=["\n\n"],
                max_tokens=300,
            )
            return response
        except (openai.error.RateLimitError, openai.error.APIError) as e:
            st.write(e)
            tries += 1
            time.sleep(10)


if __name__ == "__main__":
    data = load(open("legislators-current.yaml").read(), Loader=Loader)
    csv_output = []
    for x in data:
        name = x["name"]["official_full"]
        gender = x["bio"]["gender"]
        birthday = x["bio"]["birthday"]
        latest_term = x["terms"][-1]
        office = latest_term["type"]
        state = latest_term["state"]
        party = latest_term["party"]

        # Discretize age to decade
        d1 = datetime.strptime(birthday, "%Y-%m-%d")
        d2 = datetime.now()
        age = d2.year - d1.year - ((d2.month, d2.day) < (d1.month, d1.day))
        age = str("%d0s" % (age / 10))

        csv_output.append(
            {
                "Name": name,
                "Office": _OFFICES[office],
                "State": _STATES[state],
                "Party": party,
                "Gender": gender,
                "Age": age,
            }
        )

    # Get GPT-3 answers and output rows
    fieldnames = list(csv_output[0].keys()) + [x["csv_column"] for x in _QUESTIONS]
    csv_out = csv.DictWriter(open("congress_gpt3.csv", "w"), fieldnames)
    csv_out.writeheader()

    for x in csv_output:
        for q in _QUESTIONS:
            prompt = q["prompt"]
            for var in ["Name", "Office", "State"]:
                prompt = prompt.replace("[" + var + "]", x[var])
            print(prompt)
            gpt3_result = run_completion_query(prompt + "\n")
            print(gpt3_result)
            answer = gpt3_result["choices"][0]["text"]
            x[q["csv_column"]] = answer
        csv_out.writerow(x)
