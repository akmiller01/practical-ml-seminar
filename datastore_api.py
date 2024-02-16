import os
from dotenv import load_dotenv
import json
import requests
import pandas as pd
import progressbar

load_dotenv()
API_KEY = os.getenv('API_KEY')

def main(org_ref):
    # Use the IATI Datastore API to fetch all titles for a given publisher
    rows = 1000
    next_cursor_mark = '*'
    current_cursor_mark = ''
    results = []
    with progressbar.ProgressBar(max_value=1) as bar:
        while next_cursor_mark != current_cursor_mark:
            url = (
                'https://api.iatistandard.org/datastore/activity/select'
                '?q=(reporting_org_ref:"{}")'
                '&sort=id asc'
                '&wt=json&fl=iati_identifier,title_narrative,tag_narrative&rows={}&cursorMark={}'
            ).format(org_ref, rows, next_cursor_mark)
            api_json_str = requests.get(url, headers={'Ocp-Apim-Subscription-Key': API_KEY}).content
            api_content = json.loads(api_json_str)
            if bar.max_value == 1:
                bar.max_value = api_content['response']['numFound']
            activities = api_content['response']['docs']
            len_results = len(activities)
            current_cursor_mark = next_cursor_mark
            next_cursor_mark = api_content['nextCursorMark']
            for activity in activities:
                results_dict = {}
                results_dict['iati_identifier'] = activity['iati_identifier']
                results_dict['text'] = activity['title_narrative'][0]
                if 'tag_narrative' in activity.keys():
                    climate = 'International Climate Finance' in activity['tag_narrative']
                else:
                    climate = False
                if climate:
                    results_dict['label'] = "Related to climate"
                else:
                    results_dict['label'] = "Not related to climate"
                results.append(results_dict)
            if bar.value + len_results <= bar.max_value:
                bar.update(bar.value + len_results)
    
    # Collate into Pandas dataframe
    df = pd.DataFrame.from_records(results)

    # Drop any possible duplicate records
    df = df.drop_duplicates()

    # Balance dataset
    print("Balancing dataset...")
    print("Rows prior to balancing: {}.".format(df.shape[0]))
    climate_related = df.loc[df.label == "Related to climate"]
    not_climate_related = df.loc[df.label == "Not related to climate"]
    climate_row_count = climate_related.shape[0]
    not_climate_related = not_climate_related.sample(n=climate_row_count, random_state=1337)
    df = pd.concat([not_climate_related, climate_related])
    print("Rows after balancing: {}.".format(df.shape[0]))

    # Write to disk
    df.to_csv(
        os.path.join('data', '{}.csv'.format(org_ref)),
        index=False,
    )



if __name__ == '__main__':
    main('GB-GOV-1')