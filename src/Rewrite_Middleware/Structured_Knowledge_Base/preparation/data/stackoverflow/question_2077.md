# Yii: MySQL and MongoDB together
[Link to question](https://stackoverflow.com/questions/18127535/yii-mysql-and-mongodb-together)
**Creation Date:** 1375969097
**Score:** 0
**Tags:** mysql, mongodb, yii
## Question Body
<p>I'm starting quite big project in Yii framework and I'll need to work on MySQL and MongoDB together. And I wanted to ask, if someone have any experience working with this two databases and Yii together. Is it possible to use (for example) YiiMongoDBSuite Yii plugin, and choose which database to query? Or will I need to rewrite some of the Yii functionality to achieve this? What are best practices to to use this two databases together?</p>

## Answers
### Answer ID: 18127723
<p>Each extension will (should) take different configuration variables from the <code>main.php</code> config. CActiveRecord will take <code>db</code> and ymds will take <code>mongodb</code>. As such keeping the models between MySQL and MongoDB separate (repicate models between CActiveRecord and ymds) should be enough to use both databases together with Yii.</p>

