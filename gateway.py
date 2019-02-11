import requests
import logging
import re
import js2py

class CiscoRouterGateway(object):

    ENDPOINT_LOGIN = "/login.cgi"
    ENDPOINT_APPLY = "/apply.cgi"

    def __init__(self, address='http://192.168.1.1', username='', password=''):
        self._address = address
        self._username = username
        self._password = password
        self._session = requests.Session()

    @property
    def _encrypted_password(self):
        '''
            Cisco does logic in javascript to encrypt your router password
            before authenticating. This js function contains a nonce that changes
            from request to request (probably done server side). This function
            downloads the javascript, modifies it to add an invocation with the
            router password, and executes.
        '''
        gateway = self._session.get(self._address)
        html_and_js = "".join(gateway.content.splitlines())
        encryption_function_js_str = re.findall('md5 for more info. \*\/(.*)function chk_keypress', html_and_js)[0]

        # Add line to call the function that encrypts the password
        encryption_function_with_invocation_js = encryption_function_js_str + ' en_value(en_value("' + self._password + '")+nonce);'
        
        # Invoke
        encrypted_password = js2py.eval_js(encryption_function_with_invocation_js)

        return encrypted_password

    @property
    def session_id(self):
        '''
            SessionId is used to authenticate each call/ page-transition in the
            router gateway site. Login using the encrypted password and then find
            the session_id in the result.
        '''        
        login = self._session.post(self._address + self.ENDPOINT_LOGIN, data={
            'submit_button': 'login',
            'change_action': '',
            'action': 'Apply',
            'wait_time': 19,
            'submit_type': '',
            'http_username': self._username,
            'http_passwd': self._encrypted_password
        })

        # SessionId is in the login response content
        session_id = re.findall('session_id=(.*)\";', str(login.content))[0]
        return session_id

    def execute_basic_settings_change(self, channel):
        main_result = self._session.post(self._address + self.ENDPOINT_APPLY + ';session_id=' + self.session_id, data={
            'submit_button': 'Wireless_Basic',
            'gui_action': 'Apply',
            'submit_type': '',
            'change_action': '',
            'next_page': '',
            'wl_nctrlsb': 'none',
            'wl_channel': channel,
            'wl_nbw': 20,
            'commit': 1,
            'wps_security_mode': '',
            'wait_time': 3,
            'change_status': 0,
            'wl_ap_ip': 4,
            'wl_wds': 4,
            'nvset_cgi': 'wireless',
            'guest_ssid': 'Cisco19003-guest',
            'wps_smode': 0,
            'wl_net_mode': 'mixed',
            'wl_ssid': 'Mark\'s Wifi',
            '_wl_nbw': 20,
            'wl_schannel': channel,
            'wl_closed': 0
        })

    def set_channel(self, channel):
        # must be between 1-11
        if 1 <= channel <= 11:
            self.execute_basic_settings_change(channel)
        else:
            print("Failed to execute - valid channels must be between 1 and 11. Channel:" + channel)




