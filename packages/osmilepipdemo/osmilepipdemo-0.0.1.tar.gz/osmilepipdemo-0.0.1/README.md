# 这是一个可以上传到pypi的例程

# pypi网站
[https://pypi.org/](https://pypi.org/)

# 操作流程
## 安装需要的包
```
python -m pip install --upgrade build
python -m pip install --upgrade twine
```
## 编译包
```
python -m build
```

## 上传包
```
python -m twine upload --repository testpypi dist/*
```