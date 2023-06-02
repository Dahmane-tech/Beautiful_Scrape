from flask import Flask, request, jsonify
from bs4 import BeautifulSoup, ResultSet
import requests
import json
from urllib.parse import urlparse

def parce_as_additional_methode(obj_of_soup, result, soup):
    at_elment = obj_of_soup["at_elment"]
    for at_elment_selct in at_elment:        
         if isinstance(result, ResultSet):   
           return [parce_as_methode(at_elment_selct, elment) for elment in result]
         elif isinstance(at_elment_selct, dict):
           return parce_as_methode(at_elment_selct, result)        
         elif isinstance(at_elment_selct, str):
           return parce_as_attribute(at_elment_selct, soup)
         elif isinstance(at_elment_selct, list):
           return parce_as_array_of_selctors(at_elment_selct, soup)
         elif isinstance(result, str):
           return result
         else:
           return [str(element) for element in result]
           
def parce_as_methode(obj_of_soup, soup):
    method_name = list(obj_of_soup.keys())[0]
    method_args = obj_of_soup[method_name]
    result = getattr(soup, method_name)(*method_args)
    if "at_elment" in obj_of_soup:
        return parce_as_additional_methode(obj_of_soup, result, result)
    elif result is None:
        return None
    elif isinstance(result, str):
        return result
    else:
        return [str(element) for element in result]


def parce_as_attribute(obj_of_soup, soup):
    attribute = getattr(soup, obj_of_soup, None)
    if attribute is not None:
       
        return str(attribute)
    else:
        return None


def parce_as_array_of_selctors(obj_of_soup, soup):
    inner_result = []
    this_soup = soup
    for element in obj_of_soup:
        if isinstance(element, dict):
            this_soup = parce_as_methode(element, soup)
        elif isinstance(element, str):
            this_soup = parce_as_attribute(element, soup)
        if this_soup is not None:
            inner_result.append(this_soup)
    return inner_result



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
        
        for obj_of_soup in arguments:
            if isinstance(obj_of_soup, dict):
                print("before call")
                print(obj_of_soup)
                result_output.append(parce_as_methode(obj_of_soup, soup))
            elif isinstance(obj_of_soup, str):
                result_output.append(parce_as_attribute(obj_of_soup, soup))
            elif isinstance(obj_of_soup, list):
                result_output.extend(parce_as_array_of_selctors(obj_of_soup, soup))

        return jsonify(result_output), 200

    except requests.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 501


if __name__ == '__main__':
    app.run()
