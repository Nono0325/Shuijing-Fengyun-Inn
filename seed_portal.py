import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fengyun.settings')
django.setup()

from inn_app.models import Story, USRAchievement, TechProject, ExperienceCourse

# 1. Seed Stories
stories = [
    {
        'title': '水井村：從鹽分地帶到智慧聚落的變遷',
        'category': 'local',
        'content': '''
        <p>水井村位於雲林縣口湖鄉，長期面臨土地鹽化、人口老化及青壯年外流的挑戰。然而，這裡的居民從未放棄。</p>
        <p>早期居民依賴傳統漁業維生，但在氣候變遷與環境壓力下，經營愈發困難。近年來，在地方領袖與虎科大團隊的攜手努力下，開始導入「三生共好」觀念。</p>
        <p>透過智慧養殖技術的導入，居民不僅降低了勞動強度，更提升了產品價值。每一口魚塭背後，都是在地人對家鄉土地的深情與對未來的堅持。</p>
        '''
    },
    {
        'title': '虎科大 USR 計畫：深耕在地，鏈結國際',
        'category': 'usr',
        'content': '''
        <p>國立虎尾科技大學推動的「水井村智慧減碳節水三生一體社會實踐計畫」，由電機資訊學院許永和院長領軍。</p>
        <p>計畫不僅僅是技術的導入，更是人心的鏈結。師生們走入村落，與長輩對話，了解真實需求。從水質檢測到智慧行銷，USR 團隊將實驗室的成果應用於魚塭與農田，實現真正的社會價值。</p>
        '''
    },
    {
        'title': '卓越表現：許永和院長與師生團隊獲獎連連',
        'category': 'achievement',
        'content': '''
        <p>許永和院長帶領的 USR 團隊不僅在地方服務上有成，其研究成果亦獲得多項國內外創新獎項肯定。</p>
        <p>學生團隊在「海洋科學節」及各大發明展中展示的智慧控制系統，展現了虎科大師生理論與實務並重的優點。他們的努力不僅改善了水井村，也讓世界看見台灣智慧農業的實力。</p>
        '''
    }
]

for s in stories:
    Story.objects.get_or_create(title=s['title'], category=s['category'], content=s['content'])

# 2. Seed Achievements
achievements = [
    {
        'title': '2026 海洋科學節：水井村智慧科技亮點展示',
        'type': 'news',
        'summary': '虎科大團隊於雲林三條崙海水浴場參與活動，展出智慧養殖監控、三寶奇緣等主題，吸引大量民眾關注。',
        'external_link': 'https://nfu.edu.tw/news/12345',
        'date': datetime.date(2026, 2, 10)
    },
    {
        'title': '【成果影片】三生一體：水井村智慧轉型實錄',
        'type': 'video',
        'summary': '完整紀錄從技術開發到落地推廣的感人過程，展現智慧漁業與文化創生的完美結合。',
        'external_link': 'https://ossr.nfu.edu.tw/video/display',
        'date': datetime.date(2025, 12, 15)
    }
]

for a in achievements:
    USRAchievement.objects.get_or_create(title=a['title'], type=a['type'], summary=a['summary'], external_link=a['external_link'], date=a['date'])

# 3. Seed Tech Projects
techs = [
    {
        'name': '智慧養殖監控與節約水資源系統',
        'type': 'aiot',
        'description': '結合物聯網感測器，實時監測魚塭水質（DO、pH、溫度），實現自動化投餌與節水控制系統。'
    },
    {
        'name': '水井村 Qrobt 趣味導覽地圖',
        'type': 'ar_interact',
        'description': '利用 AR 技術，掃描 QR Code 即可出現在地 Q 版代言人引導遊客參觀水井村景點與地景。'
    },
    {
        'name': '智慧水質監測雲端服務',
        'type': 'aiot',
        'description': '全天候數據上雲，農民可透過手機即時控管魚塭狀態，大幅降低因水質突變導致的損失。'
    }
]

for t in techs:
    # Adding a placeholder image path (actual file handling expected separately)
    TechProject.objects.get_or_create(name=t['name'], type=t['type'], description=t['description'])

# 4. Seed Experience Courses
workshops = [
    {
        'name': '「不蒜花」農廢藝術工作坊',
        'description': '利用大蒜皮（蒜糢）轉化為精緻的手作花藝，落實永續循環經濟。',
        'category': '不蒜花'
    },
    {
        'name': '「三寶奇緣」姻緣花小夜燈製作',
        'description': '揉合在地傳說與工藝，製作專屬水井三寶主題的溫馨小夜燈。',
        'category': '姻緣花'
    },
    {
        'name': 'OTTO 機器人智慧組裝課',
        'description': '適合國中小學生，從組裝到簡易 Python 編程，認識智慧感測原理。',
        'category': '機器人'
    }
]

for w in workshops:
    ExperienceCourse.objects.get_or_create(name=w['name'], description=w['description'], category=w['category'])

print("Portal expansion data seeded successfully!")
