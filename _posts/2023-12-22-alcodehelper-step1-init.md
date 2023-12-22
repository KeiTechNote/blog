---
title: AI로 동영상 만들기 - Step1 Init
date: 2023-12-22 05:30 +09:00
published: true
categories: [AI]
tags: [AI, Dev, udemy, ffmpeg, nodejs, openai, chatgpt, aicodehelper]
---

***본 컨텐츠는 Udemy의 "인공지능 코딩으로 동영상 제작 로봇 만들고 영상 무한으로 찍어내기" 내용 중 일부를 정리한 글입니다. 문제시 삭제될 수 있습니다.**


### 기술스택

- OS : Windows11
- OS 언어 : 한글
- 프로젝트 경로 : C:\Users\amana\OneDrive\바탕 화면\AI\mpeg
- IDE : VSCode ([다운로드][download_nodejs])
- 개발언어
    - NodeJS ([다운로드][[download_nodejs]])
- 필수 프로그램
    - AICodeHelper (VSCode Extension)
    - FFMPEG ([다운로드][download_ffmpeg])

> VSCode([VSCode 설치][install_vscode]) 와 NodeJS([NodeJS 설치][install_nodejs]) 는 이전에 다룬 바 있으므로 이전 Post 를 참고하기 바랍니다. 
{: .prompt-info}

### VSCode Extension : AICodeHelper 설치하기

VSCode Extension 은 VSCode 에서 추가 설치해 사용할 수 있는 확장 프로그램입니다. VSCode 화면 왼쪽의 아이콘 중 "Extension" 을 선택합니다. 

![extension_vscode](/assets/images/extension_vscode.png)

_VSCode 확장 프로그램_

> 이전 Post 에서 진행된 개발 환경이 함께 설정되어 있어 AWS, Docker 와 같은 확장 프로그램이 설치되어 있어 기본 화면과는 조금 차이가 있습니다. 하지만, Extension 은 모두에게 공통된 부분이므로 오해없으시길 바랍니다 .
{: .prompt-info}

검색 창에서 "AICodeHelper" 를 선택해 설치(Install) 합니다. 설치가 완료되면 아래와 같은 화면을 볼 수 있습니다. 

![aicodehelper_extension](/assets/images/aicodehelper_extension.png)

_AICodeHelper 설치 완료 화면_


### chatGPT API Key 발급하기

AICodeHelper 는 chatGPT 의 기능을 활용하는 확장 프로그램입니다. 따라서, chatGPT 기능을 사용하기 위해 다음의 조건이 만족되어야 합니다. 

1. 인터넷을 사용할 수 있어야 합니다.
2. chatGPT API 를 사용할 수 있는 API Key 가 있어야 합니다. 

그 중 chatGPT API Key 는 chatGPT 에서 무료로 발급받을 수 있습니다. 

> chatGPT API Key 는 무료로 사용하는 만큼 조회할 수 있는 횟수 등 제한사항이 있습니다. 하지만, 본 프로젝트를 진행할 때는 무료로 사용할 수 있는 수준에서 진행됩니다.
{: .prompt-info}

chatGPT API Key 는 [OpenAI 사이트][openai]에서 제공하고 있습니다. 우선 OpenAI 사이트에 접속해 로그인합니다. (계정이 없다면, 가입 후 로그인 합니다.)
로그인 후 "ChatGPT" 와 "API" 선택 화면에서 "API"를 선택합니다. 

로그인 계정에서 "API Keys" 페이지를 선택합니다. 

![apikeys_openai_1](/assets/images/apikeys_openai_1.png)

_OpenAI 홈페이지 내 API Keys 생성 페이지 위치_

"Create new secret key" 로 API Key 를 생성합니다. 이때, 생성된 키가 어떤 용도로 사용되는지 식별하기 위해 "Name" 을 지정합니다. 본 Post 에서는 AICodeHelper에서 활용하기 위한 용도이므로 "aicodehelper" 로 지정하겠습니다. Name 입력 후 "Create Secret Key" 버튼을 눌러 키를 생성합니다. 

![apikeys_openai_2](/assets/images/apikeys_openai_2.png)

_API Key 생성_

생성된 API Key 는 최초 생성된 시점에만 확인할 수 있습니다. 따라서, 앞으로 사용하기 위해 안전한 곳에 복사해 둡니다. 

![apikeys_openai_3](/assets/images/apikeys_openai_3.png)

> API Key만 있다면, 누구든 접속해 chatGPT 를 사용할 수 있습니다. 따라서, 반드시 API Key 는 노출되어선 안됩니다. 
{: .prompt-warning}


### AICodeHelper 설정하기

VSCode 의 Settings (설정화면) 으로 이동합니다. 

- 위치 : 
    - (Windows) File -> Preferences -> Settings (단축키 : `Ctrl + ,`)
    - (Mac OSX) Menu -> Settings
    
![settings_vscode](/assets/images/settings_vscode.png)

_Settings 위치 (Windows)_

Settings 화면에서 설치했던 AICodeHelper 를 검색합니다. 

![aicodehelper_settings](/assets/images/aicodehelper_settings.png)

_AICodeHelper 설정화면_

이 중 `Gptkey` 와 `Language` 를 설정합니다. 
Gptkey 는 chatGPT 의 API Key 입니다. 단, 여기에 입력하면 API Key 가 노출되므로 설명과 같이 단축키를 눌러 나타나는 입력창에 API Key 를 입력합니다. 

