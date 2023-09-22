---
title: Obsidian 초기 설정하기 (1)
date: 2023-09-23 05:30 +09:00
published: true
categories: [Vault]
tags: [Vault, Memo, Obsidian, Obsidian-Git, Github, Backup]
---

## Obsidian

Obsidian 을 2년정도 사용해 오면서 가장 큰 불편사항이었던 동기화 부분을 해소해 주는 Obsidian Plugin 인 Obsidian-Git 을 소개합니다. 
이름에 알 수 있듯 Obsidian 의 수익모델인 Sync 를 Github 로 대신하는 컨셉의 Plugin 이며 노트북 뿐만 아니라 모바일에서도 사용할 수 있어 효율적입니다. 


### 설치하기

- Obsidian [다운로드](https://obsidian.md/download)

![Download Obsidian](/dkei.github.io/assets/images/Obsidian_download.png)

설치 후 실행하면 다음과 같은 시작 화면을 볼 수 있습니다. 

![Start Obsidian](/dkei.github.io/assets/images/Obsidian_start.png)

Obsidian에서 작성할 md 파일을 저장할 공간인 `Vault` 를 생성합니다. 

- 순서 : `Create New Vault > Vault Name 기입 > Browser 로 저장할 폴더 설정 > Create`

![Init Obsidian](/dkei.github.io/assets/images/Obsidian_init.png)

본 Post 에서는 Vault Name 은 `Vault`, 저장할 폴더는 `바탕화면\Note` 폴더로 지정했습니다. `Create` 하면 해당 폴더 아래에 `Vault` 이름의 폴더가 생성됩니다. 

![Empty Obsidian](/dkei.github.io/assets/images/Obsidian_Empty.png)

### Plug-In Obsidian Git

Obsidian 은 기본적으로 무료도구 이지만 작성된 md 파일을 노트북, 핸드폰, 태블릿에서 모두 활용하려면 Obsidian 의 `Sync`를 활용해야 합니다. 하지만 아쉽게도 sync 는 유료기능으로 처음 써보는 입장에서 Obsidian 을 유료로 쓰는 것은 어려운 부분입니다. 하지만 다행히도 이 부분을 해소해 줄 수 있는 플러그인이 있습니다.  바로 `Obsidian Git` 입니다.
이름에서 알 수 있듯 작성한 md 파일을 Github 에 저장하는 Plug-In 으로 이를 활용하면 어디서든 기존에 작성한 md 파일을 확인할 수 있다. 

> 만약 디바이스 한 곳에서만 사용할 예정이라면 Obsidian Git 설치는 넘어가도 상관없습니다. 단지 편의성을 위한 Plug-In 일 뿐 입니다. 
{: .prompt-info}


#### Obsidian Git 설치하기

Obsidian Git 은 Community Plugin 에서 찾아볼 수 있다. 

- 경로 : `Settings > Community plugins > (Turn on Community plugins)`

![Community Plugin](/dkei.github.io/assets/images/Obsidian_Communityplugin.png)

> 처음 사용하면 Obsidian Community plugins 는 비활성화되어 있습니다. 따라서 `Turn On Community plugins` 로 사용할 수 있도록 활성화해야 합니다. 이후 바로 사용할 수 있습니다. 
{: .prompt-info}

- 경로 : `Browse > 'Obsidian Git' 검색 > 'Obsidian Git' 선택 > Install`

![Install Obsidian Git](/dkei.github.io/assets/images/Obsidian_Install_Git.png)

설치가 완료되면 Community plugins 화면에서 `Installed Plugins` 항목 하위에 설치된 Obsidian Git 을 확인할 수 있습니다. 이제 사용할 수 있도록 활성화 후 Github 로 백업될 수 있도록 설정하면 됩니다. 

![Enable Obsidian Git](/dkei.github.io/assets/images/Obsidian_Git_Enable.png)

> Obsidian Git을 활성화하면 `Can't find ~` 오류가 나옵니다. 이는 Obsidian Git 은 활성화됐지만 백업할 수 있는 Github 정보가 없기 때문에 발생한 오류이므로 지금은 무시해도 상관없습니다. 
{: .prompt-info}


#### Github 설정하기 

개인 Github 에서 신규 Repository를 생성합니다. 

> [Github](https://github.com) 계정이 없다면 신규 가입 후 진행합니다. 
{: .prompt-info}

- 경로 : `Github 로그인 >  'Repository' 탭 > 'New'`

![New Repository](/dkei.github.io/assets/images/Github_Repository_New_1.png)


- 설정 정보
    - Repository Name
    - `Private` 

![Setup New Repository](/dkei.github.io/assets/images/Github_Repository_New_2.png)

신규 Repository 용도는 Obsidian 을 백업하기 위함입니다. Github 는 외부 공개(Public)가 기본 설정이므로 신경쓰인다면 외부 비공개 (Private) 을 설정하기 바랍니다. 

Github Repository 를 생성했다면 다음과 같이 Repository 가 보입니다. 
이제 Obsidian Git 설정에 필요한 Repository 주소를 복사해 둡니다. 

![Github Repo URL](/dkei.github.io/assets/images/Github_Repo_URL.png)

#### Github Token 발행하기

우리가 신경쓰지 않더라도 Obsidian 에서 주기적으로 백업하기 위해선 Obsidian 이 Github 의 Repository에 접근할 수 있는 정보가 필요합니다. 예전에는 ID/PW 를 사용했지만 요즘에는 Token 을 사용하므로 Token 을 발행합니다. 

> ID/PW 는 Github 의 계정정보로 노출시 중요한 문제가 발생할 수 있습니다. 따라서, 계정정보는 아니지만 접근할 수 있도록 Token 을 사용하고 있습니다. Token 은 접근할 수 있는 권한과 기간을 지정할 수 있기 때문에 노출되더라도 Token 을 삭제 후 다시 만들면 되므로 상대적으로 위험도가 낮아집니다. 그렇다하더라고 중요한 정보이므로 노출되지 않도록 주의해야 합니다. 
{: .prompt-warning}

우측 상단의 가장 오른쪽의 계정 아이콘을 선택합니다. 

![User Icon](/dkei.github.io/assets/images/Github_User_Icon.png)

다음의 순서대로 선택합니다. 

- 경로 : `Settings > Developer Settings > Personal Access Tokens > Tokens (classic) > 'Generatre New token' 선택 > 'Generate New token (Classic) 선택`

![Token (Classic)](/dkei.github.io/assets/images/Github_Token_1.png)

Token 을 생성하는 화면으로 이동했습니다. 
이 부분에서 Token 생성에 필요한 최소한의 값을 기입하면 됩니다. 
- Note : Token 이름으로 Token 의 용도를 쉽게 파악하기 위함입니다. 
- Expiration : Token 유효기간으로 자신의 취향에 맞춰 선택합니다.  
- Select Scopes : Token 권한 으로 `repo` 권한을 부여합니다. 

![New Token](/dkei.github.io/assets/images/Github_Token_2.png)

Token 권한을 제외하면 원하는 대로 지정하면 됩니다. 
페이지 하단의 `Generate Token` 을 선택하면 Token 생성이 완료됩니다. 

이전 페이지로 이동되면서 선택한 이름에 맞는 Token (`ghp_`로 시작하는 문자열) 이 보이면 복사해 둡니다. 

> Token 은 한번 보인 이후 다시 접속해서 보면 Token 을 확인할 수 없습니다. 만약, 설정과정에서 복사해둔 Token 을 잊어버렸다면 기존에 생성했던 Token 은 삭제한 후 재생성해 사용해야 합니다. 
{: .prompt-warning}


#### Obsidian Git 설정하기 

Obsidian 으로 이동합니다. Command 입력창 (윈도우 `Ctrl + P`, 맥 `Command + P`) 을 실행해 Obsidian Git 기능 중 Clone 기능을 통해 이전에 생성해 둔 Github Repository를 가져올 예정입니다. Command 입력창에서 `clone` 을 입력합니다. 
이전에 설치해 둔 Obsidian Git 의 기능인 Clone 이 보이면 선택합니다. 

- 순서 : `Command 입력창(Ctrl + P or Command + P) 실행 > 'Clone' 입력 > 'Obsidian Git : Clone an existing remote repo' 선택`

![Obsidian_Command](/dkei.github.io/assets/images/Obsidian_Command.png)

URL 을 입력합니다. URL 은 Github URL 이며 다음의 형식으로 입력해야 합니다. 

- 형식 : `https://<Token>@<Github Repository URL>`

Token 정보는 이전 Token 생성 과정에서 복사해 두었고 Github Repository URL 은 Github Repository 생성 후 복사해 두었으니 그대로 조합하면 됩니다. 

- 최종 remote URL : `https://<Token>@github.com 부터 .git 까지 나머지 주소`

> 주의해야 할 점은 Github Repository URL 은 `https://github.com/` 으로 시작되지만 remote URL 을 생성할 때는 앞 https:// 를 뺀 github.com/부터 입력해야 합니다. 
{: .prompt-warning}

다음은 Github Repository 를 저장할 최상위 폴더명을 입력합니다. 여기서 입력된 이름으로 폴더가 생성되고 그 하위에 Github Repository 에 백업할 내용들을 입력하게 됩니다. 
이점을 고려해 원하는 이름을 기입합니다. 

> 생성 후 Obsidian 에서 폴더를 삭제하려고 하면 삭제되지 않고 오류가 발생합니다. 이는 폴더 하위에 Github Repository 정보가 있어 이를 보호하기 위함입니다. 따라서, 삭제하려면 윈도우 탐색기에서 해당 폴더로 직접 이동해 삭제해야 합니다. 
{: .prompt-warning}

다음 입력 부분은 무시하고 엔터로 넘어가면 Obsidian-Git 설정까지 모두 완료됩니다. 
Obsidian 왼쪽부분에 지정한 폴더명이 보이고 만약 Github Repository 에 README.md 를 설정했다면 해당 파일이 함께 보입니다. 

![Obsidian Git Done](/dkei.github.io/assets/images/Obsidian_Git_Done.png)

이제 Obsidian 을 종료 후 재시작합니다. 

#### Obsidian Git 사용해 보기 

생성한 폴더 하위에 Note 또는 폴더를 생성해 봅니다. 
본 Post 에서는 생성한 폴더명은 'Github_Root_Backup' 이고 하위에 6개의 폴더를 생성했습니다. 

![Obsidian Git Test1](/dkei.github.io/assets/images/Obsidian_Git_Test_1.png)

Obsidian Command 창에서 backup 명령을 수행합니다. 

![Obsidian Git Test2](/dkei.github.io/assets/images/Obsidian_Git_Test_2.png)

본 Post 와 같이 폴더만을 생성해 `backup` 했다면 Github Repository에 아무런 변화가 없을 것입니다. Github 는 파일 단위로 동작합니다. 따라서, 저장할 파일(Obsidian 에서는 Note)
가 없다면 기록만 될 뿐, Github Repository 에 저장하지 않습니다. 따라서, 폴더 하위에 Note 파일을 생성 후 backup 하면 정상 동작을 확인할 수 있습니다. 

![Obsidian Git Test3](/dkei.github.io/assets/images/Obsidian_Git_Test_3.png)

> `1. Project` 폴더만 생성되어 `Project Test Note.md` 만 저장됐을 뿐 다른 폴더는 보이지 않는 것을 알 수 있습니다. 
{: .prompt-info}


---
### 참고
- Youtube : [천재들이 쓰는 노트앱? 옵시디언 활용법 200%](https://youtu.be/h6rxKbbgI28?si=OuShur0Q6h-ASKT4)
- Youtube : [The easiest way to setup obsidian git (4 minutes)](https://youtu.be/5YZz38U20ws?si=2lXRVkvyohQRj1jv)
