import requests, socket, time, datetime, threading

origin_ip = socket.gethostbyname(socket.gethostname()) #for checker
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
threa = int(input("Threads: "))
def scrape(prox_type, timeout):
    list_url = [f'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/{prox_type}.txt', f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol={prox_type}&timeout=10000&country=all&ssl=all&anonymity=all', f'https://www.proxy-list.download/api/v1/get?type={prox_type}', f'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-{prox_type}.txt', f'https://raw.githubusercontent.com/roosterkid/openproxylist/main/{str(prox_type).upper()}_RAW.txt', f'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/{prox_type}.txt', f'https://github.com/UptimerBot/proxy-list/blob/main/proxies/{prox_type}.txt', f'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/{prox_type}.txt']
    for url in list_url:
        try:
            r = requests.get(url, headers=header, timeout=timeout)
            if r.status_code == 200:
                outFile = open(f"scraped_{prox_type}.txt", 'a')
                outFile.write(r.text+'\n')
                outFile.close()
                print(f'[+] {prox_type} list downloaded with {url}')
        except:
            pass
def checker(checkFile,timeout): #working with http and https only
    f = open(f"{checkFile}", 'r').readlines()
    for line in f:
        if "@" in line:
            mode = 'pre'
        else:
            mode = 'nor'
            proxy = line.split(':')
        try:
            prox = ({"http": f"http://{proxy[0]}:{proxy[1]}", "https": f"http://{proxy[0]}:{proxy[1]}"} if mode == 'nor' else {"http": f"http://{line}", "https": f"http://{line}"})
            r = requests.get('https://ipinfo.io/json', headers=header, proxies=prox, timeout=timeout).json()
            if r['ip'] == origin_ip:
                print(f'[-] {proxy[0]}:{proxy[1]} Not working')
            else:
                print(f'[!] {proxy[0]}:{proxy[1]} Working')
                with open(f"Checked.txt", 'a') as outFile:
                    outFile.write(f"{proxy[0]}:{proxy[1]}" if mode == 'nor' else f"{line}")
        except:
            pass

if __name__ == '__main__':
    def main():
        print("""
        [1] Scrape proxy list
        [2] Check proxy list
        """)
        mode = input("[+] Enter mode: ")
        if mode == '1':
            print("""
            [1] http
            [2] https
            [3] socks4
            [4] socks5
            """)
            type = input("[+] Enter type <http/https/socks4/socks5> : ")
            to = input("[+] Enter timeout: ")
            if type not in ['http', 'https', 'socks4', 'socks5']:
                print("Please enter a valid type")
                time.sleep(3)
                main()
            else:
                scrape(type, int(to))
        elif mode == '2':
            File = input("[+] Enter file name to check: ")
            to2 = input("[+] Enter timeout: ")
            for _ in range(threa):
                threading.Thread(target=checker, args=(File, int(to2))).start()
        else:
            print("Please enter a valid mode")
            time.sleep(3)
            main()
    main()

