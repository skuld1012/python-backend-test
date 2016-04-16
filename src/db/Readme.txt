create schema:
/*************************************/
CREATE TABLE `account` (
	`id`	INTEGER,
	`acct_name`	TEXT NOT NULL,
	`acct_type`	TEXT,
	`balance`	NUMERIC NOT NULL,
	`created_at`	TEXT NOT NULL,
	`last_updated_at`	TEXT NOT NULL,
	PRIMARY KEY(id)
)
/*************************************/
CREATE TABLE `transaction` (
	`trans_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`from_acct_id`	INTEGER NOT NULL,
	`to_acct_id`	INTEGER NOT NULL,
	`amount`	NUMERIC NOT NULL,
	`created_at`	TEXT NOT NULL
)