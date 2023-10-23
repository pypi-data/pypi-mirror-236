import string
import random


class crypto:
 def __init__(self,text,key):
      self.text = text
      self.key = key 
      
      
 def encrypt(self):
     shift = self.key
     key2 = 26
     plain_text = self.text
     shift %= key2
     alphabet = string.ascii_lowercase
     shifted = alphabet[shift:] + alphabet[:shift]
     table = str.maketrans(alphabet,shifted)
     encrypted =plain_text.translate(table)
    
     return  '/V1_CRYPTO '+encrypted 
          
          
 def decrypt(self):
     shift = self.key
     key2 = 26
     plain_text = self.text
     shift = key2-shift
     shift %= key2
     if '/V1_CRYPTO ' in plain_text:
      alphabet = string.ascii_lowercase
      shifted = alphabet[shift:] + alphabet[:shift]
      table = str.maketrans(alphabet,shifted)
      decrypted =plain_text.translate(table)
      decrypte = decrypted.replace(decrypted[0:11],'')
      return  decrypte
     else:
          return 'padding error ! /V1_CRYPTO not   '
 
class key_gen:
     
     
  def key_generator_num_V1(min,max):
     gen = random.randint(min,max)
     return gen+8
     
  def key_generator_num_V1_1(string_lowercase,key):
     out = int(string_lowercase, base=key)
     return out
     
  def key_generator_num_V2(size,chars=string.ascii_uppercase+ string.digits +string.ascii_lowercase + '@#£_.&-+()/*:;!? \n\n~`|•√π÷×¶∆€¥$¢^°={}\"%()©®™+✓[]<>' ):
       return ''.join(random.choice(chars) for _ in range(size))
       
"""'.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))"""

          
class key_varibale:
     
  key_var_all = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#£_.&-+()/*:;!? \n\n~`|•√π÷×¶∆€¥$¢^°={}\%"()©®™+✓[]<>'   
  key_var_alp_number = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
  
  key_var_number = '1234567890'
  
  key_var_sim = '@#£_"&-+()/*:;!?~`|•√π÷×¶∆€¥$¢^°={}\%©®™✓[]<>' + " '"
  
  key_var_more =  'àáâäæãåāqwêéèëērtyūüúûùìīïíîõōøœòöôópßdfghjklzxçvbñmqwertyuioplkjhgfdsazxcvbnm1234567890රු'
  
  
class crypto_V2:
     
     def __init__(self,string,key):
          self.string = string
          self.key = key
     
     def encrypt(self):
           keys = self.key
           value = keys[-1] + keys[0:-1]
           encrypt = dict(zip(keys,value))
           string = self.string
           encryptnew = ''.join([encrypt[letter] for letter in string.lower()])
           return '/V2_CRYPTO '+ encryptnew
           
     def decrypt(self):
          keys = self.key
          string = self.string
          if '/V2_CRYPTO ' in string:
           value = keys[-1] + keys[0:-1]
           decrypt = dict(zip(value,keys))
           decryptnew = ''.join([decrypt[letter] for letter in string.lower()])
           decryptne = decryptnew.replace(decryptnew[0:11],'')
           return decryptne
          else:
               return 'padding error '
               
class crypto_V3_num:
     
     def __init__(self,number,key):
          self.number = number
          self.key = key
          
     def decrypt(self):
          key = self.key
          text = self.number
     def encrypt(self):
          pass

hellow_bro = "hhhhhhhhhhhhh"



