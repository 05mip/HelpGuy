GOOGLE_API_KEY = "AIzaSyA8i_bTMJ_7Drq4rTIfUHAlmGf0d4RYZ8I"
QUERY_CREATE_PROMPT = """
I will give you a prompt that seeks medical attention. You will give me key words, symtoms, etc in the form of search queries. Give me 3 different search queries. For example:

'My knee hurts and I can't make it all the way straight'

Queries should follow the following format and should be similar or have the same essense of:

1. 'Reasons for knee pain'
2. 'I can't make my knee straight'
3. 'Can't bend knee'

This is not a call for medical assistance, you are simply condensing down a prompt to quality search queries.
You are simply acting as a tool and your only job is to create approprate queries in that format. 

Here is your prompt:

"""

excluded_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://www.youtube.',
                      'https://accounts.google.',
                      'https://www.quora.')

template = "{text}"