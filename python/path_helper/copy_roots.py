#%%
import os
import shutil
import json

# roots_path = '/Users/namnt/Documents/Work/DOUNets/SHINE_source/backup/backup_20200421'
roots_path = "/Users/namnt/Documents/Work/DOUNets/SHINE_source/slim/webapp/static/media"
new_matching_sandbox_dir = "/Users/namnt/Documents/Work/DOUNets/SHINE_source/sandbox/new_matching/root_2"
si_doc_path = "/Users/namnt/Documents/Work/DOUNets/SHINE_source/backup/si_doc"
new_matching_roots_path = os.path.join(new_matching_sandbox_dir, "roots")

count = []

for matching_type in ["key", "multi"]:
    type_roots_path = os.path.join(roots_path, matching_type)
    for type_root_id in os.listdir(type_roots_path):
        if ".DS_Store" in type_root_id:
            continue
        new_pdf_name = f"new_matching_ROOT-{matching_type}-{type_root_id}.pdf"
        pdf_root_path = os.path.join(type_roots_path, type_root_id, "root.pdf")
        # dest_pdf_path = os.path.join(si_doc_path, new_pdf_name)
        shutil.copy(pdf_root_path, os.path.join(si_doc_path, new_pdf_name))
        # shutil.copy(pdf_root_path, os.path.join(new_matching_roots_path, new_pdf_name))

        print(f"COPIED {matching_type}-{type_root_id}")
        count.append(new_pdf_name)

with open(os.path.join(new_matching_sandbox_dir, "files.json"), "w") as f:
    json.dump(count, f)

print("count:", len(count))


# %%
"new_matching_ROOT-key-1_1.pdf".split("-", 1)[1:][0].split(".")[0]


# %%
import shutil
from pathlib import Path

root_path = Path("key")
src_path = root_path / "1_3"
dst_path = root_path / "1_4"

shutil.copy2((root_path / "1_1" / "new.txt").absolute(), (root_path / "1_4"))

# another_path = root_path / "value" / "hello"
# another_path.mkdir(parents=True, exist_ok=True)

# for child_path in root_path.glob("*"):
#     print(child_path, child_path.suffix)
#     if child_path.suffix:
#         shutil.copy2(child_path, dst_path)

# file_path = root_path
# if src_path.is_dir():
#     if dst_path.is_dir():
#         for src_files in src_path.glob("*"):
#             shutil.copy2(src_files, dst_path)
#     else:
#         shutil.copytree(src_path, dst_path)
# else:
#     raise

# %%
child_path.absolute()
# child_path

# %%
child_path.absolute()
# %%
print(str(child_path.absolute()))
print(str(child_path))
# %%
for i in []:
    if i == 0:
        break
else:
    print("Hello")
# %%
