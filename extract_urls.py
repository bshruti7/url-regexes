import json
import sys
import datetime
import re


'''this class has all modules for extracting twitter and linkedin handles given various kinds of text'''
class SocialExtraction(object):
    '''

    if pattern not found, return None
    '''
    def extract_twitter_from_url(self,input_url):
        '''twitter url is the only content in the field so return input_url'''
        twitter_handle = None
        search_obj1 = re.search('twitter',input_url,re.IGNORECASE|re.UNICODE)
        if search_obj1:
            twitter_handle = input_url.lower()
        return twitter_handle

    '''
    Example :   Input : This is my linkedin account http://www.linkedin.com/in/abcdeef
                Output: http://www.linkedin.com/in/abcdeef
                        
    if pattern not found, return None
    '''
    def extract_linkedin_from_url(self,input_url):
        '''linkedin url is the only content in the field so return input_url'''
        linkedin_handle = None
        lowercase_input_url = input_url.lower()
        search_obj1 = re.search('linkedin.com|lnkd.in',input_url,re.IGNORECASE|re.UNICODE)
        if search_obj1:
            linkedin_handle = lowercase_input_url
            search_obj2 = re.search('lnkd.in',linkedin_handle,re.IGNORECASE|re.UNICODE)
            if search_obj2:
            # if the url has lnkd.in we have to return the extended version of the url
                try:
                    req = requests.get(linkedin_handle)                 
                except Exception as ex:
                    Log.warning('Unexpected error when opening lnkd shortened urls', params={'opern_type' : 'extract_linkedin_from_url'}, ex=ex)
                    return linkedin_handle
                # check status code of request made
                linkedin_handle = req.url if req.status_code != 404 else None   
        return linkedin_handle


    def extract_twitter_from_text(self,input_text):
        '''search for occurrence of "twitter.com/" in the text'''
        twitter_handle = None
        search_obj1 = re.search('twitter.com/\w+',input_text,re.IGNORECASE|re.UNICODE)
        if search_obj1:
            potential_username = input_text[:search_obj1.end()]
            search_obj2 = re.search('twitter.com/',potential_username,re.IGNORECASE|re.UNICODE)
            if search_obj2:
                twitter_id = potential_username[search_obj2.end():]
                twitter_handle = ("http://twitter.com/"+str(twitter_id)).lower()
            else:
                '''If pattern "twitter.com/username" is not found, the text is searched for @username occurrences'''
                return self.extract_twitter_from_only_handles(input_text)
        return twitter_handle

    def extract_twitter_from_only_handles(self,input_text):
        '''@ symbol matched with @ in handle.
            \w following the @ symbolises valid character in twitter username
            the part before @ is used to remove any matched with email ids of the form hello@gmail.com'''
        twitter_handle = None
        search_obj = re.search('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@(\w+)',input_text,re.IGNORECASE|re.UNICODE)
        if search_obj:
            twitter_id = search_obj.group()[1:]
            twitter_handle = ("http://twitter.com/"+str(twitter_id)).lower()
        else:
            # this handles the case where the handle is mentioned without the @ symbol : twitter: abcdhfj
            search_obj = re.search('twitter: ',input_text,re.IGNORECASE|re.UNICODE)
            if search_obj:
                potential_username = input_text[(search_obj.end()):]
                search_obj1 = re.search('\w+',potential_username)
                twitter_id = search_obj1.group()
                twitter_handle = ("http://twitter.com/"+str(twitter_id)).lower()
        return twitter_handle

   
    def extract_linkedin_from_text(self,input_text):
        linkedin_handle = None
        input_text = input_text.replace('&#xA','')
        input_text = input_text.replace('&#xD','')
        #about_me = about_me.replace('&amp','')
        search_obj1 = re.search('linkedin.com/|lnkd.in/',input_text,re.IGNORECASE|re.UNICODE)
        if search_obj1:
            search_obj2 = re.search('(https?://)?([\w]*\.)?linkedin\.com/(in|pub|profile|companies)/?([\w]*[=|-|/|\|&|;|%]?)*[^;|<|&|>|?|=|\"]',input_text,re.I|re.U)
            if search_obj2:
                linkedin_handle = search_obj2.group()
            else:
                search_obj3 = re.search('lnkd.in',input_text,re.IGNORECASE|re.UNICODE)
                if search_obj3:
                    search_obj4 = re.search('(https?://)?lnkd\.in/([\w]*[=|-|/|\|&|;|%]?)*[^;|<|&|>|?|=|\"]',input_text,re.I|re.U)
                    linkedin_handle = search_obj4.group()
                    try:
                        req = requests.get(linkedin_handle)
                    except Exception as ex:
                        Log.warning('Unexpected error when opening lnkd shortened urls', params={'opern_type' : 'extract_linkedin_from_text'}, ex=ex)
                        return linkedin_handle
                    linkedin_handle = req.url if req.status_code != 404 else None
        return linkedin_handle.lower()


obj = SocialExtraction()
print obj.extract_twitter_from_text("This is my twitter account http://twitter.com/abcdeef")
print obj.extract_linkedin_from_text("This is my linkedin account http://www.linkedin.com/in/abcdeef")
print obj.extract_twitter_from_only_handles("This is my twitter account @abcdeef")