import os
import json
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(os.path.abspath('templates')))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, 'static')

class TransactionForm(BoxLayout):
    kid_spinner = ObjectProperty(None)
    description = ObjectProperty(None)
    amount = ObjectProperty(None)

    def submit(self):
        kid_id = self.kid_spinner.selected_value
        description = self.description.text
        amount = self.amount.text
        data = {'kid_id': kid_id, 'description': description, 'amount': amount}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        UrlRequest('http://localhost:8080/add_transaction',
                   req_body=json.dumps(data),
                   req_headers=headers,
                   on_success=self.transaction_added,
                   on_error=self.transaction_error)

    def transaction_added(self, request, result):
        self.kid_spinner.text = ''
        self.description.text = ''
        self.amount.text = ''

    def transaction_error(self, request, error):
        print('Error:', error)


class KidTrackerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        form = TransactionForm()
        layout.add_widget(form)
        return layout

if __name__ == '__main__':
    KidTrackerApp().run()
