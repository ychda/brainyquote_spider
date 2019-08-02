## brainyquote.com spider
> 中国的人民是伟大的人民。

> The Chinese nation is a great nation that has been through hardships and adversity but remains indomitable, the Chinese people are a great people. They are industrious and brave and they never pause in pursuit of progress.

### 输入： scrapy crawl quotev2

### 输出：example
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
```

### 指定作者搜索
```
$ scrapy crawl author_quote -a author="lu xun"
$ scrapy crawl author_quote
如果不指定参数则在列表中随机选择一个。
```
----------------
```
2019-08-02 12:42:40 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 17995397,
 'downloader/request_count': 45227,
 'downloader/request_method_count/GET': 45227,
 'downloader/response_bytes': 729567755,
 'downloader/response_count': 45227,
 'downloader/response_status_count/200': 45227,
 'elapsed_time_seconds': 2801.401287,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2019, 8, 2, 4, 42, 40, 614332),
 'item_scraped_count': 744433,
 'log_count/DEBUG': 789660,
 'log_count/INFO': 56,
 'memusage/max': 167641088,
 'memusage/startup': 55152640,
 'request_depth_max': 29,
 'response_received_count': 45227,
 'scheduler/dequeued': 45227,
 'scheduler/dequeued/memory': 45227,
 'scheduler/enqueued': 45227,
 'scheduler/enqueued/memory': 45227,
 'start_time': datetime.datetime(2019, 8, 2, 3, 55, 59, 213045)}
2019-08-02 12:42:40 [scrapy.core.engine] INFO: Spider closed (finished)
(venv) ychda@cstdlib:~/PycharmProjects/scrapy/brainyquote_com$ 
```
----------------
IGNORE
----------------

`response.xpath('//ul[contains(@class,"pagination")]').xpath('li[contains(@class,"disable")]').getall()`
```
['<li class="disabled"><a>\nPrev\n</a></li>',
 '<li class="disabled"><span>..</span></li>',
 '<li class="disabled"><a>\nPrev\n</a></li>',
 '<li class="disabled"><span>..</span></li>']
```
### mongodb OK
```mongo
db.quote.aggregate([
        {$group: {_id: {quote: '$quote', author: '$author'}, count: {$sum: 1}, dups: {$addToSet: '$_id'}}},
        {$match: {count: {$gt: 1}}}
]).forEach(function(doc){
    doc.dups.shift();
    db.quote.remove({_id: {$in: doc.dups}});
})
```

```mongo
db.quote.aggregate([
    {$group: {_id : '$text', count: {$sum : 1}}},
    {$match: {count: {$gt : 1}}}
])
```
