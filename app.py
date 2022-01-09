from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    found_libraries_list = []
    if request.method == "POST":
        website_link = request.form['content']
        try:
            found_libraries_list = _find_libraries_on_website(website_link)
            _find_vulnerabilities_for_libraries(found_libraries_list)
            return render_template("index.html", libraries=found_libraries_list)
        except:
            return 'There is an issue with this link'

    else:
        return render_template("index.html", libraries=found_libraries_list)


@app.route("/vulnerabilities")
def vulnerabilities():
    return render_template("vulnerabilities.html")


def _find_libraries_on_website(website_link):
    libraries_list = []
    found_libraries = []
    page = requests.get(website_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    html_as_string = str(soup)
    with open('libraries') as file:
        [libraries_list.append(line.rstrip()) for line in file]
    [found_libraries.append(library) for library in libraries_list if library in html_as_string]
    return found_libraries


def _find_vulnerabilities_for_libraries(libraries):
    responses_html = []
    f = open("templates/vulnerabilities.html", "w")
    for library in libraries:
        search_url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={library}"
        search_response = requests.get(search_url)
        search_response_html = BeautifulSoup(search_response.content, 'html.parser')
        responses_html.append(search_response_html.find_all(id='TableWithRules'))

    for responses in responses_html:
        f.write(str(responses))


if __name__ == '__main__':
    app.run(debug=True)
