## scrapy spider - brainyquote.com

- 20190805 - 修复了作者页面带有背景图片的quote没有抓取的问题。
   - author 27845
   - quote 437166

> 中国人民是伟大的人民。

> The Chinese nation is a great nation that has been through hardships and adversity but remains indomitable, the Chinese people are a great people. They are industrious and brave and they never pause in pursuit of progress.

### 所有quote
- 输入： scrapy crawl quote
- 输出：
```sql
    {
	"_id" : ObjectId("5d43b453a809347148f490d1"),
	"quote" : "The Chinese people are a great people; they are industrious and brave, and they never pause in pursuit of progress.",
	"author" : "Xi Jinping",
	"tags" : [
		"People",
		"Great",
		"Progress",
		"Brave"
	],
	"url" : "https://www.brainyquote.com/quotes/xi_jinping_875846"
    }
    ...
```

### 所有author
- 输入： scrapy crawl quote
- 输出：
```sql
    {
	    "_id" : ObjectId("5d4716c25d41b2f4789175da"),
	    "author" : "Xi Jinping",
	    "url" : "https://www.brainyquote.com/authors/xi-jinping-quotes"
    }
    ...
```

### 指定作者搜索
```
$ scrapy crawl author_quote -a author="lu xun"
$ scrapy crawl author_quote
如果不指定参数则在列表中随机选择一个。
```
----------------
## 请忽略以下内容

### mongodb 去重
```mongo
db.quote.aggregate([
        {$group: {_id: {quote: '$quote', author: '$author'}, count: {$sum: 1}, dups: {$addToSet: '$_id'}}},
        {$match: {count: {$gt: 1}}}
]).forEach(function(doc){
    doc.dups.shift();
    db.quote.remove({_id: {$in: doc.dups}});
})
```

```mongodb 查重
db.quote.aggregate([
    {$group: {_id : '$text', count: {$sum : 1}}},
    {$match: {count: {$gt : 1}}}
])
```
