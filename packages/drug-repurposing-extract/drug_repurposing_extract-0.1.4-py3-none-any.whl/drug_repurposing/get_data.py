import requests
import csv
from padelpy import from_smiles

def generate_data(cids=[]):
    results = []
    fails = []
    for cid in cids:
        try:
            resp = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str(cid) + "/property/MolecularWeight,MolecularFormula,IsomericSMILES,IUPACName/JSON")
            content = resp.json()
            desc_fp = from_smiles(content['PropertyTable']['Properties'][0]['IsomericSMILES'], fingerprints=True)
            desc_fp['cid'] = cid
            results.append(desc_fp)
        except Exception as e:
            print(e)
            # print(content)
            fails.append(cid)
    if(len(fails)>0):
        print("Fails CIDS: ", fails)

    if(len(results)>0):
        csv_file = 'complete_data.csv'
        field_names = results[0].keys()
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for row in results:
                writer.writerow(row)

# generate_data([942])