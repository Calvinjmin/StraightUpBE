from chalice import Chalice

app = Chalice(app_name='straightUpBE')


@app.route('/')
def index():
    return {'hello': 'world'}

