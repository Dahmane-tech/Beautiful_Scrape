from flask import Flask, request, jsonify
from bs4 import BeautifulSoup, ResultSet
import requests
import json
from urllib.parse import urlparse
from bs4.element import Tag

def parce_as_additional_methode(obj_of_soup, result, soup):
    at_elment = obj_of_soup["at_elment"]
    for at_elment_selct in at_elment:
        if isinstance(at_elment_selct, dict):
            if isinstance(result, ResultSet):
                return [parce_as_methode(at_elment_selct, elment) for elment in result]
            return parce_as_methode(at_elment_selct, result)
        elif isinstance(at_elment_selct, str):
            if isinstance(result, ResultSet):
                return [parce_as_attribute(at_elment_selct, elment) for elment in result]
            return parce_as_attribute(at_elment_selct, soup)
        elif isinstance(at_elment_selct, list):
            if isinstance(result, ResultSet):
                return [parce_as_array_of_selctors(at_elment_selct, elment) for elment in result]
            return parce_as_array_of_selctors(at_elment_selct, soup)
        elif isinstance(result, str):
            return result
        else:
            return [str(element) for element in result]


def parce_as_methode(obj_of_soup, soup):
    method_name = list(obj_of_soup.keys())[0]
    method_args = obj_of_soup[method_name]
    result = getattr(soup, method_name)(*method_args)
    print(type(result))
    print(result)
    if "at_elment" in obj_of_soup:
        return parce_as_additional_methode(obj_of_soup, result, result)
    elif result is None:
        return None
    elif isinstance(result,  (str, Tag)) :
        return result
    else:
        return [str(element) for element in result]


def parce_as_attribute(obj_of_soup, soup, as_str=True):
  if (not obj_of_soup == "zipped" ):
    attribute = getattr(soup, obj_of_soup, None)
    print(attribute)
    if attribute is not None:
        if as_str:
            return str(attribute)
        else:
            return attribute
    else:
        return None
  else:
      zipped = True


def parce_as_array_of_selctors(obj_of_soup, soup):
    inner_result = []
    this_soup = soup
    result_only = False
    for element in obj_of_soup:
        print(element, this_soup)
        if isinstance(element, dict):
            this_soup = parce_as_methode(element, this_soup)
        elif isinstance(element, str):
            if not element == "result_only":
                this_soup = parce_as_attribute(element, this_soup, False)
                print(this_soup)
            else: 
                result_only = True
        if this_soup is not None:
            if isinstance(this_soup, list):
                inner_result.append(this_soup)
            else:
                inner_result.append(str(this_soup))
    return str(this_soup) if result_only else inner_result

app = Flask(__name__)


@app.route('/api/scrap', methods=['POST', 'GET'])
def scrap_data():
    if request.method == 'POST':
        payload = request.get_json()
        url = payload.get('url', '')
        arguments = payload.get('arguments', [])
    else:
        url = request.args.get('url', '')
        arguments = request.args.getlist('arguments', [])
        for i in range(len(arguments)):
            try:
                arguments[i] = json.loads(arguments[i])
                print(arguments)
            except json.JSONDecodeError:
                pass
        print(arguments)

    if not url:
        return jsonify({'error': 'URL is missing'}), 400
    if not arguments:
        return jsonify({'error': 'arguments are missing'}), 400
    else:
        print(arguments)

    try:
        response = requests.get(url)
        response.raise_for_status()
        main_html = response.text
        soup = BeautifulSoup(main_html, 'html.parser')
        result_output = []
        zipped= False
        
        for obj_of_soup in arguments:
            if isinstance(obj_of_soup, dict):
                print("before call")
                print(obj_of_soup)
                result_output.append(parce_as_methode(obj_of_soup, soup))
            elif isinstance(obj_of_soup, str):
                result_output.append(parce_as_attribute(obj_of_soup, soup))
            elif isinstance(obj_of_soup, list):
                result_output.extend(parce_as_array_of_selctors(obj_of_soup, soup))
		
        return jsonify([list(pair) for pair in zip(*result_output)] if zipped  else result_output), 200

    except requests.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 501


if __name__ == '__main__':
    app.run()
