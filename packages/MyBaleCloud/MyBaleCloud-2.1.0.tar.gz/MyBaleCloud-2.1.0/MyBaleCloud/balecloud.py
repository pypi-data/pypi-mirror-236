#!/usr/bin/env python3
"""
BaleCloud
~~~~~~~~~~

this library are created with bale apis

```
from MyBaleCloud.balecloud import BaleCloud
```

for installition = `pip install MyBaleCloud`


"""
# BackTrack
# HosT1LeT

# python3


import requests
import os 
os.system("cls || clear")


print("""
\033[34m[</>] \033[97mMyBaleCloud is \033[96mStarting\033[97m !

\033[34m[</>] \033[97mpreparing to \033[91msetup \033[97mlibrary

""")

class BaleCloud:
    def __init__(self, botToken : str, proxies = None) -> dict:
        self.token = str(botToken)
        global headers
        headers = {'*/*'}
        self.proxy = proxies
        

    def sendMessage(self, message : str = None, chatID : str = None, messageID : str = None):
         
        if (message == None or chatID == None):
            raise ValueError('message or chatID argument cannot be empty')
        else:
            paramSM = {'chat_id' : chatID,
                       'text' : message,
                       'reply_to_message_id' : messageID
                       }
            
            return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/sendMessage', params=paramSM).json())

    def editMessageText(self, newMessage : str = None, chatID : str = None, messageID : str = None, ):
         
        if (newMessage == None or chatID == None or messageID == None):
            raise ValueError('newMessage / chatID / messageID cannot be empty')
        else:
            paramEMT = {'chat_id' : chatID,
                        'text' : newMessage,
                        'message_id' : messageID
                        }
            
            return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/editMessageText', params=paramEMT).json())

    def delMessage(self, chatID : str = None, messageID : str = None):
         
        if (chatID == None or messageID == None):
            raise ValueError('chatID or messageID argument cannot be empty')
        else:
            paramDM = {'chat_id' : chatID,
                       'message_id' : messageID
                       }
            
            return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/deleteMessage', params=paramDM).json())

    def getUpdates(self, offset : int = None, limit : int = None):
         
        while 1:
            try:
                paramGU = {'offset' : offset,
                           'limit' : limit
                           }
                
                return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/getUpdates', params=paramGU).json())
                break
                
            except:continue

    def setWebhook(self, url : str = None):
         
        if (url == None):
            raise ValueError('url argument cannot be empty')
        else:
            paramSW = {'url' : url}
            return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/setWebhook', params=paramSW).json())

    def deleteWebhook(self):
         
        while 1:
            try:
                req = requests.get(f'https://tapi.bale.ai/bot{self.token}/deleteWebhook', headers=headers, proxies=self.proxy)
                return dict(req.json())
                break
            except:continue


    def getMe(self):
         
        while 1:
            try:
                req = requests.post(f'https://tapi.bale.ai/bot{self.token}/getMe', headers=headers, proxies=self.proxy)
                return dict(req.json())
                break
            except:continue

    def sendUrlPhoto(self, photo : str = None, chatID : str = None, caption : str = '', messageID : str = None):
         
        if (photo == None or chatID == None):
            raise ValueError('photo or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramSUP = {'chat_id' : chatID,
                                'photo' : photo,
                                'caption' : caption,
                                'reply_to_message_id' : messageID
                                }
                    req = requests.post(f'https://tapi.bale.ai/bot{self.token}/sendPhoto', params=paramSUP,headers=headers, proxies=self.proxy)
                    return dict(req.json())
                    break
                except:continue

    def sendUrlAudio(self, audio : str = None, chatID : str = None, caption : str= None, messageID : str = None):
         
        if (audio == None or chatID == None):
            raise ValueError('audio or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramSUA = {"chat_id" : chatID,
                                'audio' : audio,
                                'caption' : caption,
                                'reply_to_message_id' : messageID
                                }
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/sendAudio', params=paramSUA).json())
                    break
                except:continue

    def sendUrlDocument(self, document : str = None, chatID : str = None, caption : str = None, messageID : str = None):
         
        if (document == None or chatID == None):
            raise ValueError('document or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramSUD = {'chat_id' : chatID,
                                'document' : document,
                                'caption' : caption,
                                'reply_to_message_id' : messageID
                                }
                    
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/sendDocument', params=paramSUD).json())
                    break

                except:continue

    def sendUrlVideo(self, video : str = None, chatID : str = None, caption : str = None, messageID : str = None):
         
        if (video == None or chatID == None):
            raise ValueError('video or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramSUV = {'chat_id' : chatID,
                                'video' : video,
                                'caption' : caption,
                                'reply_to_message_id' : messageID
                                }
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/sendVideo', params=paramSUV).json())
                    break
                except:continue
                
    def sendLocalPhoto(self, photo : str = None, chatID : str = None, caption : str = '', messageID : str = None):
         
        if (photo == None or chatID == None):
            raise ValueError('photo or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramSLP = {
                        'chat_id' : chatID,
                        'caption' : caption,
                        'reply_to_message_id' : messageID
                    }
                    
                    fileP = {'photo' : open(photo, 'rb')}
                
                    return dict(requests.post(f"https://tapi.bale.ai/bot{self.token}/sendPhoto", params=paramSLP, files=fileP).json())
                
                except:continue
                
    def sendLocalAudio(self, audio : str = None, chatID : str = None, caption : str= None, messageID : str = None):
         
        if (audio == None or chatID == None):
            raise ValueError('audio or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramSUA = {"chat_id" : chatID,
                                'caption' : caption,
                                'reply_to_message_id' : messageID
                                }
                    
                    fileA = {'audio' : open(audio, 'rb')}
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/sendAudio', params=paramSUA, files=fileA).json())

                    break
                except:continue
                
    def sendLocalVideo(self, video : str = None, chatID : str = None, caption : str = None, messageID : str = None):
         
        if (video == None or chatID == None):
            raise ValueError('video or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramSUV = {'chat_id' : chatID,
                                'caption' : caption,
                                'reply_to_message_id' : messageID
                                }
                    fileV = {'video' : open(video, 'rb')}
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/sendVideo', params=paramSUV, files=fileV).json())

                    break
                except:continue
                
    def sendLocalDocument(self, document : str = None, chatID : str = None, caption : str = None, messageID : str = None):
         
        if (document == None or chatID == None):
            raise ValueError('document or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramSUD = {'chat_id' : chatID,
                                'caption' : caption,
                                'reply_to_message_id' : messageID
                                }
                    
                    fileD = {'document' : document}
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/sendPhoto', params=paramSUD, files=fileD).json())

                    break
                except:continue
                


    def getFile(self, fileID : str = None):
         
        if (fileID == None):
            raise ValueError('fileID argument cannot be empty')
        else:
            while 1:
                try:
                    return dict(requests.get(f'https://tapi.bale.ai/bot{self.token}/getFile', params={
                        'file_id' : str(fileID)
                    }, headers=headers, proxies=self.proxy).json())
                    break
                except:continue

    def getChat(self, chatID : str = None):
         
        if (chatID == None):
            raise ValueError('chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramGC = {'chat_id' : chatID}
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/getChat', params=paramGC).json())
                    break
                except:continue

    def getChatAdministrators(self, chatID : str = None):
         
        if (chatID == None):
            raise ValueError('chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramGCA = {'chat_id' : chatID}
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/getChatAdministrators', params=paramGCA).json())
                    break
                except:continue

    def getChatMembersCount(self, chatID : str = None):
         
        if (chatID == None):
            raise ValueError('chatID argument cannot be empty')
        else:
            while 1:
                try:
                    paramGCMC = {'chat_id' : chatID}
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/getChatMembersCount', params=paramGCMC).json())
                    break
                except:continue

    def getChatMember(self, chatID : str = None, userID : str = None):
         
        if (chatID == None or userID == None):raise ValueError('chatID or userID argument cannot be empty')
        else:
            while 1:
                try:
                    paramGCM = {'chat_id' : chatID,
                                'user_id' : userID
                                }
                    return dict(requests.post(f'https://tapi.bale.ai/bot{self.token}/getChatMember', params=paramGCM).json())
                    break
                except:continue
                
                
    def getLastUpdates(self, offset : int = 0, limit : int = 0):
        try:
            req = requests.post(f'https://tapi.bale.ai/bot{self.token}/getUpdates', data={
                'offset' : int(offset),
                'limit' : int(limit)
            },
            headers=headers, proxies=self.proxy)
            return dict(req.json()).get('result')[-1]
        except:pass

    def sendItToMyPVs(self, adminChatIDs = None):
        try:
            UP = self.getUpdates().get('result')[-1].get('message')
            fromWhat = UP.get('from')
            name = fromWhat.get('first_name')
            _chatID = fromWhat.get('id')
            msgID = UP.get('message_id')
            text = str(UP.get('text'))
            
            if text:
                if type(adminChatIDs) == list:
                    for acis in adminChatIDs:
                        self.sendMessage(message=f'NewMessage !\n\nfrom: {name}\nchatID: {_chatID}\nmessage: {text}', chatID=acis)
                        self.sendMessage(message='your message sent in my Admin(s) PVs', chatID=_chatID, messageID=msgID if msgID else '')
                else:
                    self.sendMessage(message=f'NewMessage !\n\nfrom: {name}\nchatID: {_chatID}\nmessage: {text}', chatID=adminChatIDs)
                    self.sendMessage(message='your message sent in my Admin(s) PVs', chatID=_chatID, messageID=msgID if msgID else '')
        
        except Exception as ESITMPV:
            pass
            return ESITMPV
        
    def sendItAgain(self, starter : str = None):
        try:
            UP = self.getUpdates().get('result')[-1].get('message')
            text = str(UP.get('text'))
            if text.startswith(starter):
                stData = text.replace(f"{starter}", '')
                self.sendMessage(message=stData, chatID=UP.get('chat').get('id'), messageID=UP.get('message_id') if UP.get('message_id') else '')
        except Exception as ESIA:
            pass
            return ESIA
        
        
    def responeText(self, targetText : str = "/"):
        """
        When a User start with a `/` or anything in `targetText` parameter, robot get all of the sentence in front of `/` or anything in `targetText` parameter
        """
        try:
            UP = self.getUpdates().get('result')[-1].get('message')
            text = str(UP.get('text'))
            if text.startswith(targetText):
                return text.replace(f'{targetText}', '')
        except Exception as ERT:
            pass
            return ERT