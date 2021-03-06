#!/usr/bin/env python
"""
script is used to fetch and publish all failed tests in TestNG
file to fetch 'testng-results.xml'
"""
import sys
import re
import argparse
from xml.dom import minidom


def getargs():
    """
    Supports the following command-line arguments listed below.
    testng_file - testng file name
    url - bitbucket/stash url
    """
    parser = argparse.ArgumentParser(description='fetch all failed functional tests')
    parser.add_argument('testng_file', help='testng xml file name')
    parser.add_argument('url', help='bitbucket/stash url')
    args = parser.parse_args()
    return args


def fetch_testng(testng_file, url):
    """ create empty list """
    failed_tests = [] 
    """ create an empty list for failed config """
    failed_config = []
    """ parse xml file """
    xmldoc = minidom.parse(testng_file)
    testng = xmldoc.getElementsByTagName("testng-results")[0]
    test = testng.getElementsByTagName("test")[0]
    test_class = test.getElementsByTagName("class")
    """ iterate through all classes """ 
    for test_classes in test_class: 
        test_method=test_classes.getElementsByTagName("test-method")
        for test_methods in test_method: 
            signature = test_methods.getAttribute("signature")
            status = test_methods.getAttribute("status")
            name = test_methods.getAttribute("name")
            config = test_methods.getAttribute("is-config")
            """ Check status of test and configuration """
            if status == "FAIL" and config == "true":
                """ Get all failed configs """
                failed_config.append(signature) 
            elif status == "FAIL":
                """ Get all failed tests """
                failed_tests.append(signature) 

    """ find tests failed on retry """
    list_tests = set([x for x in failed_tests if failed_tests.count(x) > 2])
    for i in list_tests:  # print all failed tests in the retry

        """ 
        Apply some regular expression to find test_name and method and package
        """
        lst1 = i.split('(')
        test_name1 = lst1[0]
        lst2 = lst1[1].split('instance:')[1].split('@')[0]
        test_group1 = lst2.split('.')[-1]
        package1 = re.sub(r'.[a-zA-Z]*$', "", lst2)
        """ URL for the failed test """
        url1 = url + "testngreports/" + package1 + "/" + test_group1 + "/" + test_name1
        """ failed test """
        test_case1=package1 + "." + test_group1 + "." + test_name1
        """
        This is [an example](http://www.example.com/) inline link - example to insert a link for a text in stash
        """
        print("[" + test_case1 + "](" + url1 + ")")
    for j in failed_config:  # print all failed config
        """
        Apply some regular expression to find test_name and method and package
        """
        lst3 = j.split('(')
        test_name2 = lst3[0]
        lst4 = lst3[1].split('instance:')[1].split('@')[0]
        test_group2 = lst4.split('.')[-1]
        package2 = re.sub(r'.[a-zA-Z]*$', "", lst4)
        """ URL for the failed test """
        url2 = url + "testngreports/" + package2 + "/" + test_group2 + "/" + test_name2
        """ failed test config """
        test_case2 = package2 + "." + test_group2 + "." + test_name2
        print("[" + test_case2 + "](" + url2 + ")")


def main():
    """ gather all command line arguments """
    args = getargs()
    testng_file = args.testng_file
    url = args.url
    fetch_testng(testng_file, url)


if __name__ == '__main__':
    main()
