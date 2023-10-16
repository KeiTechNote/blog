---
title: SSI 개발 환경 구성하기 - Step4 Configuring the FastAPI environment for API development
date: 2023-10-15 05:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

## 개요

[Step2 First Contract][step2_first_contract] 에서 개발한 VDR 스마트 컨트랙트를 [Deploy Smart Contract on Ganache-Cli][step3_Deploy_Contract] 
에서 로컬 개발 환경인 Ganache-Cli 에 배포해 보았습니다. 이제 배포된 스마트 컨트랙트의 Register 와 Resolve 함수를 호출하력고 합니다. 

배포된 스마트 컨트랙트의 함수에 접근하기 위해선 스마트 컨트랙트 주소로 접속하고 함수를 호출하는 과정이 필요합니다. 하지만 빈번하게 발생하는 동작이 복잡하면 사용하기 불편하고, 스마트 컨트랙트 주소가 변경되면 이를 사용하는 모든 사용자가 주소를 알아야 한다는 문제가 있습니다. 

만약, 작성된 스마트 컨트랙트를 100명이 사용하고 있다면, 스마트 컨트랙트가 업그레이드되거나 문제를 수정해 다시 배포하면 주소가 변경되기 때문에 사용자 100명에게 변경된 주소를 알려줘야 하는 문제가 있습니다. 
따라서, 사용자는 스마트 컨트랙트에 직접 접속하지 않지만 스마트 컨트랙트의 함수 호출을 보장해 줄 수 있는 별도의 프로그램을 만든다면, 이러한 문제의 상당 부분을 해소할 수 있습니다. 

본 Post 에서는 이러한 부분을 해결해 줄 프로그램으로 API서버를 만듭니다. 이 API서버는 스마트 컨트랙트에 대신 접속하고 사용자가 호출한 함수를 대신 호출해 주고 결과를 전달해 주는 중계인 역할을 하게 됩니다. 

> API 는 *A*pplication *P*rogramming *I*nterface 의 첫 머리글자를 딴 약자입니다. 어플리케이션(또는 프로그램, 서비스) 간 연결해 주는 것을 의미합니다. 본 Post 에서는 사용자와 VDR 스마트 컨트랙트간을 연결해 주는 것을 의미합니다.
{: .prompt-info}

> 앞서 언급한 API 는 "사용자 - API - 스마트 컨트랙트" 간 연결로 발생할 수 있는 문제를 해소하고 있습니다. 하지만 사용자와 스마트 컨트랙트 간의 문제는 해소되지만 이는 사용자가 갖는 불편함을 API 가 대신 감내하는 것입니다. 즉, API 와 스마트 컨트랙트 간의 문제는 동일한 문제가 여전히 존재합니다. 이 점은 스마트 컨트랙트가 처음 공개되었을 때 부터 재기되어 왔던 문제점이며 최근에는 프록시를 통해 해소하려고 노력하고 있습니다. 본 블로그의 [블록체인 카테고리][BlockChain_Category] 를 참고하기 바랍니다. 
{: .prompt-warning}

### API 개발하기 앞서...

파이썬으로 API 를 개발하는 방식은 다양합니다. 구글에서 "파이썬 API 만들기" 로 검색하면 "Flask", "FastAPI", "Django" 외 여러가지 방법이 있음을 알 수 있습니다. 물론 모두 좋은 방법이고 개발된 철학에 맞는 장점을 품고 있지만, 본 Post 에서는 그 중 "FastAPI" 를 사용합니다. 

[FastAPI 홈페이지][fastapi_homepage] 를 보면 다양한 장점들을 설명하고 있지만 "빠름", "짧음", "견고함"과 같은 용어들은 다양한 형태로 API 를 작성해 보지 않은 사용자라면 와닿지 않습니다. 다만, FastAPI 로 개발했을 때, 사용하기 쉽다라는 장점도 있지만, 더욱 큰 장점이라면 "개발 문서를 기본 제공하는 것"입니다. 
어떤 것이든 문서를 작성하고 그 문서를 다른 사람들과 함께 공유해 본 사람이라면, 가장 골치 아픈 부분이 항상 최신버전을 유지하는 부분일 것입니다. 앞으로 만들 API 는 다른 사용자가 스마트 컨트랙트의 기능을 사용할 수 있도록 기능을 제공하지만, 완성된 상태가 아닌, 꾸준히 수정, 개발되어야 하기 때문에 빈번히 변경이 발생합니다. 그리고 이 모든 것을 매번 문서에 반영하고 다시 공유하는 것은 개발자에게 있어 매우 고된 작업입니다. 하지만, FastAPI 는 Swagger UI 나 ReDoc 두가지 형태로 문서를 자동 생성하므로 개발자는 개발에만 집중할 수 있습니다. 

