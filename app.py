from flask import Flask, render_template, abort
from utils.show_utils import get_shows, get_show_from_slug
from utils.stream_utils import get_live_info

# init app and configs
app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False
shows = get_shows()

# routes
@app.route('/', methods=['GET'])
def index():
    if get_live_info():
        live_info = get_live_info()
        return render_template('live.html', live_info=live_info)

    return render_template('index.html')


@app.route('/shows', methods=['GET'])
def show_listing():
    return render_template('show_listing.html')


@app.route('/shows/<slug>', methods=['GET'])
def show(slug):
    show = get_show_from_slug(slug)
    if show:
        return render_template('show.html', show=show.to_dict())
    else:
        abort(404)


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
