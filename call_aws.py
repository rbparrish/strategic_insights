"""
Created on March 19 2016

Intent: Make a call to AWS Alexa to obtain web traffic for a set of web domains
http://docs.aws.amazon.com/AlexaWebInfoService/latest/
"""
import sys, os, xmltodict
sys.path.insert(0, '/Users/RobParrish/Envs/awis')
from myawis import *

def get_alexa_rank(url, aws_access_key_id, aws_scret_access_key):
	# just returns the current average rank (3 month rolling)
	return CallAwis(url, 'Rank', aws_access_key_id, aws_scret_access_key).urlinfo()

def get_alexa_history(url, aws_access_key_id, aws_scret_access_key):
	# Gets specific history information
	obj = CallAwis(url, 'History', aws_access_key_id, aws_scret_access_key)
	return obj.traffichistory(myrange='5',start='20170301')
	# TODO FIRST - make range & start date configurable
	# TODO SECOND - error handling wrong URLS

def parse_single_result(single_result):
	# parses a single datum from parsed beautiful soup alexa history result
	output = {
		'date': str(single_result.Date.string),
		'pageviews_millions': float(single_result.PageViews.PerMillion.string),
		'avg_pageviews_per_user': float(single_result.PageViews.PerUser.string),
		'rank': int(single_result.Rank.string),
		'reach_permillion': float(single_result.Reach.PerMillion.string)
		}
	return output

def alexa_history_into_pd_table(full_alexa_history_api_response):
	#runs parse_single_result for all data in alexa history result. 
	#RETURNS: list of dicts 
	# TODO: return pandas dataframe instead of list of dicts
	all_data_soup = full_alexa_history_api_response.find_all('Data')
	output = list()
	for row in all_data_soup:
		output.append(parse_single_result(row))
	return output

if __name__ == "__main__":
	AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
	AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
	url = 'www.domain.com'
	alexa_history_result = get_alexa_history(url, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	print(alexa_history_into_pd_table(alexa_history_result))

