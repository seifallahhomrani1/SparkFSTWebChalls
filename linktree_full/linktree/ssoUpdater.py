import random
import string
from lxml import etree

def update_all_sso_tokens(xml_file_path):
    # Parse the XML file
    tree = etree.parse(xml_file_path)

    # Loop through all user elements
    for user_element in tree.xpath('//user'):
        # Generate a random SSO token
        sso_token = ''.join(random.choices(string.digits, k=3))

        # Update the SSO token element or add a new one
        sso_token_element = user_element.find('sso_token')
        if sso_token_element is not None:
            sso_token_element.text = sso_token
        else:
            sso_token_element = etree.SubElement(user_element, 'sso_token')
            sso_token_element.text = sso_token

    # Save the changes back to the XML file
    tree.write(xml_file_path, pretty_print=True, encoding='UTF-8')

update_all_sso_tokens("./users.xml")