![swagger_ui_sample](/assets/images/swagger_ui_sample.png)

_Swagger UI (출처 : FastAPI 홈페이지)_

### 파이썬 환경 변수 등록하기

> 미리 파이썬 또는 파이썬 프레임워크를 설치한 경우, 다음과 같이 출력된다면, 다음 섹션 'FastAPI 설치하기'로 이동합니다.
![register_env_4](/assets/images/register_env_4.png)
{: .prompt-info}

앞으로 파이썬으로 필요한 라이브러리 설치를 진행합니다. 다만, Prolog에서 소개한 대로 파이썬만을 설치하거나 Anaconda(파이썬 프레임워크) 을 그대로 설치하는 경우 종종 터미널에서 `python` 을 실행하면 설치된 파이썬이 실행되지 않고 (윈도우의 경우) Windows Store 가 실행되거나 (공통) `command not found` 오류가 나올 수 있습니다. 이러한 오류는 터미널에서 `python`이 어디에 설치되어 있는지 알 수 없어 발생합니다. 따라서, 원할하게 사용하기 위해선 `환경변수`에 등록해야 합니다. 

윈도우 환경변수 등록 위치는 다음과 같습니다. 

- 위치 : '제어판' -> '시스템'(또는 제어판 검색창에서 '시스템' 검색) -> '고급 시스템 설정' -> '환경변수'

![register_env_1](/assets/images/register_env_1.png)

_제어판에서 시스템 검색_

![register_env_2](/assets/images/register_env_2.png)

_시스템에서 환경변수로 이동_

파이썬을 환경변수에 등록할 때, 두 곳을 등록해야 합니다. 한 곳은 `python.exe` 실행파일이 있는 디렉토리와 `pip.exe` (또는 `pip3.exe`) 가 있는 경로입니다. python.exe 가 있는 디렉토리 하위 디렉토리에 pip.exe 가 있지만, 환경변수는 등록한 디렉토리만을 검색합니다. 따라서, 각각의 경로를 등록합니다. 

- 변수 이름 : path
- 변수 값 : C:\Users\amana\anaconda3, C:\Users\amana\anaconda3\Scripts

파이썬이 설치된 경로는 사용자마다 다를 수 있으니 변수 값에 표기된 경로는 자신에게 맞는 경로를 넣어줍니다. 

> 자신이 설치한 파이썬 프로그램의 설치 경로를 찾기 어렵다먄, 1) 윈도우 검색으로 'Python' 을 검색한 후, 2) '앱' 항목에 나오는 'python.exe' 을 선택하고, 3) 하단 '파일 위치 열기' 를 선택하면 설치된 python 경로를 볼 수 있습니다. 
![register_env_5](/assets/images/register_env_5.png)

![register_env_3](/assets/images/register_env_3.png)

_파이썬 등록_

> 환경변수를 등록할 때, 'C:\Users\amana\anaconda3' 가 두번째 등록되어 있음을 알 수 있습니다. 이는 세번째 등록된 변수 값 때문입니다. 세번째 변수 값을 보면 `%USERPROFILE%\AppData\Local\Microsoft\WindowsApps` 입니다. 만약 이 변수값 이후에 'C:\Users\amana\anaconda3'를 등록하고 python.exe 를 실행하면 Windows Store 의 Python 프로그램 화면이 나타납니다. 즉, Windows 는 python.exe 를 환경변수에 등록된 변수 값을 순서대로 검색해 가장 먼저 발견되는 곳의 python.exe 를 실행하게 되는데, WindowsApps 에서 python.exe 가 발견되고 이는 Windows Store 에서 지원하는 프로그램이므로 Windows Store 가 열리는 것입니다. 따라서, 우리가 개별 설치한 python.exe가 실행되길 원한다면 `%USERPROFILE%\AppData\Local\Microsoft\WindowsApps` 변수 값 이전에 위치해야 합니다.
{: .prompt-warning}

