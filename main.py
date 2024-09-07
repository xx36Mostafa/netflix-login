import requests , time , json , sys , os 
from colorama import Fore , init 
from bs4 import BeautifulSoup
import urllib.parse
from rich import print as printf
from rich.console import Console
from rich.panel import Panel

init(strip=not sys.stdout.isatty())
os.system('cls')

class smsSender:
    def __init__(self,account):
        self.account = account
        self.email , self.password = account.split(':')[0] , account.split(':')[1]

    def start(self):
        self.sesion = requests.Session()
        login_url = 'https://www.netflix.com/login'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36'
            }
        response = self.sesion.get(login_url,headers=headers)
        self.esn = response.text.split('"esn":"')[1].split('"')[0]
        self.auth_url = response.text.split('"authURL":"')[1].split('"')[0].replace("\\x3D",'=')
        allocation = response.text.split('"abAllocations":')[1].split('],')[0] + ']'
        data_list = json.loads(str(allocation))
        self.name , self.value = '' , ''
        for item in data_list:
            self.name = item['testId']
            self.value = item['cellId']
        result = {item['testId']: item['cellId'] for item in data_list}
        self.abAllocation = json.dumps(result)
        r = self.login()


    def login(self):
        URL = 'https://www.netflix.com/api/aui/pathEvaluator/web/%5E2.0.0?landingURL=%2Feg-en%2Flogin&landingOrigin=https%3A%2F%2Fwww.netflix.com&inapp=false&languages=en-EG&netflixClientPlatform=browser&flow=websiteSignUp&mode=login&method=call&falcor_server=0.1.0&callPath=%5B%22aui%22%2C%22moneyball%22%2C%22next%22%5D'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.netflix.com',
            'referer': 'https://www.netflix.com/login',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-netflix-ftl-bypass': 'true',
            'x-netflix.browsername': 'Chrome',
            'x-netflix.browserversion': '128',
            'x-netflix.client.request.name': 'ui/xhrUnclassified',
            'x-netflix.clienttype': 'akira',
            'x-netflix.esnprefix': 'NFCDCH-02-',
            'x-netflix.nq.stack': 'prod',
            'x-netflix.osfullname': 'Windows 10',
            'x-netflix.osname': 'Windows',
            'x-netflix.osversion': '10.0',
            'x-netflix.request.routing': '{"path":"/nq/aui/endpoint/%5E1.0.0-web/pathEvaluator","control_tag":"auinqweb"}',
            'x-netflix.uiversion': 'vb396e4f2'
        }
        payload = {
            'param': '{"action":"loginAction","fields":{"nextPage":"","rememberMe":"true","countryCode":"+20","countryIsoCode":"EG","userLoginId":"'+self.email+'","password":"'+self.password+'","recaptchaResponseToken":"03AFcWeA6etAOvXDUI6NNcpjPevUs-3tnQfkMRzI4shSoVtxp4LxiohJHNN1KqYk5o-tqHgah-1oVdserllBmawsMpj3yNOlTE5Bbn_xOcxWOSkM5DkEw2tJS4QiVUNV9CBU_3epGiPyv6Gu1GGFxJvJNhE8v7ToKr-NLEBlqGK_QdrcT3mvQZWrGVDa_pU4w1goud9MqZUg3yOGNFX2RYlvyCogb6jMHs_M1p-nq6ayPUqamgs7gQyZR5cUAlUaETQ4nHLD6Tw7IvA4hV3RP9HO7Wfxm3MUn7wn_xn8CJlAgUCZT6GcrLi6eWMP3Y5rE9nobefuWL81cEI6qa2Z4F_HZ-bnsB603819rQkPg_F27HX2dpwHqGbk455t-AwN6OKbSAqHBG7mOXXTMwmgtk-TM18gCytASl_rF1WYqXrdT69CLgXS10hzCemkGIITeXlnuC8D563YGuaLfb3axm_ZDC7NwAboqv9jwRQZib8kHMwiC752xaDaWgz5IKxoQxapJBaPecE-KU45bAXR3RitHYBl7j2ZntzzkqlbN_wzhaWtbhqMLmrLC64DS_jGYYOf5PrVVPty1Y50NbRSl4d3XOHmMuMAU2mH3YnYzJtnHGt5jdqe_Ap36s2RKZArIdhSDIZX7pF4Z_Xb078JUlYFi189sVqYJgbQckkSXTBsw7U5tkv2MHLFdN46g86g0FWgSP68G0QpSpxLlpVPl2NbpjJjmrc21LGwYHRV5ltfYlF7OJlySSvoQdf8kIrVtpZjsEPE0mZOj7lUjiNzHpBAO__umsP0ReSO6v5etJihGcsmEC6pGsoLZEosB7hyS55pqfzEZ68gwthc4cwQ24Yu2C-u-rFXjygNReAW1KBm_JqNFYWGDHNb1rpy2d4ClDcqDgSBTvgtPMhzcp6GCNHKX3Ta3fNfdPilu3zieR4UvUqfDTSW-ZHmM0K1qyWFR7zGS7_dSGoR8qaeAPRGAnX2NEp-RToGkP1vLIouSFCVKgrqFQk2_mi6cXApcW-e8nI5P_UfkbbFNRYcyy_3qe6RogO7fiVmS4QBoxBlraNeleztq9oD0nJcxY2znHO5-bByVBUMyKf-TWuViLTMhXj-r1sWfH8Ma0Smx29uZUuwKa2_bApAiihUlLqBPZrA3HzRdQTrOyYswjKHvAunlH1VnhNjXEVlHksB4bHVYpXs0TM9YPuArcTuHB3nrdsHx_yZ_FLb0qhGx3ztlhXacvfOm4glpz--WvvbIg2SzVtVNZVCe8d_mUIg-NHXPNX2Qq04XcYHJPsjoeHWPq1chCHQmM3vG64uzD4-hKDDbPsALZH4tdvsGfBmYNcvxQj_Ikz_2AcsyyCC646EjHx6ohDJTlHXRvBnk0vHOQZR3f1AFPCtDMVQsZN25wAWjleqiCj72PXyAD5wNS_kWd560JCgrF1dO9jK26UYRYEnGI7zc0tKFqPIKBcFPQ43J2g0uRh-TaKxQ8G6_x5maAT27NW3dED9Swq8dGts6lW7Y7jDmlkik6p6PeusAhCUsA5_PKoAAt7laCzwEzVcwXoioP8gJaWKi-_1XRiZMLnwVU5BPEq8SkAvkk61yVT4snBlcwl9isT6L6dtVahIlv4w5QPePkNrpi7XIraTFLp2h7MuD2jJiyuu5Nb3qxgL4f7avGOhqI0dENzSab9SWWe0YhehW3yb5Nji43hi2AgoTV2dysla6thnlzlMv-uKGNR1cHx-DcaV1D8ZnxUkLBVqPpq9rGtuI-ckqStwzeI75MUzZ7OL3PCZrwyXI-DVjrHnJ4pgWSmdf9W2S5NgUMc2_KfmsWXjJ8f7R2TSTIXhK_-CeYkbmfpANG_Bj12hgH-bkdxe52fGuEiecu_aPah0TrgiqIHGWwELhIL85b8uWf1OuMicqYm04zSHM","recaptchaResponseTime":"408","previousMode":""}}',
            f'allocations[{self.name}]': self.value,
            'esn': self.esn,
            'authURL': self.auth_url
        }
        for i in range(7):
            response = self.sesion.post(URL,headers=headers,data=payload,
                                        cookies=self.sesion.cookies.get_dict())
            if response.status_code == 200:
                printf(Panel(f"""[bold green]Successfully Login Account: [bold white]{self.email}""", width=58, style="bold bright_white", title="[ Success ]"))
                return True
            else:
                if i == 6:
                    printf(Panel(f"""[bold red]Failed Login Account: [bold white]{self.email}""", width=55, style="bold bright_white", title="[ Failed ]"))
                    return False
            time.sleep(1)

def LOGO():
    os.system('cls' if os.name == 'nt' else 'clear')
    printf(
        Panel("""[bold red]● [bold yellow]● [bold green]●[bold white]
[bold red]██████╗░░█████╗░██████╗░░█████╗░██████╗░░█████╗░
[bold red]╚════██╗██╔═══╝░██╔══██╗██╔══██╗██╔══██╗██╔══██╗
[bold red]░█████╔╝██████╗░██████╦╝██║░░██║██║░░██║███████║
[bold white]░╚═══██╗██╔══██╗██╔══██╗██║░░██║██║░░██║██╔══██║
[bold white]██████╔╝╚█████╔╝██████╦╝╚█████╔╝██████╔╝██║░░██║
[bold white]╚═════╝░░╚════╝░╚═════╝░░╚════╝░╚═════╝░╚═╝░░╚═╝
   [underline green]Coded By BoDa - Whatsapp [+201098974486]""", width=55,style="bold bright_white")
    )

if __name__ == '__main__':
    LOGO()
    s = smsSender('cpmhmbgcuiaifal@gmail.com:Rga@7YT3ApB$01YB')
    s.start()