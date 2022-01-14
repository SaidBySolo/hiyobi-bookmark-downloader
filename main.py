import json
from typing import Any, List
from requests import Session
from config import email, password

headers = {
    "Origin": "https://hiyobi.me",
    "Referer": "https://hiyobi.me/",
    "Host": "api.hiyobi.me",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
}

session = Session()
session.headers.update(headers)

print("계정 정보 가져오는중")
r = session.post(
    "https://api.hiyobi.me/user/login",
    headers={
        "Origin": "https://hiyobi.me",
        "Referer": "https://hiyobi.me/",
        "Host": "api.hiyobi.me",
    },
    json={"email": email, "password": password, "remember": True},
)
print("성공적으로 가져왔습니다.")
r = session.post("https://api.hiyobi.me/bookmark/1")

bookmark_total = r.json()["count"]
print(f"총 북마크가 된 갯수는 {bookmark_total}개 입니다.")

count = (
    round(bookmark_total / 15) + 1
    if not (bookmark_total / 15).is_integer()
    else round(bookmark_total / 15)
) + 1

bookmark_info_list: List[Any] = []

for paging in range(1, count):
    print(f"페이지 {count}/{paging} 읽는중..")
    r = session.post(
        f"https://api.hiyobi.me/bookmark/{paging}",
        json={"paging": paging},
    )
    res = r.json()

    for bookmark_element in res["list"]:
        search = bookmark_element.get("search")
        number = bookmark_element.get("galleryid")
        if search:
            bookmark_info_list.append(search)
        elif number:
            bookmark_info_list.append(str(number))
        else:
            raise Exception

print("파일을 저장할게요!")
with open("bookmark.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(bookmark_info_list))
print("완료!")
