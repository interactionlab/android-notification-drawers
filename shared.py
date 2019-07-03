import pandas as pd

# Category mapping

PATH_PACKAGE_CATEGORY_MAPPING = '/path/to/package_category_mapping.pkl.gz'
category_mapping = pd.read_pickle(PATH_PACKAGE_CATEGORY_MAPPING, compression='gzip')
category_mapping = pd.Series(category_mapping.Category.values, index=category_mapping.PackageName).to_dict()

# Filter active

def filter_active(active):
    has_summary = {}
    package_group_count = {}

    for n in active:
        pn = n['packageName']
        gk = n['groupKeyCompat'] if 'groupKeyCompat' in n else ''
        key = pn + gk

        if key not in has_summary:
            has_summary[key] = False
            package_group_count[key] = 0

        if n['isGroupSummaryCompat']:
            has_summary[key] = True

        package_group_count[key] = package_group_count[key] + 1

    result = []

    for n in active:
        pn = n['packageName']
        gk = n['groupKeyCompat'] if 'groupKeyCompat' in n else ''
        key = pn + gk
        is_summary = n['isGroupSummaryCompat']

        if (package_group_count[key] == 1) or (has_summary[key] and is_summary) or (not has_summary[key]):
            result.append(n)
    return result