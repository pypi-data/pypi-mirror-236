from client import AskSageClient

client = AskSageClient('nicolas@after-mouse.com', '3912492342449027ad4d5d25b705420a8ddba9a5a6ce46452da143d31e0e3f94')

ret = client.file(file_path='C:/Users/NicolasChaillan/OneDrive/Companies/AskSage/Marketing/Ask Sage - Case Study Veteran Guardian.pdf')
print(ret)

if ret['response'] == 'OK':
    content = ret['ret']

    ret = client.query_plugin('SUMMARIZE', content=content, prompt_template = 'Write a 4,000-character summary of the provided text, focusing on the main points without using introductory phrases. Ensure the summary is concise and effectively communicates the key points of the content:\n')
    print(ret)

exit()

ret = client.query_plugin('SUMMARIZE_WEB', url='https://en.wikipedia.org/wiki/Chief_master_sergeant', prompt_template = 'Write a 4,000-character summary of the provided text coming from a HTML page, focusing on the main points. Do not include any introductory phrases. Never use phrases like "the text is about". Ensure the summary is concise and effectively communicates the key points of the content.')
print(ret)

exit()

ret = client.query('who is Nic Chaillan?')
print(ret)

ret = client.query_with_file('what is this file about?', file='C:/Users/NicolasChaillan/OneDrive/Companies/AskSage/Marketing/Ask Sage - Case Study Veteran Guardian.pdf')
print(ret)