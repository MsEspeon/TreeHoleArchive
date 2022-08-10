import json
import datetime
from pathlib import Path
import os
from re import T

def dump_as_md():
    root_path = "./json"
    result_html = ''
    index = 601
    for root, dirs, files in os.walk(root_path):
        dirs = sorted(dirs, reverse=True)
        for dir in dirs:
            print(dir)
            index -= 1
            post_list = list(Path(root_path + '/' + dir).glob('*.json'))
            post_list = sorted(post_list, key=lambda x:int(x.stem), reverse=True)
            for post_path in post_list: 
                try:
                    with open(post_path, encoding='utf-8') as f:
                        post = json.load(f)
                except Exception as JSONDecodeError:
                    continue

                result_html += '# ' + str(post['post']['pid'])
                if post['post']['tag']: result_html += ' ['+str(post['post']['tag'])+']'
                result_html += '\n'
                result_html += datetime.datetime.fromtimestamp(post['post']['timestamp']).strftime("%Y/%m/%d, %H:%M:%S")+'\n'

                PostReply = post['post']['text']
                result_html += PostReply
                result_html += '\n'
                
                PostUrl=post['post']['url']
                # if post['post']['type']=='image': result_html += f'<br/><a href="https://i.thuhole.com/{PostUrl}">{PostUrl}</a>'
                # if post['post']['type']=='image': result_html += f'<br><a href="./images/{PostUrl}"><img src="./images/{PostUrl}" width="600"></a>'
                if post['post']['type']=='image': result_html += f'![](./images/{PostUrl})\n'

                result_html += '\n'
                for reply in post['data']:
                    text = reply['text']
                    name = reply['name']
                    result_html += f'- [{name}] {text}'
                    url = reply['url']
                    # if reply['type'] == 'image': result_html += f'<br/><a href="https://i.thuhole.com/{url}">{url}</a>'
                    # if reply['type'] == 'image': result_html += f'<br><a href="./images/{url}"><img src="./images/{url}" width="600"></a>'
                    if reply['type'] == 'image': result_html += f'![](./images/{url})\n'
                    result_html += '\n'
                result_html += '\n'

            if index % 10 == 0 and index != 600:
                with open('./md/' + str(1000*index) + '_' + str(1000*(index+10)-1) + '.md', 'w', encoding='utf-8') as f:
                    f.write(result_html)
                result_html = ''


if __name__ == '__main__':
    dump_as_md()