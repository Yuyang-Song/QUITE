# How can I load query from SQLite database into tableview in ios 7 ( xcode 5.1.1 )?
[Link to question](https://stackoverflow.com/questions/25328627/how-can-i-load-query-from-sqlite-database-into-tableview-in-ios-7-xcode-5-1-1)
**Creation Date:** 1408114142
**Score:** -1
**Tags:** ios, sql, database, xcode, sqlite
## Question Body
<p>I have an SQLite database named "BookDataBase.sqlite" with two columns : Category , Name .</p>

<p>It contains categories for books and some book names for each category .</p>

<p>I have a table view controller connected to class "CategoryTableViewController" which is a subclass of "UITableViewController" .</p>

<p>I want the table view to display the result for a query from the database where only the categories are displayed .</p>

<p>I have tried this code but it didn't work for me .</p>

<p>CategoryTableViewController.m  :</p>

<pre><code>#import "CategoryTableViewController.h"
#import &lt;sqlite3.h&gt;

@interface CategoryTableViewController ()

@end

sqlite3 *BookDatabase;
NSString *databasepath;
const char *filepath;
NSString *querySQL;
const char *query_stmt;
sqlite3_stmt *statement;
NSMutableDictionary *BookRecord;
NSUserDefaults *BookData;
NSMutableArray *BookArray;


@implementation CategoryTableViewController

- (id)initWithStyle:(UITableViewStyle)style
{
    self = [super initWithStyle:style];
    if (self) {
        // Custom initialization
    }
    return self;
}

-(void) viewWillAppear:(BOOL)animated {

    databasepath = [[NSBundle mainBundle]pathForResource:@"BookDatabase" ofType:@"sqlite"];
    filepath = [databasepath UTF8String];

    if (sqlite3_open(filepath, &amp;BookDatabase) == SQLITE_OK) {


        querySQL = @"SELECT Category FROM BookTable Group By Categoy" ;
        query_stmt = [querySQL UTF8String];

        if (sqlite3_prepare_v2(BookDatabase, query_stmt, -1, &amp;statement, NULL) == SQLITE_OK) {
            while (sqlite3_step(statement) == SQLITE_ROW) {

                BookRecord =[[NSMutableDictionary alloc] initWithCapacity:sqlite3_column_count(statement)];

                for (int i=0; i&lt;sqlite3_column_count(statement); i++) {

                    NSString *ColName = [[NSString alloc] initWithUTF8String:sqlite3_column_name(statement, i)];
                    NSString *ColVal = [[NSString alloc] initWithUTF8String:(char *)sqlite3_column_value(statement, i)];




                    [BookRecord setObject:ColVal forKey:ColName];
                }


                [BookArray addObject:BookRecord];



            }


             sqlite3_finalize(statement);

        }

        sqlite3_close(BookDatabase);





    }





}




- (void)viewDidLoad
{
    [super viewDidLoad];

    // Uncomment the following line to preserve selection between presentations.
    // self.clearsSelectionOnViewWillAppear = NO;

    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    // self.navigationItem.rightBarButtonItem = self.editButtonItem;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{

    // Return the number of sections.
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{

    // Return the number of rows in the section.
    return [BookArray count];
}



- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"CategoryTableViewCell";
   UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier forIndexPath:indexPath];





    // Configure the cell...

    int row = [indexPath row];



    cell.textLabel.text = [BookArray[row] objectForKey:@"Category"];




    return cell;
}

@end
</code></pre>

<p>I have already added the libsqlite3 framework.</p>

<p>The database file is located in the app folder :</p>

<p><a href="https://dl-web.dropbox.com/get/Screen%20Shot%202014-08-15%20at%207.18.22%20PM.png?_subject_uid=104745578&amp;w=AADDzW343bbSsnQ9wko1dFQ3yQes8N5tY9hJmEDb3qnwNw" rel="nofollow">https://dl-web.dropbox.com/get/Screen%20Shot%202014-08-15%20at%207.18.22%20PM.png?_subject_uid=104745578&amp;w=AADDzW343bbSsnQ9wko1dFQ3yQes8N5tY9hJmEDb3qnwNw</a></p>

<p>The type for the table view prototype cell is set to basic and the cell identifier is "CategoryTableViewCell".</p>

<p>The name of the table in the database is "BookTable".</p>

<p>Can someone please help me fix this?</p>

<p>Feel free to rewrite my entire code if needed &lt; but please keep in mind that it's a subcalass of "UITableViewController".</p>

<p>Thanks .</p>

## Answers
### Answer ID: 25335651
<p>I FINALLY FOUND IT</p>

<p>Turns out I didn't add the database file to the main bundle .</p>

<p>I didn't know I should do that .</p>

