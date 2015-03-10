#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Identity v3 Service Catalog action implementations"""

import logging

from cliff import lister

from openstackclient.common import utils


def _format_endpoints(eps=None):
    if not eps:
        return ""
    ret = ''
    for ep in eps:
        region = ep.get('region_id') or ep.get('region', '<none>')
        ret += region + '\n'
        ret += "  %s: %s\n" % (ep['interface'], ep['url'])
    return ret


class ListCatalog(lister.Lister):
    """List services in the service catalog"""

    log = logging.getLogger(__name__ + '.ListCatalog')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        # This is ugly because if auth hasn't happened yet we need
        # to trigger it here.
        sc = self.app.client_manager.session.auth.get_auth_ref(
            self.app.client_manager.session,
        ).service_catalog

        data = sc.get_data()
        columns = ('Name', 'Type', 'Endpoints')
        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={
                        'Endpoints': _format_endpoints,
                    },
                ) for s in data))
