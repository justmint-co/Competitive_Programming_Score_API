from flask import Flask, render_template
from flask_restful import Api, Resource
from flask_cors import CORS
import json
from version import version

from details_soup import (
    UserData,
    UserDataVerify,
    UsernameError,
    PlatformError,
    BrokenChangesError,
)

app = Flask(__name__)
CORS(app)
api = Api(app)


class Details(Resource):
    def get(self, platform, username):

        user_data = UserData(username)

        try:
            return user_data.get_details(platform)

        except UsernameError:
            return {"status": "Failed", "details": "Invalid username"}

        except PlatformError:
            return {"status": "Failed", "details": "Invalid Platform"}

        except BrokenChangesError:
            return {"status": "Failed", "details": "API broken due to site changes"}


class Verify(Resource):
    def get(self, platform, username, verifycode):
        user_data_verify = UserDataVerify(username)

        try:
            return user_data_verify.verify(platform, verifycode)

        except UsernameError:
            return {"status": "Failed", "details": "Invalid username"}

        except PlatformError:
            return {"status": "Failed", "details": "Invalid Platform"}

        except BrokenChangesError:
            return {"status": "Failed", "details": "API broken due to site changes"}


api.add_resource(Details, "/api/<string:platform>/<string:username>")
api.add_resource(
    Verify,
    "/api/verify/<string:platform>/<string:username>/verifycode/<string:verifycode>",
)


@app.route("/")
def root():
    return json.dumps(
        {
            "status": "healthy",
            "version": version,
        }
    )


@app.errorhandler(404)
def invalid_route(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
