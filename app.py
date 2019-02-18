from flask import Flask, render_template, abort

# init app and configs
app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False

# routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/shows', methods=['GET'])
def show_listing():
    return render_template('show_listing.html')


@app.route('/shows/<id>', methods=['GET'])
def show(id):
    id = id
    return render_template('show')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


# error handlers
@app.errorhandler(404)
def not_found(error):
    error = 'Page Not Found'
    return render_template('error.html', error=error)


@app.errorhandler(500)
def server_error(error):
    error = 'Server Error'
    return render_template('error.html', error=error)

# start app
if __name__ == '__main__':
    app.run()