# hoshino-qqimagedeliver
hoshino插件，接收并处理POST请求后处理，发送消息和图片到QQ好友或群

如何使用？按照hoshino插件进行使用，配置__bot__.py启用，并将主体文件加入modules。
改自https://github.com/tkkcc/qqimagedeliver/tree/master
（改动幅度大，一点都没有原来的了，只套了功能）
可选发送个人还是群组，群组前缀＋g



## 客户端

post数据格式
```js
{
  image, // base64编码图片
  to, // 接收QQ号或群号
  info, // 文字信息
} 
```

curl
```sh
curl -d "info=好的&to=12345" http://123.456.789.100:49875
```

python
```python
requests.post(
    "http://123.456.789.100:49875",
    data={"to": to, "info": info, "image": image}
)
```

示例本地端传post，解析并发送至群组12345678
```lua
import requests

to='g12345678'
info='nihao'
image='imagetest(base64)'

requests.post(
    "http://127.0.0.1:8888",
    data={"to": to, "info": info, "image": image}
)

print('传入成功')
```
