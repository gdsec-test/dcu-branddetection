import json
import logging
import threading
from datetime import datetime, timedelta
from urllib import request

from netaddr.ip import all_matching_cidrs


class ASNPrefixes(object):

    _url_base = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS'

    def __init__(self, asns=list(), update_hrs=24):
        self._logger = logging.getLogger(__name__)
        self._asns = asns
        self._update_hrs = update_hrs
        self._last_query = datetime(1970, 1, 1)
        self._update_lock = threading.RLock()
        self._prefixes = []
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
                    self._ripe_get_prefixes_per_asn()
                    self._logger.info("Updating prefix list for ASN's: {}".format(self._asns))
                return all_matching_cidrs(ipaddr, self._prefixes)
            except Exception as e:
                self._logger.error('Exception in _update_lock(): {}'.format(e))
                return []

    def _ripe_get_prefixes_per_asn(self):
        """
        Uses RIPE's API (https://stat.ripe.net/data/announced-prefixes/data.?)
        to list the prefixes associated to a given Autonomous System Number (ASN)
        e.g., e.g. https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS3333&starttime=2011-12-12T12:00
        This API is documented on https://stat.ripe.net/docs/data_api
        """
        with self._update_lock:
            pref_list = []
            query_time = datetime.utcnow()

            for asn in self._asns:
                js_data = self._query_ripe(asn, query_time)

                if js_data:
                    for record in js_data['data']['prefixes']:
                        pref_list.append(record['prefix'])
                if len(pref_list) == 0:
                    self._logger.error("Failed to fetch any prefixes for ASN: {}".format(asn))

            self._last_query = query_time
            if pref_list:
                self._prefixes = pref_list

    def _query_ripe(self, asn, query_time):
        """
        Given an asn and query_time perform a RIPE database lookup and fetch any data associated with this asn
        :param asn:
        :param query_time:
        :return:
        """
        try:
            rep = request.urlopen(self._url_base + str(asn) + '&starttime=' + query_time.isoformat().split('.')[0])
            data = str(rep.read().decode(encoding='UTF-8'))
            rep.close()
            return json.loads(data)
        except Exception as e:
            self._logger.error("Unable to update the prefix list. Last update at {} : {}".format(self._last_query, e))
