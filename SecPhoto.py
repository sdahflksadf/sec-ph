def main():
    try:
        from telethon import TelegramClient, events
        from socks import SOCKS5
        from argparse import ArgumentParser
        from sys import argv as name
    except: print(f'Please install dependencies~> python3 -m pip install -r requierments.txt');exit(0)
    api_id = 1520270
    api_hash = "82bd7b4562a5cd24d182bdc39b2d9352"

    parser = ArgumentParser(add_help=False)
    parser.add_argument('-p', '--proxy')
    parser.add_argument('-Sid', '--string-id')
    parser.add_argument('-Nid', '--numeric-id')
    parser.add_argument('-help', '--help', action='store_true')
    argv = parser.parse_args()

    if argv.proxy != None:
        ip = argv.proxy.split(':')[0]
        port = int(argv.proxy.split(':')[1])
        cli = TelegramClient('secret', api_id, api_hash, proxy=(SOCKS5, ip, port))
    else:
        cli = TelegramClient('secret', api_id, api_hash)
    if argv.help:
        print('''
socks5 proxy (tor) ~> -p 127.0.0.1:9050
-Sid or --string-id USERNAME ~> set chat of self destructing media
-Nid or --numeric-id USER CHAT ID ~> set numeric id
    ''')
        exit(0)
    if argv.string_id == None and argv.numeric_id == None:
        print(f'Please see help~> python3 {name[0]} --help')
        exit(0)
    elif argv.string_id != None and argv.numeric_id == None:
        id = argv.string_id
    elif argv.string_id == None and argv.numeric_id != None:
        id = int(argv.numeric_id)
    elif argv.string_id != None and argv.numeric_id != None:
        print(f'Please see help~> python3 {name[0]} --help')
        exit(0)
    print(f'Waiting for reply to a photo...')
    cli.start()
    @cli.on(events.NewMessage(chats=id, func=lambda e: e.reply_to != None))
    async def run(event):
        mes = await cli.get_messages(id, ids=event.reply_to_msg_id)
        # print(mes.media)
        try:
            if mes.media.photo != None:
                print(f'Downloading photo...', end='')
                await cli.download_media(mes.media, 'secret.jpg')
                await cli.send_file('me', open('secret.jpg', 'rb'))
                print('\r Secret photo sent in your saved messages')
        except AttributeError:
            try:
                if mes.media.document != None:
                    print(f'Downloading video...', end='')
                    await cli.download_media(mes.media, 'secret.mp4')
                    await cli.send_file('me', open('secret.mp4', 'rb'))
                    print(f'\r Secret video sent in your saved messages')
            except AttributeError:
                if mes.media.video != None:
                    print(f'Downloading video...', end='')
                    await cli.download_media(mes.media, 'secret.mp4')
                    await cli.send_file('me', open('hock.mp4', 'rb'))
                    print(f'\r Secret video sent in your saved messages')
    cli.run_until_disconnected()
if '__main__' == __name__:
    while True:
        try:
            main()
        except KeyboardInterrupt as e:
            print('Bye :)')
            exit(0)
        except Exception as e:
            print(f'warning: {e}')

