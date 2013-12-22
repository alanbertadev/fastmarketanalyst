import re

class FormatUtils:
    
    @staticmethod
    def isValidEmailAddressFormat(emailkey):

        """Email validation, checks for syntactically valid email courtesy of Mark Nenadov.
        See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65215"""
        emailregex = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3\})(\\]?)$"
        if len(emailkey) > 7:
            if re.match(emailregex, emailkey) != None:
            
                if "\'" in emailkey or "\"" in emailkey:
                    return False
                            
                return True
            return False
        else:
            return False
