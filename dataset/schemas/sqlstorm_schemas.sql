create table PostHistoryTypes (
    Id   smallint    not null,
    Name varchar(50) not null,
    primary key (Id)
);
create table LinkTypes (
    Id   smallint    not null,
    Name varchar(50) not null,
    primary key (Id)
);
create table PostTypes (
    Id   smallint    not null,
    Name varchar(50) not null,
    primary key (Id)
);
create table CloseReasonTypes (
    Id   smallint    not null,
    Name varchar(50) not null,
    primary key (Id)
);
create table VoteTypes (
    Id   smallint    not null,
    Name varchar(50) not null,
    primary key (Id)
);

create table Users (
    Id              int       not null primary key,
    Reputation      int       not null,
    CreationDate    timestamp not null,
    DisplayName     varchar(40),
    LastAccessDate  timestamp not null, 
    WebsiteUrl      varchar(200),
    Location        varchar(300),
    AboutMe         text,
    Views           int, 
    UpVotes         int, 
    DownVotes       int,
    ProfileImageUrl varchar(200),
    AccountId       int 
);

create table Badges (
    Id       int         not null primary key,
    UserId   int         not null,
    Name     varchar(50) not null,
    Date     timestamp   not null, 
    Class    smallint    not null, 
    TagBased bool        not null 
);

create table Posts (
    Id                    int not null primary key,
    PostTypeId            smallint,
    AcceptedAnswerId      int, 
    ParentId              int, 
    CreationDate          timestamp,
    Score                 int, 
    ViewCount             int,
    Body                  text, 
    OwnerUserId           int, 
    OwnerDisplayName      varchar(40),
    LastEditorUserId      int,
    LastEditorDisplayName varchar(40),
    LastEditDate          timestamp, 
    LastActivityDate      timestamp, 
    Title                 varchar(300), 
    Tags                  varchar(4000), 
    AnswerCount           int, 
    CommentCount          int,
    FavoriteCount         int,
    ClosedDate            timestamp,
    CommunityOwnedDate    timestamp, 
    ContentLicense        varchar(30)
);

create table Comments (
    Id              int           not null primary key,
    PostId          int           not null,
    Score           int,
    Text            varchar(2000) not null,
    CreationDate    timestamp     not null,
    UserDisplayName varchar(40),
    UserId          int, 
    ContentLicense  varchar(30)
);

create table PostHistory (
    Id                int not null primary key,
    PostHistoryTypeId smallint, 
    PostId            int,
    RevisionGUID      varchar(36), 
    CreationDate      timestamp,
    UserId            int,
    UserDisplayName   varchar(40), 
    Comment           varchar(800), 
    Text              text, 
    ContentLicense    varchar(30)
);

create table PostLinks (
    Id            bigint    not null primary key,
    CreationDate  timestamp not null,
    PostId        int       not null, 
    RelatedPostId int       not null, 
    LinkTypeId    smallint  not null 
);

create table Tags (
    Id              int not null primary key,
    TagName         varchar(35),
    Count           int not null,
    ExcerptPostId   int, 
    WikiPostId      int, 
    IsModeratorOnly bool,
    IsRequired      bool
);

create table Votes (
    Id           int      not null primary key,
    PostId       int      not null,
    VoteTypeId   smallint not null, 
    UserId       int,
    CreationDate timestamp,
    BountyAmount int
);
