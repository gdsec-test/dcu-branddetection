import logging
import threading
import json

from urllib import urlopen
from datetime import datetime, timedelta
from netaddr.ip import all_matching_cidrs


class ASNPrefixes(object):

    def __init__(self, asn=26496, update_hrs=24):
        self._logger = logging.getLogger(__name__)
        self._asn = asn
        self._last_query = datetime(1970, 1, 1)
        self._url_base = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS'
        self._update_hrs = update_hrs
        self._prefixes = []
        self._update_lock = threading.RLock()
        threading.Thread(target=self._ripe_get_prefixes_per_asn).start()

    def get_network_for_ip(self, ipaddr):
        """
        Returns a list of networks that ipaddr exists in based on
        the announced prefixes for the given ASN
        NOTE: Based on update_hrs, this call may block while an up
        to date list is being retrieved
        """
        with self._update_lock:
            try:
                if self._last_query < datetime.utcnow() - timedelta(hours=self._update_hrs):
                    self._logger.info("Updating prefix list for ASN{}".format(self._asn))
                    self._ripe_get_prefixes_per_asn()
                return all_matching_cidrs(ipaddr, self._prefixes)
            except Exception as e:
                self._logger.error('Exception in _update_lock(): {}'.format(e.message))
                return []

    def _ripe_get_prefixes_per_asn(self):
        """
        Uses RIPE's API (https://stat.ripe.net/data/announced-prefixes/data.?)
        to list the prefixes associated to a given Autonomous System Number (ASN)
        e.g., e.g. https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS3333&starttime=2011-12-12T12:00
        This API is documented on https://stat.ripe.net/docs/data_api
        """
        with self._update_lock:
            try:
                query_time = datetime.utcnow()
                rep = urlopen(self._url_base + str(self._asn) + '&starttime=' + query_time.isoformat().split('.')[0])
                data = str(rep.read().decode(encoding='UTF-8'))
                rep.close()
                js_data = json.loads(data)
                pref_list = []

                for record in js_data['data']['prefixes']:
                    pref_list.append(record['prefix'])
                # If prefix list is empty, don't overwrite _prefixes nor update _last_query time
                if len(pref_list) == 0:
                    raise ValueError('Currently obtained Prefix List is empty.')
                self._prefixes = pref_list
                self._last_query = query_time
            except Exception as e:
                self._logger.error("Unable to update the prefix list. Last update at {}:{}".format(self._last_query, e))

