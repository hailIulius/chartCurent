import requests

cookies = {
    '$Cookie: renderCtx': '%7B%22pageId%22%3A%22edb2e571-22f8-4deb-a623-33d81fb788d5%22%2C%22schema%22%3A%22Published%22%2C%22viewType%22%3A%22Published%22%2C%22brandingSetId%22%3A%2223c4f89e-242c-4008-a38a-97393db5acbd%22%2C%22audienceIds%22%3A%226Au1o000000PBrR%22%7D',
    'oinfo': 'c3RhdHVzPUFDVElWRSZ0eXBlPTYmb2lkPTAwRDI0MDAwMDAwY3ZHMA==',
    'autocomplete': '1',
    'sid': '00D24000000cvG0\\u0021ARgAQCJjjVUkNcHMWyZfStujX8tGJ1XwTGE05mrJwYE8Ct.fu9Qs3uBFzoLjErPm7iqrJDdtQarE5VX6xbT3xKxcxtR6fLCo',
    'sid_Client': 'o00000DhUQ34000000cvG0',
    'clientSrc': '86.107.59.50',
    'inst': 'APP_1o',
    'oid': '00D24000000cvG0',
    'sfdc-stream': '\\u00215bBwYQWmEoQds7oQNTP8TpmCoMKtVIL6KLeDnNrVzWrmBjiZHZxZt/JppJXI6hpGuebDdRvMB8vLBiM=',
}

headers = {
    'Connection': 'keep-alive',
    'X-SFDC-Request-Id': '1464780000cc9629cc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Origin': 'https://contulmeu.e-distributie.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://contulmeu.e-distributie.com/s/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = (
    ('r', '1'),
    ('other.PED_Utility.getAccountInfo', '1'),
    ('other.PED_Utility.getContactInfo', '1'),
    ('other.PED_Utility.getUserName', '1'),
    ('ui-chatter-components-messages.Messages.getMessagingPermAndPref', '1'),
    ('ui-communities-components-aura-components-forceCommunity-navigationMenu.NavigationMenuDataProvider.getNavigationMenu', '1'),
)

data = {
    'message': '{"actions":[{"id":"27;a","descriptor":"serviceComponent://ui.chatter.components.messages.MessagesController/ACTION$getMessagingPermAndPref","callingDescriptor":"UNKNOWN","params":{},"storable":true},{"id":"38;a","descriptor":"serviceComponent://ui.communities.components.aura.components.forceCommunity.navigationMenu.NavigationMenuDataProviderController/ACTION$getNavigationMenu","callingDescriptor":"markup://forceCommunity:navigationMenuBase","params":{"navigationLinkSetIdOrName":"Default_Navigation2","includeImageUrl":false,"addHomeMenuItem":true,"menuItemTypesToSkip":[]},"version":"48.0","storable":true},{"id":"71;a","descriptor":"apex://PED_Utility/ACTION$getUserName","callingDescriptor":"markup://c:PED_CustomProfileHeader","params":{}},{"id":"72;a","descriptor":"apex://PED_Utility/ACTION$getAccountInfo","callingDescriptor":"markup://c:PED_CustomProfileHeader","params":{}},{"id":"73;a","descriptor":"apex://PED_Utility/ACTION$getContactInfo","callingDescriptor":"markup://c:PED_CustomProfileHeader","params":{}}]}',
    'aura.context': '{"mode":"PROD","fwuid":"2a7dI3yJAq4Ks9x5yB5pfg","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"-X3DgayUWgiqPDRFrIX5uA"},"dn":[],"globals":{},"uad":false}',
    'aura.pageURI': '/s/',
    'aura.token': 'eyJub25jZSI6IkdNYkhWaWdZUGtsbHFnYS1CcTk2cm8zRlRlQS1GWUcwY3BDUzlUY281ZU1cdTAwM2QiLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IntcInRcIjpcIjAwRDI0MDAwMDAwczY1OFwiLFwidlwiOlwiMDJHMW8wMDAwMDA0bEQ3XCIsXCJhXCI6XCJjYWltYW5zaWduZXJcIn0iLCJjcml0IjpbImlhdCJdLCJpYXQiOjE1ODIxMTk2NDc4OTAsImV4cCI6MH0=..MwWZtfShHGq_c94RbAyKahMSsNsPb_8GPG8i-KdHYN4='
}

response = requests.post('https://contulmeu.e-distributie.com/s/sfsites/aura',
                         headers=headers, params=params, cookies=cookies, data=data, verify=False)

print (response, "POST call")
print (response.text.encode("utf-8"), "TEXT")
print (response.content, "CONTENT")
print (response.status_code, "STATUS CODE")
# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.post('https://contulmeu.e-distributie.com/s/sfsites/aura?r=1&other.PED_Utility.getAccountInfo=1&other.PED_Utility.getContactInfo=1&other.PED_Utility.getUserName=1&ui-chatter-components-messages.Messages.getMessagingPermAndPref=1&ui-communities-components-aura-components-forceCommunity-navigationMenu.NavigationMenuDataProvider.getNavigationMenu=1', headers=headers, cookies=cookies, data=data)
