This file describes the table structures and indexing.

create schema:
/*************************************/
CREATE TABLE "account" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`acct_name`	TEXT NOT NULL,
	`acct_type`	INTEGER NOT NULL DEFAULT 0,
	`balance`	INTEGER NOT NULL DEFAULT 0,
	`created_at`	TEXT NOT NULL,
	`last_updated_at`	TEXT NOT NULL,
	UNIQUE (`acct_name`, `acct_type`) ON CONFLICT REPLACE
)
CREATE INDEX unique_index1 on 'account' ('acct_name', 'acct_type')
/*************************************/
CREATE TABLE "transaction" (
	`trans_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`from_acct_id`	INTEGER DEFAULT -1,
	`to_acct_id`	INTEGER DEFAULT -1,
	`amount`	INTEGER NOT NULL DEFAULT 0,
	`created_at`	TEXT NOT NULL
)
CREATE INDEX unique_index1 on 'transaction' ('from_acct_id');
CREATE INDEX unique_index2 on 'transaction' ('to_acct_id');