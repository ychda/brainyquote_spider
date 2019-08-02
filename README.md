## brainyquote.com spider
> 中国的人民是伟大的人民。

> The Chinese nation is a great nation that has been through hardships and adversity but remains indomitable, the Chinese people are a great people. They are industrious and brave and they never pause in pursuit of progress.

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