환경변수 등록이 완료되었다면 사용중이던 터미널을 종료 후 재시작합니다. 'python.exe' 와 'pip.exe' 명령어가 정상실행되는지 확인합니다.

![register_env_4](/assets/images/register_env_4.png)


### FastAPI 설치하기

FastAPI 는 파이썬용 웹 프레임워크입니다. 앞서 설명한 Swagger UI 나 ReDoc 외에 다양한 기능을 활용하기 위해 FastAPI 프레임워크를 설치합니다. 

- 명령어 : `pip install fastapi`

![install_fastapi](/assets/images/install_fastapi.png)

_FastAPI 설치_

FastAPI 프레임워크 설치가 완료됐으므로 이를 활용해 어떻게 API 를 만들 수 있는지 FastAPI 홈페이지 [예제 코드][fastapi_example_code]로 확인해 보겠습니다 main.py 파일을 생성합니다. 샘플용 테스트 코드이므로 main.py 파일을 어디에 만들어도 상관없습니다. 다만, SSI 를 개발하면서 생성한 모든 코드들을 별도 Repository 에 모아 공개할 예정이므로 본 Post 의 예제 코드는 `\Dev\test\api\app\main.py`에 파일을 생성합니다. main.py 에 예제 코드를 붙여넣습니다. 

![fastapi_example_1](/assets/images/fastapi_example_1.png)

_FastAPI 예제코드 실행 준비_

FastAPI 와 같이 작성된 API 코드는 다른 사용자와 통신하기 위해, 서버를 사용합니다. 일반적으로 개발자들은 자신의 PC 를 개발용 서버로 사용합니다. 즉, 자신이 개발하고 자신의 PC 를 서버로 만들고, 동작을 웹 브라우저로 확인합니다. 따라서, 개발된 코드가 실행된 웹 서버를 만들어주는 `Uvicorn` 프로그램을 설치합니다. 

### Uvicorn 설치하기 

Uvicorn 프로그램 설치 방법은 설치할 프로그램 이름만 다를 뿐 FastAPI 와 다르지 않습니다. 

- 명령어 : `pip install "uvicorn[standard]"`

![install_uvicorn](/assets/images/install_uvicorn.png)

_Uvicorn 설치_

모든 준비가 완료됐습니다. 이제 실행합니다. 

### API 서버 실행하기

터미널에서 main.py 파일이 있는 위치로 이동해 Uvicorn 으로 API 서버를 실행합니다. 

- 명령어 : `uvicorn main:app --reload`

![run_api_1](/assets/images/run_api_1.png)

uvicorn 이 PC를 API 서버로 만들어주는 프로그램이라는 점은 이전 설명에서 언급했습니다. 그럼 함께 실행된 다른 명령어는 무엇을 의미하고 있는지 살펴보겠습니다. 

- uvicorn : PC 를 API 서버로 만들어주는 프로그램
- main : main.py 파일에서 .py 를 제외한 파일명. 만약 파일명이 example.py 라면, example 이 됩니다. 
- app : 예제코드 5번째 줄 `app = FastAPI()` 의 변수명 app. 만약, api = FastAPI() 로 만들었다면, app 대신 api 를 넣습니다. 
- --reload : 코드가 변경되면 자동으로 변경된 내용이 반영되도록 하는 uvicorn 옵션. 일반적으로 이러한 기능을 `hot reload` 라고 합니다. 

예제 코드가 동작중인 API 서버를 만들었습니다. 웹 브라우저를 통해 API 서버로 접근해 보겠습니다. 웹 브라우저를 통해 접근한다는 것은 우리가 만든 API 서버가 접근할 수 있는 웹 주소가 있다는 의미입니다. 하지만 본 Post 에서 별도 웹 주소를 설정하진 않았습니다. API 서버를 실행한 터미널 화면을 살펴보면 API 서버 주소를 확인할 수 있습니다. 

- API 서버 주소 : `http://127.0.0.1:8000`

