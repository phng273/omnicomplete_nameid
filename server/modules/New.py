import json
import os


with open('D:\Viettel\Git\omnicomplete_nameid\omnicomplete_nameid\prompt_tests\omnicomplete\knowledge_bases\domain_knowledge_v1.json', 'r') as infile:
    data = json.load(infile)  # Đọc toàn bộ nội dung file JSON và chuyển thành đối tượng Python (danh sách các từ điển)

# Thêm trường "hit": 0 vào mỗi đối tượng
for item in data:
    item['hit'] = 0

# Ghi dữ liệu đã được cập nhật vào file đầu ra
with open('D:\Viettel\Git\omnicomplete_nameid\omnicomplete_nameid\prompt_tests\omnicomplete\knowledge_bases\domain_knowledge_v2.json', 'w') as outfile:
    json.dump(data, outfile, indent=4) 