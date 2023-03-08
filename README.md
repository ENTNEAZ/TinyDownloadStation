# TinyDownloadStation

## 简介

这是一个轻量化下载站，只需一条指令即可可以轻松搭建一个下载站

## 使用方法

```
python3 main.py
```

## 注意事项

由于并没有注册界面 请使用以下 javaScript 代码生成哈希密码 并加入`userPassword.json`中

```
function generateHash(password) {
    password =  password + "saltysalt";
    var hash = 0;
    if (password.length == 0) return hash;
    for (i = 0; i < password.length; i++) {
        char = password.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
        ret = md5(hash + "NaCl");
    }

    return ret;
}
```

格式为

```
{"username":"hashPassword"}
```

例如:

需要添加用户 123 密码 123

```
User:123
Passwd:123
generateHash("123") =='8b22cd608bab7fdb4a9bede9f77d6da3'
```

则`userPassword.json`中应该写入

```
{"123":"8b22cd608bab7fdb4a9bede9f77d6da3"}
```

## 配置文件

### ssl 证书

```
# ssl证书 若没有ssl 则留空
# 不填证书信息将会使用http
keyfile = ''
certfile = ''
```

### 用户信息存储路径

```
userPasswordFilePath = 'userData/userPassword.json'
userCookieFilePath = 'userData/userCookie.json'
userCookieExpireTime = 60 * 60 * 24 * 7  # 7 days
```

### log 路径

```
logPath = 'log/'
```

### 文件保存路径

```
savePath = '/opt/download/'
```

### 域名信息（用于 cookie）

```
domain = ""
```

### 端口信息

```
port = 443
```