![run_api_2](/assets/images/run_api_2.png)

_API 서버 주소_

웹 브라우저로 접속하기 전, 터미널과 웹 브라우저를 동시에 볼 수 있도록 화면을 배치한 상태에서 웹 브라우저로 API 서버에 접속합니다. 
다음과 같은 화면이 보인다면, API 서버가 정상적으로 동작한다는 것을 알 수 있습니다. 

![run_api_3](/assets/images/run_api_3.png)

_API 서버 웹 브라우저로 접속하기_

웹 브라우저로 접속한 후 API 서버를 실행한 터미널을 보면, 다음과 같이 변경된 부분을 볼 수 있습니다. API 서버에 접속하거나 변경되는 등의 이벤트가 발생하면 API 서버는 터미널 화면에 로그를 남깁니다. 앞으로 API 서버 부분을 개발하면서 동작을 확인할 때, 출력되는 로그를 살펴보면 많은 도움이 됩니다. 

![run_api_4](/assets/images/run_api_4.png)

앞서 unicorn 명령어로 부여한 hot reload 기능도 확인해 보겠습니다. 예제 코드의 read_root 함수의 코드를 다음과 같이 변경해 봅니다. 

```python

...생략

@app.get("/")
def read_root():
    return {"Hello": "D.Kei"}

...생략
```

hot reload 기능이 정상적으로 동작한다면, 코드 수정 및 저장 후 웹 브라우저로 접속하면 변경된 코드가 반영되었음을 알 수 있습니다. 또한 이러한 변경여부는 터미널에서 로그로 확인할 수 있습니다. 

![run_api_5](/assets/images/run_api_5.png)

_hot reload 동작 테스트_

FastAPI 의 가장 큰 장점으로 꼽았던 Swagger UI 와 ReDoc 으로 예제 코드가 어떻게 출력되는지 확인해 보겠습니다.  

- Swagger UI 접속 경로 : `http://127.0.0.1:8000/docs`
- ReDoc 접속 경로 : `http://127.0.0.1:8000/redoc`

![run_api_6](/assets/images/run_api_6.png)

_Swagger UI 화면(왼쪽) 과 ReDoc 화면(오른쪽)_

> Swagger UI 와 ReDoc 은 자동 문서화 이외에 추가적인 기능을 제공하고 있습니다. 앞으로 개발하면서 이 부분도 함께 다룰 예정입니다. 
{: .prompt-info}

지금까지 FastAPI 를 활용해 API 서버 개발을 위한 환경 구성을 완료했습니다. 다음 Post 에서는 배포된 스마트 컨트랙트와 통신하는 API 함수를 개발해 보겠습니다. 


---
### 정리
* FastAPI 를 활용해 API 를 개발하는 경우, Swagger UI 나 ReDoc 기능을 활용할 수 있습니다. 
* FastAPI 로 개발된 코드는 Uvicorn 으로 실행한 API 서버에서 실행되며 http://127.0.0.1:8000 으로 접속헤 볼 수 있습니다. 
* Swagger UI 는 http://127.0.0.1:8000/docs 로 접속해 볼 수 있습니다. 
* ReDoc 은 http://127.0.0.1:8000/redoc 로 접속해 볼 수 있습니다. 

---
### 참고
* [Step0 - Prolog](https://keitechnote.github.io/blog/posts/vdr-step0-prolog/)
* [Step1 - Init (VSCode + TruffleSuite + Ganache-cli)](https://keitechnote.github.io/blog/posts/vdr-step1-init/)
* [Step2 - First Contract](https://keitechnote.github.io/blog/posts/vdr-step2-first-contract/)
* [Step3 - Deploy Smart Contract on Ganache-Cli](https://keitechnote.github.io/blog/posts/vdr-step3-deploy-ganache/)

[step2_first_contract]: https://keitechnote.github.io/blog/posts/vdr-step2-first-contract/
[step3_Deploy_Contract]: https://keitechnote.github.io/blog/posts/vdr-step3-deploy-ganache/
[BlockChain_Category]: https://keitechnote.github.io/blog/categories/blockchain/
[fastapi_homepage]: https://fastapi.tiangolo.com/ko/
[fastapi_example_code]: https://fastapi.tiangolo.com/ko/#_5