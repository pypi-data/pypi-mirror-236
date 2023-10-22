from totpak import pdf2text
t = pdf2text.convert()
t


# import tarfile

# with tarfile.open(
#     r"D:\VS Code Projects\Python\pypipack\dist\pypipdf-1.0.tar.gz"
# ) as tr:
#     print(tr.list())


# with ZipFile(
#     r"D:\VS Code Projects\Python\pypipack\dist\pypipdf-1.0.tar.gz"
# ) as zip:
#     print(zip.namelist())
#     info = zip.getinfo("ecommerce/__init__.py")
#     print(info.file_size)
#     print(info.compress_size)
