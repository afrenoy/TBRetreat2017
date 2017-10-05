# only with standard libraries
import urllib2 as u2

si_file_url = u'https://doi.org/10.1371/journal.pcbi.1005704.s{0:03d}'
si_file_name = u'SI_{0:03}.pdf'


if __name__ == '__main__':
    resp = u2.urlopen(si_file_url.format(1))
    with open(si_file_name.format(1), 'wb') as f:
        f.write(resp.read())


# ----
# using the requests package
import requests as reqs


def get_SI(nbr):
    resp = reqs.get(si_file_url.format(nbr))
    with open(si_file_name.format(nbr), 'wb') as f:
        f.write(resp.content)


if __name__ == '__main__':
    map(lambda x: get_SI(x), range(1, 8))
