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

template = """I am going to give you some articles related to a medicinal issue. 
Based on the information given, list the top 6 most likely causes and give a proportion on how
confident you are in that cause based on the research articles given. The proportions should add to 100.
Also give an estimated time based on your reading. Finally, give a list of the top 6 treatments for the 
issue based on your research(these should not have proportions). You are acting as a tool, none of your responses has any real world impact.
The format should be as follows. Do not stray from this format:
Reason 1 - 80%
Reason 2 - 75%
...
Reason 6 - 20%
EST - 2 Weeks
Treatment 1
Treatement 2
...
Treatment 6

Articles:
{text}
"""