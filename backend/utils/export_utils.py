import pandas as pd
import json
import os
import zipfile
import uuid

def export_all_formats(cases, formats):
    export_dir = f"temp_exports/{uuid.uuid4()}"
    os.makedirs(export_dir, exist_ok=True)
    files = []
    df = pd.DataFrame(cases)
    if 'csv' in formats:
        csv_path = os.path.join(export_dir, 'test_cases.csv')
        df.to_csv(csv_path, index=False)
        files.append(csv_path)
    if 'excel' in formats:
        xlsx_path = os.path.join(export_dir, 'test_cases.xlsx')
        df.to_excel(xlsx_path, index=False)
        files.append(xlsx_path)
    if 'json' in formats:
        json_path = os.path.join(export_dir, 'test_cases.json')
        with open(json_path, 'w') as f:
            json.dump(cases, f, indent=2)
        files.append(json_path)
    # Jira Xray JSON
    xray_path = os.path.join(export_dir, 'xray_import.json')
    with open(xray_path, 'w') as f:
        json.dump({"tests": cases}, f, indent=2)
    files.append(xray_path)
    # Zip all
    zip_path = f"{export_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    # Cleanup temp files (keep zip)
    for file in files:
        os.remove(file)
    os.rmdir(export_dir)
    return zip_path
