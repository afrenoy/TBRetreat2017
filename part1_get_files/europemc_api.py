import request as reqs
from matplotlib import pyplot as plt
# Minimal example for getting json data, filtering and displaying it.

api_url = u'https://www.ebi.ac.uk/europepmc/webservices/rest/search'

# specify here the search parameters
search_p = {
    'query': 'AUTH:"Bonhoeffer S"',
    'format': 'json',
    'pageSize': 1000
}

response = reqs.get(api_url, params=search_p)
# check if the response was ok (200)
print response.status_code

as_json = response.json()

# check what is in the json
print as_json.keys()

tb_pub_list = as_json['resultList']['result']

pub_per_year = {}

for a_pub in tb_pub_list:
    try:
        pub_per_year[a_pub[u'pubYear']] += 1
    except KeyError:
        pub_per_year[a_pub[u'pubYear']] = 1

year_count = [(int(k), v) for k, v in pub_per_year.itesm()]
# we need to make sure the ordering is correct
year_count.sort(key=lambda x: x[0])

# plot the data
plt.plot(*zip(*year_count))