- 단축키 : 
    - (Windows) `Ctrl + Alt + Shift + Q`
    - (Mac OSX) `Ctrl + Opt + Shift + Q`

![aicodehelper_settings_apikey_1](/assets/images/aicodehelper_settings_apikey_1.png)

_chatGPT API Key 입력 (1)_

![aicodehelper_settings_apikey_2](/assets/images/aicodehelper_settings_apikey_2.png)

_chatGPT API Key 입력 (2)_

Language 는 `korean` 으로 변경합니다. 여기서 선택된 언어는 AICodeHelper 로 출력되는 결과물들이 사용하는 언어입니다. 예를 들어, 코드 주석 기능을 사용한다면, 설정된 언어로 주석을 넣게 됩니다. 

![aicodehelper_settings_language](/assets/images/aicodehelper_settings_language.png)

_사용언어 `korean` 으로 변경_


### FFMPEG 설치하기

영화나 동영상을 PC 에서 다운받아 실행해 본 경험이 있다면, mpeg 또는 mpg 와 같은 동영상 확장자를 본 적이 있을 것입니다. 
mpeg (Movie Picture Experts Group) 는 비디오, 오디오와 같은 미디어 표준을 정의하고 만드는 단체(Group) 또는 그 단체에서 정의한 형식으로 만든 멀티미디어를 의미합니다. 

mpeg 를 포함해 멀티미디어를 지원하는 다양한 포멧들은 퀄리티를 유지하면서 파일의 크기를 줄이기 위해 영상 또는 음성 데이터를 "압축"합니다. 압축은 용량을 줄이는 장점도 있지만, 순차적으로 일정 크기로 나누고 각각을 압축하는 방식을 사용하기 때문에, 임의의 위치로 바로 이동하거나 빨리감기(Fast Forward) 와 같은 작업에 불리하다는 단점이 있습니다. 
FFMPEG 는 MPEG의 이러한 단점을 보완한, 빨리 감기(Fast-Forward)에 용이한 MPEG 형식을 의미함과 동시에 멀티미디어를 조작, 가공시 사용되는 프로그램입니다. 앞으로 AI 동영상을 제작할 때, 필요한 도구입니다. 

- FFMPEG [다운로드][download_ffmpeg]

운영체제 맞춰 클릭하면, 다운로드할 수 있는 Github 페이지로 이동합니다. 

![download_ffmpeg_1](/assets/images/download_ffmpeg_1.png)

_FFMPEG 다운로드 (1)_

Github 페이지에서 "2023-05-31" 을 찾은 후 Assets 를 선택해 운영체제에 맞는 압축 파일을 다운로드 합니다. 

![download_ffmpeg_2](/assets/images/download_ffmpeg_2.png)

_FFMPEG 다운로드 (2)_

다운로드된 압축파일은 적절한 폴더에 압축 해제하면 됩니다. 저는 프로젝트 경로 하위에 ffmpeg 폴더를 생성한 후 저장했습니다.

> 강좌에서는 최신 버전이 있었지만, "2023-05-31" 에 작성된 버전을 사용하고 있습니다. 최신 버전을 사용하지 않는 특별한 이유가 있을 것으로 보이므로 ffmpeg 폴더 하위에 날짜별 폴더를 생성한 후 각각 저장했습니다. ffmpeg 프로그램을 사용할 때 차이를 비교해 보겠습니다. 
{: .prompt-info}

### AICodeHelper 사용해 보기

AICodeHelper 설정까지 완료되었다면 동작을 확인해 보겠습니다. VSCode 에서 빈 파일을 하나 생성한 후 다음과 같이 글을 입력해 봅니다. 

```text
Welcome to the AI World.
```

입력한 글을 모두 선택한 후 마우스 오른쪽 메뉴에서 `General Requests with Inputbox` (단축키 : `Ctrl + Alt + Shift + ,`) 를 선택합니다. 
VSCode 상단에 나타나는 입력창에 "한국말로 번역해줘" 라고 입력하면 한글로 번역되는 것을 확인할 수 있습니다. 

![test_aicodehelper_1](image.png)

_AICodeHelper 사용해 보기 - 번역 (1)_


![test_aicodehelper_2](image-1.png)

_AICodeHelper 사용해 보기 - 번역 (2)_


지금까지 AICodeHelper 를 활용해 동영상을 제작하기 위한 환경 구축을 마쳤습니다. 다음 Post 부터는 본격적으로 동영상 제작을 시작해 보겠습니다. 


---
### 정리
* chatGPT 를 코드에서 활용하기 위해선 API Key 가 필요합니다. 
* API Key 를 알고 있다면 누구든 API Key 를 발급한 계정으로 chatGPT 를 사용할 수 있고, 그로 인해 과금이 발생할 수 있으므로 노출되어선 안됩니다. 


[download_nodejs]: https://nodejs.org/ko/download
[download_ffmpeg]: https://www.ffmpeg.org/download.html
[install_vscode]: https://keitechnote.github.io/blog/posts/vdr-step1-init/#%EC%84%A4%EC%B9%98-%EB%B0%A9%EB%B2%95---vscode
[install_nodejs]: https://keitechnote.github.io/blog/posts/vdr-step1-init/#1-nodejs
[openai]: https://openai.com
