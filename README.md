# 山东商职课表

#### 介绍
使用selenium对山东商业职业技术学院官网进行爬取获得课表，使用Django进行API开发，iOS用户可使用快捷指令请求该API实现让Siri查询当日课程

#### 安装教程

1.  先在自己电脑或服务器配置python3环境
2.  将本项目拉取到本地
3.  `pip install django`
4.  `pip install selenium`

#### 使用说明

1.  在项目根目录下使用`python manage.py runserver`即可运行本项目
2.  使用iOS快捷指令的网页-获取URL内容或Ajax等方式请求接口即可

#### 请求类型

GET/

#### 请求参数

| 名称     | 类型   | 必选  | 说明               |
| -------- | ------ | ----- | ------------------ |
| username | string | true  | 教务系统用户名     |
| password | string | true  | 教务系统密码       |
| week     | string | false | 要获取第几周的课表，默认为第一周 |

#### 返回结果

| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 200    | OK | 成功 | Inline   |

#### 返回数据结构

成功示例 状态码 **200**

| 参数       | 类型    | 说明               |
| ---------- | ------- | ------------------ |
| data       | Object  | 一周的课组成的数组 |
| courseName | string  | 课程名称           |
| teacher    | string  | 课程讲师           |
| classroom  | string  | 上课教室           |
| day        | integer | 周几上课           |
| num        | integer | 第几节课开始上     |
| continued  | integer | 此课程将要讲几节课 |
| state      | integer | 请求状态           |

> 示例代码

```json
{
    "data": [
        {
            "courseName": "PHP动态网站开发",
            "teacher": "XXX",
            "classroom": "本部E202",
            "day": 2,
            "num": 1,
            "continued": "4"
        },
        {
            "courseName": "就业指导实务",
            "teacher": "XX",
            "classroom": "本部F303",
            "day": 4,
            "num": 3,
            "continued": "2"
        }
    ],
    "state": 1
}
```

密码错误 状态码 **200**

| 名称  | 类型    | 说明     |
| ----- | ------- | -------- |
| data  | string  | 错误内容 |
| state | integer | 请求状态 |

> 示例代码

```json
{
    "data": "密码错误",
    "state": 0
}
```

> 项目已部署到[http://coursespider.tippy.website](http://coursespider.tippy.website)
> 
> 使用时请部署到自己的服务器或电脑上
> 
> 受限于服务器带宽和校园网登录等环境，请求时长可能较长，请耐心等待
> 
> 测试时请求时长约为28秒左右，放在自己电脑上请求约为6秒左右