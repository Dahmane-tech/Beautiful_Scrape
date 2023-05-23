from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlparse


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
        this_soup = soup
        for obj_of_soup in arguments:
            if isinstance(obj_of_soup, dict):
                method_name = list(obj_of_soup.keys())[0]
                method_args = obj_of_soup[method_name]
                result = getattr(soup, method_name)(*method_args)
                if "at_elment" in obj_of_soup:
                    at_elment = obj_of_soup["at_elment"]
                    for at_elment_selct in at_elment:
                        if isinstance(at_elment_selct, dict):
                            method_name = list(at_elment_selct.keys())[0]
                            method_args = at_elment_selct[method_name]
                            # Apply the additional method to each element in the result
                            result = [getattr(element, method_name)(*method_args) for element in result]
                            result_output.append([str(element) for element in result])
                            print(f"{obj_of_soup.get('at_elment')}::{result}")
                        elif isinstance(at_elment_selct, str):
                            attribute = getattr(result, at_elment_selct, None)
                            if attribute is not None:
                                result_output.append([str(attribute)])
                            else:
                                result_output.append([])
                else:
                    result_output.append([str(element) for element in result])

            elif isinstance(obj_of_soup, str):
                attribute = getattr(soup, obj_of_soup, None)
                if attribute is not None:
                    result_output.append([str(attribute)])
                else:
                    result_output.append([])
            elif isinstance(obj_of_soup, list):
                inner_result = []
                for element in obj_of_soup:
                    if isinstance(element, dict):
                        method_name = list(element.keys())[0]
                        method_args = element[method_name]
                        this_soup = getattr(this_soup, method_name, None)
                        if this_soup is not None:
                            this_soup = this_soup(*method_args)
                    elif isinstance(element, str):
                        this_soup = getattr(this_soup, element, None)
                    if this_soup is not None:
                        inner_result.append(str(this_soup))
                result_output.append(inner_result)

        return jsonify(result_output), 200

    except requests.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 501

if __name__ == '__main__':
    app.run()
